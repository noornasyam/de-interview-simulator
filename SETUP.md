# Setup Guide - DE Interview Simulator

## Prerequisites
- Python 3.8+
- pip

## Installation & Setup

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.template .env
# Edit .env with your configuration (API keys, etc.)
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will start at `http://localhost:8501`

## Project Structure
```
app/
├── config/           # Configuration (levels, platforms)
├── data/            # Question banks (JSON format)
├── prompts/         # LLM prompt templates
├── services/        # Core services (LLM, simulator, evaluation)
└── utils/           # Utilities (session state)
```

## Available Features
- **Platforms**: AWS, Azure, GCP, Multi-Cloud
- **Difficulty Levels**: Level 0, Junior, Mid-Level, Senior, Lead, Architect
- **Mode**: Certification (Interview Simulator)

## Troubleshooting
- If packages don't install: `pip install --upgrade pip setuptools`
- If port 8501 is in use: `streamlit run app.py --server.port 8502`
- Missing API keys? Ensure `.env` is configured with required credentials

## Next Steps
- Add more questions to `app/data/question_bank/`
- Implement LLM evaluation logic in `services/llm_service.py`
- Configure your LLM provider API keys
