---
description: 'Security, testing, logging, performance, build, deployment, and documentation guidance for Spring Boot projects.'
applyTo: '**/*Test.java, **/*IT.java, **/*IntegrationTest.java, **/logback*.xml, **/application*.yml, **/application*.yaml, **/*.properties, pom.xml, build.gradle, build.gradle.kts, README.md'
---

# Quality and Operations Standards

## Security Best Practices

- Use Spring Security.
- Use OAuth2 / JWT where applicable.
- Apply role-based or authority-based authorization.
- Hash passwords with BCrypt or another approved algorithm.
- Validate all inputs.
- Enforce HTTPS.
- Store secrets in environment variables or secret managers.
- Implement rate limiting for sensitive or public endpoints.
- Enable CSRF protection for session or cookie-based applications.
- For stateless token-based APIs, configure CSRF according to the security model rather than enabling it blindly.

## Performance Optimization

- Use connection pooling.
- Monitor slow queries.
- Avoid N+1 issues.
- Use pagination.
- Use caching only for clearly beneficial paths.
- Use async processing for long-running tasks where appropriate.
- Compress large HTTP responses where useful.
- Profile before optimizing.

## Testing Standards

- Use JUnit 5 for unit tests.
- Use Mockito for mocking.
- Use Spring Boot Test for integration tests.
- Use MockMvc or TestRestTemplate for API tests.
- Use Testcontainers for database-backed persistence tests.
- Test business logic thoroughly.
- Mock external systems in unit tests.
- Use integration tests for repository, security, and controller wiring.
- Keep tests deterministic and independent.
- Follow Arrange–Act–Assert.
- Name tests by behavior.
- Aim for meaningful coverage on business-critical paths.

## Logging and Monitoring

- Use SLF4J with Logback.
- Use parameterized logging.
- Use structured logging where supported.
- Include correlation IDs and request tracing IDs.
- Never log secrets, tokens, passwords, or sensitive personal data.
- Use Spring Boot Actuator.
- Expose health, metrics, and readiness endpoints appropriately.
- Integrate with Prometheus/Grafana or equivalent tooling.

## Build and Delivery

- Keep dependency versions explicit or centrally managed.
- Remove unused dependencies.
- Scan dependencies for vulnerabilities.
- Use multi-module builds only when justified by project complexity.
- Externalize configuration.
- Run tests before packaging.
- Enforce code quality gates.
- Scan for vulnerabilities.
- Automate versioning where appropriate.
- Support zero-downtime rollout patterns when required.

## Documentation Standards

- Maintain OpenAPI documentation.
- Keep README setup steps accurate.
- Include architecture diagrams where useful.
- Document integration points, environment variables, and local run instructions.
- Keep docs aligned with code changes.

## Definition of Done

- Code follows project standards.
- Unit and integration tests are added as appropriate.
- API changes are documented.
- Logs and metrics are considered.
- No critical vulnerabilities are introduced.
- Code is reviewed.
- Database migrations are included where needed.
