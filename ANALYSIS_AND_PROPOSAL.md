# DE Interview Simulator - Repository Analysis & Proposal

## Current State Assessment

### ✅ What Exists
1. **Certification Mode**
   - Multiple choice quiz format
   - Immediate feedback (correct/incorrect)
   - Score tracking & final summary
   - Supports: AWS, Azure, GCP, Multi-Cloud
   - Difficulty levels: Level 0 through Architect

2. **Question Bank Structure**
   - JSON-based storage: `app/data/question_bank/{platform}/{level}.json`
   - Currently: Level 0 questions for GCP, AWS, Azure
   - Format: id, topic, question, options, correct_answer, explanation

3. **Code Structure**
   - `certification_engine.py`: Load & evaluate multiple choice answers
   - `simulator_engine.py`: Stub for interview simulation (empty)
   - `llm_service.py`: Stub for LLM integration (empty)
   - `question_prompt.py`: Template exists for question generation
   - `evaluation_prompt.py`: Empty (needs implementation)

4. **UI Framework**
   - Streamlit-based main app
   - Session state management (basic)
   - Mode selector (currently only "Certification")

---

## Identified Improvements

### 🔴 Critical Gaps
1. **LLM Integration**
   - No OpenAI/LLM API calls implemented
   - No evaluation logic for free-form answers
   - No follow-up question generation

2. **Interview Mode**
   - Not implemented
   - No hybrid architecture established
   - No interview history tracking
   - No final report generation

3. **Session Management**
   - Basic implementation only
   - Missing: interview state, conversation history, score tracking
   - No persistence layer

4. **Prompt Engineering**
   - Only question_prompt.py has content
   - evaluation_prompt.py is empty
   - No follow-up prompt templates

---

## Proposed Architecture: Interview Mode (Hybrid)

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                         │
│  ┌──────────┬──────────────┬──────────┬────────────────┐     │
│  │ Mode Sel │ Platform/Lvl │ Question │ Answer Input   │     │
│  │ Interview│ Session Ctrl │ Display  │ & Follow-ups   │     │
│  └──────────┴──────────────┴──────────┴────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Interview Engine Layer                       │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  InterviewEngine                                      │   │
│  │  ├─ Initialize interview session                      │   │
│  │  ├─ Get seed question (from bank OR AI-generated)     │   │
│  │  ├─ Manage interview flow & history                   │   │
│  │  ├─ Track responses & evaluations                     │   │
│  │  └─ Generate final report                             │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┴──────────────────┐
        ↓                                      ↓
┌──────────────────────┐         ┌──────────────────────┐
│  Question Source     │         │  LLM Service Layer   │
│                      │         │                      │
│ ├─ Seed QB (JSON)    │         │ ├─ Evaluate answer  │
│ ├─ Static questions  │         │ ├─ Generate follow-up
│ └─ AI-generated      │         │ ├─ Score response   │
│                      │         │ └─ Generate report  │
└──────────────────────┘         └──────────────────────┘
                                         ↓
                                   OpenAI API
                                   (GPT-4/3.5)
```

### Key Components

#### 1. **Interview Session State**
```python
InterviewSession {
  session_id: str
  platform: str
  level: str
  start_time: datetime
  interview_state: "started" | "in_progress" | "completed"
  
  questions_asked: List[Question]
  responses: List[InterviewResponse]
  evaluations: List[Evaluation]
  
  current_question: Question
  current_question_index: int
  conversation_history: List[Turn]
}
```

#### 2. **Interview Response & Evaluation**
```python
InterviewResponse {
  question_id: str
  original_question: str
  candidate_answer: str
  ai_evaluation: {
    score: float (0-100)
    strengths: List[str]
    weaknesses: List[str]
    feedback: str
    follow_up_justification: str
  }
}

FollowUp {
  parent_question_id: str
  follow_up_question: str
  rationale: str
  topic_focus: str
}
```

#### 3. **Interview Report**
```python
InterviewReport {
  session_id: str
  duration: str
  total_questions: int
  average_score: float
  performance_by_topic: Dict[str, float]
  key_strengths: List[str]
  areas_for_improvement: List[str]
  recommendations: List[str]
  detailed_feedback: List[QuestionFeedback]
}
```

---

## Implementation Plan

### Phase 1: Core Infrastructure
**Files to Create/Modify:**
1. `app/models/interview.py` (NEW)
   - InterviewSession dataclass
   - InterviewResponse dataclass
   - FollowUp dataclass
   - InterviewReport dataclass

2. `app/utils/session_state.py` (MODIFY)
   - Initialize interview session
   - Manage interview state transitions
   - Store responses & evaluations
   - Export session data

3. `app/prompts/evaluation_prompt.py` (IMPLEMENT)
   - Evaluation prompt template
   - Follow-up generation prompt
   - Report generation prompt

### Phase 2: LLM Integration
**Files to Create/Modify:**
1. `app/services/llm_service.py` (IMPLEMENT)
   - `evaluate_answer(question, answer)`: Score & feedback
   - `generate_follow_up(question, answer, feedback)`: Follow-up question
   - `generate_report(interview_session)`: Final report
   - Error handling & retry logic

2. `app/config/prompts.py` (NEW)
   - Centralized prompt configurations
   - Model parameters (temperature, max_tokens)
   - System instructions

### Phase 3: Interview Engine
**Files to Create/Modify:**
1. `app/services/interview_engine.py` (IMPLEMENT)
   - `start_interview()`: Initialize session
   - `get_next_question()`: Fetch seed or generate new
   - `submit_answer(answer)`: Process response
   - `complete_interview()`: Finalize session
   - `get_report()`: Generate final report

2. `app/services/certification_engine.py` (ENHANCE)
   - Add seed question rotation
   - Keep existing multiple-choice logic

### Phase 4: UI Layer
**Files to Create/Modify:**
1. `app.py` (MODIFY)
   - Add "Interview" mode to selectbox
   - Route between Certification & Interview modes
   - Add interview-specific UI components

2. `pages/interview.py` (NEW) - Optional
   - Interview-specific Streamlit page
   - Question display
   - Answer input (text area)
   - Follow-up display
   - Session controls (pause, end)

### Phase 5: Data & Configuration
**Files to Create/Modify:**
1. `app/data/seed_questions/` (NEW)
   - High-quality starter questions per platform/level
   - Formatted for interview context

2. `app/config/interview_config.py` (NEW)
   - Question budget per interview
   - Time limits
   - Scoring weights

---

## Technical Details

### Question Flow (Hybrid Approach)
```
1. Interview Start
   ↓
