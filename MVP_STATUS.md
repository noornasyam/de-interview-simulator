# MVP Status

## What Is Complete

- AI-first Streamlit application: DailyDEHub AI Interview Coach.
- Single main UI with no Learning/Exam/Interview mode dropdown.
- AI Interview Mode powered by Google ADK + Gemini Flash.
- Level selector for Beginner, Junior Data Engineer, Mid-Level Data Engineer, Senior Data Engineer, Lead Data Engineer, and Architect.
- Domain selector for SQL, Python, GCP / BigQuery, AWS, Azure, Databricks, Git, Terraform, Airflow, dbt, Data Modeling, Production Engineering, and Mixed Interview.
- AI interview flow with 5 questions, one question at a time, varied question types, increasing complexity, lightweight per-answer feedback, and detailed local final summary.
- Hybrid question-bank foundation under `app/data/question_bank/v2/`.
- SQL v2 curated question bank is complete across Beginner, Junior, Mid-Level, Senior, Lead, and Architect with at least 10 questions per level.
- Hybrid evaluation service scores MCQ, fill-blank, match, and short-answer questions locally to reduce Gemini usage.
- Open-ended scenario, troubleshooting, design, architecture, governance, reliability, cost, and trade-off questions continue to use Gemini evaluation.
- v2 validation script checks JSON parsing, duplicate IDs, required fields, type-specific fields, explanations, ideal answers, and per-file counts.
- File-based JSON question loading.
- Legacy certification question support under `app/data/question_bank/{platform}/certification/`.
- Taxonomy-aware senior interview question loading under `core/` and `cloud/`.
- Senior interview domains:
  - SQL
  - Python
  - Data Modeling
  - Production Engineering
  - GCP
- One-question-at-a-time AI interview flow.
- Progress text and visual progress bar.
- Final summary computes total score, readiness percentage, average score, correct count, partial count, incorrect count, domain-wise score, dimension-wise score, strengths, weak areas, top concepts to revise, next-level recommendation, and hiring recommendation.
- Downloadable PDF interview report is available after completing a session.
- Level progression uses 80+ ready for next level, 60-79 borderline, and below 60 repeat level.
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
- Legacy local modes remain in code but are hidden from the main UI.
- Runtime has no OpenAI, database, authentication, payment, or deployment dependency.

## What Is Partially Complete

- AI interview requires live Gemini credentials and still needs manual end-to-end validation with a real API key.
- Python, GCP / BigQuery, Terraform, Airflow, and Data Modeling v2 folders are scaffolded but pending curated content.
- Non-SQL domains currently continue to rely on Gemini-generated questions.
- Legacy Learning Mode, Exam Mode, and local Interview Mode functions exist but are not exposed in the main UI.
- Session blueprints are documented but not wired into runtime selection.
- Public README includes screenshot placeholders, but screenshots have not been captured yet.
- Validation was completed through Python compilation, local engine checks, Streamlit boot, and Streamlit AppTest smoke paths. Manual browser click-through remains pending.

## What Is Missing

- Curated v2 banks for Python, GCP / BigQuery, Terraform, Airflow, and Data Modeling.
- Curated v2 banks for AWS, Azure, Databricks, Git, dbt, Production Engineering, and Mixed Interview.
- Optional advanced/local mode toggle if offline usage becomes a product requirement.
- Session blueprint execution.
- Automated tests.
- Automated tests for the 5-question AI interview state machine.
- UI screenshot smoke tests.
- Project license.
- Public release screenshots.

## What Should Be Built Next

1. Populate the next curated v2 bank: Python or GCP / BigQuery.
2. Manually validate SQL Beginner and SQL Junior without Gemini, then SQL Senior with a real `GOOGLE_API_KEY`.
3. Manually validate the full 5-question flow and PDF download for Senior Data Engineer + GCP / BigQuery and Architect + Mixed Interview with a real `GOOGLE_API_KEY`.
4. Add automated tests for setup-required state, curated SQL start flow, answer submission, final report, and mode-free UI.
5. Implement session blueprints for role-based domain mixes.
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
| SQL v2 bank | Passed | Six level files created with 60 total curated questions. |
| V2 bank validation | Passed | `python3 scripts/validate_v2_question_bank.py` passed. |
| Missing domain handling | Passed | Returns empty list. |
| Malformed interview handling | Passed | Returns score 0 without crashing. |
| Streamlit launch | Passed | Booted with `venv/bin/streamlit run app.py --server.headless true --server.port 8502`, then stopped cleanly. |
| Streamlit AppTest paths | Pending refresh | Needs updated smoke test for the new single-page AI UI. |
| AI Interview Mode | Pending | Needs live 5-question Gemini validation with `GOOGLE_API_KEY`. |
| Manual browser click-through | Pending | Needs human verification in a browser before tagging a public release. |
