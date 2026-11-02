import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from .errors import ConfigurationError

STORY_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,19}-[1-9][0-9]{0,9}$")
SERVICE_RE = re.compile(r"^[a-z][a-z0-9-]{0,62}$")
BRANCH_PART_RE = re.compile(r"^[A-Za-z0-9._/-]+$")


def story_key(value):
    if not STORY_RE.fullmatch(value or ""):
        raise ConfigurationError("story key must look like TEAM-123")
    return value


def service_id(value):
    if not SERVICE_RE.fullmatch(value or ""):
        raise ConfigurationError(f"unsafe service ID: {value!r}")
    return value


def branch_name(value):
    if not value or not BRANCH_PART_RE.fullmatch(value) or value.startswith(("-", "/")):
        raise ConfigurationError(f"unsafe branch name: {value!r}")
    if ".." in value or "//" in value or value.endswith(("/", ".lock")):
        raise ConfigurationError(f"unsafe branch name: {value!r}")
    return value


def absolute_path(value, label):
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ConfigurationError(f"{label} must be an absolute path")
    return path.resolve()


def https_url(value, label):
    parsed = urlsplit(value or "")
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ConfigurationError(f"{label} must be an HTTPS URL without credentials")
    return value.rstrip("/")


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(value):
    raw = value if isinstance(value, bytes) else canonical_json(value).encode()
    return hashlib.sha256(raw).hexdigest()


def redact(text, secrets=()):
    result = str(text)
    for secret in secrets:
        if secret:
            result = result.replace(secret, "[REDACTED]")
    result = re.sub(r"(?i)(authorization|cookie|token|password)(\s*[:=]\s*)\S+", r"\1\2[REDACTED]", result)
    result = re.sub(r"https://[^/@\s:]+:[^/@\s]+@", "https://[REDACTED]@", result)
    return result
