# Gap Analysis

## Current State

The repository has evolved from a basic quiz app into an early local-first learning platform.

What exists today:

- Streamlit app with `Learning Mode`, `Exam Mode`, and `Interview Mode`.
- Local JSON-based question evaluation.
- Working runtime question bank under:
  - `app/data/question_bank/gcp/{certification,interview}/level0.json`
  - `app/data/question_bank/aws/{certification,interview}/level0.json`
  - `app/data/question_bank/azure/{certification,interview}/level0.json`
  - `app/data/question_bank/multi-cloud/{certification,interview}/level0.json`
- Long-term taxonomy scaffold under:
  - `app/data/question_bank/core/...`
  - `app/data/question_bank/cloud/...`
  - `app/data/session_blueprints/`
- Initial SQL content:
  - `core/sql/certification/level0.json`
  - `core/sql/interview/level0.json`
- Local evaluators for:
  - `mcq`
  - `fill_blank`
  - `interview` / rubric-based questions
- No active OpenAI dependency in the runtime path.
- No database.

## Desired State

The product vision is a Data Engineering Career Accelerator, not a quiz app.

Desired capabilities:

- Structured learning paths for Data Engineer, Senior Data Engineer, Lead Data Engineer, and Data Architect.
- Learning Mode for concept learning with immediate feedback.
- Exam Mode for timed certification-style practice with final performance reporting.
- Interview Mode for scenario-based, rubric-evaluated practice.
- Architecture Review mode for senior, lead, and architect preparation.
- Coverage across core domains:
  - SQL
  - Python
  - Terraform
  - Git
  - Data Modeling
  - Streaming
  - Architecture
  - Security
  - Monitoring
  - Cost
  - Leadership
- Coverage across cloud domains:
  - GCP
  - AWS
  - Azure
  - Multi-cloud
- Rich reporting:
  - Overall score
  - Domain-wise score
  - Difficulty-wise score
  - Strengths
  - Weaknesses
  - Recommended learning path
  - Recommended domains to practice

## Missing Components

### Product Structure

- No explicit product-level navigation for learning paths, roles, or career tracks.
- No role target selection, such as Data Engineer vs Senior Data Engineer.
- No architecture review mode.
- No structured learning path system.

### Content Taxonomy

- Runtime still loads from the older platform-first structure.
- The long-term `core/` and `cloud/` taxonomy exists but is not yet used by the app.
- Missing core domain folders from the stated vision:
  - `core/security`
  - `core/monitoring`
  - `core/cost`
  - `core/leadership`
- `cloud/multi_cloud` is not yet present in the long-term taxonomy.
- Content coverage is still very small outside SQL and Level 0 cloud samples.

### Question Schema

- Existing schema is flexible but not yet validated.
- No schema contract file or JSON schema exists.
- `role_targets` is recommended in docs but not consistently used in content.
- Difficulty mapping exists conceptually but is not enforced.
- Question types like `scenario` and `architecture_review` are not implemented yet.

### Evaluation

- MCQ and fill-blank evaluation are simple and useful.
- Interview evaluation matches weighted expected points by keyword.
- No partial keyword scoring inside a single expected point.
- No support for architecture-review evaluation.
- No support for scenario questions distinct from MCQ/fill/interview.
- No answer-quality dimensions like clarity, trade-offs, production readiness, or seniority.

### Session Generation

- Random selection exists in foundation form.
- No blueprint-driven session generation yet.
- No domain mix balancing.
- No difficulty range selection.
- No role-based filtering.
- No repeat tracking across sessions.

### Reporting

- Current reporting is basic.
- Domain-wise and difficulty-wise reporting are not implemented.
- Weak area detection is not yet connected to recommended learning paths.
- No historical progress tracking.
- No report model or export structure beyond text download.

### UX

- Learning Mode has the right immediate-feedback pattern.
- Exam Mode is not timed yet.
- Interview Mode does not yet feel like a real interview loop with adaptive follow-ups.
- No dashboard or progress overview.
- No curriculum map.

## Recommended Order Of Implementation

1. Stabilize the content schema.
2. Complete the long-term taxonomy folders.
3. Add session blueprints for target roles.
4. Update loaders to support both current and long-term taxonomy.
5. Add domain-wise and difficulty-wise reporting.
6. Add timed Exam Mode.
7. Add role-based session generation.
8. Add more Level 0 and Junior content across core domains.
9. Add architecture review question type and evaluator.
10. Add learning paths and recommendations.

## Estimated Effort

| Area | Effort |
|---|---:|
| Schema stabilization | 0.5-1 day |
| Taxonomy completion | 0.5 day |
| Session blueprints | 0.5-1 day |
| Loader upgrade | 1-2 days |
| Reporting upgrade | 2-3 days |
| Timed Exam Mode | 0.5-1 day |
| Role-based random generation | 1-2 days |
| Architecture Review MVP | 2-4 days |
| Initial content expansion | ongoing |

