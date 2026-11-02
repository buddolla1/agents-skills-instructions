# Story reader

Input: story key and validated Jira configuration. Permission: read-only Jira access.

Fetch the story, configured acceptance-criteria field, parent feature, dependency links, and only relevant comments. Follow pagination where required. Record issue keys, update timestamps, source field IDs, and retrieval time. Confirm the issue is an eligible existing story in an allowed project.

Produce a normalized story contract containing title, description, acceptance criteria with stable IDs (`AC-1`, etc.), exclusions, parent context, dependencies, unresolved questions, and source references. Parent context explains the story but does not silently expand its scope. Missing testable requirements or unresolved blocking dependencies produce `BLOCKED`, not guessed requirements. Do not create or edit issues.
