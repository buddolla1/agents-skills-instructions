import json
from pathlib import Path
from urllib.parse import urlsplit

from .errors import ConfigurationError
from .validation import absolute_path, branch_name, https_url, service_id


def _read(path):
    try:
        with Path(path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ConfigurationError(f"missing configuration: {path}; copy the corresponding example file") from exc
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"invalid JSON in {path}: {exc}") from exc


def _command(value, label):
    if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
        raise ConfigurationError(f"{label}.command must be a nonempty string array")


def load(config_path, services_path):
    config = _read(config_path)
    catalog = _read(services_path)
    for name in ("jira", "bitbucket", "policy"):
        if not isinstance(config.get(name), dict):
            raise ConfigurationError(f"config requires object {name!r}")
    for name in ("jira", "bitbucket"):
        section = config[name]
        if section.get("deployment") not in {"cloud", "data_center"}:
            raise ConfigurationError(f"{name}.deployment must be cloud or data_center")
        https_url(section.get("base_url"), f"{name}.base_url")
        auth = section.get("auth", {})
        if auth.get("strategy") not in {"basic", "bearer", "none"}:
            raise ConfigurationError(f"unsupported {name} authentication strategy")
        if not isinstance(auth.get("environment", {}), dict):
            raise ConfigurationError(f"{name}.auth.environment must map credential roles to variable names")
    projects = config["jira"].get("allowed_project_keys")
    if not isinstance(projects, list) or not projects:
        raise ConfigurationError("jira.allowed_project_keys must be nonempty")
    if config["policy"].get("publication_mode", "review") not in {"review", "automatic"}:
        raise ConfigurationError("policy.publication_mode must be review or automatic")
    services = catalog.get("services")
    if not isinstance(services, list) or not services:
        raise ConfigurationError("service catalog requires a nonempty services array")
    indexed = {}
    for entry in services:
        sid = service_id(entry.get("id"))
        if sid in indexed:
            raise ConfigurationError(f"duplicate service ID: {sid}")
        repo = entry.get("repository", {})
        entry["local_path"] = str(absolute_path(entry.get("local_path", ""), f"{sid}.local_path"))
        entry["worktree_root"] = str(absolute_path(entry.get("worktree_root", ""), f"{sid}.worktree_root"))
        branch_name(entry.get("base_branch", ""))
        branch_name(entry.get("branch_prefix", "story"))
        if repo.get("deployment") not in {"cloud", "data_center"}:
            raise ConfigurationError(f"{sid}.repository.deployment is invalid")
        if not repo.get("slug"):
            raise ConfigurationError(f"{sid}.repository.slug is required")
        if repo["deployment"] == "cloud" and not repo.get("workspace"):
            raise ConfigurationError(f"{sid}.repository.workspace is required for Cloud")
        if repo["deployment"] == "data_center" and not repo.get("project_key"):
            raise ConfigurationError(f"{sid}.repository.project_key is required for Data Center")
        identity = {"deployment": repo["deployment"], "slug": repo["slug"]}
        identity["workspace" if repo["deployment"] == "cloud" else "project_key"] = repo.get("workspace") if repo["deployment"] == "cloud" else repo.get("project_key")
        entry["canonical_repository_identity"] = json.dumps(identity, sort_keys=True, separators=(",", ":"))
        for check in entry.get("checks", []):
            _command(check.get("command"), f"{sid}.{check.get('name', 'check')}")
            if not isinstance(check.get("timeout_seconds", 300), int) or check.get("timeout_seconds", 300) < 1:
                raise ConfigurationError(f"{sid} check timeout must be a positive integer")
        indexed[sid] = entry
    repository_settings = {}
    for sid, entry in indexed.items():
        identity = entry["canonical_repository_identity"]
        settings = (entry["local_path"], entry["worktree_root"], entry.get("allowed_remote", "origin"), entry["base_branch"], entry.get("branch_prefix", "story"))
        if identity in repository_settings and repository_settings[identity][0] != settings:
            other = repository_settings[identity][1]
            raise ConfigurationError(f"services {other} and {sid} share a repository but disagree on local path, worktree, remote, base, or branch prefix")
        repository_settings[identity] = (settings, sid)
    hosts = {urlsplit(config[x]["base_url"]).hostname for x in ("jira", "bitbucket")}
    config["trusted_hosts"] = sorted(hosts)
    return config, catalog, indexed
