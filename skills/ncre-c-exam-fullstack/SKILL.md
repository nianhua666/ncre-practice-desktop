---
name: ncre-c-exam-fullstack
description: Build, audit, extend, or package a Chinese National Computer Rank Examination (NCRE) mock-exam desktop app, especially when the task involves Level 2 C language question banks, system-generated exams, AI-generated questions, AI grading, SQLite history tracking, OpenAI-compatible provider settings, desktop webview packaging, or end-to-end quality hardening for an offline-first Windows app.
---

# NCRE C Exam Fullstack

## Overview

Use this skill when building or improving a desktop mock-exam program for the Chinese National Computer Rank Examination.
Use this skill when the request touches Level 2 C language practice, fixed question banks, simulated exams, AI-assisted grading, local persistence, or Windows EXE delivery.
Act as both a C-language domain expert and a pragmatic full-stack engineer.
Prefer shipping a runnable product over writing broad plans without implementation.
Prefer defensive engineering over optimistic assumptions.
Prefer measurable correctness over aesthetic claims.

## Working Posture

Treat the application as an exam product, not a demo page.
Treat every question bank change as data engineering.
Treat AI integration as optional enhancement, not the only path.
Treat offline grading as the baseline.
Treat AI grading as a second opinion or required path only for open-ended questions.
Treat Windows packaging as a first-class requirement from day one.
Treat the front end, back end, and data model as one coherent system.
Treat user records as durable artifacts that must survive app restarts.
Treat errors as product defects that need explicit handling.

## Primary Goals

Deliver a local-first desktop application.
Deliver a complete built-in Level 2 C language question bank that covers the official syllabus breadth.
Deliver built-in question banks for multiple NCRE levels, even if some non-C subjects start smaller than Level 2 C.
Deliver system-generated mock exams from fixed banks.
Deliver AI-generated practice sets.
Deliver offline grading for objective questions and bank-backed subjective questions when possible.
Deliver AI grading for AI-generated or open-ended content.
Deliver score history, answer history, wrong-answer analysis, and review flows.
Deliver configurable AI provider settings with OpenAI-compatible protocols.
Deliver packaging scripts that can produce a Windows EXE.

## Non-Negotiable Quality Rules

Keep the app runnable after every meaningful change.
Keep question bank schema stable and explicit.
Keep front-end state derivable from API responses.
Keep database initialization idempotent.
Keep AI settings optional so the app still works without them.
Keep all timestamps stored in ISO 8601 format.
Keep every exam attempt reproducible from stored payloads.
Keep every grading result explainable.
Keep network errors non-fatal to the rest of the app.
Keep packaging instructions inside the repository.

## Scope Boundaries

Do not require a cloud backend for baseline usage.
Do not block core practice features behind AI.
Do not hardcode a single AI provider.
Do not rely on undocumented OpenAI consumer-login tricks.
Do not promise official content ownership or exclusive materials.
Do not silently overwrite user data.
Do not leave grading logic only in the front end.
Do not mix transient view state with persisted exam records.

## Expected Deliverables

Create a desktop launcher entry point.
Create an HTTP API or equivalent local interface for the front end.
Create a front-end shell with dashboard, practice, history, settings, and resources views.
Create a SQLite database with migrations or idempotent bootstrap logic.
Create built-in question bank files in a normalized JSON format.
Create exam generation services for fixed-bank and random-bank flows.
Create grading services for objective and subjective questions.
Create AI provider abstraction and prompt templates.
Create test or verification scripts for seed data and exam generation.
Create EXE build scripts.

## Decision Framework

Choose the simplest architecture that supports local packaging.
Choose deterministic grading when the question type allows it.
Choose AI grading only when deterministic grading would be brittle or misleading.
Choose reusable question templates when expanding the fixed bank.
Choose JSON for portable question-bank storage.
Choose SQLite for local persistence.
Choose a web-based front end if it speeds up UI delivery without harming packaging.
Choose a browser fallback if embedded webview support is unavailable.

## Canonical Architecture

Use Python for the application runtime unless the repository already standardizes on another stack.
Use a lightweight local web API for orchestration.
Use static HTML, CSS, and JavaScript or a minimal web front-end stack for UI delivery.
Use SQLite through the standard library when possible.
Use a clear separation between data models, services, routers, and static assets.
Use a bootstrap script to generate or validate built-in banks.
Use PyInstaller or an equivalent packager for EXE output.

## Recommended Repository Layout

