# DailyDEHub AI Interview Coach

AI-powered Data Engineering interview practice from Beginner to Architect level.

The current MVP is an AI-first Streamlit interview simulator powered by Google ADK + Gemini Flash. It does not require OpenAI, a database, authentication, payments, or deployment services.

## Features

- Single AI interview coach page with no mode dropdown.
- Gemini status indicator: Gemini enabled or Setup required.
- Level selector for Beginner, Junior, Mid-Level, Senior, Lead, and Architect.
- Domain selector for SQL, Python, GCP / BigQuery, AWS, Azure, Databricks, Git, Terraform, Airflow, dbt, Data Modeling, Production Engineering, and Mixed Interview.
- Hybrid 5-question interview sessions, one question at a time.
- Curated v2 question bank support for objective and structured practice.
- SQL v2 bank is complete across Beginner, Junior, Mid-Level, Senior, Lead, and Architect.
- Python, GCP / BigQuery, Terraform, Airflow, and Data Modeling v2 folders are scaffolded and currently fall back to Gemini-generated questions.
- Cost-saving evaluation strategy: MCQ, fill-blank, match, and short-answer questions are evaluated locally; open-ended scenario/design/troubleshooting questions use Gemini.
- Mixed question types: conceptual, scenario-based, troubleshooting, design decision, cost optimization, security/governance, debugging/root cause analysis, and trade-off comparison.
- Complexity increases across the session: fundamentals, practical concepts, scenario-based, troubleshooting/RCA, then design decisions/trade-offs.
- During the interview, each answer shows only score and short feedback to reduce fatigue.
- The final report includes explanations, missing points, ideal answers, and detailed review.
- Scoring dimensions: Technical Knowledge, Problem Solving, Communication Clarity, Architecture Thinking, Cost Awareness, and Security Awareness.
- Final report with total score out of 100, readiness percentage, correct/partial/incorrect counts, average score, domain-wise score, dimension-wise score, strengths, weak areas, top concepts to revise, question-by-question explanations, ideal answers, next-level readiness, and hiring recommendation.
- Downloadable PDF interview report for testers and candidates.
- Level progression logic: 80+ ready for next level, 60-79 borderline, below 60 repeat level.
- Legacy local learning, exam, and rubric interview code remains in the repository but is not shown in the main UI.
- File-based JSON content remains available for grounding and future local/offline features.
- File-based JSON content model for easy extension.

## Folder Structure

```text
.
├── app.py
├── requirements.txt
├── app/
│   ├── config/
│   │   ├── levels.py
│   │   └── platforms.py
│   ├── agents/
│   │   ├── interview_orchestrator_agent.py
│   │   ├── question_generator_agent.py
│   │   ├── follow_up_agent.py
│   │   ├── evaluation_agent.py
│   │   └── final_report_agent.py
│   ├── data/
│   │   ├── question_bank/
│   │   │   ├── v2/
│   │   │   │   ├── schema.json
│   │   │   │   ├── sql/
│   │   │   │   ├── python/
│   │   │   │   ├── gcp_bigquery/
│   │   │   │   ├── terraform/
│   │   │   │   ├── airflow/
│   │   │   │   └── data_modeling/
│   │   │   ├── core/
│   │   │   │   ├── sql/
│   │   │   │   ├── python/
│   │   │   │   ├── data_modeling/
│   │   │   │   └── production_engineering/
│   │   │   ├── cloud/
│   │   │   │   └── gcp/
│   │   │   ├── aws/
│   │   │   ├── azure/
│   │   │   ├── gcp/
│   │   │   └── multi-cloud/
│   │   └── session_blueprints/
│   └── services/
│       ├── certification_engine.py
│       ├── adk_interview_service.py
│       ├── question_bank_service.py
│       └── hybrid_evaluation_service.py
├── scripts/
│   └── validate_v2_question_bank.py
├── GAP_ANALYSIS.md
├── CONTENT_ROADMAP.md
├── IMPLEMENTATION_ROADMAP.md
├── RELEASE_CHECKLIST.md
└── MVP_STATUS.md
```

## How to Run

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure Gemini:

```bash
cp .env.template .env
```

Then edit `.env`:

```bash
GOOGLE_API_KEY=your_google_ai_studio_key
```

The main interview coach requires this key. If it is missing, the app shows setup instructions and does not start an interview.

4. Start the app:

```bash
streamlit run app.py
```

5. Open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Legacy Question Bank Paths

Legacy Senior Interview content remains in the repo and can be reused for grounding or future offline modes:

```text
app/data/question_bank/core/sql/interview/senior.json
app/data/question_bank/core/python/interview/senior.json
app/data/question_bank/core/data_modeling/interview/senior.json
app/data/question_bank/core/production_engineering/interview/senior.json
app/data/question_bank/cloud/gcp/interview/senior.json
```

Legacy certification content remains available under:

```text
app/data/question_bank/{platform}/certification/level0.json
```

## Hybrid Question Bank

The app now prefers curated v2 questions when a complete bank exists for the selected domain and level. SQL is complete across all six levels:

```text
app/data/question_bank/v2/sql/beginner.json
app/data/question_bank/v2/sql/junior_data_engineer.json
app/data/question_bank/v2/sql/mid_level_data_engineer.json
app/data/question_bank/v2/sql/senior_data_engineer.json
app/data/question_bank/v2/sql/lead_data_engineer.json
app/data/question_bank/v2/sql/architect.json
```

Priority folders for Python, GCP / BigQuery, Terraform, Airflow, and Data Modeling are present but pending curated content. Those selections continue to use Gemini-generated questions.

Validate the v2 bank with:

```bash
python scripts/validate_v2_question_bank.py
```

## Screenshots

Screenshots will be added before the first tagged public release.

- Home page placeholder
- Active interview question placeholder
- Per-answer feedback placeholder
- Final report placeholder

## Future Roadmap

- Populate v2 banks for Python, GCP / BigQuery, Terraform, Airflow, and Data Modeling.
- Add automated coverage for the hybrid 5-question interview flow.
- Add optional local/offline mode behind an advanced setting.
- Add session blueprint support for role-weighted domain mixes.
- Add richer report export formats.
- Add automated tests for Streamlit session flows.
- Add optional screenshot-based UI smoke tests.
