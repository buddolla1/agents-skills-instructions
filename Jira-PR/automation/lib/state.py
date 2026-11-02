import contextlib
import json
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .errors import LockError, WorkflowError

SCHEMA_VERSION = 1
TERMINAL = {"COMPLETED", "CANCELED"}


def now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)


def read_json(path):
    try:
        with Path(path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"state is missing or unreadable: {path}") from exc


@contextlib.contextmanager
def lock(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise LockError(f"lock is held: {path}") from exc
    try:
        os.write(fd, f"{os.getpid()} {now()}\n".encode())
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


class RunStore:
    def __init__(self, root):
        self.root = Path(root)

    def run_dir(self, run_id):
        if not re.fullmatch(r"RUN-[A-Za-z0-9][A-Za-z0-9-]{0,95}", run_id or ""):
            raise WorkflowError("invalid run ID")
        return self.root / run_id

    def manifest_path(self, run_id):
        return self.run_dir(run_id) / "manifest.json"

    def repository_path(self, run_id, service):
        return self.run_dir(run_id) / "repositories" / f"{service}.json"

    def journal(self, run_id, operation, status, details=None):
        entry = {"time": now(), "operation": operation, "status": status, "details": details or {}}
        path = self.run_dir(run_id) / "journal.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")

    def save_manifest(self, value):
        value["updated_at"] = now()
        atomic_json(self.manifest_path(value["run_id"]), value)

    def load_manifest(self, run_id):
        return read_json(self.manifest_path(run_id))

    def save_repository(self, value):
        value["updated_at"] = now()
        atomic_json(self.repository_path(value["run_id"], value["service_id"]), value)

    def load_repository(self, run_id, service):
        return read_json(self.repository_path(run_id, service))
