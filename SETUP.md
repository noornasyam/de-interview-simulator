# Setup Guide

## Prerequisites

- Python 3.8+
- pip
- Google AI Studio API key for the main AI interview flow

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Gemini Configuration

DailyDEHub AI Interview Coach uses Google ADK with Gemini Flash. Create a local
`.env` file:

```bash
cp .env.template .env
```

Then set:

```bash
GOOGLE_API_KEY=your_google_ai_studio_key
```

Do not commit `.env`. If the key is missing, the app opens but the interview
cannot start.

## Run

```bash
streamlit run app.py
```

The app usually starts at:

```text
http://localhost:8501
```

If port 8501 is already in use:

```bash
streamlit run app.py --server.port 8502
```

## Notes

- `.env` is required to start the AI interview.
- No OpenAI API key is required.
- The app uses Google ADK + Gemini Flash.
- Legacy local modes remain in the repository but are not shown in the main UI.
