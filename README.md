# Data Engineering Career Accelerator

A local-first learning, assessment, and interview preparation app for Data Engineering roles.

The current MVP focuses on Senior Data Engineering interview preparation with rubric-based evaluation from JSON question banks. It does not require OpenAI, external services, a database, authentication, or environment variables.

## Features

- Learning Mode for certification-style practice with immediate feedback.
- Exam Mode for certification-style practice with final review.
- Interview Mode for open-ended Senior Data Engineering interview practice.
- Role selector for Data Engineer, Senior Data Engineer, Lead Data Engineer, and Architect.
- Domain selector for SQL, Python, Data Modeling, Production Engineering, GCP, and All Domains.
- Random 5-question interview sessions with duplicate prevention.
- Local rubric scoring with matched points, missing points, explanations, follow-up questions, and ideal answers.
- Final interview report with overall score, domain scores, strongest areas, weakest areas, recommended topics, and question-by-question review.
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
│       └── certification_engine.py
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

3. Start the app:

```bash
streamlit run app.py
```

4. Open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Question Bank Paths

Current Senior Interview MVP content:

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

- Learning Mode placeholder
- Exam Mode placeholder
- Interview Mode question placeholder
- Interview Mode final report placeholder

## Future Roadmap

- Add role-specific question banks for Data Engineer, Lead Data Engineer, and Architect.
- Add more Level 0, Junior, Mid-Level, Lead, and Architect content.
- Add session blueprint support for role-weighted domain mixes.
- Add richer report export formats.
- Add automated tests for Streamlit session flows.
- Add optional screenshot-based UI smoke tests.
