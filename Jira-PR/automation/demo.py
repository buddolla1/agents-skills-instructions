#!/usr/bin/env python3
"""Run an entirely offline fixture demonstration in temporary directories."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from automation import flow
from automation.lib.state import atomic_json


def git(*args, cwd=None):
    subprocess.run(["git", *args], cwd=cwd, check=True, text=True, capture_output=True)


def main():
    with tempfile.TemporaryDirectory(prefix="jira-pr-demo-") as temporary:
        root = Path(temporary)
        remote, repo = root / "remote.git", root / "orders"
        git("init", "--bare", str(remote))
        git("init", "-b", "main", str(repo))
        git("config", "user.name", "Fixture User", cwd=repo)
        git("config", "user.email", "fixture@example.test", cwd=repo)
        (repo / "README.md").write_text("fixture repository\n", encoding="utf-8")
        git("add", "README.md", cwd=repo); git("commit", "-m", "fixture base", cwd=repo)
        git("remote", "add", "origin", str(remote), cwd=repo); git("push", "-u", "origin", "main", cwd=repo)
        config = {
            "jira": {"deployment": "cloud", "base_url": "https://jira.example.test", "auth": {"strategy": "none", "environment": {}}, "story_issue_types": ["Story"], "acceptance_criteria_field_id": "customfield_10000", "parent_field_id": "parent", "allowed_project_keys": ["TEAM"]},
            "bitbucket": {"deployment": "cloud", "base_url": "https://api.bitbucket.org", "auth": {"strategy": "none", "environment": {}}},
            "policy": {"maximum_repair_cycles": 2, "maximum_network_retries": 0, "publication_mode": "review", "jira_commenting_enabled": False, "jira_transition_enabled": False},
        }
        services = {"catalog_version": "fixture", "services": [{"id": "orders", "local_path": str(repo), "repository": {"deployment": "cloud", "workspace": "fixture", "slug": "orders"}, "allowed_remote": "origin", "base_branch": "main", "worktree_root": str(root / "worktrees"), "branch_prefix": "story", "checks": [{"name": "fixture-test", "command": [sys.executable, "-c", "from pathlib import Path; assert Path('status.txt').read_text() == 'ready\\n'"], "working_directory": ".", "timeout_seconds": 30, "required": True}]}]}
        config_path, services_path, state_root = root / "config.json", root / "services.json", root / ".agent-runs"
        atomic_json(config_path, config); atomic_json(services_path, services)
        common = ["--config", str(config_path), "--services-config", str(services_path), "--state-root", str(state_root)]
        intake_args = ["intake", *common, "--story", "TEAM-100", "--services", "orders", "--fixture", str(HERE / "fixtures" / "jira-cloud.json"), "--dry-run", "--run", "RUN-DEMO"]
        if flow.main(intake_args): return 1
        if flow.main(["impact", *common, "--run", "RUN-DEMO", "--plan", str(HERE / "fixtures" / "impact-plan.json")]): return 1
        if flow.main(["prepare", *common, "--run", "RUN-DEMO", "--all-selected-changes"]): return 1
        state = json.loads((state_root / "RUN-DEMO" / "repositories" / "orders.json").read_text())
        (Path(state["worktree"]) / "status.txt").write_text("ready\n", encoding="utf-8")
        state["stage"] = "IMPLEMENTED"; atomic_json(state_root / "RUN-DEMO" / "repositories" / "orders.json", state)
        if flow.main(["verify", *common, "--run", "RUN-DEMO", "--service", "orders"]): return 1
        if flow.main(["verify-contracts", *common, "--run", "RUN-DEMO"]): return 1
        if flow.main(["record-review", *common, "--run", "RUN-DEMO", "--service", "orders"]): return 1
        if flow.main(["approve", *common, "--run", "RUN-DEMO", "--service", "orders"]): return 1
        manifest = json.loads((state_root / "RUN-DEMO" / "manifest.json").read_text())
        state = json.loads((state_root / "RUN-DEMO" / "repositories" / "orders.json").read_text())
        print(json.dumps({"result": "PASS", "run_id": "RUN-DEMO", "story_stage": manifest["stage"], "repository_stage": state["stage"], "checks_passed": state["checks_passed"], "publication": "intentionally not attempted in fixture/dry-run mode"}, indent=2))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
