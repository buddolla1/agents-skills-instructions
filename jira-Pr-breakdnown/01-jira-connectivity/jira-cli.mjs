#!/usr/bin/env node
import { parseArgs } from 'node:util';
import { ConfigurationError, JiraClient, JiraError, credentialHeaders, loadConfig, loadFixture, storySummary } from './jira-connectivity.mjs';

function usage() {
  console.log(`Usage:
  node jira-cli.mjs doctor [--config config.json]
  node jira-cli.mjs test-connection [--config config.json]
  node jira-cli.mjs fetch-story --story TEAM-123 [--config config.json]
  node jira-cli.mjs fetch-story --story TEAM-123 --fixture fixtures/story.json [--config config.json]`);
}

async function main() {
  const command = process.argv[2];
  if (!command || ['-h', '--help'].includes(command)) {
    usage();
    return 0;
  }
  const { values } = parseArgs({
    args: process.argv.slice(3),
    options: { config: { type: 'string', default: 'config.json' }, story: { type: 'string' }, fixture: { type: 'string' } },
    strict: true,
  });
  const config = await loadConfig(values.config);
  if (command === 'doctor') {
    credentialHeaders(config);
    console.log(JSON.stringify({ configuration: 'PASS', deployment: config.deployment, base_url: config.base_url, credential_variables: 'CONFIGURED', network: 'NOT_RUN' }, null, 2));
    return 0;
  }
  if (command === 'test-connection') {
    const user = await new JiraClient(config).testConnection();
    console.log(JSON.stringify({ status: 'PASS', deployment: config.deployment, account: user.displayName ?? user.name ?? user.accountId ?? 'authenticated' }, null, 2));
    return 0;
  }
  if (command === 'fetch-story') {
    if (!values.story) throw new ConfigurationError('--story is required');
    const issue = values.fixture
      ? await loadFixture(values.fixture, values.story, config.allowed_project_keys)
      : await new JiraClient(config).fetchStory(values.story);
    console.log(JSON.stringify({ source: values.fixture ? 'fixture' : 'jira', story: storySummary(issue) }, null, 2));
    return 0;
  }
  throw new ConfigurationError(`Unknown command: ${command}`);
}

main().then((code) => { process.exitCode = code; }).catch((error) => {
  const message = error instanceof JiraError ? error.message : 'Unexpected failure';
  console.error(`ERROR: ${message}`);
  process.exitCode = 2;
});
