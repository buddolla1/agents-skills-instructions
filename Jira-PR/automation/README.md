# Jira-to-Bitbucket story delivery

This workspace coordinates one existing Jira story across explicitly selected microservice repositories. The active Codex session performs reasoning and edits; `flow.py` owns validated API/Git operations, evidence, state, and publication gates. It never merges or deploys.

## Setup

1. Copy `config.example.json` to `../config.json` and `services.example.json` to `../services.json`.
2. Replace placeholders with deployment-specific HTTPS URLs, Jira field/hierarchy mappings, absolute repository/worktree paths, exact repository identities, commands, and policy choices.
3. Put credential values only in the environment variables named by configuration. Do not add credentials to JSON, Git URLs, Markdown, or worktrees.
4. Confirm the configured Jira/Bitbucket deployment and version against the official documentation before live use:
   - Jira Cloud REST v3: <https://developer.atlassian.com/cloud/jira/platform/rest/v3/>
   - Jira Data Center REST: <https://developer.atlassian.com/server/jira/platform/rest-apis/>
   - Bitbucket Cloud REST: <https://developer.atlassian.com/cloud/bitbucket/rest/>
   - Bitbucket Data Center REST: <https://developer.atlassian.com/server/bitbucket/rest/>
5. Run `python3 automation/flow.py doctor` from `Jira-PR`.

Jira and Bitbucket deployment types are independent. Missing or unresolved live configuration blocks only the affected live operation; fixture tests require no network.

## Offline validation and demonstration

Run the complete suite:

```bash
cd Jira-PR
python3 -m unittest discover -s automation/tests -v
python3 automation/demo.py
```

For a fixture intake, first use temporary repository paths in local `config.json` and `services.json`, then run:

```bash
python3 automation/flow.py intake \
  --story TEAM-100 \
  --services orders \
  --fixture automation/fixtures/jira-cloud.json \
  --dry-run
```

The command prints a run ID and writes only ignored local evidence under `.agent-runs/`. Use that ID to freeze an agent-produced impact plan:

```bash
python3 automation/flow.py impact --run RUN_ID --plan automation/fixtures/impact-plan.json
python3 automation/flow.py prepare --run RUN_ID --all-selected-changes
```

After the active session implements the story in the dedicated worktree:

```bash
python3 automation/flow.py verify --run RUN_ID --service orders
python3 automation/flow.py verify-contracts --run RUN_ID
python3 automation/flow.py record-review --run RUN_ID --service orders --findings findings.json
python3 automation/flow.py status --run RUN_ID
```

`findings.json` is a JSON array. Each finding has severity, location, rationale, required action, `blocking`, and `resolved`. An omitted findings file records an empty same-session review; it must not be described as independent model review.

In review mode, show the story-wide revision summary to the user. Only after the user approves that exact run/diff/destination, record the approval:

```bash
python3 automation/flow.py approve --run RUN_ID --service orders
python3 automation/flow.py publish --run RUN_ID
```

`approve` is workflow bookkeeping bound to the current diff, not a machine-owner security boundary. `publish` rechecks all gates, stages only `reviewed_paths` from the frozen impact plan, pushes without force, looks up an existing PR before creation, and resumes from per-repository checkpoints.

Other recovery commands:

```bash
python3 automation/flow.py resume --run RUN_ID
python3 automation/flow.py resume --run RUN_ID --service payments
python3 automation/flow.py cancel --run RUN_ID
```

Cancellation preserves worktrees, commits, branches, PRs, and evidence. Push failures preserve the recorded commit. If a PR succeeds and Jira synchronization fails, the repository remains `PR_CREATED_SYNC_PENDING` so only the pending synchronization is retried.

## State and safety

State is versioned and split between a story manifest and repository documents. JSON replacements are atomic; story and repository locks prevent concurrent duplicate work; an append-only journal records operations. Evidence is tied to a diff fingerprint. A changed diff invalidates verification, review, and approval.

Commands use subprocess argument arrays from validated configuration. Story text cannot supply commands or trusted hosts. HTTP requests require configured HTTPS hosts, disable redirects, verify TLS, bound response sizes/timeouts/retries, and redact credentials. Logs are capped. Local configuration, secrets, and `.agent-runs/` are ignored.

Current deliberate boundaries:

- The CLI does not invoke Codex or infer impact. The active session follows the role files sequentially.
- Parent retrieval, comment pagination/deduplication, Jira comments/transitions, and PR cross-link updates have deployment-specific adapters, but require deployment/version confirmation and a read-only staging validation before live writes.
- Jira commenting/transitions default off. A configured transition is executed only when it appears in Jira's current valid transition list. Synchronization failures preserve PR success in `PR_CREATED_SYNC_PENDING`.
- No live Jira/Bitbucket access or mutation occurs in automated tests.
