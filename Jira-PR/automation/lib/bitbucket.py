import urllib.parse

from .http import JsonClient
from .jira import auth_headers


class BitbucketAdapter:
    def __init__(self, section, policy, trusted_hosts):
        self.section = section
        self.client = JsonClient(section["base_url"], trusted_hosts, auth_headers(section), policy.get("maximum_network_retries", 3))


class BitbucketCloud(BitbucketAdapter):
    documentation = "https://developer.atlassian.com/cloud/bitbucket/rest/"

    def pull_requests(self, repository, branch, destination):
        workspace = urllib.parse.quote(repository["workspace"], safe="")
        slug = urllib.parse.quote(repository["slug"], safe="")
        query = urllib.parse.quote(f'state="OPEN" AND source.branch.name="{branch}" AND destination.branch.name="{destination}"')
        return self.client.request("GET", f"2.0/repositories/{workspace}/{slug}/pullrequests?q={query}")

    def create_pull_request(self, repository, title, branch, destination, description):
        path = f"2.0/repositories/{repository['workspace']}/{repository['slug']}/pullrequests"
        return self.client.request("POST", path, {"title": title, "description": description, "source": {"branch": {"name": branch}}, "destination": {"branch": {"name": destination}}})

    def update_pull_request(self, repository, pull_request_id, title, branch, destination, description):
        path = f"2.0/repositories/{repository['workspace']}/{repository['slug']}/pullrequests/{pull_request_id}"
        payload = {"title": title, "description": description, "source": {"branch": {"name": branch}}, "destination": {"branch": {"name": destination}}}
        return self.client.request("PUT", path, payload)


class BitbucketDataCenter(BitbucketAdapter):
    documentation = "https://developer.atlassian.com/server/bitbucket/rest/"

    def pull_requests(self, repository, branch, destination):
        project = repository["project_key"]
        slug = repository["slug"]
        path = f"rest/api/1.0/projects/{project}/repos/{slug}/pull-requests?state=OPEN&at=refs/heads/{urllib.parse.quote(branch, safe='')}"
        return self.client.request("GET", path)

    def create_pull_request(self, repository, title, branch, destination, description):
        path = f"rest/api/1.0/projects/{repository['project_key']}/repos/{repository['slug']}/pull-requests"
        payload = {"title": title, "description": description, "fromRef": {"id": f"refs/heads/{branch}"}, "toRef": {"id": f"refs/heads/{destination}"}}
        return self.client.request("POST", path, payload)

    def update_pull_request(self, repository, pull_request_id, title, branch, destination, description):
        path = f"rest/api/1.0/projects/{repository['project_key']}/repos/{repository['slug']}/pull-requests/{pull_request_id}"
        current = self.client.request("GET", path)
        payload = {"version": current["version"], "title": title, "description": description, "fromRef": current["fromRef"], "toRef": current["toRef"], "reviewers": current.get("reviewers", [])}
        return self.client.request("PUT", path, payload)


def adapter(section, policy, trusted_hosts):
    return (BitbucketCloud if section["deployment"] == "cloud" else BitbucketDataCenter)(section, policy, trusted_hosts)
