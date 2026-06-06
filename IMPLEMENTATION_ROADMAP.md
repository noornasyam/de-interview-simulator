# Implementation Roadmap

## Current State

The app is a Streamlit application with a local JSON question engine.

Current modes:

- Learning Mode
- Exam Mode
- Interview Mode

Current engine capabilities:

- Load questions from JSON files.
- Randomly select questions.
- Evaluate MCQ.
- Evaluate fill-in-the-blank.
- Evaluate interview/rubric questions using weighted expected points.

Current limitations:

- Runtime still uses the older platform-first bank.
- Long-term `core/` and `cloud/` taxonomy exists but is not wired into the app.
- Exam Mode is not timed.
- Reporting is basic.
- No session blueprint implementation.
- No architecture review mode.
- No role-based learning paths.

## Desired State

The implementation should support:

- Role-based preparation:
  - Data Engineer
  - Senior Data Engineer
  - Lead Data Engineer
  - Data Architect
- Blueprint-driven session generation.
- Core + cloud question loading.
- Timed Exam Mode.
- Domain-wise and difficulty-wise scoring.
- Recommended learning paths.
- Architecture Review mode.
- Content taxonomy validation.

## Missing Components

### Engine Layer

Missing:

- Unified taxonomy-aware loader.
- Blueprint parser.
- Session generator that mixes domains.
- Difficulty range filtering.
- Role target filtering.
- Question type filtering.
- Runtime support for `scenario` and `architecture_review`.

### Reporting Layer

Missing:

- Domain-wise score calculation.
- Difficulty-wise score calculation.
- Weak area detection.
- Strength detection.
- Recommended domain generation.
- Recommended learning path generation.

### UI Layer

Missing:

- Role selector.
- Domain selector.
- Session blueprint selector.
- Timer for Exam Mode.
- Architecture Review mode UI.
- Progress dashboard.

### Content Tooling

Missing:

- JSON schema validation.
- Duplicate ID checks.
- Required field checks.
- Weight total checks for expected points.
- Difficulty and domain validation.

## Recommended Order Of Implementation

### Phase 1: Stabilize Local Platform

Scope:

- Keep current app behavior stable.
- Add content validation scripts or checks.
- Define canonical schema in documentation or JSON schema.
- Add missing long-term taxonomy folders.

Estimated effort: 1-2 days.

### Phase 2: Add Blueprint Files

Scope:

- Create:
  - `data_engineer.json`
  - `senior_data_engineer.json`
  - `lead_data_engineer.json`
  - `architect.json`
- Include domain mix, difficulty range, mode defaults, and recommended question counts.

Estimated effort: 0.5-1 day.

### Phase 3: Taxonomy-Aware Loader

Scope:

- Load from `core/` and `cloud/`.
- Preserve support for the current platform-first working bank during migration.
- Allow filters:
  - role
  - mode
  - domain
  - category
  - cloud
  - level
  - difficulty range
  - type

Estimated effort: 1-2 days.

### Phase 4: Blueprint-Driven Session Generation

Scope:

- Generate sessions from blueprint domain mix.
- Avoid repeated questions in a session.
- Fall back when a domain does not have enough questions.
- Return selected questions with selection metadata.

Estimated effort: 1-2 days.

### Phase 5: Reporting Upgrade

Scope:

- Overall score.
- Domain-wise score.
- Difficulty-wise score.
- Strengths.
- Weaknesses.
- Recommended domains to practice.
- Recommended learning path.

Estimated effort: 2-3 days.

### Phase 6: Timed Exam Mode

Scope:

- Add configurable timer.
- End session when time expires.
- Hide explanations until completion.
- Include final score and domain breakdown.

Estimated effort: 1 day.

### Phase 7: Architecture Review MVP

Scope:

- Add `architecture_review` question type.
- Define schema for proposed architecture, constraints, and expected critique points.
- Evaluate against weighted criteria:
  - scalability
  - reliability
  - cost
  - security
  - monitoring
  - governance
  - trade-offs

Estimated effort: 2-4 days.

### Phase 8: Learning Path System

Scope:

- Map weak domains to recommended content.
- Generate next-practice recommendations.
- Add role-based progression.

Estimated effort: 2-4 days.

## Implementation Principles

- Keep the system local-first.
- Do not add a database until progress tracking truly needs persistence.
- Keep JSON content human-editable.
- Prefer deterministic rubric evaluation before AI evaluation.
- Do not over-engineer abstractions ahead of content volume.
- Preserve the current working app while migrating taxonomy.

## Estimated Effort Summary

| Phase | Effort |
|---|---:|
| Stabilize local platform | 1-2 days |
| Add blueprint files | 0.5-1 day |
| Taxonomy-aware loader | 1-2 days |
| Blueprint session generation | 1-2 days |
| Reporting upgrade | 2-3 days |
| Timed Exam Mode | 1 day |
| Architecture Review MVP | 2-4 days |
| Learning path system | 2-4 days |

Total estimated implementation effort: 10-19 engineering days, excluding content creation.

