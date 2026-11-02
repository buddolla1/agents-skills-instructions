#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent))

from automation.lib import git as git_ops
from automation.lib.bitbucket import adapter as bitbucket_adapter
from automation.lib.checks import execute_checks, required_passed
from automation.lib.config import load
from automation.lib.errors import GateError, WorkflowError
from automation.lib.jira import adapter as jira_adapter, fixture_issue, normalize
from automation.lib.policy import enforce_publication
from automation.lib.state import RunStore, SCHEMA_VERSION, atomic_json, lock, now
from automation.lib.validation import fingerprint, service_id, story_key


def paths(args):
    config_path = Path(args.config or os.environ.get("JIRA_PR_CONFIG", SCRIPT_DIR / "../config.json")).resolve()
    services_path = Path(args.services_config or os.environ.get("JIRA_PR_SERVICES", SCRIPT_DIR / "../services.json")).resolve()
    state_root = Path(args.state_root or os.environ.get("JIRA_PR_STATE", SCRIPT_DIR / "../.agent-runs")).resolve()
    return config_path, services_path, state_root


def context(args):
    config_path, services_path, state_root = paths(args)
    config, catalog, services = load(config_path, services_path)
    return config, catalog, services, RunStore(state_root)


def selected(raw, services):
    values = [service_id(x.strip()) for x in (raw or "").split(",") if x.strip()]
    if not values:
        raise WorkflowError("a nonempty explicit --services list is required")
    unknown = sorted(set(values) - set(services))
    if unknown:
        raise WorkflowError(f"unknown service IDs: {', '.join(unknown)}")
    return list(dict.fromkeys(values))


def new_run_id(story):
    return f"RUN-{story}-{now()[:10].replace('-', '')}-{uuid.uuid4().hex[:8]}"


def repository_groups(service_ids, services):
    groups = {}
    for sid in service_ids:
        groups.setdefault(services[sid]["canonical_repository_identity"], []).append(sid)
    return [members for _, members in sorted(groups.items())]


def changed_groups(manifest, services):
    changed = {sid for sid, item in manifest["impact_plan"]["services"].items() if item["classification"] == "CHANGE_REQUIRED"}
    return [members for members in repository_groups(manifest["selected_services"], services) if changed.intersection(members)]


def verification_groups(manifest, services):
    relevant = {sid for sid, item in manifest["impact_plan"]["services"].items() if item["classification"] in {"CHANGE_REQUIRED", "VERIFY_ONLY"}}
    return [members for members in repository_groups(manifest["selected_services"], services) if relevant.intersection(members)]


def cmd_doctor(args):
    config, _, services, _ = context(args)
    result = {"configuration": "PASS", "python": sys.version.split()[0], "git": shutil.which("git") or "NOT_FOUND", "git_identity": {}, "adapters": {"jira": config["jira"]["deployment"], "bitbucket": config["bitbucket"]["deployment"]}, "services": {}}
    for key in ("user.name", "user.email"):
        check = subprocess.run(["git", "config", "--global", "--get", key], text=True, capture_output=True)
        result["git_identity"][key] = "CONFIGURED" if check.returncode == 0 and check.stdout.strip() else "NOT_CONFIGURED"
    for sid, service in services.items():
        try:
            root, head = git_ops.repository_identity(service["local_path"])
            result["services"][sid] = {"status": "PASS", "repository": str(root), "head": head, "worktree_root_parent_writable": os.access(Path(service["worktree_root"]).parent, os.W_OK)}
        except WorkflowError as exc:
            result["services"][sid] = {"status": "FAIL", "error": str(exc)}
    result["live_access"] = "NOT_RUN (doctor does not mutate; use configured credentials for live commands)"
    print(json.dumps(result, indent=2))
    return 0 if result["git"] != "NOT_FOUND" and all(x["status"] == "PASS" for x in result["services"].values()) else 2


