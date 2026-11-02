import base64
import json
import os
from pathlib import Path
from datetime import datetime, timezone

from .errors import ConfigurationError, WorkflowError
from .http import JsonClient
from .validation import fingerprint


def auth_headers(section):
    auth = section.get("auth", {})
    env = auth.get("environment", {})
    strategy = auth.get("strategy")
    if strategy == "none":
        return {}
    if strategy == "bearer":
        token = os.environ.get(env.get("token", ""))
        if not token:
            raise ConfigurationError(f"missing Jira credential environment variable {env.get('token')!r}")
        return {"Authorization": f"Bearer {token}"}
    username = os.environ.get(env.get("username", ""))
    token = os.environ.get(env.get("token", ""))
    if not username or not token:
        raise ConfigurationError("missing Jira basic-auth environment variables")
    encoded = base64.b64encode(f"{username}:{token}".encode()).decode()
    return {"Authorization": f"Basic {encoded}"}


class JiraAdapter:
    def __init__(self, section, policy, trusted_hosts):
        self.section = section
        self.client = JsonClient(section["base_url"], trusted_hosts, auth_headers(section), policy.get("maximum_network_retries", 3))

    def fetch_issue(self, key):
        raise NotImplementedError

    def fetch_comments(self, key):
        raise NotImplementedError

    def fetch_relevant_comments(self, key):
        keywords = [x.lower() for x in self.section.get("relevant_comment_keywords", [])]
        if not keywords:
            return []
        comments = self.fetch_comments(key)
        return [comment for comment in comments if any(word in _text(comment.get("body")).lower() for word in keywords)]


class JiraCloud(JiraAdapter):
    documentation = "https://developer.atlassian.com/cloud/jira/platform/rest/v3/"

    def fetch_issue(self, key):
        return self.client.request("GET", f"rest/api/3/issue/{key}?expand=names")

    def fetch_comments(self, key):
        return self._paged_comments(f"rest/api/3/issue/{key}/comment")

    def _paged_comments(self, path):
        start, comments = 0, []
        while True:
            page = self.client.request("GET", f"{path}?startAt={start}&maxResults=100")
            values = page.get("comments", [])
            comments.extend(values)
            start += len(values)
            if not values or start >= page.get("total", start):
                return comments

    def add_comment(self, key, body):
        document = {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": body}]}]}
        return self.client.request("POST", f"rest/api/3/issue/{key}/comment", {"body": document})

    def transitions(self, key):
        return self.client.request("GET", f"rest/api/3/issue/{key}/transitions").get("transitions", [])

    def transition(self, key, transition_id):
        return self.client.request("POST", f"rest/api/3/issue/{key}/transitions", {"transition": {"id": str(transition_id)}})


class JiraDataCenter(JiraAdapter):
    documentation = "https://developer.atlassian.com/server/jira/platform/rest-apis/"

    def fetch_issue(self, key):
        return self.client.request("GET", f"rest/api/2/issue/{key}?expand=names")

    def fetch_comments(self, key):
        start, comments = 0, []
        while True:
            page = self.client.request("GET", f"rest/api/2/issue/{key}/comment?startAt={start}&maxResults=100")
            values = page.get("comments", [])
            comments.extend(values)
            start += len(values)
            if not values or start >= page.get("total", start):
                return comments

    def add_comment(self, key, body):
        return self.client.request("POST", f"rest/api/2/issue/{key}/comment", {"body": body})

    def transitions(self, key):
        return self.client.request("GET", f"rest/api/2/issue/{key}/transitions").get("transitions", [])

    def transition(self, key, transition_id):
        return self.client.request("POST", f"rest/api/2/issue/{key}/transitions", {"transition": {"id": str(transition_id)}})


def adapter(section, policy, trusted_hosts):
    return (JiraCloud if section["deployment"] == "cloud" else JiraDataCenter)(section, policy, trusted_hosts)


def fixture_issue(path, key):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    issue = data.get("issues", {}).get(key)
    if not issue:
        raise WorkflowError(f"fixture does not contain {key}")
    return issue


def _text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if value.get("type") == "text":
            return value.get("text", "")
        return "".join(_text(x) for x in value.get("content", []))
    if isinstance(value, list):
        return "".join(_text(x) for x in value)
    return str(value)


def normalize(issue, section, parent=None, comments=None):
    fields = issue.get("fields", {})
    key = issue.get("key", "")
    project = key.split("-", 1)[0]
    issue_type = fields.get("issuetype", {}).get("name")
    if project not in section["allowed_project_keys"]:
        raise WorkflowError(f"project {project} is not allowed")
    if issue_type not in section["story_issue_types"]:
        raise WorkflowError(f"{key} is not a configured story type")
    criteria_field = section.get("acceptance_criteria_field_id")
    if not criteria_field:
        raise ConfigurationError("jira.acceptance_criteria_field_id is unresolved")
    raw_criteria = fields.get(criteria_field)
    if isinstance(raw_criteria, list):
        criteria = [_text(x).strip() for x in raw_criteria if _text(x).strip()]
    else:
        criteria = [x.strip(" -*\t") for x in _text(raw_criteria).splitlines() if x.strip(" -*\t")]
    if not criteria:
        raise WorkflowError("story has no testable acceptance criteria")
    dependencies = []
    for link in fields.get("issuelinks", []):
        linked = link.get("outwardIssue") or link.get("inwardIssue")
        if linked:
            dependencies.append({"key": linked.get("key"), "status": linked.get("fields", {}).get("status", {}).get("name", "UNKNOWN")})
    blocked = [x for x in dependencies if x["status"].lower() not in {"done", "closed", "resolved"}]
    contract = {
        "story_key": key,
        "title": fields.get("summary", ""),
        "description": _text(fields.get("description")),
        "acceptance_criteria": [{"id": f"AC-{i}", "text": text} for i, text in enumerate(criteria, 1)],
        "exclusions": [],
        "parent_context": {"key": parent.get("key"), "title": parent.get("fields", {}).get("summary", ""), "description": _text(parent.get("fields", {}).get("description"))} if parent else {},
        "dependencies": dependencies,
        "blocking_dependencies": blocked,
        "relevant_comments": [{"id": x.get("id"), "body": _text(x.get("body")), "updated": x.get("updated")} for x in (comments or [])],
        "unresolved_questions": [],
        "updated": fields.get("updated"),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "source_fields": {"description": "description", "acceptance_criteria": criteria_field},
        "source_references": [{"issue_key": key, "field_id": "description"}, {"issue_key": key, "field_id": criteria_field}],
    }
    contract["content_hash"] = fingerprint(contract)
    return contract
