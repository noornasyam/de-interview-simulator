# Setup Guide

## Prerequisites

- Python 3.8+
- pip

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

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

- No `.env` file is required.
- No OpenAI API key is required.
- All evaluation is local and JSON-based.
- The current MVP uses Senior-level interview content for every role selector option.
