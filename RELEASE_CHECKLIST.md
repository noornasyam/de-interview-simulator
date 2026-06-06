# Release Checklist

## Functionality Checks

- [x] Python files compile with `python3 -B -m py_compile app.py app/services/certification_engine.py`.
- [x] Learning Mode uses certification question loading, answer evaluation, immediate feedback, key takeaways, and `Continue to Next Question`.
- [x] Exam Mode uses certification question loading, answer evaluation, no per-question explanation, final score, review, and text report download.
- [x] Interview Mode loads taxonomy-aware senior question banks.
- [x] Interview Mode supports SQL, Python, Data Modeling, Production Engineering, GCP, and All Domains.
- [x] Interview Mode selects 5 random questions and avoids duplicate IDs in a session.
- [x] Interview Mode shows one question at a time.
- [x] Interview Mode shows progress text and progress bar.
- [x] Interview Mode rejects empty open-ended answers.
- [x] Interview Mode shows score, matched points, missing points, explanation, follow-up questions, and ideal answer.
- [x] Interview Mode final report shows overall score, domain score, strongest areas, weakest areas, recommended topics, and question-by-question breakdown.
- [x] Local engine validation passed for certification and interview evaluation paths.
- [x] Streamlit app booted successfully with `venv/bin/streamlit run app.py --server.headless true --server.port 8502`.
- [x] Streamlit AppTest smoke paths passed for Learning, Exam, and Interview start flows.
- [ ] Manual browser click-through pending for Learning, Exam, and Interview modes.

## Content Checks

Validated senior interview banks:

| Bank | Path | Total Questions | Missing Fields | Invalid Structures | Duplicate IDs |
|---|---|---:|---:|---:|---:|
| SQL Senior | `app/data/question_bank/core/sql/interview/senior.json` | 20 | 0 | 0 | 0 |
| Python Senior | `app/data/question_bank/core/python/interview/senior.json` | 20 | 0 | 0 | 0 |
| Data Modeling Senior | `app/data/question_bank/core/data_modeling/interview/senior.json` | 20 | 0 | 0 | 0 |
| Production Engineering Senior | `app/data/question_bank/core/production_engineering/interview/senior.json` | 20 | 0 | 0 | 0 |
| GCP Senior | `app/data/question_bank/cloud/gcp/interview/senior.json` | 20 | 0 | 0 | 0 |

Summary:

- [x] Senior interview content total: 100 questions.
- [x] No duplicate IDs inside or across the five senior interview banks.
- [x] All senior interview questions include expected points with weights.
- [x] All senior interview questions include explanations, key takeaways, and follow-up questions.
- [x] Missing JSON files return empty question banks without crashing.
- [x] Empty or invalid JSON files return empty question banks without crashing.
- [x] Invalid question structures are skipped by loaders or handled by evaluation.

## GitHub Readiness Checks

- [x] README describes the current MVP accurately.
- [x] Setup guide does not require `.env`, OpenAI, or external services.
- [x] Runtime dependencies are reduced to direct app dependency: `streamlit`.
- [x] Dead LLM prompt files and unused service stubs removed.
- [x] No database or authentication setup required.
- [x] Release status documented in `MVP_STATUS.md`.
- [ ] Add screenshots before tagging the first public release.
- [ ] Run `pip install -r requirements.txt` in a fresh virtual environment.
- [ ] Manually click through Learning, Exam, and Interview modes in the browser.
- [ ] Review public repository metadata, license, and description before publishing.
