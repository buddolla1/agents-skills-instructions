import json
import ssl
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .errors import WorkflowError
from .validation import redact


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise WorkflowError("HTTP redirects are disabled to prevent credential forwarding")


class JsonClient:
    def __init__(self, base_url, trusted_hosts, headers=None, retries=3, timeout=30, max_bytes=5_000_000):
        self.base_url = base_url.rstrip("/") + "/"
        self.trusted_hosts = set(trusted_hosts)
        self.headers = headers or {}
        self.retries = retries
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.opener = build_opener(NoRedirect())

    def request(self, method, path, payload=None):
        url = urljoin(self.base_url, path.lstrip("/"))
        if urlsplit(url).hostname not in self.trusted_hosts or not url.startswith("https://"):
            raise WorkflowError("request target is not a configured trusted HTTPS host")
        body = json.dumps(payload).encode() if payload is not None else None
        headers = {"Accept": "application/json", **self.headers}
        if body is not None:
            headers["Content-Type"] = "application/json"
        for attempt in range(self.retries + 1):
            try:
                response = self.opener.open(Request(url, data=body, headers=headers, method=method), timeout=self.timeout)
                raw = response.read(self.max_bytes + 1)
                if len(raw) > self.max_bytes:
                    raise WorkflowError("HTTP response exceeded configured size limit")
                return json.loads(raw) if raw else {}
            except HTTPError as exc:
                if exc.code == 429 or 500 <= exc.code < 600:
                    if attempt < self.retries:
                        retry_after = min(float(exc.headers.get("Retry-After", 2**attempt)), 30)
                        time.sleep(retry_after)
                        continue
                raise WorkflowError(f"HTTP {exc.code} from configured service") from exc
            except (URLError, TimeoutError, ssl.SSLError) as exc:
                if attempt < self.retries:
                    time.sleep(min(2**attempt, 10))
                    continue
                raise WorkflowError(redact(f"network request failed: {exc}")) from exc
