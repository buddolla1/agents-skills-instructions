import json
import os
import subprocess
import time
from pathlib import Path

from .git import diff_fingerprint
from .state import atomic_json, now
from .validation import redact


def execute_checks(service, worktree, evidence_dir, secrets=()):
    evidence_dir = Path(evidence_dir)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for index, check in enumerate(service.get("checks", []), 1):
        cwd = (Path(worktree) / check.get("working_directory", ".")).resolve()
        root = Path(worktree).resolve()
        if root not in (cwd, *cwd.parents):
            raise ValueError("check working directory escapes worktree")
        started = time.monotonic()
        status = "NOT_RUN"
        exit_code = None
        output = ""
        try:
            result = subprocess.run(check["command"], cwd=cwd, text=True, capture_output=True, timeout=check.get("timeout_seconds", 300), env=os.environ.copy())
            exit_code = result.returncode
            status = "PASS" if result.returncode == 0 else "FAIL"
            output = redact(result.stdout + result.stderr, secrets)
        except FileNotFoundError as exc:
            output = f"tool not found: {exc.filename}"
        except subprocess.TimeoutExpired as exc:
            status = "FAIL"
            output = f"timed out after {check.get('timeout_seconds', 300)} seconds\n{exc.stdout or ''}\n{exc.stderr or ''}"
        log = evidence_dir / f"{index:02d}-{check.get('name', 'check')}.log"
        log.write_text(redact(output, secrets)[:1_000_000], encoding="utf-8")
        results.append({"name": check.get("name", f"check-{index}"), "command": check["command"], "working_directory": str(cwd), "required": check.get("required", True), "status": status, "exit_code": exit_code, "duration_seconds": round(time.monotonic() - started, 3), "log": str(log)})
    evidence = {"created_at": now(), "diff_fingerprint": diff_fingerprint(worktree), "results": results}
    atomic_json(evidence_dir / "verification.json", evidence)
    return evidence


def required_passed(evidence):
    return all(not result["required"] or result["status"] == "PASS" for result in evidence["results"])
