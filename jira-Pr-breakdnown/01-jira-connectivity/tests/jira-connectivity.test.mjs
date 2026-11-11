import assert from 'node:assert/strict';
import { mkdtemp, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import { ConfigurationError, JiraClient, JiraError, credentialHeaders, loadConfig, loadFixture, storySummary, validateStoryKey } from '../jira-connectivity.mjs';

function config(overrides = {}) {
  return {
    deployment: 'cloud',
    base_url: 'https://jira.example.test',
    auth: { strategy: 'basic', username_env: 'JIRA_USER', token_env: 'JIRA_TOKEN' },
    allowed_project_keys: ['TEAM'],
    timeout_seconds: 1,
    maximum_retries: 1,
    maximum_response_bytes: 10_000,
    ...overrides,
  };
}

test('loads and validates configuration', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jira-connectivity-'));
  const file = path.join(directory, 'config.json');
  await writeFile(file, JSON.stringify(config()));
  const value = await loadConfig(file);
  assert.equal(value.deployment, 'cloud');
  assert.equal(value.base_url, 'https://jira.example.test');
});

test('rejects insecure base URLs and unsafe story keys', async () => {
  const directory = await mkdtemp(path.join(os.tmpdir(), 'jira-connectivity-'));
  const file = path.join(directory, 'config.json');
  await writeFile(file, JSON.stringify(config({ base_url: 'http://jira.example.test' })));
  await assert.rejects(loadConfig(file), ConfigurationError);
  assert.throws(() => validateStoryKey('TEAM-1;rm', ['TEAM']), ConfigurationError);
  assert.throws(() => validateStoryKey('OTHER-1', ['TEAM']), ConfigurationError);
});

test('builds basic and bearer headers only from environment values', () => {
  const basic = credentialHeaders(config(), { JIRA_USER: 'user@example.test', JIRA_TOKEN: 'secret' });
  assert.equal(basic.Authorization, `Basic ${Buffer.from('user@example.test:secret').toString('base64')}`);
  const bearer = credentialHeaders(config({ auth: { strategy: 'bearer', token_env: 'TOKEN' } }), { TOKEN: 'secret' });
  assert.equal(bearer.Authorization, 'Bearer secret');
  assert.throws(() => credentialHeaders(config(), {}), ConfigurationError);
});

test('uses Jira Cloud v3 and Data Center v2 endpoints', async () => {
  const urls = [];
  const request = async (url) => {
    urls.push(url.pathname);
    return { status: 200, headers: {}, body: JSON.stringify({ key: 'TEAM-123', fields: {} }) };
  };
  await new JiraClient(config(), { headers: {}, request }).fetchStory('TEAM-123');
  await new JiraClient(config({ deployment: 'data_center' }), { headers: {}, request }).fetchStory('TEAM-123');
  assert.deepEqual(urls, ['/rest/api/3/issue/TEAM-123', '/rest/api/2/issue/TEAM-123']);
});

test('tests authentication through the deployment-specific myself endpoint', async () => {
  let requested;
  const request = async (url) => {
    requested = url.pathname;
    return { status: 200, headers: {}, body: '{"displayName":"Fixture User"}' };
  };
  const user = await new JiraClient(config(), { headers: {}, request }).testConnection();
  assert.equal(requested, '/rest/api/3/myself');
  assert.equal(user.displayName, 'Fixture User');
});

test('retries transient failures within the configured budget', async () => {
  let attempts = 0;
  const request = async () => {
    attempts += 1;
    return attempts === 1
      ? { status: 429, headers: { 'retry-after': '0' }, body: '{}' }
      : { status: 200, headers: {}, body: '{"ok":true}' };
  };
  const client = new JiraClient(config(), { headers: {}, request, sleep: async () => {} });
  assert.deepEqual(await client.testConnection(), { ok: true });
  assert.equal(attempts, 2);
});

test('returns credential-safe authentication errors', async () => {
  const request = async () => ({ status: 401, headers: {}, body: '{}' });
  const client = new JiraClient(config(), { headers: {}, request });
  await assert.rejects(client.testConnection(), (error) => error instanceof JiraError && error.message.includes('authentication failed') && !error.message.includes('secret'));
});

test('loads an offline fixture and returns a small story summary', async () => {
  const fixture = new URL('../fixtures/story.json', import.meta.url);
  const issue = await loadFixture(fixture, 'TEAM-123', ['TEAM']);
  assert.deepEqual(storySummary(issue), {
    key: 'TEAM-123',
    summary: 'Fixture Jira connectivity story',
    issue_type: 'Story',
    status: 'To Do',
    updated: '2026-11-01T12:00:00.000+0000',
  });
});
