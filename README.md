# DailyDEHub AI Interview Coach

AI-powered Data Engineering interview practice from Beginner to Architect level.

The current MVP is an AI-first Streamlit interview simulator powered by Google ADK + Gemini Flash. It does not require OpenAI, a database, authentication, payments, or deployment services.

## Features

- Single AI interview coach page with no mode dropdown.
- Gemini status indicator: Gemini enabled or Setup required.
- Level selector for Beginner, Junior, Mid-Level, Senior, Lead, and Architect.
- Domain selector for SQL, Python, GCP / BigQuery, AWS, Azure, Databricks, Git, Terraform, Airflow, dbt, Data Modeling, Production Engineering, and Mixed Interview.
- 5-question interview sessions, one question at a time.
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
│       └── adk_interview_service.py
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

## Screenshots

Screenshots will be added before the first tagged public release.

- Home page placeholder
- Active interview question placeholder
- Per-answer feedback placeholder
- Final report placeholder

## Future Roadmap

- Add automated coverage for the 5-question AI interview flow.
- Add exportable interview reports.
- Add optional local/offline mode behind an advanced setting.
- Add session blueprint support for role-weighted domain mixes.
- Add richer report export formats.
- Add automated tests for Streamlit session flows.
- Add optional screenshot-based UI smoke tests.
