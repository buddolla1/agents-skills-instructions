# Step 1 — Jira connectivity

This step proves that Node.js can securely connect to the configured Jira deployment and read one existing story. It does not modify Jira, inspect repositories, connect to Bitbucket, or create branches.

## Files

- `jira-connectivity.mjs` — validated configuration, authentication, HTTPS client, retries, and story retrieval.
- `jira-cli.mjs` — small command-line interface.
- `config.example.json` — nonsecret configuration template.
- `fixtures/story.json` — offline test story.
- `tests/jira-connectivity.test.mjs` — Node built-in tests.

No npm packages are required. Use Node.js 18 or later.

## 1. Run offline tests

```bash
cd jira-Pr-breakdnown/01-jira-connectivity
npm test
```

## 2. Try fixture mode

Copy the example configuration:

```bash
cp config.example.json config.json
```

Fixture mode does not require a network connection, but the configured project key must match the story:

```bash
node jira-cli.mjs fetch-story \
  --story TEAM-123 \
  --fixture fixtures/story.json
```

## 3. Configure live Jira access

Edit `config.json`:

- `deployment`: `cloud` or `data_center`.
- `base_url`: Jira HTTPS base URL, without credentials.
- `auth.strategy`: `basic` or `bearer`.
- `username_env`: environment variable containing the username; required for basic authentication.
- `token_env`: environment variable containing the API token, personal access token, or password supported by the configured Jira deployment.
- `allowed_project_keys`: projects this script may read.

Set credential values in the terminal, not in JSON or source files:

```bash
export JIRA_USER_EMAIL='your-account-email'
export JIRA_API_TOKEN='your-token'
```

Do not paste secrets into chat or commit them. `config.json` is ignored by Git.

## 4. Validate local configuration

This checks JSON, URL, deployment, and credential environment variables without making a network request:

```bash
node jira-cli.mjs doctor
```

Expected result:

```json
{
  "configuration": "PASS",
  "deployment": "cloud",
  "base_url": "https://your-company.atlassian.net",
  "credential_variables": "CONFIGURED",
  "network": "NOT_RUN"
}
```

## 5. Test live authentication

```bash
node jira-cli.mjs test-connection
```

The command performs only `GET /myself`. Cloud uses REST API v3; Data Center uses REST API v2.

## 6. Fetch one live story

```bash
node jira-cli.mjs fetch-story --story TEAM-123
```

The output intentionally contains only key, summary, issue type, status, and update timestamp. Step 2 will normalize description, acceptance criteria, parent context, dependencies, and comments.

## Completion gate

Step 1 is complete when:

1. `npm test` passes.
2. `doctor` reports configuration and credential variables as configured.
3. `test-connection` authenticates successfully.
4. `fetch-story` returns the expected story from an allowed project.

Only the offline tests can be completed without the user's Jira URL and credential environment variables.