Keep `backend/` for Python application code.
Keep `frontend/` for static assets.
Keep `data/` for built-in banks and seed artifacts.
Keep `scripts/` for developer automation and packaging.
Keep `tests/` for automated checks.
Keep `skills/ncre-c-exam-fullstack/` for this skill.
Keep generated runtime data outside source-controlled seed banks when practical.

## Workflow

### 1. Establish Ground Truth

Read the current repository layout.
Read any existing app entry point.
Read the question bank schema before adding data.
Read the database bootstrap before changing persistence.
Read the front-end router or state model before changing UI flows.
Read packaging scripts before adding dependencies.
Check whether the workspace is empty or partially built.
Check whether there are user modifications in flight.
Check whether the requested feature depends on AI or can work offline.

### 2. Map the Request to Product Areas

Classify the request as one or more of:

1. Question bank construction
2. Exam generation
3. Grading
4. AI integration
5. History and analytics
6. UI and interaction
7. Packaging and deployment
8. Performance and reliability

Trace each affected product area to files and data structures.
Refuse to make blind edits across unrelated layers.

### 3. Implement End to End

Update schemas first when the data contract changes.
Update seed data next when built-in content changes.
Update services next when business logic changes.
Update APIs next when front-end consumption changes.
Update front-end rendering next when user behavior changes.
Update packaging only after the runtime works in development.
Run validation after each substantial slice.

### 4. Verify Like an Exam Product

Create at least one deterministic test path for every new question type.
Create at least one random-exam generation path per subject.
Create at least one full submission path that persists attempt data.
Create at least one AI-disabled path and one AI-enabled path.
Create at least one restart test to confirm persistence survives app relaunch.
Create at least one packaging or build dry run whenever dependencies change.

## Question Bank Standard

Represent every subject with a top-level manifest.
Represent every question with a stable `id`.
Represent every question with a `type`.
Represent every question with a numeric `score`.
Represent every question with tags.
Represent every question with an analysis or explanation.
Represent every objective question with a canonical answer key.
Represent every subjective question with a scoring rubric or reference answer.
Represent every question with difficulty metadata.
Represent every question with a source classification such as `official-outline`, `curated`, `ai-assisted-curation`, or `internet-public`.

## Supported Question Types

Support `single_choice`.
Support `multiple_choice` if the chosen subject actually uses it.
Support `true_false` if needed by imported banks.
Support `fill_blank`.
Support `code_completion`.
Support `bug_fix`.
Support `short_answer`.
Support `programming`.

Map each type to an explicit grading strategy.
Avoid introducing a new type without updating grading and UI rendering.

## Level 2 C Bank Requirements

Cover public basic knowledge.
Cover algorithm and data structure basics.
Cover C syntax and semantics.
Cover identifiers, constants, and types.
Cover operators and expression evaluation.
Cover control flow.
Cover arrays and strings.
Cover functions and storage classes.
Cover pointers.
Cover structures and unions.
Cover files.
Cover preprocessing and compilation basics.
Cover common bug patterns from NCRE practice.
Cover code reading, completion, correction, and design tasks.

Do not fake coverage by duplicating near-identical stems.
Do not overfit only to multiple-choice items.
Do not omit program-design questions.
Do not omit explanation fields.

## Other Subject Bank Requirements

Include at least one built-in bank from each NCRE level if the product claims multi-level support.
Allow smaller starter banks for non-core subjects.
Mark each bank with completeness metadata.
Expose the completeness level in the UI.
Keep the architecture ready for more banks without schema changes.

## Bank Curation Rules

Prefer paraphrased content over direct bulk copying from proprietary material.
Use official outlines to define coverage, not to copy entire papers.
Use publicly visible sample questions or public-domain style knowledge only within legal and ethical limits.
Normalize terminology across the bank.
Normalize score ranges by question type.
Normalize explanations to plain, direct Chinese.
Normalize tags to stable vocabulary.

## Bank Expansion Strategy

Start with the official syllabus categories.
Create a coverage matrix per category.
Add objective items for breadth.
Add code items for application.
Add mock-exam blueprints for balanced assembly.
Track per-category counts.
Track unanswered weak areas through history data.
Use AI only to propose candidate questions, never to bypass review.

## Exam Blueprint Rules

Define a blueprint for each subject.
Specify target duration.
Specify total score.
Specify per-type quotas.
Specify per-difficulty spread.
Specify per-topic distribution.
Use blueprint validation before publishing exam generation.

## System-Generated Exam Rules

Pull only from the fixed bank.
Respect blueprint quotas.
Avoid repeating the same question within one exam.
Prefer lower recent-repeat probability for users with history.
Persist the exact selected question IDs.
Persist the exam snapshot even if the bank changes later.

