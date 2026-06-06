# MVP Status

## What Is Complete

- Local Streamlit application with Learning Mode, Exam Mode, and Interview Mode.
- File-based JSON question loading.
- Legacy certification question support under `app/data/question_bank/{platform}/certification/`.
- Taxonomy-aware senior interview question loading under `core/` and `cloud/`.
- Senior interview domains:
  - SQL
  - Python
  - Data Modeling
  - Production Engineering
  - GCP
- All Domains interview sessions across the five senior banks.
- Random 5-question interview sessions with duplicate prevention.
- One-question-at-a-time interview flow.
- Progress text and visual progress bar for Interview Mode.
- Local rubric scoring based on expected points and keywords.
- Matched points, missing points, explanations, follow-up questions, and ideal answers after each interview answer.
- Final interview report with:
  - Overall score
  - Domain score
  - Strongest domains
  - Weakest domains
  - Strongest areas
  - Weakest areas
  - Recommended topics to improve
  - Question-by-question breakdown
- Text report download for completed sessions.
- Missing files, empty files, invalid JSON, malformed question structures, and empty interview answers are handled without crashing.
- Runtime is local-only: no OpenAI, no database, no authentication, no `.env`.

## What Is Partially Complete

- Role selector exists, but every role currently maps to Senior-level content.
- Learning Mode and Exam Mode are functional, but still use the legacy certification structure rather than the new `core/` taxonomy.
- Certification reporting shows score and review, but does not yet include domain-wise analytics.
- Session blueprints are documented but not wired into runtime selection.
- Public README includes screenshot placeholders, but screenshots have not been captured yet.
- Validation was completed through Python compilation, local engine checks, Streamlit boot, and Streamlit AppTest smoke paths. Manual browser click-through remains pending.

## What Is Missing

- Role-specific banks for Data Engineer, Lead Data Engineer, and Architect.
- Taxonomy-aware Learning Mode and Exam Mode.
- Timed Exam Mode.
- Domain-wise reporting for certification sessions.
- Session blueprint execution.
- Automated tests.
- UI screenshot smoke tests.
- Project license.
- Public release screenshots.

## What Should Be Built Next

1. Add a small automated test suite for question loading, random selection, rubric scoring, and report generation.
2. Wire Learning Mode and Exam Mode into the `core/` and `cloud/` taxonomy.
3. Add timed Exam Mode and domain-wise exam reporting.
4. Implement session blueprints for role-based domain mixes.
5. Add role-specific content for Data Engineer, Lead Data Engineer, and Architect.
6. Capture screenshots and add them to the README.
7. Add a license and finalize GitHub repository metadata.

## Current Validation Summary

| Area | Status | Notes |
|---|---|---|
| Python compile | Passed | `app.py` and `certification_engine.py` compile successfully. |
| Certification loading | Passed | Legacy GCP Level 0 certification bank loads. |
| Interview loading | Passed | All Domains Senior loads 100 questions. |
| Random selection | Passed | Selects 5 unique interview questions. |
| Rubric evaluation | Passed | Returns score, matched points, missing points, explanation, and follow-ups. |
| Missing domain handling | Passed | Returns empty list. |
| Malformed interview handling | Passed | Returns score 0 without crashing. |
| Streamlit launch | Passed | Booted with `venv/bin/streamlit run app.py --server.headless true --server.port 8502`, then stopped cleanly. |
| Streamlit AppTest paths | Passed | Learning, Exam, and Interview start flows rendered without exceptions. |
| Manual browser click-through | Pending | Needs human verification in a browser before tagging a public release. |
