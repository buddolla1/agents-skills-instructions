---
name: figma-ui-generator
description: 'Generate implementation-ready React UI from a Figma URL, exported frame, or screenshot. Use when a design needs to be translated into React components, JSX/TSX structure, styles, responsive behavior, and accessible code that matches the repository stack.'
---

# Figma UI Generator

Use this skill when the user provides a Figma link or design export and wants the matching React UI implemented in the repository.

## When To Use

- A Figma URL, frame link, or screenshot is available.
- The goal is to turn a design into working React UI, not just describe it.
- The repo already has a frontend stack or component system to build against.

## Goal

Translate the design into React code that fits the existing project conventions:

- identify the screen, layout, and React component structure
- extract spacing, typography, colors, states, and responsive behavior
- reuse existing components and design tokens when available
- produce accessible, implementation-ready React UI

## Workflow

1. Open the Figma URL or inspect the exported design artifact.
2. Identify the target frame, view, and any linked states or variants.
3. Extract the layout hierarchy, spacing scale, typography, colors, and interactions.
4. Compare the design against the repository’s React stack and existing components.
5. Map design pieces to reusable UI parts before creating new ones.
6. Build the React UI with responsive behavior and accessibility in mind.
7. If details are missing or the Figma file is inaccessible, ask for the minimum needed input:
   - public access to the Figma file, or
   - exported frame images/PDF, or
   - the specific frame name and desired state.

## Guardrails

- Do not guess at hidden product logic from the design alone.
- Do not force pixel-perfect positioning if it breaks responsiveness or the existing system.
- Do not introduce new visual language when the repo already has a design system.
- Keep semantic HTML, keyboard support, and readable contrast as part of the implementation.
- Prefer idiomatic React patterns already used by the repo, such as function components, hooks, and the local styling approach.

## Output Standard

When using this skill, return:

- the frame or screen identified
- the design tokens or UI decisions extracted
- the React implementation approach
- any gaps or ambiguities that need user confirmation
- the generated code or file plan, if code is being written

## Notes

- Prefer existing components, icons, and spacing conventions from the repository.
- Treat the Figma file as the source for layout and visual structure, not as a substitute for product requirements.
- If multiple frames exist, start with the primary screen and call out any secondary states separately.