def cmd_intake(args):
    config, catalog, services, store = context(args)
    story = story_key(args.story)
    scope = selected(args.services, services)
    if args.fixture:
        issue = fixture_issue(args.fixture, story)
        jira = None
    else:
        jira = jira_adapter(config["jira"], config["policy"], config["trusted_hosts"])
        issue = jira.fetch_issue(story)
    parent = None
    parent_field = config["jira"].get("parent_field_id")
    parent_ref = issue.get("fields", {}).get(parent_field) if parent_field else None
    if parent_ref and args.fixture:
        parent_key = parent_ref.get("key") if isinstance(parent_ref, dict) else str(parent_ref)
        parent = fixture_issue(args.fixture, parent_key)
    elif parent_ref and jira:
        parent_key = parent_ref.get("key") if isinstance(parent_ref, dict) else str(parent_ref)
        parent = jira.fetch_issue(parent_key)
    comments = [] if args.fixture else jira.fetch_relevant_comments(story)
    contract = normalize(issue, config["jira"], parent, comments)
    run_id = args.run or new_run_id(story)
    manifest = {"schema_version": SCHEMA_VERSION, "run_id": run_id, "story_key": story, "story_updated": contract["updated"], "story_content_hash": contract["content_hash"], "selected_services": scope, "catalog_fingerprint": fingerprint(catalog), "stage": "BLOCKED" if contract["blocking_dependencies"] else "INTAKE_READY", "dry_run": bool(args.dry_run), "created_at": now(), "repositories": {}, "desired_jira_effects": {"comment": "disabled", "transition": "disabled"}}
    run_dir = store.run_dir(run_id)
    with lock(store.root / "locks" / f"story-{story}.lock"):
        if store.manifest_path(run_id).exists():
            raise WorkflowError(f"run already exists: {run_id}")
        atomic_json(run_dir / "evidence" / "story-contract.json", contract)
        for sid in scope:
            repo = {"schema_version": SCHEMA_VERSION, "run_id": run_id, "service_id": sid, "story_key": story, "story_update_timestamp": contract["updated"], "story_content_hash": contract["content_hash"], "repository_identity": services[sid]["repository"], "stage": manifest["stage"], "retry_counts": {}, "created_at": now()}
            store.save_repository(repo)
            manifest["repositories"][sid] = str(store.repository_path(run_id, sid).relative_to(run_dir))
        store.save_manifest(manifest)
        store.journal(run_id, "intake", "completed", {"fixture": bool(args.fixture), "dry_run": bool(args.dry_run)})
    print(json.dumps({"run_id": run_id, "stage": manifest["stage"], "selected_services": scope, "contract": str(run_dir / "evidence" / "story-contract.json")}, indent=2))


def cmd_impact(args):
    config, catalog, services, store = context(args)
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    if args.run:
        manifest = store.load_manifest(args.run)
        scope = manifest["selected_services"]
        if args.services and selected(args.services, services) != scope:
            raise GateError("resumed run service scope differs from the persisted user selection")
    else:
        story = story_key(args.story)
        scope = selected(args.services, services)
        matches = []
        for candidate in store.root.glob("RUN-*/manifest.json"):
            value = json.loads(candidate.read_text(encoding="utf-8"))
            if value.get("story_key") == story and value.get("selected_services") == scope and not value.get("canceled"):
                matches.append(value)
        if not matches:
            raise GateError(f"run intake first for {story}; impact never creates or expands run scope")
        if len(matches) > 1:
            raise GateError("multiple matching runs exist; reconcile them and pass --run explicitly")
        manifest = matches[0]
        args.run = manifest["run_id"]
    entries = plan.get("services", {})
    if set(entries) - set(scope):
        raise GateError("impact plan references services outside the selected scope")
    classifications = {"CHANGE_REQUIRED", "VERIFY_ONLY", "UNAFFECTED", "UNKNOWN"}
    for sid in scope:
        if entries.get(sid, {}).get("classification") not in classifications:
            raise GateError(f"impact plan lacks a valid classification for {sid}")
    if any(entries[sid]["classification"] == "UNKNOWN" for sid in scope):
        raise GateError("UNKNOWN material impact blocks plan freeze")
    plan.update({"frozen": True, "selected_services": scope, "catalog_fingerprint": manifest["catalog_fingerprint"], "fingerprint": fingerprint(plan), "frozen_at": now()})
    atomic_json(store.run_dir(args.run) / "evidence" / "impact-plan.json", plan)
    manifest["impact_plan"] = plan
    manifest["stage"] = "PLAN_READY"
    store.save_manifest(manifest)
    for sid in scope:
        state = store.load_repository(args.run, sid)
        state["stage"] = "PLAN_READY"
        state["plan_fingerprint"] = plan["fingerprint"]
        store.save_repository(state)
    store.journal(args.run, "impact", "completed", {"plan_fingerprint": plan["fingerprint"]})
    print(json.dumps({"run_id": args.run, "plan_fingerprint": plan["fingerprint"]}, indent=2))