## AI-Generated Exam Rules

Require an active AI configuration before generation.
Pass subject, level, blueprint, language, difficulty, and output schema to the model.
Request structured JSON output.
Validate the JSON before storing it.
Reject malformed AI output with actionable error messages.
Store AI-generated questions separately from built-in banks unless explicitly imported.
Mark every AI-generated exam item with provenance metadata.

## Grading Strategy Matrix

Grade `single_choice` by exact answer match.
Grade `multiple_choice` by exact set match unless the product explicitly defines partial credit.
Grade `true_false` by boolean match.
Grade `fill_blank` by normalized text match or allowed answer set.
Grade `code_completion` by allowed answer tokens or reference snippets.
Grade `bug_fix` by rubric or AI, depending on the task structure.
Grade `short_answer` by rubric or AI.
Grade `programming` by rubric or AI, and optionally by heuristic checks when available.

Record which grading path was used.
Record whether the score is deterministic, heuristic, or AI-produced.

## AI Grading Rules

Use AI grading only after deterministic grading has been attempted when relevant.
Provide the model with the question, the candidate answer, the reference answer, the rubric, and the scoring scale.
Request structured output with `score`, `reason`, `strengths`, `mistakes`, and `improvement_suggestions`.
Clamp returned scores to the valid range.
Store raw AI grading payloads for auditability when privacy requirements allow.
Fall back gracefully when AI grading fails.

## AI Provider Compatibility

Support OpenAI official API key workflows.
Support OpenAI-compatible `base_url` configuration.
Support `Responses API` style requests when the provider uses that protocol.
Support `Chat Completions` style requests for compatible providers.
Support custom headers when enterprise gateways require them.
Support optional organization or project identifiers where relevant.
Expose model selection in settings.
Expose request timeout and temperature controls in settings when the UI remains understandable.

## OpenAI Guidance

Prefer official API-key-based access for OpenAI.
Do not claim that consumer ChatGPT web login is a stable third-party integration method unless official documentation explicitly supports it.
Offer a quick link to the official OpenAI platform login or API-key page if helpful.
Explain clearly in the product copy whether the app needs an API key.

## Prompting Rules for AI Question Generation

Specify the subject and level precisely.
Specify the target audience as NCRE candidates.
Specify the desired question types.
Specify the difficulty spread.
Specify the scoring requirements.
Specify the JSON schema.
Specify that explanations must be concise and correct.
Specify that C code must compile conceptually and avoid undefined behavior unless the question explicitly targets bug analysis.
Reject outputs that violate schema or subject boundaries.

## Prompting Rules for AI Grading

Specify the score range.
Specify that grading must be strict but constructive.
Specify that reasons must cite the rubric, not just opinions.
Specify that wrong answers should include likely misunderstanding categories.
Specify that improvement suggestions should be brief and actionable.
Specify that the model must return machine-readable JSON only.

## Front-End Rules

Design for Chinese-language usage first.
Design for desktop screens first, then make the layout responsive enough for smaller windows.
Keep navigation shallow.
Show subject selection, mock generation, exam progress, and history clearly.
Show whether an exam came from the built-in bank or AI.
Show which answers were auto-graded and which were AI-graded.
Show wrong-answer analysis inline with review mode.
Show AI settings in a dedicated page with protocol explanations.
Show data completeness indicators for each subject bank.

## Front-End Style Rules

Avoid bland default enterprise styling.
Use a deliberate visual direction.
Use a small, coherent color system.
Use strong typography suitable for Chinese text.
Use cards and panels with clear visual hierarchy.
Use motion sparingly for section transitions and feedback states.
Use contrast and spacing to help exam focus.
Avoid decorative clutter during test-taking mode.

## UX Rules for Exam Mode

Expose remaining time when the blueprint is timed.
Expose question palette navigation.
Expose answer-save state.
Expose current progress.
Warn before submitting incomplete exams.
Allow review after submission.
Allow retry or generate-similar-exam actions from results.
Preserve user answers across accidental refresh or desktop window closure when feasible.

## Persistence Rules

Store attempts in SQLite.
Store subject metadata separately from attempt records.
Store the full exam payload snapshot with each attempt.
Store the user answers payload.
Store grading payloads.
Store summary metrics for quick dashboard queries.
Store AI analysis text separately from numeric scores when that improves queryability.

## History and Analytics Rules

List attempts by newest first.
Filter by subject.
Filter by generation mode.
Compute correct rate.
Compute average score.
Compute weak-tag counts.
Compute recent trend.
Compute repeated mistake patterns when enough data exists.