2. Load SEED question from bank
   (Ensures quality & consistency)
   ↓
3. User answers
   ↓
4. AI Evaluates answer
   ├─ Score: 0-100
   ├─ Feedback
   └─ Strengths/Weaknesses
   ↓
5. AI Generates FOLLOW-UP
   (Based on response & gaps)
   ↓
6. Repeat until interview quota met
   ↓
7. Generate REPORT
```

### LLM Prompting Strategy
- **Evaluation**: 
  - Input: Original question + candidate answer
  - Output: JSON with score, feedback, follow-up rationale
  
- **Follow-up Generation**:
  - Input: Previous Q&A + evaluation + current level
  - Output: Follow-up question + topic focus
  
- **Report Generation**:
  - Input: All Q&A pairs + evaluations
  - Output: Structured report with insights

### Error Handling & Resilience
- Fallback to pre-written feedback if LLM fails
- Retry logic with exponential backoff
- Rate limiting & token management
- Input validation & sanitization

---

## Data Flow Example

```
User starts Interview Mode
  ↓
Select: Platform=GCP, Level=Mid-Level
  ↓
[Interview Engine] Initializes session
  ↓
[Q1] Loads seed question from gcp/midlevel.json
     "What is BigQuery's advantage over Dataproc?"
  ↓
User answers: "BigQuery is serverless..."
  ↓
[LLM Service] Evaluates
  → Score: 75/100
  → Strengths: Good understanding of serverless
  → Weakness: Didn't mention cost efficiency
  → Suggestion: Ask about data pipeline optimization
  ↓
[LLM Service] Generates follow-up
  → "Can you explain how BigQuery handles data optimization?"
  ↓
[Q2] User answers follow-up
  ↓
[Repeat 3-5 questions total]
  ↓
[Interview Engine] Generates report
  → Duration: 12 minutes
  → Avg Score: 72/100
  → Strengths: Good cloud concepts
  → Areas: Practice architecture design
  → Recommendations: Review data pipeline patterns
```

---

## File Structure After Implementation

```
app/
├── config/
│   ├── interview_config.py          (NEW)
│   ├── levels.py
│   ├── platforms.py
│   └── prompts.py                   (NEW)
├── data/
│   └── question_bank/
│       ├── aws/level0.json
│       ├── azure/level0.json
│       └── gcp/level0.json
├── models/
│   └── interview.py                 (NEW)
├── prompts/
│   ├── evaluation_prompt.py          (IMPLEMENT)
│   ├── question_prompt.py
│   ├── followup_prompt.py            (NEW)
│   └── report_prompt.py              (NEW)
├── services/
│   ├── certification_engine.py       (ENHANCE)
│   ├── interview_engine.py           (NEW)
│   └── llm_service.py                (IMPLEMENT)
└── utils/
    └── session_state.py              (ENHANCE)

pages/
└── interview.py                      (OPTIONAL)

app.py                               (MODIFY)
```

---

## Key Features Summary

| Feature | Certification | Interview |
|---------|---------------|-----------|
| Question Type | Multiple choice | Open-ended |
| Question Source | Seed bank only | Seed + AI-generated follow-ups |
| Evaluation | Exact match | AI-based scoring (0-100) |
| Feedback | Explanation only | Score + strengths + weaknesses |
| Follow-ups | None | AI-generated based on gaps |
| History | Score only | Full conversation + evaluations |
| Report | Score card | Detailed performance analysis |
| Duration | Variable | 10-15 mins (configurable) |

---

## Implementation Complexity Estimate

| Phase | Complexity | Estimated Time | Files |
|-------|-----------|-----------------|-------|
| 1: Infrastructure | Low | 2-3 hours | 2-3 |
| 2: LLM Integration | Medium | 4-6 hours | 2-3 |
| 3: Interview Engine | Medium | 4-5 hours | 2 |
| 4: UI Layer | Low | 2-3 hours | 2 |
| 5: Configuration | Low | 1-2 hours | 2 |
| **Total** | **Medium** | **13-19 hours** | **11-13** |

---

## Next Steps (Awaiting Approval)

1. ✅ Review this architecture proposal
2. ✅ Identify any concerns or modifications needed
3. ✅ Approve proceeding to implementation
4. ⏳ I will then:
   - Create data models
   - Implement LLM service calls
   - Build interview engine
   - Update UI layer
   - Test end-to-end flow

---

## Questions for Clarification

1. **Question Depth**: How many follow-up questions per interview? (Currently proposed: 3-5)
2. **Scoring**: Should scoring be absolute (0-100) or relative to level?
3. **AI Model**: Preference for GPT-4 or GPT-3.5-turbo? (Cost vs. quality tradeoff)
4. **Interview Duration**: Target interview time? (Currently proposed: 10-15 minutes)
5. **Report Format**: HTML export, PDF, or Streamlit display only?
6. **Session Persistence**: Save interviews to database or session-only?