def cmd_prepare(args):
    config, _, services, store = context(args)
    manifest = store.load_manifest(args.run)
    if manifest.get("stage") != "PLAN_READY":
        raise GateError("prepare requires a frozen impact plan")
    groups = verification_groups(manifest, services)
    if not args.all_selected_changes:
        raise GateError("prepare requires --all-selected-changes")
    prepared = []
    for members in groups:
        representative = members[0]
        with lock(store.root / "locks" / f"repo-{fingerprint(services[representative]['canonical_repository_identity'])[:16]}-{manifest['story_key']}.lock"):
            publication_required = any(manifest["impact_plan"]["services"][sid]["classification"] == "CHANGE_REQUIRED" for sid in members)
            details = git_ops.prepare_worktree(services[representative], manifest["story_key"], args.run) if publication_required else git_ops.prepare_verification_worktree(services[representative], args.run)
            for sid in members:
                state = store.load_repository(args.run, sid)
                state.update(details)
                state["stage"] = "WORKTREE_READY"
                state["repository_run_service"] = representative
                state["repository_service_ids"] = members
                state["publication_required"] = manifest["impact_plan"]["services"][sid]["classification"] == "CHANGE_REQUIRED"
                store.save_repository(state)
            prepared.append({"repository_run_service": representative, "service_ids": members})
            store.journal(args.run, f"prepare:{representative}", "completed", {**details, "service_ids": members})
    manifest["stage"] = "WORKTREE_READY"
    store.save_manifest(manifest)
    print(json.dumps({"run_id": args.run, "prepared": prepared}, indent=2))


def cmd_verify(args):
    config, _, services, store = context(args)
    state = store.load_repository(args.run, service_id(args.service))
    if state.get("stage") not in {"WORKTREE_READY", "IMPLEMENTED", "VERIFIED", "FAILED"}:
        raise GateError(f"cannot verify from stage {state.get('stage')}")
    evidence = execute_checks(services[args.service], state["worktree"], store.run_dir(args.run) / "evidence" / args.service)
    state["checks"] = evidence["results"]
    state["verified_diff_fingerprint"] = evidence["diff_fingerprint"]
    state["checks_passed"] = required_passed(evidence)
    if not state["checks_passed"]:
        state.setdefault("retry_counts", {})["verification_failures"] = state.setdefault("retry_counts", {}).get("verification_failures", 0) + 1
        limit = config["policy"].get("maximum_repair_cycles", 2) + 1
        if state["retry_counts"]["verification_failures"] >= limit:
            state["error_summary"] = "verification repair budget exhausted"
    state["stage"] = "VERIFIED" if state["checks_passed"] else "FAILED"
    store.save_repository(state)
    store.journal(args.run, f"verify:{args.service}", "completed", {"passed": state["checks_passed"], "diff_fingerprint": evidence["diff_fingerprint"]})
    print(json.dumps(evidence, indent=2))
    return 0 if state["checks_passed"] else 3


def cmd_verify_contracts(args):
    config, _, services, store = context(args)
    manifest = store.load_manifest(args.run)
    checks = manifest.get("impact_plan", {}).get("contract_checks", [])
    synthetic = {"id": "contracts", "checks": checks}
    evidence = execute_checks(synthetic, SCRIPT_DIR.parent, store.run_dir(args.run) / "evidence" / "contracts")
    evidence["candidate_revisions"] = {}
    for sid, item in manifest.get("impact_plan", {}).get("services", {}).items():
        if item.get("classification") in {"CHANGE_REQUIRED", "VERIFY_ONLY"}:
            state = store.load_repository(args.run, sid)
            evidence["candidate_revisions"][sid] = {"base_sha": state.get("base_sha"), "diff_fingerprint": git_ops.diff_fingerprint(state["worktree"]) if state.get("worktree") else None}
    atomic_json(store.run_dir(args.run) / "evidence" / "contracts" / "verification.json", evidence)
    manifest["contract_evidence"] = evidence
    manifest["contracts_passed"] = required_passed(evidence)
    store.save_manifest(manifest)
    print(json.dumps(evidence, indent=2))
    return 0 if manifest["contracts_passed"] else 3


