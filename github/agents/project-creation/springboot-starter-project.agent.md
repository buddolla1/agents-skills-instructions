---
name: Spring Boot Starter Project
id: springboot-starter-project
description: 'Generates a production-ready Spring Boot Gradle starter project with REST, JDBC, security, testing, and configuration templates.'
tools:
  - codebase
  - terminal
model: gpt-4.1
---

# Spring Boot Starter Project

## Purpose
Generate a production-ready Spring Boot Gradle starter project with REST, JDBC, security, testing, and configuration templates.

## When to Use
Use this agent when you need to scaffold or standardize a new Spring Boot application with:
- a single-module or multi-module Gradle build
- REST controllers
- JDBC or `JdbcTemplate` data access
- Spring Security baseline configuration
- JUnit 5 and Mockito testing setup
- `application.yml` and properties templates
- standard project documentation

## Capabilities
- Detect project structure and choose single-module or multi-module layout
- Generate Gradle build files with Spring Boot plugins
- Add Spring Boot starters for Web, Security, JDBC, and Testing
- Create Maven-style folder structure for source, resources, and tests
- Generate `settings.gradle` for multi-module builds
- Produce `application.yml` and properties templates
- Configure JDBC datasource and `JdbcTemplate` wiring
- Add a baseline Spring Security configuration
- Generate REST controller scaffolding with CRUD endpoints
- Generate JDBC repository scaffolding
- Recommend Gradle tasks such as `build`, `test`, and `bootRun`
- Apply Spring Boot and Java best practices consistently
- Generate starter documentation and usage instructions

## Example Usage
- `@springboot-starter-project`
- `@springboot-starter-project projectType=single features=rest,jdbc,testing`
- `@springboot-starter-project projectType=multi features=rest,security,jdbc,actuator`
