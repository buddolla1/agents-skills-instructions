# Tours

This folder contains the CodeTour files and the prompts used to create them.

## Files

- `ics-overview.tour` - Main onboarding tour for this repository
- `prompts.md` - General prompts for the CodeTour agent
- `tour-prompts.md` - Prompts used to create and maintain the included tour

## How to run the tour file

CodeTour files are not run from the terminal. Open them in VS Code with the CodeTour extension.

### Prerequisite

Install the VS Code extension:

- `CodeTour`
- Publisher: `Jonathan Carter`
- Extension id: `vsls-contrib.codetour`

### Start the tour with its logical name

1. Open this repository in VS Code
2. Open the Command Palette: `Cmd+Shift+P`
3. Run `CodeTour: Start Tour`
4. Select the logical tour name: `ICS Project Overview`

The logical name is the `title` field inside the `.tour` file, not the filename.

For this repo:

- File name: `ics-overview.tour`
- Logical tour name: `ICS Project Overview`

### Direct file

You can also open:

- `.tours/ics-overview.tour`

Then start it through the CodeTour UI if VS Code prompts you.

## Alternative

1. In VS Code Explorer, open `.tours/ics-overview.tour`
2. If CodeTour is installed, it should offer to open or start the tour

## What happens

- CodeTour will walk through the steps
- Each step opens the target file and line automatically
- You move through the tour in the CodeTour panel

## Important

This is not a Spring Boot runtime artifact.

- `mvn spring-boot:run` runs the application
- It does not run the tour