## Error-Handling Rules

Handle missing bank files explicitly.
Handle malformed question data explicitly.
Handle unavailable AI settings explicitly.
Handle HTTP timeout and provider authentication failures explicitly.
Handle database initialization failures explicitly.
Handle packaging-time missing assets explicitly.
Return structured API errors.
Render human-readable error states in the UI.

## Security and Privacy Rules

Avoid sending local exam history to an AI provider unless the specific feature requires it.
Minimize prompt payloads.
Redact secrets from logs.
Do not commit real API keys.
Do not expose secrets in front-end bundles.
Use server-side storage for API settings when a local backend exists.

## Packaging Rules

Make the application runnable with one command in development.
Make the application packageable with one script in Windows.
Include static files and seed data in the packaged build.
Handle first-run data directory creation.
Handle packaged-path resolution differently from source-path resolution when needed.
Test packaged startup after changing asset paths.

## Performance Rules

Cache parsed bank manifests in memory after load.
Avoid reparsing all banks on every API call.
Avoid N+1 database access patterns for history lists.
Avoid blocking the UI thread during AI requests.
Avoid blocking startup on optional AI availability checks.

## Validation Checklist

Validate bank JSON shape.
Validate unique question IDs within a bank.
Validate blueprint quotas against available question counts.
Validate deterministic grading behavior.
Validate history persistence.
Validate settings save and load behavior.
Validate AI request serialization.
Validate packaged asset resolution.

## Review Checklist for Code Changes

Check for broken imports.
Check for path issues on Windows.
Check for stale front-end API paths.
Check for schema drift between seed data and runtime models.
Check for missing null handling.
Check for duplicated grading logic between front end and back end.
Check for inconsistent score totals.
Check for accidental loss of backward compatibility in saved history rows.

## Common Failure Modes

The subject catalog exists but the bank file path is wrong.
The bank file loads but question IDs collide.
The exam blueprint asks for more questions than the bank provides.
The front end sends answers in a shape the grader does not expect.
The AI provider returns prose instead of JSON.
The packaged EXE cannot find static assets.
The browser fallback works but the embedded webview path does not.
The history detail view renders old attempt payloads incorrectly after schema changes.

## Debugging Playbook

Reproduce with the smallest subject bank that still fails.
Inspect the exact exam snapshot stored with the attempt.
Inspect the raw request payload sent from the front end.
Inspect the normalized answer payload used by the grader.
Inspect raw AI responses before JSON parsing.
Inspect packaged resource paths separately from source-mode paths.
Add a focused regression test for the confirmed defect.

## Done Definition

The app launches locally.
The dashboard loads.
The built-in Level 2 C bank is available.
At least one other level is available with a built-in starter bank.
A system-generated exam can be created.
A submission can be graded.
The attempt appears in history.
Wrong-answer analysis is visible.
AI settings can be saved.
AI generation can be attempted with a compatible provider.
The EXE build script exists and resolves app assets.

## Change Protocol

Update schemas before updating dependent code.
Update seed data and manifests together.
Update UI copy when a feature is optional or degraded.
Update packaging paths when adding new data directories.
Update validation scripts when introducing new bank fields.
Update tests when changing scoring or history shape.

## Communication Rules

Explain assumptions explicitly.
Call out when a bank is curated rather than official.
Call out when AI grading was used.
Call out when a subject bank is a starter bank instead of a broad bank.
Call out when official OpenAI login is not a documented integration path and API-key access is used instead.
Call out residual risks after large changes.

## Fast Path for Common Requests

If the user asks to add a subject, extend the subject catalog, add its bank manifest, add a starter blueprint, and add seed questions.
If the user asks to improve Level 2 C, expand the coverage matrix first, then add missing questions by weak topic.
If the user asks to improve grading, update the strategy matrix before touching prompts.
If the user asks to package to EXE, verify source-mode startup first, then build.
If the user asks to add AI support, wire settings, provider abstraction, request validation, and fallback UI states together.

## Resource Usage

Read repository code before rewriting architecture.
Read official NCRE outline or sample material when coverage questions arise.
Read official AI provider docs for volatile API behavior.
Use bundled scripts for validation when present.
Prefer improving existing seed generators over hand-editing giant JSON files repeatedly.

## Final Standard

Leave the project in a state where another agent can continue without reverse engineering.
Leave data formats explicit.
Leave the app runnable.
Leave the banks auditable.
Leave the grading logic explainable.
Leave the packaging path documented by code, not only by memory.