def cmd_record_review(args):
    _, _, _, store = context(args)
    state = store.load_repository(args.run, service_id(args.service))
    if state.get("stage") != "VERIFIED" or not state.get("checks_passed"):
        raise GateError("a passing verification is required before review")
    current = git_ops.diff_fingerprint(state["worktree"])
    if current != state.get("verified_diff_fingerprint"):
        raise GateError("diff changed after verification")
    findings = json.loads(Path(args.findings).read_text(encoding="utf-8")) if args.findings else []
    blocking = [x for x in findings if x.get("blocking") and not x.get("resolved")]
    state.update({"reviewed_diff_fingerprint": current, "review_findings": findings, "blocking_findings": blocking, "stage": "REVIEWED" if not blocking else "FAILED"})
    store.save_repository(state)
    print(json.dumps({"stage": state["stage"], "diff_fingerprint": current, "blocking_findings": len(blocking)}, indent=2))


def cmd_approve(args):
    _, _, _, store = context(args)
    state = store.load_repository(args.run, service_id(args.service))
    if state.get("stage") != "REVIEWED":
        raise GateError("approval can only bind a reviewed revision")
    state["approval_scope"] = {"run_id": args.run, "diff_fingerprint": state["reviewed_diff_fingerprint"], "destination": state["base_ref"], "allowed_writes": ["commit", "push", "pull_request"], "recorded_at": now(), "source": "active-session-user-approval"}
    state["stage"] = "AWAITING_APPROVAL"
    store.save_repository(state)
    print(json.dumps(state["approval_scope"], indent=2))


def cmd_status(args):
    _, _, _, store = context(args)
    manifest = store.load_manifest(args.run)
    manifest["repository_states"] = {sid: store.load_repository(args.run, sid).get("stage") for sid in manifest["selected_services"]}
    print(json.dumps(manifest, indent=2))


def cmd_resume(args):
    _, _, _, store = context(args)
    manifest = store.load_manifest(args.run)
    scope = [service_id(args.service)] if args.service else manifest["selected_services"]
    report = {}
    for sid in scope:
        state = store.load_repository(args.run, sid)
        if state.get("worktree") and Path(state["worktree"]).exists():
            state["actual_diff_fingerprint"] = git_ops.diff_fingerprint(state["worktree"])
            if state.get("reviewed_diff_fingerprint") and state["actual_diff_fingerprint"] != state["reviewed_diff_fingerprint"]:
                state["stage"] = "IMPLEMENTED"
                state.pop("approval_scope", None)
                state["error_summary"] = "diff changed; verification and review invalidated"
                store.save_repository(state)
        report[sid] = {"stage": state["stage"], "next": next_action(state["stage"])}
    print(json.dumps(report, indent=2))


def next_action(stage):
    return {"INTAKE_READY": "create and freeze impact plan", "PLAN_READY": "prepare worktree", "WORKTREE_READY": "implement story", "IMPLEMENTED": "verify", "VERIFIED": "review", "REVIEWED": "record user approval", "AWAITING_APPROVAL": "publish", "COMMITTED": "resume push", "PUSHED": "resume PR creation", "PR_CREATED_SYNC_PENDING": "retry Jira synchronization", "FAILED": "repair or resolve blocker", "CANCELED": "none"}.get(stage, "inspect status")


