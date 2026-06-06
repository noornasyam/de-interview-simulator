# Content Roadmap

## Current State

Current content is concentrated in Level 0 samples.

Existing working bank:

- GCP certification and interview Level 0
- AWS certification and interview Level 0
- Azure certification and interview Level 0
- Multi-cloud certification and interview Level 0

Existing long-term taxonomy scaffold:

- `core/sql`
- `core/python`
- `core/terraform`
- `core/git`
- `core/data_modeling`
- `core/streaming`
- `core/architecture`
- `cloud/gcp`
- `cloud/aws`
- `cloud/azure`
- `session_blueprints`

Existing long-term content:

- `core/sql/certification/level0.json`
- `core/sql/interview/level0.json`

## Desired State

The content library should support four career tracks:

- Data Engineer
- Senior Data Engineer
- Lead Data Engineer
- Data Architect

It should cover six levels:

- Level 0
- Junior
- Mid-Level
- Senior
- Lead
- Architect

It should cover these core domains:

- SQL
- Python
- Terraform
- Git
- Data Modeling
- Streaming
- Architecture
- Security
- Monitoring
- Cost
- Leadership

And these cloud domains:

- GCP
- AWS
- Azure
- Multi-cloud

## Missing Components

### Missing Domain Folders

Add long-term taxonomy folders for:

- `app/data/question_bank/core/security`
- `app/data/question_bank/core/monitoring`
- `app/data/question_bank/core/cost`
- `app/data/question_bank/core/leadership`
- `app/data/question_bank/cloud/multi_cloud`

Each should have:

- `certification/`
- `interview/`

### Missing Content By Domain

Current SQL Level 0 is a good start. The next missing content areas are:

- Python Level 0
- Git Level 0
- Data Modeling Level 0
- Cloud fundamentals Level 0
- Monitoring fundamentals Level 0
- Cost fundamentals Level 0
- Security fundamentals Level 0

### Missing Content By Seniority

The platform needs a progression from basics to real production engineering:

- Level 0: vocabulary, simple queries, basic cloud services
- Junior: simple implementation and debugging
- Mid-Level: pipeline ownership, quality, orchestration, cost awareness
- Senior: design trade-offs, incident handling, scaling, governance
- Lead: stakeholder management, mentoring, platform standards
- Architect: multi-region, compliance, cross-domain architecture, long-term strategy

## Recommended Content Build Order

### Phase 1: Foundation Library

Goal: make Learning Mode valuable for beginners.

Recommended content:

- SQL Level 0 certification: already started
- SQL Level 0 interview: already started
- Python Level 0 certification
- Python Level 0 interview
- Git Level 0 certification
- Git Level 0 interview
- Data Modeling Level 0 certification
- Data Modeling Level 0 interview

Estimated effort: 3-5 days for a useful first pass.

### Phase 2: Cloud Foundation Library

Goal: support cloud-aware data engineering fundamentals.

Recommended content:

- GCP Level 0 and Junior
- AWS Level 0 and Junior
- Azure Level 0 and Junior
- Multi-cloud Level 0 and Junior

Focus on:

- Object storage
- Warehouses
- Streaming services
- IAM basics
- Monitoring basics
- Cost basics

Estimated effort: 4-7 days.

### Phase 3: Production Engineering Library

Goal: make the product differentiated from quiz apps.

Recommended domains:

- Monitoring
- Alerting
- Incident Management
- Root Cause Analysis
- Runbooks
- SLOs
- Data Quality
- Cost Optimization
- Security and Governance

Estimated effort: 1-2 weeks.

### Phase 4: Senior, Lead, Architect Library

Goal: prepare experienced engineers for real interviews.

Recommended content:

- Architecture scenarios
- Architecture review questions
- Trade-off analysis
- Stakeholder management
- Mentoring and prioritization
- Platform standards
- Multi-region and disaster recovery
- Batch vs streaming decisions
- CDC and data consistency

Estimated effort: 2-4 weeks for a strong initial library.

## Question Type Strategy

### MCQ

Use for:

- Definitions
- Clause behavior
- Tool selection
- Basic trade-off recognition

Avoid:

- Pure trivia with no job relevance

### Fill In The Blank

Use for:

- Syntax recall
- Command recall
- SQL clauses
- Git commands
- Terraform concepts

### Scenario

Use for:

- Learning and Exam Mode
- Production problem solving
- Service selection
- Debugging and incident analysis

### Interview

Use for:

- Open-ended reasoning
- Rubric-based evaluation
- Follow-up practice

### Architecture Review

Use for:

- Senior
- Lead
- Architect
- Production design critique
- Trade-off analysis

## Session Blueprints

Create these files:

- `app/data/session_blueprints/data_engineer.json`
- `app/data/session_blueprints/senior_data_engineer.json`
- `app/data/session_blueprints/lead_data_engineer.json`
- `app/data/session_blueprints/architect.json`

Recommended first blueprint shape:

```json
{
  "role": "senior_data_engineer",
  "level": "Senior",
  "domains": {
    "sql": 2,
    "python": 1,
    "data_modeling": 1,
    "cloud": 2,
    "terraform": 1,
    "architecture": 1
  },
  "difficulty_range": [7, 8]
}
```

## Estimated Effort

| Content Area | Effort |
|---|---:|
| Complete Level 0 core content | 1 week |
| Add Junior core content | 1 week |
| Add cloud foundation content | 1 week |
| Add production engineering content | 1-2 weeks |
| Add Senior/Lead/Architect scenarios | 2-4 weeks |
| Add content QA and consistency review | ongoing |

