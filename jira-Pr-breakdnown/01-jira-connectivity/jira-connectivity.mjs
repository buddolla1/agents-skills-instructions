/** Dependency-free, read-only Jira connectivity helpers. */
import { readFile } from 'node:fs/promises';
import https from 'node:https';

export class JiraError extends Error {}
export class ConfigurationError extends JiraError {}

const STORY_KEY = /^[A-Z][A-Z0-9_]{0,19}-[1-9][0-9]{0,9}$/;

export async function loadConfig(path) {
  let config;
  try {
    config = JSON.parse(await readFile(path, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new ConfigurationError(`Configuration not found: ${path}; copy config.example.json to config.json`);
    }
    throw new ConfigurationError(`Configuration is not valid JSON: ${error.message}`);
  }

  if (!['cloud', 'data_center'].includes(config.deployment)) {
    throw new ConfigurationError("deployment must be 'cloud' or 'data_center'");
  }
  let baseUrl;
  try {
    baseUrl = new URL(config.base_url);
  } catch {
    throw new ConfigurationError('base_url must be a valid HTTPS URL');
  }
  if (baseUrl.protocol !== 'https:' || baseUrl.username || baseUrl.password) {
    throw new ConfigurationError('base_url must be HTTPS and must not contain credentials');
  }
  const auth = config.auth ?? {};
  if (!['basic', 'bearer'].includes(auth.strategy)) {
    throw new ConfigurationError("auth.strategy must be 'basic' or 'bearer'");
  }
  if (!auth.token_env) throw new ConfigurationError('auth.token_env is required');
  if (auth.strategy === 'basic' && !auth.username_env) {
    throw new ConfigurationError('auth.username_env is required for basic authentication');
  }
  if (!Array.isArray(config.allowed_project_keys) || config.allowed_project_keys.length === 0 || config.allowed_project_keys.some((key) => typeof key !== 'string' || !key)) {
    throw new ConfigurationError('allowed_project_keys must be a nonempty string array');
  }
  for (const [name, defaultValue] of [['timeout_seconds', 30], ['maximum_retries', 3], ['maximum_response_bytes', 5_000_000]]) {
    config[name] ??= defaultValue;
    if (!Number.isInteger(config[name]) || config[name] < 1) {
      throw new ConfigurationError(`${name} must be a positive integer`);
    }
  }
  config.base_url = config.base_url.replace(/\/$/, '');
  return config;
}

export function validateStoryKey(value, allowedProjects) {
  if (!STORY_KEY.test(value ?? '')) throw new ConfigurationError('story key must look like TEAM-123');
  if (!allowedProjects.includes(value.split('-', 1)[0])) {
    throw new ConfigurationError(`story project is not in allowed_project_keys: ${value}`);
  }
  return value;
}

export function credentialHeaders(config, environment = process.env) {
  const { auth } = config;
  const token = environment[auth.token_env];
  if (!token) throw new ConfigurationError(`Missing credential environment variable: ${auth.token_env}`);
  if (auth.strategy === 'bearer') return { Authorization: `Bearer ${token}` };
  const username = environment[auth.username_env];
  if (!username) throw new ConfigurationError(`Missing credential environment variable: ${auth.username_env}`);
  return { Authorization: `Basic ${Buffer.from(`${username}:${token}`).toString('base64')}` };
}

export class JiraClient {
  constructor(config, { headers, request = httpsRequest, sleep = delay } = {}) {
    this.config = config;
    this.baseUrl = new URL(`${config.base_url}/`);
    this.headers = headers ?? credentialHeaders(config);
    this.request = request;
    this.sleep = sleep;
    this.apiVersion = config.deployment === 'cloud' ? '3' : '2';
  }

  async testConnection() {
    return this.#get(`rest/api/${this.apiVersion}/myself`);
  }

  async fetchStory(storyKey) {
    const key = validateStoryKey(storyKey, this.config.allowed_project_keys);
    return this.#get(`rest/api/${this.apiVersion}/issue/${key}?expand=names`);
  }

  async #get(path) {
    const url = new URL(path, this.baseUrl);
    if (url.protocol !== 'https:' || url.host !== this.baseUrl.host) {
      throw new JiraError('Request escaped the configured Jira HTTPS host');
    }
    const attempts = this.config.maximum_retries + 1;
    for (let attempt = 0; attempt < attempts; attempt += 1) {
      try {
        const response = await this.request(url, {
          headers: { Accept: 'application/json', ...this.headers },
          timeoutMs: this.config.timeout_seconds * 1000,
          maxBytes: this.config.maximum_response_bytes,
        });
        if ((response.status === 429 || response.status >= 500) && attempt + 1 < attempts) {
          await this.sleep(Math.min(retryDelay(response.headers['retry-after'], attempt), 30_000));
          continue;
        }
        if (response.status === 401) throw new JiraError('Jira authentication failed (HTTP 401); check credential environment variables');
        if (response.status === 403) throw new JiraError('Jira access was denied (HTTP 403); check account permissions');
        if (response.status === 404) throw new JiraError('Jira resource was not found (HTTP 404); check URL, project, and issue key');
        if (response.status < 200 || response.status >= 300) throw new JiraError(`Jira request failed with HTTP ${response.status}`);
        try {
          return response.body ? JSON.parse(response.body) : {};
        } catch {
          throw new JiraError('Jira returned a non-JSON response');
        }
      } catch (error) {
        if (error instanceof JiraError) throw error;
        if (attempt + 1 < attempts) {
          await this.sleep(Math.min(2 ** attempt * 1000, 10_000));
          continue;
        }
        throw new JiraError(`Jira network request failed: ${safeError(error)}`);
      }
    }
    throw new JiraError('Jira request exhausted its retry budget');
  }
}

export async function loadFixture(path, storyKey, allowedProjects) {
  const key = validateStoryKey(storyKey, allowedProjects);
  const data = JSON.parse(await readFile(path, 'utf8'));
  const issue = data.issues?.[key];
  if (!issue) throw new JiraError(`Fixture does not contain story ${key}`);
  return issue;
}

export function storySummary(issue) {
  const fields = issue.fields ?? {};
  return {
    key: issue.key,
    summary: fields.summary ?? '',
    issue_type: fields.issuetype?.name ?? '',
    status: fields.status?.name ?? '',
    updated: fields.updated ?? null,
  };
}

export function httpsRequest(url, { headers, timeoutMs, maxBytes }) {
  return new Promise((resolve, reject) => {
    const request = https.request(url, { method: 'GET', headers, timeout: timeoutMs, rejectUnauthorized: true }, (response) => {
      const chunks = [];
      let size = 0;
      response.on('data', (chunk) => {
        size += chunk.length;
        if (size > maxBytes) {
          request.destroy(new JiraError('Jira response exceeded maximum_response_bytes'));
          return;
        }
        chunks.push(chunk);
      });
      response.on('end', () => resolve({ status: response.statusCode, headers: response.headers, body: Buffer.concat(chunks).toString('utf8') }));
    });
    request.on('timeout', () => request.destroy(new Error('request timed out')));
    request.on('error', reject);
    request.end();
  });
}

function retryDelay(header, attempt) {
  const seconds = Number(header);
  return Number.isFinite(seconds) && seconds >= 0 ? seconds * 1000 : 2 ** attempt * 1000;
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

function safeError(error) {
  return String(error?.message ?? error).replace(/https:\/\/[^/@\s:]+:[^/@\s]+@/g, 'https://[REDACTED]@');
}