def cmd_publish(args):
    config, _, services, store = context(args)
    manifest = store.load_manifest(args.run)
    groups = changed_groups(manifest, services)
    changed_services = [sid for members in groups for sid in members if manifest["impact_plan"]["services"][sid]["classification"] == "CHANGE_REQUIRED"]
    gated_services = [sid for sid, item in manifest["impact_plan"]["services"].items() if item["classification"] in {"CHANGE_REQUIRED", "VERIFY_ONLY"}]
    states = [store.load_repository(args.run, sid) for sid in gated_services]
    if manifest.get("dry_run"):
        raise GateError("fixture/dry-run evidence cannot be published")
    current_story = jira_adapter(config["jira"], config["policy"], config["trusted_hosts"]).fetch_issue(manifest["story_key"])
    current_updated = current_story.get("fields", {}).get("updated")
    if current_updated != manifest.get("story_updated"):
        raise GateError("Jira story changed after intake; revalidate requirements and downstream evidence")
    enforce_publication(config, manifest, states)
    client = bitbucket_adapter(config["bitbucket"], config["policy"], config["trusted_hosts"])
    for members in groups:
        changed_members = [sid for sid in members if sid in changed_services]
        sid = changed_members[0]
        state = store.load_repository(args.run, sid)
        service = services[sid]
        try:
            if state["stage"] in {"REVIEWED", "AWAITING_APPROVAL"}:
                explicit = sorted({path for member in changed_members for path in manifest["impact_plan"]["services"][member].get("reviewed_paths", [])})
                state["commit_sha"] = git_ops.commit_reviewed(state, explicit, f"{manifest['story_key']}: implement story")
                state["stage"] = "COMMITTED"
                _propagate_publication(store, state, changed_members)
            if state["stage"] == "COMMITTED":
                state["remote_sha"] = git_ops.push(state, service.get("allowed_remote", "origin"))
                state["stage"] = "PUSHED"
                _propagate_publication(store, state, changed_members)
            if state["stage"] == "PUSHED":
                repository = service["repository"]
                existing = client.pull_requests(repository, state["branch"], service["base_branch"])
                values = existing.get("values", existing.get("pullRequests", []))
                if values:
                    pr = values[0]
                else:
                    body = f"Jira: {manifest['story_key']}\n\nVerified diff: {state['reviewed_diff_fingerprint']}\n\nChecks:\n" + "\n".join(f"- {x['name']}: {x['status']}" for x in state["checks"])
                    pr = client.create_pull_request(repository, f"{manifest['story_key']}: story implementation", state["branch"], service["base_branch"], body)
                state["pr_identifier"] = pr.get("id")
                state["pr_url"] = pr.get("links", {}).get("html", {}).get("href") or pr.get("links", {}).get("self", [{}])[0].get("href")
                state["stage"] = "PR_CREATED"
                _propagate_publication(store, state, changed_members)
        except Exception as exc:
            state["error_summary"] = str(exc)
            _propagate_publication(store, state, changed_members)
            store.journal(args.run, f"publish:{sid}", "failed", {"error": str(exc)})
            raise
    try:
        pr_states = [store.load_repository(args.run, members[0]) for members in groups]
        links = [state.get("pr_url") for state in pr_states if state.get("pr_url")]
        if len(links) > 1:
            link_section = "\n\nRelated pull requests:\n" + "\n".join(f"- {url}" for url in links)
            for members, state in zip(groups, pr_states):
                sid = next(x for x in members if x in changed_services)
                service = services[sid]
                title = f"{manifest['story_key']}: story implementation"
                body = _pull_request_body(manifest, state) + link_section
                client.update_pull_request(service["repository"], state["pr_identifier"], title, state["branch"], service["base_branch"], body)
                state["pr_cross_links"] = links
                _propagate_publication(store, state, [x for x in members if x in changed_services])
        jira_writes = config["policy"].get("jira_commenting_enabled") or config["policy"].get("jira_transition_enabled")
        if jira_writes:
            jira = jira_adapter(config["jira"], config["policy"], config["trusted_hosts"])
            marker = f"[jira-pr-run:{args.run}]"
            if config["policy"].get("jira_commenting_enabled"):
                comments = jira.fetch_comments(manifest["story_key"])
                existing = next((comment for comment in comments if marker in json.dumps(comment.get("body", ""), sort_keys=True)), None)
                if existing:
                    manifest["jira_comment_identifier"] = existing.get("id")
                else:
                    body = marker + "\nPull requests created:\n" + "\n".join(f"- {url}" for url in links)
                    created = jira.add_comment(manifest["story_key"], body)
                    manifest["jira_comment_identifier"] = created.get("id")
            if config["policy"].get("jira_transition_enabled"):
                transition_id = config["jira"].get("review_transition_id")
                if not transition_id:
                    raise GateError("Jira transition is enabled but review_transition_id is unresolved")
                valid = {str(item.get("id")) for item in jira.transitions(manifest["story_key"])}
                if str(transition_id) not in valid:
                    raise GateError("configured Jira review transition is not currently valid for the story")
                jira.transition(manifest["story_key"], transition_id)
                manifest["jira_transition_result"] = {"transition_id": str(transition_id), "status": "completed"}
        for sid in changed_services:
            state = store.load_repository(args.run, sid)
            state["stage"] = "COMPLETED"
            state["jira_comment_identifier"] = manifest.get("jira_comment_identifier")
            state["transition_result"] = manifest.get("jira_transition_result")
            store.save_repository(state)
    except Exception as exc:
        for sid in changed_services:
            state = store.load_repository(args.run, sid)
            if state.get("pr_identifier"):
                state["stage"] = "PR_CREATED_SYNC_PENDING"
                state["error_summary"] = str(exc)
                store.save_repository(state)
        manifest["stage"] = "PR_CREATED_SYNC_PENDING"
        store.save_manifest(manifest)
        store.journal(args.run, "reconcile-and-jira-sync", "failed", {"error": str(exc)})
        raise
    manifest["stage"] = "COMPLETED" if all(store.load_repository(args.run, sid)["stage"] == "COMPLETED" for sid in changed_services) else "PR_CREATED_SYNC_PENDING"
    store.save_manifest(manifest)
    print(json.dumps({sid: {"stage": store.load_repository(args.run, sid)["stage"], "pr_url": store.load_repository(args.run, sid).get("pr_url")} for sid in changed_services}, indent=2))


