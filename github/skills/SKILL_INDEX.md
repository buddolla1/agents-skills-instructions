## Skill index

Agent skills are focused, reusable instruction bundles that help an AI agent perform specialized tasks more consistently. Each skill defines when it should be used, the workflow it should follow, and the guardrails it should respect.

Why skills are useful:

- They make task handling more consistent across similar requests.
- They capture domain-specific rules so the agent does not have to infer everything from scratch.
- They reduce prompt repetition by bundling reusable guidance in one place.
- They improve safety by defining scope, review steps, and decision boundaries.
- They help teams scale common patterns across repositories and use cases.

Key advantages:

- Faster onboarding for recurring engineering tasks
- More predictable outputs
- Better adherence to local standards
- Clearer review and execution workflows
- Easier reuse across projects

Checklist

- [x] Gather top-level skills in `github/skills/`
- [x] Extract `name` and `description` from each `SKILL.md`
- [x] Provide a short "Why to use" and "How to use" guidance for each skill

This file lists the repository skills with a short description, why you'd use the skill, and a quick how-to for getting started. For full usage details, open the skill's `SKILL.md` file in the skill folder.

| Skill name | Description | Why to use | How to use |
| --- | --- | --- | --- |
| `code-review-skill` | Coordinates full repository and git-diff code review into focused skills for null safety, exception handling, and code quality. | Use when you need a repo-wide or diff-focused static review that covers null-safety, exceptions, and quality. | Provide repo root or git-diff scope; choose full repo or diff and the coordinator will load specialized subskills. |
| `create-agentsmd` | Prompt for generating an AGENTS.md file for a repository. | Use when you want a clear, agent-focused AGENTS.md to help automated tools work on the repo. | Provide repository context and desired commands/output; the skill scaffolds an AGENTS.md template. |
| `create-spring-boot-java-project` | Create a Spring Boot Java project skeleton. | Use when starting a new Spring Boot application and you need a conventional starter structure. | Provide target Java version, build tool, and main dependencies; the skill generates a minimal starter layout. |
| `engineering-design-agent` | Creates repo-aware engineering design artifacts (design docs, BDD, HLD/LLD, Mermaid diagrams). | Use when requirements must be turned into repo-aware design artifacts aligned with the codebase. | Provide the requirement, optional tech stack and output mode (bdd/architecture/full_design); the skill reads repo context and produces markdown + a JSON summary. |
| `event-driven-architecture` | Design and review event-driven Java systems using Kafka or RabbitMQ patterns. | Use when building or reviewing asynchronous integrations, message contracts, retries, and idempotency. | Provide the producer/consumer code, broker conventions, and message contracts; the skill evaluates delivery semantics and recommendations. |
| `fullstack-project-architecture-analyzer` | Coordinates React, Spring Boot, or full-stack architecture analysis into focused artifacts (HLD, LLD, flowcharts). | Use when you want progressive architecture analysis or a specific artifact such as HLD/LLD or component map. | Indicate which artifact you want first (HLD, LLD, flowcharts, external APIs); supply repo root so the skill can inspect files. |
| `java-21-upgrade-recommender` | Reviews Java source and build configuration and recommends a migration path to Java 21. | Use when you need a practical assessment and staged migration recommendations before changing code. | Provide Java sources and build files (pom.xml, build.gradle); optionally specify scope and target version (default 21). |
| `java-code-quality-analyzer` | Coordinates Java code quality review into correctness, security, performance, and design concerns. | Use when reviewing Java/Spring code for bugs, security issues, performance, or maintainability. | Specify which concern (correctness, security, performance, design) and provide files or diff to analyze; the skill will load subskills accordingly. |
| `jpa-jdbc-performance-optimizer` | Analyze JPA and JDBC code for performance bottlenecks (N+1, lazy-loading, over-fetching). | Use when database access patterns cause performance issues or you suspect ORM inefficiencies. | Provide repository code, example traces, or queries and the transaction boundary; the skill recommends fetch strategies and fixes. |
| `logging-enhancer` | Improve Log4j2-based logging and observability in Java or Spring Boot services. Use when reviewing request traceability, ThreadContext correlation IDs, structured JSON or pattern layouts, logger level discipline, exception logging, async logging, and production supportability. | Use when you need consistent, structured, and traceable logs with Log4j2-specific guidance for correlation IDs, layouts, levels, and exception handling. | Provide Java files and Log4j2 config; the skill inspects the current logging format, recommends minimal improvements, and asks for user consent before code edits. |
| `npe` | Review Java code for null-pointer risks, trace nullable flows, and suggest safe fixes and focused tests. | Use when analyzing Java, Spring, JPA, DTO, or service-layer code for probable NPE failure paths. | Provide the Java files or file paths to analyze; the skill will trace nullable sources, recommend fixes, and suggest tests. |
| `openapi-swagger-generator` | Generate and validate OpenAPI or Swagger documentation for Spring Boot APIs. | Use when controllers, DTOs, or endpoint contracts need documentation or validation against published specs. | Provide controller and DTO code or an existing spec; the skill compares implementation vs spec and can generate docs under `doc/`. |
| `projection-creation` | Create Spring Data JPA or JDBC projections and DTO views to avoid over-fetching. | Use when read paths should return only the needed fields and avoid loading full entity graphs. | Provide the repository method or read path and indicate JPA vs JDBC; the skill suggests interface or constructor projections. |
| `react-ada-analysis` | Analyze React projects for ADA accessibility issues (keyboard, ARIA, contrast, semantics). | Use when you need to improve accessibility, make pages screen-reader friendly, or comply with ADA patterns. | Provide React components/pages and package.json; if accessibility tooling is missing, the skill will prompt you to add it before analysis. |
| `react-test-generator` | Generate tests for React applications (component, hook, interaction tests). | Use when creating or improving React test coverage for user-visible behavior. | Provide the component or page and the target testing library; the skill will produce tests and prompt to add missing packages if needed. |
| `secrets-management-checker` | Detect hardcoded secrets in code, config, and build files; recommend secret managers. | Use when reviewing projects for passwords, API keys, tokens, or insecure credential handling. | Provide code, config, and CI files; the skill inspects for hardcoded secrets and suggests secure replacements and rotation steps. |
| `splunk-query-helper` | Help write, refine, and troubleshoot Splunk SPL queries for log analysis and dashboards. | Use when building searches, parsing fields, or improving SPL performance and clarity. | Provide sample events, index/sourcetype, and the query goal; the skill returns SPL with explanations and validation notes. |
| `spring-3x-to-4x-modernization` | Modernize Spring Framework 3.x applications to 4.x safely (config, APIs, wiring). | Use when migrating legacy Spring XML apps and you need an incremental, behavior-preserving upgrade path. | Provide the legacy project or files; the skill inventories config and recommends small, test-backed migration steps. |
| `sql-code-review` | Review SQL code for security, maintainability, and injection risks. | Use when SQL statements, stored logic, or schema-driven queries need correctness and safety review. | Provide SQL statements or artifacts and target DB platform; the skill checks for injection, access control, and anti-patterns. |
| `sql-optimization` | Optimize SQL queries and indexing strategy (plans, joins, pagination). | Use when a query is slow or an execution plan needs tuning. | Provide the SQL, table schema, and execution plan; the skill suggests index and query-shape changes with tradeoffs. |
| `stored-procedure-function-explainer` | Explain stored procedures and functions (Oracle/MySQL) in plain language. | Use when you need a readable explanation, control-flow diagram, or risk notes for a DB routine. | Provide the routine text and platform (Oracle or MySQL); the skill will summarize behavior and optionally produce a Mermaid flow diagram. |
| `test-coverage-analyzer` | Analyze test coverage to identify low-coverage areas and missing tests. | Use when coverage reports or changes need translation into concrete test gaps prioritized by risk. | Provide coverage reports, changed files, or the area under review; the skill maps gaps to focused test suggestions. |
| `ultimate-codebase-analysis` | Coordinates repository-wide analysis into subskills for runtime risk, dependency health, performance hotspots, and final report assembly. | Use when you want a consolidated, multi-concern review across an entire repo or diff. | Provide repo root or diff and the desired focus areas (runtime risk, dependencies, performance); the coordinator runs subskills and assembles a report. |
| `unit-test-generator` | Generate JUnit and Mockito unit tests for Java code. | Use when creating or improving unit tests for services, utilities, and business logic. | Provide the class under test, collaborators, and desired behaviors; the skill generates focused, maintainable unit tests. |
| `yaml-validator` | Validate YAML files for syntax, structure, and common config mistakes. | Use when reviewing config files, manifests, CI definitions, or skill files for correctness. | Provide the YAML file or snippet and any expected schema; the skill reports exact locations for syntax or structural issues. |
