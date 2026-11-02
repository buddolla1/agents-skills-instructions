import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

AUTOMATION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION.parent))

from automation.lib import git as git_ops
from automation.lib.bitbucket import BitbucketCloud, BitbucketDataCenter
from automation.lib.checks import execute_checks, required_passed
from automation.lib.config import load
from automation.lib.errors import ConfigurationError, GateError, LockError, WorkflowError
from automation.lib.jira import JiraCloud, JiraDataCenter, normalize
from automation.lib.policy import enforce_publication
from automation.lib.state import RunStore, atomic_json, lock, read_json
from automation.lib.validation import branch_name, redact, story_key


def command(args, cwd=None, check=True):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=check)


class FakeClient:
    def __init__(self):
        self.calls = []

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        return {"values": []}


class PageClient:
    def __init__(self):
        self.calls = []

    def request(self, method, path, payload=None):
        self.calls.append(path)
        if "startAt=0" in path:
            return {"comments": [{"id": "1", "body": "scope decision"}], "total": 2}
        return {"comments": [{"id": "2", "body": "unrelated note"}], "total": 2}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def make_repo(self):
        remote = self.root / "remote.git"
        repo = self.root / "repo"
        command(["git", "init", "--bare", str(remote)])
        command(["git", "init", "-b", "main", str(repo)])
        command(["git", "config", "user.name", "Fixture User"], repo)
        command(["git", "config", "user.email", "fixture@example.test"], repo)
        (repo / "README.md").write_text("original\n", encoding="utf-8")
        command(["git", "add", "README.md"], repo)
        command(["git", "commit", "-m", "fixture"], repo)
        command(["git", "remote", "add", "origin", str(remote)], repo)
        command(["git", "push", "-u", "origin", "main"], repo)
        return repo, remote

    def config_files(self, repo, checks=None, mode="review"):
        config = {
            "jira": {"deployment": "cloud", "base_url": "https://jira.example.test", "auth": {"strategy": "none", "environment": {}}, "story_issue_types": ["Story"], "acceptance_criteria_field_id": "customfield_1", "allowed_project_keys": ["TEAM"]},
            "bitbucket": {"deployment": "data_center", "base_url": "https://bitbucket.example.test", "auth": {"strategy": "none", "environment": {}}},
            "policy": {"publication_mode": mode, "maximum_network_retries": 0, "jira_commenting_enabled": False, "jira_transition_enabled": False},
        }
        catalog = {"catalog_version": "1", "services": [{"id": "orders", "local_path": str(repo), "repository": {"deployment": "cloud", "workspace": "acme", "slug": "orders"}, "allowed_remote": "origin", "base_branch": "main", "worktree_root": str(self.root / "worktrees"), "branch_prefix": "story", "checks": checks or []}]}
        config_path, catalog_path = self.root / "config.json", self.root / "services.json"
        atomic_json(config_path, config); atomic_json(catalog_path, catalog)
        return config_path, catalog_path

    def test_intake_normalizes_parent_criteria_and_dependencies(self):
        issue = {"key": "TEAM-1", "fields": {"summary": "Title", "description": "Body", "issuetype": {"name": "Story"}, "updated": "time", "customfield_1": ["first", "second"], "issuelinks": [{"outwardIssue": {"key": "TEAM-2", "fields": {"status": {"name": "Done"}}}}]}}
        section = {"allowed_project_keys": ["TEAM"], "story_issue_types": ["Story"], "acceptance_criteria_field_id": "customfield_1"}
        value = normalize(issue, section, {"key": "TEAM-0"})
        self.assertEqual(["AC-1", "AC-2"], [x["id"] for x in value["acceptance_criteria"]])
        self.assertEqual("TEAM-0", value["parent_context"]["key"])
        self.assertFalse(value["blocking_dependencies"])

    def test_missing_criteria_and_configuration_block(self):
        issue = {"key": "TEAM-1", "fields": {"issuetype": {"name": "Story"}, "customfield_1": []}}
        base = {"allowed_project_keys": ["TEAM"], "story_issue_types": ["Story"], "acceptance_criteria_field_id": "customfield_1"}
        with self.assertRaises(WorkflowError): normalize(issue, base)
        with self.assertRaises(ConfigurationError): normalize(issue, {**base, "acceptance_criteria_field_id": None})

    def test_blocking_dependency_is_recorded(self):
        issue = {"key": "TEAM-1", "fields": {"issuetype": {"name": "Story"}, "customfield_1": ["works"], "issuelinks": [{"inwardIssue": {"key": "TEAM-9", "fields": {"status": {"name": "Open"}}}}]}}
        value = normalize(issue, {"allowed_project_keys": ["TEAM"], "story_issue_types": ["Story"], "acceptance_criteria_field_id": "customfield_1"})
        self.assertEqual("TEAM-9", value["blocking_dependencies"][0]["key"])

    def test_cloud_and_data_center_adapter_paths_differ(self):
        jira_section = {"base_url": "https://jira.example.test", "auth": {"strategy": "none"}}
        cloud = JiraCloud(jira_section, {"maximum_network_retries": 0}, {"jira.example.test"}); cloud.client = FakeClient(); cloud.fetch_issue("TEAM-1")
        dc = JiraDataCenter(jira_section, {"maximum_network_retries": 0}, {"jira.example.test"}); dc.client = FakeClient(); dc.fetch_issue("TEAM-1")
        self.assertIn("rest/api/3", cloud.client.calls[0][1]); self.assertIn("rest/api/2", dc.client.calls[0][1])
        bb_section = {"base_url": "https://bb.example.test", "auth": {"strategy": "none"}}
        bbc = BitbucketCloud(bb_section, {}, {"bb.example.test"}); bbc.client = FakeClient(); bbc.pull_requests({"workspace": "w", "slug": "r"}, "x", "main")
        bbd = BitbucketDataCenter(bb_section, {}, {"bb.example.test"}); bbd.client = FakeClient(); bbd.pull_requests({"project_key": "P", "slug": "r"}, "x", "main")
        self.assertTrue(bbc.client.calls[0][1].startswith("2.0/")); self.assertTrue(bbd.client.calls[0][1].startswith("rest/api/1.0/"))

    def test_comment_pagination_and_relevance_filter(self):
        section = {"base_url": "https://jira.example.test", "auth": {"strategy": "none"}, "relevant_comment_keywords": ["scope"]}
        cloud = JiraCloud(section, {"maximum_network_retries": 0}, {"jira.example.test"}); cloud.client = PageClient()
        comments = cloud.fetch_relevant_comments("TEAM-1")
        self.assertEqual(["1"], [x["id"] for x in comments])
        self.assertEqual(2, len(cloud.client.calls))

    def test_deployment_specific_jira_write_and_pr_update_paths(self):
        jira_section = {"base_url": "https://jira.example.test", "auth": {"strategy": "none"}}
        cloud = JiraCloud(jira_section, {}, {"jira.example.test"}); cloud.client = FakeClient(); cloud.add_comment("TEAM-1", "body"); cloud.transition("TEAM-1", "31")
        self.assertIn("rest/api/3/issue/TEAM-1/comment", cloud.client.calls[0][1])
        self.assertIn("rest/api/3/issue/TEAM-1/transitions", cloud.client.calls[1][1])
        bb_section = {"base_url": "https://bb.example.test", "auth": {"strategy": "none"}}
        bitbucket = BitbucketCloud(bb_section, {}, {"bb.example.test"}); bitbucket.client = FakeClient()
        bitbucket.update_pull_request({"workspace": "w", "slug": "r"}, 7, "title", "story/x", "main", "body")
        self.assertEqual("PUT", bitbucket.client.calls[0][0]); self.assertTrue(bitbucket.client.calls[0][1].endswith("/pullrequests/7"))

    def test_worktree_preserves_original_changes(self):
        repo, _ = self.make_repo(); config_path, services_path = self.config_files(repo)
        _, _, services = load(config_path, services_path)
        (repo / "README.md").write_text("user change\n", encoding="utf-8")
        before = (repo / "README.md").read_bytes()
        details = git_ops.prepare_worktree(services["orders"], "TEAM-1", "RUN-ONE")
        self.assertEqual(before, (repo / "README.md").read_bytes())
        self.assertTrue(Path(details["worktree"]).is_dir())

    def test_branch_collision_blocks_duplicate_prepare(self):
        repo, _ = self.make_repo(); config_path, services_path = self.config_files(repo)
        _, _, services = load(config_path, services_path)
        git_ops.prepare_worktree(services["orders"], "TEAM-1", "RUN-ONE")
        with self.assertRaises(GateError): git_ops.prepare_worktree(services["orders"], "TEAM-1", "RUN-TWO")

    def test_services_sharing_repository_are_grouped_once(self):
        repo, _ = self.make_repo(); config_path, services_path = self.config_files(repo)
        catalog = json.loads(services_path.read_text())
        second = dict(catalog["services"][0]); second["id"] = "orders-api"; catalog["services"].append(second); atomic_json(services_path, catalog)
        _, _, services = load(config_path, services_path)
        from automation.flow import repository_groups
        self.assertEqual([["orders", "orders-api"]], repository_groups(["orders", "orders-api"], services))

    def test_required_fail_and_not_run_block(self):
        repo, _ = self.make_repo()
        service = {"checks": [{"name": "failure", "command": [sys.executable, "-c", "raise SystemExit(1)"], "required": True}, {"name": "missing", "command": ["tool-that-does-not-exist"], "required": True}]}
        evidence = execute_checks(service, repo, self.root / "evidence")
        self.assertEqual(["FAIL", "NOT_RUN"], [x["status"] for x in evidence["results"]])
        self.assertFalse(required_passed(evidence))

    def publication_state(self, repo, mode="review"):
        config = {"policy": {"publication_mode": mode}}
        state = {"run_id": "RUN-X", "service_id": "orders", "stage": "REVIEWED", "worktree": str(repo), "base_ref": "origin/main", "checks_passed": True, "blocking_findings": []}
        state["reviewed_diff_fingerprint"] = git_ops.diff_fingerprint(repo)
        manifest = {"impact_plan": {"frozen": True}}
        return config, manifest, state

    def test_changed_diff_invalidates_verification_and_approval(self):
        repo, _ = self.make_repo(); (repo / "new.txt").write_text("one", encoding="utf-8")
        config, manifest, state = self.publication_state(repo)
        state["approval_scope"] = {"run_id": "RUN-X", "diff_fingerprint": state["reviewed_diff_fingerprint"], "destination": "origin/main", "allowed_writes": ["commit"]}
        (repo / "new.txt").write_text("two", encoding="utf-8")
        with self.assertRaises(GateError): enforce_publication(config, manifest, [state])

    def test_review_mode_requires_revision_bound_approval(self):
        repo, _ = self.make_repo(); config, manifest, state = self.publication_state(repo)
        with self.assertRaises(GateError): enforce_publication(config, manifest, [state])
        state["approval_scope"] = {"run_id": "RUN-X", "diff_fingerprint": state["reviewed_diff_fingerprint"], "destination": "origin/main", "allowed_writes": ["commit"]}
        enforce_publication(config, manifest, [state])

    def test_automatic_mode_still_requires_authorization_and_checks(self):
        repo, _ = self.make_repo(); config, manifest, state = self.publication_state(repo, "automatic")
        with self.assertRaises(GateError): enforce_publication(config, manifest, [state])
        manifest["automatic_authorization"] = {"recorded": True}; state["checks_passed"] = False
        with self.assertRaises(GateError): enforce_publication(config, manifest, [state])

    def test_push_failure_preserves_commit_and_has_no_force_path(self):
        repo, _ = self.make_repo(); (repo / "change.txt").write_text("change", encoding="utf-8")
        fp = git_ops.diff_fingerprint(repo)
        state = {"worktree": str(repo), "reviewed_diff_fingerprint": fp, "branch": "story/team-1"}
        sha = git_ops.commit_reviewed(state, ["change.txt"], "TEAM-1: change")
        command(["git", "remote", "set-url", "origin", str(self.root / "missing.git")], repo)
        with self.assertRaises(WorkflowError): git_ops.push(state, "origin")
        self.assertEqual(sha, command(["git", "rev-parse", "HEAD"], repo).stdout.strip())

    def test_malicious_story_text_is_only_data(self):
        marker = self.root / "owned"
        issue = {"key": "TEAM-1", "fields": {"issuetype": {"name": "Story"}, "description": f"touch {marker}", "customfield_1": ["safe"]}}
        value = normalize(issue, {"allowed_project_keys": ["TEAM"], "story_issue_types": ["Story"], "acceptance_criteria_field_id": "customfield_1"})
        self.assertIn("touch", value["description"]); self.assertFalse(marker.exists())
        with self.assertRaises(ConfigurationError): branch_name("x;touch-owned")

    def test_logs_and_state_redact_fixture_credentials(self):
        secret = "fixture-secret-value"
        self.assertNotIn(secret, redact(f"Authorization: Bearer {secret}", [secret]))
        repo, _ = self.make_repo()
        service = {"checks": [{"name": "prints", "command": [sys.executable, "-c", f"print('{secret}')"], "required": True}]}
        evidence = execute_checks(service, repo, self.root / "evidence", [secret])
        self.assertNotIn(secret, Path(evidence["results"][0]["log"]).read_text())

    def test_atomic_state_and_lock_contention(self):
        path = self.root / "state.json"; atomic_json(path, {"good": True})
        leftover = self.root / ".state.json.interrupted"; leftover.write_text("{", encoding="utf-8")
        self.assertEqual({"good": True}, read_json(path))
        lock_path = self.root / "run.lock"
        with lock(lock_path):
            with self.assertRaises(LockError):
                with lock(lock_path): pass

    def test_cancellation_preserves_work(self):
        store = RunStore(self.root / "runs"); run = "RUN-CANCEL"
        manifest = {"schema_version": 1, "run_id": run, "selected_services": ["orders"], "stage": "WORKTREE_READY"}
        state = {"schema_version": 1, "run_id": run, "service_id": "orders", "stage": "WORKTREE_READY"}
        store.save_manifest(manifest); store.save_repository(state)
        work = self.root / "work.txt"; work.write_text("keep", encoding="utf-8")
        manifest["canceled"] = True; manifest["stage"] = "CANCELED"; store.save_manifest(manifest)
        state["stage"] = "CANCELED"; store.save_repository(state)
        self.assertEqual("keep", work.read_text()); self.assertEqual("CANCELED", store.load_repository(run, "orders")["stage"])

    def test_partial_pr_success_state_is_resumable(self):
        store = RunStore(self.root / "runs"); state = {"schema_version": 1, "run_id": "RUN-PARTIAL", "service_id": "orders", "stage": "PR_CREATED_SYNC_PENDING", "pr_identifier": 42, "pr_url": "https://bb.example/pr/42", "desired_jira_effect": "pending"}
        store.save_repository(state)
        loaded = store.load_repository("RUN-PARTIAL", "orders")
        self.assertEqual(42, loaded["pr_identifier"]); self.assertEqual("PR_CREATED_SYNC_PENDING", loaded["stage"])

    def test_story_and_config_reject_unsafe_values(self):
        with self.assertRaises(ConfigurationError): story_key("TEAM-1;rm")
        repo, _ = self.make_repo(); config_path, services_path = self.config_files(repo)
        data = json.loads(config_path.read_text()); data["jira"]["base_url"] = "http://jira.example.test"; atomic_json(config_path, data)
        with self.assertRaises(ConfigurationError): load(config_path, services_path)


if __name__ == "__main__":
    unittest.main()
