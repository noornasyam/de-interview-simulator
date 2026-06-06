# Session Blueprints

This folder is for future random question generation presets.

A session blueprint defines how many questions to draw from each domain, level, provider, and question type for a target interview path.

## Purpose

Use blueprints to create repeatable interview-prep sessions for:

- Data Engineer
- Senior Data Engineer
- Lead Data Engineer
- Architect

## Example Blueprint

```json
{
  "id": "senior_data_engineer_gcp",
  "role_target": "senior_data_engineer",
  "level": "Senior",
  "cloud": "gcp",
  "mode": "interview",
  "question_count": 8,
  "domain_mix": {
    "sql": 2,
    "python": 1,
    "data_modeling": 1,
    "streaming": 1,
    "architecture": 1,
    "cloud_gcp": 1,
    "monitoring": 1
  },
  "difficulty_range": [5, 8]
}
```

## Random Generation Rules

Future question generation should:

1. Load eligible questions from `core` plus selected `cloud` provider.
2. Filter by role, level, mode, type, category, domain, and difficulty.
3. Avoid question IDs already used in the current session.
4. Sample according to `domain_mix`.
5. Fall back to nearby difficulty or adjacent domains only when necessary.