def _propagate_publication(store, source, service_ids):
    publication_fields = ("stage", "commit_sha", "remote_sha", "pr_identifier", "pr_url", "pr_cross_links", "error_summary")
    for sid in service_ids:
        target = store.load_repository(source["run_id"], sid)
        for field in publication_fields:
            if field in source:
                target[field] = source[field]
        store.save_repository(target)


def _pull_request_body(manifest, state):
    return f"Jira: {manifest['story_key']}\n\nVerified diff: {state['reviewed_diff_fingerprint']}\n\nChecks:\n" + "\n".join(f"- {x['name']}: {x['status']}" for x in state["checks"])


def cmd_cancel(args):
    _, _, _, store = context(args)
    manifest = store.load_manifest(args.run)
    manifest.update({"stage": "CANCELED", "canceled": True, "canceled_at": now()})
    store.save_manifest(manifest)
    for sid in manifest["selected_services"]:
        state = store.load_repository(args.run, sid)
        if state.get("stage") != "COMPLETED":
            state["stage"] = "CANCELED"
            store.save_repository(state)
    store.journal(args.run, "cancel", "completed", {"resources_preserved": True})
    print(json.dumps({"run_id": args.run, "stage": "CANCELED", "resources_preserved": True}, indent=2))


def parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config")
    common.add_argument("--services-config")
    common.add_argument("--state-root")
    root = argparse.ArgumentParser(description="Jira-to-Bitbucket deterministic workflow helper")
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", parents=[common]).set_defaults(func=cmd_doctor)
    p = sub.add_parser("intake", parents=[common]); p.add_argument("--story", required=True); p.add_argument("--services", required=True); p.add_argument("--fixture"); p.add_argument("--dry-run", action="store_true"); p.add_argument("--run"); p.set_defaults(func=cmd_intake)
    p = sub.add_parser("impact", parents=[common]); p.add_argument("--story"); p.add_argument("--services"); p.add_argument("--run"); p.add_argument("--plan", required=True); p.set_defaults(func=cmd_impact)
    p = sub.add_parser("prepare", parents=[common]); p.add_argument("--run", required=True); p.add_argument("--all-selected-changes", action="store_true"); p.set_defaults(func=cmd_prepare)
    p = sub.add_parser("verify", parents=[common]); p.add_argument("--run", required=True); p.add_argument("--service", required=True); p.set_defaults(func=cmd_verify)
    p = sub.add_parser("verify-contracts", parents=[common]); p.add_argument("--run", required=True); p.set_defaults(func=cmd_verify_contracts)
    p = sub.add_parser("record-review", parents=[common]); p.add_argument("--run", required=True); p.add_argument("--service", required=True); p.add_argument("--findings"); p.set_defaults(func=cmd_record_review)
    p = sub.add_parser("approve", parents=[common]); p.add_argument("--run", required=True); p.add_argument("--service", required=True); p.set_defaults(func=cmd_approve)
    p = sub.add_parser("status", parents=[common]); p.add_argument("--run", required=True); p.set_defaults(func=cmd_status)
    p = sub.add_parser("resume", parents=[common]); p.add_argument("--run", required=True); p.add_argument("--service"); p.set_defaults(func=cmd_resume)
    p = sub.add_parser("publish", parents=[common]); p.add_argument("--run", required=True); p.set_defaults(func=cmd_publish)
    p = sub.add_parser("cancel", parents=[common]); p.add_argument("--run", required=True); p.set_defaults(func=cmd_cancel)
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        result = args.func(args)
        return result or 0
    except (WorkflowError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
