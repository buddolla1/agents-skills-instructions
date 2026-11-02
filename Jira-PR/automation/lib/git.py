import os
import subprocess
from pathlib import Path

from .errors import GateError, WorkflowError
from .validation import fingerprint


def run(repo, args, timeout=60, check=True):
    result = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, timeout=timeout)
    if check and result.returncode:
        raise WorkflowError(f"git {' '.join(args[:2])} failed: {result.stderr.strip()}")
    return result


def repository_identity(path):
    path = Path(path)
    if not path.is_dir():
        raise WorkflowError(f"repository path does not exist: {path}")
    root = Path(run(path, ["rev-parse", "--show-toplevel"]).stdout.strip()).resolve()
    return root, run(root, ["rev-parse", "HEAD"]).stdout.strip()


def diff_fingerprint(path):
    tracked = run(path, ["diff", "--binary", "HEAD"], check=False).stdout
    untracked = run(path, ["ls-files", "--others", "--exclude-standard"], check=False).stdout.splitlines()
    payload = tracked.encode()
    for name in sorted(untracked):
        candidate = Path(path) / name
        payload += b"\0" + name.encode() + b"\0" + candidate.read_bytes()
    return fingerprint(payload)


def prepare_worktree(service, story, run_id):
    repo, _ = repository_identity(service["local_path"])
    branch = f"{service.get('branch_prefix', 'story').rstrip('/')}/{story.lower()}"
    worktree = Path(service["worktree_root"]) / run_id / service["id"]
    base = service["base_branch"]
    remote = service.get("allowed_remote", "origin")
    local_collision = run(repo, ["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"], check=False).returncode == 0
    remote_collision = run(repo, ["ls-remote", "--exit-code", "--heads", remote, branch], check=False).returncode == 0
    if local_collision or remote_collision:
        raise GateError(f"branch collision for {branch}; reconcile the existing run instead")
    run(repo, ["fetch", "--no-tags", remote, base], timeout=180)
    base_sha = run(repo, ["rev-parse", f"{remote}/{base}"]).stdout.strip()
    worktree.parent.mkdir(parents=True, exist_ok=True)
    run(repo, ["worktree", "add", "-b", branch, str(worktree), base_sha], timeout=120)
    return {"branch": branch, "worktree": str(worktree), "base_ref": f"{remote}/{base}", "base_sha": base_sha}


def prepare_verification_worktree(service, run_id):
    repo, _ = repository_identity(service["local_path"])
    worktree = Path(service["worktree_root"]) / run_id / f"{service['id']}-verify"
    remote, base = service.get("allowed_remote", "origin"), service["base_branch"]
    if worktree.exists():
        raise GateError(f"verification worktree already exists: {worktree}")
    run(repo, ["fetch", "--no-tags", remote, base], timeout=180)
    base_sha = run(repo, ["rev-parse", f"{remote}/{base}"]).stdout.strip()
    worktree.parent.mkdir(parents=True, exist_ok=True)
    run(repo, ["worktree", "add", "--detach", str(worktree), base_sha], timeout=120)
    return {"branch": None, "worktree": str(worktree), "base_ref": f"{remote}/{base}", "base_sha": base_sha}


def commit_reviewed(state, explicit_paths, message):
    worktree = state["worktree"]
    if diff_fingerprint(worktree) != state.get("reviewed_diff_fingerprint"):
        raise GateError("diff changed after review; verification, review, and approval are invalid")
    for path in explicit_paths:
        run(worktree, ["add", "--", path])
    staged = run(worktree, ["diff", "--cached", "--quiet"], check=False)
    if staged.returncode == 0:
        raise GateError("nothing was staged")
    run(worktree, ["commit", "-m", message], timeout=120)
    return run(worktree, ["rev-parse", "HEAD"]).stdout.strip()


def push(state, remote):
    result = run(state["worktree"], ["push", remote, f"HEAD:refs/heads/{state['branch']}"], timeout=180, check=False)
    if result.returncode:
        raise WorkflowError(f"push rejected; recorded commit is preserved: {result.stderr.strip()}")
    return run(state["worktree"], ["rev-parse", "HEAD"]).stdout.strip()
