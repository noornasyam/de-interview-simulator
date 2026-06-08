import streamlit as st

from app.config.levels import LEVELS
from app.config.platforms import PLATFORMS
from app.services.certification_engine import (
    evaluate_question,
    load_questions,
    load_taxonomy_questions,
    select_random_questions,
)
from app.services.adk_interview_service import (
    AI_DOMAINS,
    AI_ROLES,
    MAX_QUESTIONS,
    build_interview_report_pdf,
    evaluate_ai_answer,
    generate_ai_final_report,
    generate_ai_question,
    is_adk_configured,
    start_ai_interview,
)
from app.services.hybrid_evaluation_service import (
    evaluate_objective_question,
    should_use_gemini,
)
from app.services.question_bank_service import (
    has_complete_v2_bank,
    load_v2_questions,
    select_session_questions,
)


CERTIFICATION_QUESTION_LIMIT = 5
INTERVIEW_QUESTION_LIMIT = 5
AI_MODE = "AI Interview Mode"
INTERVIEW_TYPES = ["Domain Practice", "Interview Track"]
INTERVIEW_TRACKS = {
    "Data Engineer": ["SQL", "Python", "GCP / BigQuery", "Airflow", "Data Modeling"],
    "Senior Data Engineer": ["SQL", "Python", "GCP / BigQuery", "Terraform", "Airflow"],
    "Lead Data Engineer": [
        "Terraform",
        "Production Engineering",
        "GCP / BigQuery",
        "Data Modeling",
        "Airflow",
    ],
    "Architect": ["GCP / BigQuery", "AWS", "Azure", "Databricks", "Production Engineering"],
}
ROLE_LEVELS = {
    "Data Engineer": "Senior",
    "Senior Data Engineer": "Senior",
    "Lead Data Engineer": "Senior",
    "Architect": "Senior",
}
INTERVIEW_DOMAINS = [
    "All Domains",
    "SQL",
    "Python",
    "Data Modeling",
    "Production Engineering",
    "GCP",
]


AI_SESSION_DEFAULTS = {
    "ai_started": False,
    "ai_complete": False,
    "ai_level": "Senior Data Engineer",
    "ai_domain": "GCP / BigQuery",
    "ai_interview_type": "Domain Practice",
    "ai_track": "",
    "ai_track_domains": [],
    "ai_question_index": 0,
    "ai_current_question": None,
    "ai_current_answer": "",
    "ai_current_follow_up": None,
    "ai_history": [],
    "ai_pending_results": [],
    "ai_answers": [],
    "ai_evaluations": [],
    "ai_final_report": None,
    "ai_explanations": [],
    "ai_current_evaluation": None,
    "ai_correct_count": 0,
    "ai_partial_count": 0,
    "ai_incorrect_count": 0,
    "ai_phase": "main_answer",
    "ai_interview": None,
    "ai_session_questions": [],
    "ai_using_question_bank": False,
    "ai_bank_warning": "",
}


def initialize_ai_session_state():
    for key, value in AI_SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, list) else value


def reset_session():
    for key in [
        "session_questions",
        "session_index",
        "session_score",
        "session_results",
        "question_answered",
        "explanation_shown",
        "waiting_for_next_question",
        "interview_questions",
        "interview_index",
        "interview_history",
        "interview_complete",
        "interview_report",
        "interview_waiting_for_next",
        "ai_started",
        "ai_complete",
        "ai_level",
        "ai_domain",
        "ai_interview_type",
        "ai_track",
        "ai_track_domains",
        "ai_question_index",
        "ai_current_question",
        "ai_current_answer",
        "ai_current_follow_up",
        "ai_history",
        "ai_pending_results",
        "ai_answers",
        "ai_evaluations",
        "ai_final_report",
        "ai_explanations",
        "ai_current_evaluation",
        "ai_correct_count",
        "ai_partial_count",
        "ai_incorrect_count",
        "ai_phase",
        "ai_interview",
        "ai_session_questions",
        "ai_using_question_bank",
        "ai_bank_warning",
        "adk_interview",
        "adk_current_question",
        "adk_question_index",
        "adk_history",
        "adk_waiting_for_next",
        "adk_complete",
    ]:
        st.session_state.pop(key, None)

    for key in list(st.session_state.keys()):
        if key.startswith("show_ideal_answer_"):
            st.session_state.pop(key, None)


def start_question_session(platform, level):
    questions = load_questions(platform, level, bank="certification")
    selected_questions = select_random_questions(
        questions,
        count=min(CERTIFICATION_QUESTION_LIMIT, len(questions)),
    )

    st.session_state.session_questions = selected_questions
    st.session_state.session_index = 0
    st.session_state.session_score = 0
    st.session_state.session_results = []
    st.session_state.question_answered = False
    st.session_state.explanation_shown = False
    st.session_state.waiting_for_next_question = False


def start_interview(domain, level):
    questions = load_taxonomy_questions(domain, level, bank="interview")
    selected_questions = select_random_questions(
        questions,
        count=min(INTERVIEW_QUESTION_LIMIT, len(questions)),
    )

    st.session_state.interview_questions = selected_questions
    st.session_state.interview_index = 0
    st.session_state.interview_history = []
    st.session_state.interview_complete = not selected_questions
    st.session_state.interview_report = ""
    st.session_state.interview_waiting_for_next = False


def show_question_input(question, key_prefix):
    question_type = question.get("type", "mcq")
    question_id = question.get("id", "question")

    if question.get("scenario"):
        st.write(question["scenario"])

    st.write(question["question"])

    if question_type == "mcq":
        options = question.get("options", [])
        if not options:
            st.warning("This multiple-choice question has no options configured.")
            return None

        return st.radio(
            "Choose your answer",
            options,
            key=f"{key_prefix}_{question_id}",
        )

    if question_type in {"interview", "rubric"}:
        return st.text_area(
            "Your answer",
            key=f"{key_prefix}_{question_id}",
            height=180,
        )

    return st.text_input("Your answer", key=f"{key_prefix}_{question_id}")


def show_basic_evaluation(result):
    if result["is_correct"]:
        st.success("Correct.")
    else:
        st.error("Incorrect.")

    st.write(f"Score: {result['score']}/100")
    if result.get("correct_answer"):
        st.write(f"Correct answer: {result['correct_answer']}")
    if result.get("explanation"):
        st.info(result["explanation"])


def get_key_takeaways(question):
    key_takeaways = question.get("key_takeaways")
    if isinstance(key_takeaways, list) and key_takeaways:
        return key_takeaways

    takeaways = []
    if question.get("domain"):
        takeaways.append(f"Domain focus: {question['domain']}.")
    if question.get("category"):
        takeaways.append(f"Category: {question['category']}.")
    if question.get("explanation"):
        takeaways.append(question["explanation"])

    return takeaways


def show_learning_evaluation(question, result):
    show_basic_evaluation(result)

    takeaways = get_key_takeaways(question)
    if takeaways:
        st.write("Key Takeaways")
        for takeaway in takeaways:
            st.write(f"- {takeaway}")


def show_interview_evaluation(result, key_suffix=""):
    evaluation = result["evaluation"]
    st.metric("Score", f"{evaluation['score']}/100")

    st.write("Matched points")
    if evaluation["matched_points"]:
        for point in evaluation["matched_points"]:
            matched_keywords = ", ".join(point.get("matched_keywords", []))
            detail = f" - matched: {matched_keywords}" if matched_keywords else ""
            st.write(f"- {point['point']} ({point['weight']} pts){detail}")
    else:
        st.write("- No expected points matched yet.")

    st.write("Missing points")
    if evaluation["missing_points"]:
        for point in evaluation["missing_points"]:
            st.write(f"- {point['point']} ({point['weight']} pts)")
    else:
        st.write("- No missing points.")

    if evaluation.get("explanation"):
        st.info(evaluation["explanation"])

    question_id = result["question"].get("id", "question")
    ideal_answer_key = f"show_ideal_answer_{question_id}_{key_suffix}"
    if st.button("Show Ideal Answer", key=f"button_{ideal_answer_key}"):
        st.session_state[ideal_answer_key] = True

    if st.session_state.get(ideal_answer_key):
        st.markdown(build_ideal_answer(result["question"]))

    follow_ups = evaluation.get("follow_ups", [])
    if follow_ups:
        st.write("Follow-up questions")
        for follow_up in follow_ups:
            st.write(f"- {follow_up}")


def build_ideal_answer(question):
    expected_points = question.get("expected_points", [])
    if not isinstance(expected_points, list):
        expected_points = []

    key_takeaways = question.get("key_takeaways")
    if not isinstance(key_takeaways, list):
        key_takeaways = []

    point_texts = [
        point.get("point", "")
        for point in expected_points
        if isinstance(point, dict) and point.get("point")
    ]
    technical_points = _format_answer_points(expected_points)
    operational_points = _filter_answer_points(
        expected_points,
        ["monitor", "alert", "security", "iam", "cost", "quality", "incident", "sla"],
    )
    tradeoff_points = _filter_answer_points(
        expected_points,
        ["trade-off", "tradeoff", "cost", "latency", "freshness", "correctness", "scale"],
    )

    lines = [
        "### Answer Summary",
        _build_answer_summary(question, point_texts),
        "",
        "### Key Technical Considerations",
    ]

    if technical_points:
        lines.extend(technical_points)
    else:
        lines.append("- Clarify the business goal, data flow, constraints, and success criteria before proposing a solution.")

    lines.extend(["", "### Trade-offs"])
    if tradeoff_points:
        lines.extend(tradeoff_points)
    else:
        lines.append("- I would call out the main trade-offs explicitly, especially correctness versus speed, reliability versus complexity, and cost versus freshness.")

    lines.extend(["", "### Monitoring / Security / Cost Considerations"])
    if operational_points:
        lines.extend(operational_points)
    else:
        lines.append("- I would include operational guardrails such as ownership, observability, access control, cost tracking, and validation checks before calling the design production-ready.")

    if question.get("explanation"):
        lines.extend(["", "### Why This Works", question["explanation"]])

    if isinstance(key_takeaways, list) and key_takeaways:
        lines.extend(["", "### Key Takeaways"])
        for takeaway in key_takeaways:
            lines.append(f"- {takeaway}")

    lines.extend(
        [
            "",
            "### Conclusion",
            "In an interview, I would finish by tying the design back to the business requirement, the production risks, and the checks I would use to prove the solution is correct and maintainable.",
        ]
    )

    return "\n".join(lines)


def _build_answer_summary(question, point_texts):
    domain = question.get("domain", "data engineering")
    category = question.get("category", "production design")
    if point_texts:
        return (
            f"I would approach this as a {domain} / {category} problem by first "
            f"confirming the requirements, then addressing the highest-impact areas: "
            f"{'; '.join(point_texts[:2])}."
        )

    return (
        "I would start by clarifying the requirement, identifying the failure or "
        "design risk, and then proposing a solution that is reliable, measurable, "
        "and maintainable in production."
    )


def _format_answer_points(expected_points):
    formatted_points = []
    for point in expected_points:
        if not isinstance(point, dict) or not point.get("point"):
            continue

        keywords = point.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = []

        keyword_text = ""
        if keywords:
            keyword_text = f" Mention: {', '.join(str(keyword) for keyword in keywords[:5])}."

        formatted_points.append(f"- {point['point']}.{keyword_text}")

    return formatted_points


def _filter_answer_points(expected_points, terms):
    filtered_points = []
    for point in expected_points:
        if not isinstance(point, dict):
            continue

        keywords = point.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = []

        searchable_text = " ".join(
            [
                str(point.get("point", "")),
                " ".join(str(keyword) for keyword in keywords if keyword),
            ]
        ).lower()

        if any(term in searchable_text for term in terms):
            filtered_points.append(point)

    return _format_answer_points(filtered_points)


def show_progress(label, current, total):
    safe_total = max(total, 1)
    progress_value = min(current / safe_total, 1.0)
    st.write(f"{label} {current}/{total}")
    st.progress(progress_value)


def get_active_ai_question_count():
    session_questions = st.session_state.get("ai_session_questions", [])
    if st.session_state.get("ai_using_question_bank") and session_questions:
        return len(session_questions)
    return MAX_QUESTIONS


def question_bank_requires_gemini(questions):
    return any(should_use_gemini(question) for question in questions)


def select_track_session_questions(track, level):
    """Pick one curated question from each track domain."""

    selected = []
    used_ids = set()
    warnings = []
    for domain in INTERVIEW_TRACKS.get(track, []):
        questions = select_session_questions(domain, level, count=1, previous_ids=used_ids)
        if not questions:
            warnings.append(f"No curated question found for {domain} at {level}.")
            continue
        question = questions[0]
        used_ids.add(question.get("id"))
        selected.append(question)
    return selected, warnings


def get_ai_session_label():
    if st.session_state.get("ai_interview_type") == "Interview Track":
        return f"{st.session_state.get('ai_track', 'Interview Track')} Track"
    return st.session_state.get("ai_domain", "Domain Practice")


def get_domain_score_extremes(domain_scores):
    if not domain_scores:
        return None, None
    sorted_scores = sorted(domain_scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_scores[0], sorted_scores[-1]


def get_question_mix_for_level(level):
    mixes = {
        "Beginner": "MCQ, Match, Fill Blank",
        "Junior Data Engineer": "MCQ, Match, Fill Blank, Short Answer",
        "Mid-Level Data Engineer": "MCQ, Scenario, Troubleshooting",
        "Senior Data Engineer": "Scenario, Design Decisions, Troubleshooting",
        "Lead Data Engineer": "Architecture, Trade-offs, Governance",
        "Architect": "Enterprise Architecture, Reliability, Security",
    }
    return mixes.get(level, "Scenario, Troubleshooting, Design Decisions")


def render_ai_answer_input(question, index):
    question_type = str(question.get("type") or question.get("question_type") or "").lower()
    question_id = question.get("id", f"ai_question_{index}")

    if question_type == "mcq":
        options = question.get("options", [])
        if not options:
            st.warning("This curated MCQ has no options configured.")
            return ""
        return st.radio("Choose your answer", options, key=f"ai_answer_{question_id}_{index}")

    if question_type == "fill_blank":
        return st.text_input("Your answer", key=f"ai_answer_{question_id}_{index}")

    if question_type == "match":
        right_items = question.get("right_items", [])
        answer = {}
        for left_item in question.get("left_items", []):
            match_key = f"ai_match_{question_id}_{index}_{left_item}"
            if match_key not in st.session_state:
                st.session_state[match_key] = ""
            answer[left_item] = st.selectbox(
                left_item,
                [""] + right_items,
                key=match_key,
            )
        return answer

    height = 120 if question_type in {"short_answer", "light_scenario"} else 190
    return st.text_area("Your answer", key=f"ai_answer_{question_id}_{index}", height=height)


def is_empty_ai_answer(answer):
    if isinstance(answer, dict):
        return not all(str(value).strip() for value in answer.values())
    return not str(answer).strip()


def format_ai_answer(answer):
    if isinstance(answer, dict):
        return "\n".join(f"{left}: {right}" for left, right in answer.items())
    return str(answer).strip()


def evaluate_pending_ai_answers():
    level = st.session_state.ai_level
    domain = st.session_state.ai_domain
    pending_results = st.session_state.get("ai_pending_results", [])
    evaluated_results = []
    evaluations = []
    explanations = []
    correct_count = 0
    partial_count = 0
    incorrect_count = 0

    for item in pending_results:
        question = item.get("question", {})
        answer = item.get("answer", "")
        prior_results = [
            {
                "question": result.get("question", {}),
                "answer": result.get("answer", ""),
                "evaluation": result.get("evaluation", {}),
            }
            for result in evaluated_results
        ]

        if should_use_gemini(question):
            evaluation = evaluate_ai_answer(question, answer, level, domain, prior_results)
        else:
            evaluation = evaluate_objective_question(question, item.get("raw_answer", answer))

        if evaluation.get("error"):
            return False, evaluation["error"]

        result = {
            "question": question,
            "answer": answer,
            "evaluation": evaluation,
        }
        evaluated_results.append(result)
        evaluations.append(evaluation)

        score = int(evaluation.get("score", 0))
        if score >= 8:
            correct_count += 1
        elif score >= 5:
            partial_count += 1
        else:
            incorrect_count += 1

        if evaluation.get("explanation"):
            explanations.append(evaluation["explanation"])

    st.session_state.ai_history = evaluated_results
    st.session_state.ai_evaluations = evaluations
    st.session_state.ai_explanations = explanations
    st.session_state.ai_correct_count = correct_count
    st.session_state.ai_partial_count = partial_count
    st.session_state.ai_incorrect_count = incorrect_count
    st.session_state.ai_final_report = generate_ai_final_report(evaluated_results, level, domain)
    st.session_state.ai_complete = True
    st.session_state.ai_phase = "assessment"
    return True, ""


def build_interview_report(results):
    if not results:
        return {
            "overall_score": 0,
            "score_by_domain": {},
            "strongest_domains": [],
            "weakest_domains": [],
            "strongest_areas": [],
            "weakest_areas": [],
            "recommended_areas": [],
        }

    scores = [item["evaluation"]["score"] for item in results]
    score_by_domain = {}
    score_by_category = {}

    for item in results:
        domain = item["question"].get("domain", "unknown")
        category = item["question"].get("category", "unknown")
        score_by_domain.setdefault(domain, []).append(item["evaluation"]["score"])
        score_by_category.setdefault(category, []).append(item["evaluation"]["score"])

    score_by_domain = {
        domain: sum(domain_scores) / len(domain_scores)
        for domain, domain_scores in score_by_domain.items()
    }
    score_by_category = {
        category: sum(category_scores) / len(category_scores)
        for category, category_scores in score_by_category.items()
    }
    sorted_domains = sorted(score_by_domain.items(), key=lambda item: item[1], reverse=True)
    sorted_categories = sorted(score_by_category.items(), key=lambda item: item[1], reverse=True)

    missing_points = []
    for item in results:
        for point in item["evaluation"].get("missing_points", []):
            missing_points.append(point["point"])

    recommended_areas = list(dict.fromkeys(missing_points))[:5]
    if not recommended_areas:
        recommended_areas = ["Keep practicing senior-level trade-offs and production examples."]

    return {
        "overall_score": sum(scores) / len(scores),
        "score_by_domain": score_by_domain,
        "score_by_category": score_by_category,
        "strongest_domains": [domain for domain, _ in sorted_domains[:3]],
        "weakest_domains": [domain for domain, _ in sorted_domains[-3:]],
        "strongest_areas": [category for category, _ in sorted_categories[:3]],
        "weakest_areas": [category for category, _ in sorted_categories[-3:]],
        "recommended_areas": recommended_areas,
    }


def show_final_interview_report(results):
    report = build_interview_report(results)
    st.metric("Overall score", f"{report['overall_score']:.1f}/100")

    st.write("Domain score")
    for domain, score in report["score_by_domain"].items():
        st.write(f"- {domain}: {score:.1f}/100")

    st.write("Strongest areas")
    for area in report["strongest_areas"]:
        score = report["score_by_category"].get(area, 0)
        st.write(f"- {area}: {score:.1f}/100")

    st.write("Weakest areas")
    for area in report["weakest_areas"]:
        score = report["score_by_category"].get(area, 0)
        st.write(f"- {area}: {score:.1f}/100")

    st.write("Recommended topics to improve")
    for area in report["recommended_areas"]:
        st.write(f"- {area}")

    st.write("Strongest domains")
    for domain in report["strongest_domains"]:
        score = report["score_by_domain"].get(domain, 0)
        st.write(f"- {domain}: {score:.1f}/100")

    st.write("Weakest domains")
    for domain in report["weakest_domains"]:
        score = report["score_by_domain"].get(domain, 0)
        st.write(f"- {domain}: {score:.1f}/100")


def build_text_report(platform, level, mode, results):
    lines = [
        "Data Engineering Career Accelerator",
        f"{mode} Report",
        "",
        f"Platform: {platform}",
        f"Level: {level}",
        f"Questions answered: {len(results)}",
        "",
    ]

    if results:
        average_score = sum(item["evaluation"]["score"] for item in results) / len(results)
        lines.append(f"Overall score: {average_score:.1f}/100")
        lines.append("")

        if mode == "Interview Mode":
            interview_report = build_interview_report(results)
            lines.append("Domain score:")
            for domain, score in interview_report["score_by_domain"].items():
                lines.append(f"- {domain}: {score:.1f}/100")
            lines.append("")
            lines.append("Strongest areas:")
            lines.extend(f"- {area}" for area in interview_report["strongest_areas"])
            lines.append("")
            lines.append("Weakest areas:")
            lines.extend(f"- {area}" for area in interview_report["weakest_areas"])
            lines.append("")
            lines.append("Recommended topics to improve:")
            lines.extend(f"- {area}" for area in interview_report["recommended_areas"])
            lines.append("")

    for index, item in enumerate(results, start=1):
        question = item["question"]
        evaluation = item["evaluation"]
        lines.extend(
            [
                f"Question {index}: {question['question']}",
                f"Answer: {item['answer']}",
                f"Score: {evaluation['score']}/100",
                f"Explanation: {evaluation.get('explanation', '')}",
                "Ideal answer:",
                build_ideal_answer(question),
                "",
            ]
        )

    return "\n".join(lines)


st.set_page_config(
    page_title="DailyDEHub AI Interview Coach",
    page_icon="🎯",
    layout="centered",
)

initialize_ai_session_state()

st.title("DailyDEHub AI Interview Coach")
st.caption("AI-powered Data Engineering interview practice from Beginner to Architect level.")

gemini_ready = is_adk_configured()
if gemini_ready:
    st.success("Gemini enabled")
else:
    st.warning("Setup required")
    st.write("Set `GOOGLE_API_KEY` in your shell or create a local `.env` file:")
    st.code("GOOGLE_API_KEY=your_google_ai_studio_key", language="bash")

selected_level = st.selectbox("Select level", AI_ROLES, index=3)
selected_interview_type = st.selectbox("Interview Type", INTERVIEW_TYPES)
selected_track = ""
selected_track_domains = []
selected_domain = "Mixed Interview"

if selected_interview_type == "Interview Track":
    selected_track = st.selectbox("Select track", list(INTERVIEW_TRACKS), index=1)
    selected_track_domains = INTERVIEW_TRACKS[selected_track]
    st.caption("Track domains: " + ", ".join(selected_track_domains))
    available_bank_questions = [
        question
        for track_domain in selected_track_domains
        for question in load_v2_questions(track_domain, selected_level)
    ]
    has_curated_bank = all(
        has_complete_v2_bank(track_domain, selected_level, minimum_count=1)
        for track_domain in selected_track_domains
    )
    bank_needs_gemini = question_bank_requires_gemini(available_bank_questions)
    selected_session_label = f"{selected_track} Track"
else:
    selected_domain = st.selectbox("Select domain", AI_DOMAINS, index=2)
    available_bank_questions = load_v2_questions(selected_domain, selected_level)
    has_curated_bank = has_complete_v2_bank(selected_domain, selected_level, minimum_count=MAX_QUESTIONS)
    bank_needs_gemini = question_bank_requires_gemini(available_bank_questions)
    selected_session_label = selected_domain

if selected_interview_type == "Interview Track":
    if has_curated_bank:
        st.info("Using curated interview track + AI feedback")
    else:
        st.warning("This track is missing one or more curated domain banks for the selected level.")
elif has_curated_bank:
    st.info("Using curated question bank + AI feedback")
else:
    st.info("Using Gemini-generated questions")

if bank_needs_gemini and not gemini_ready:
    st.warning(
        "This session includes open-ended questions that need Gemini evaluation. "
        "Configure GOOGLE_API_KEY before starting."
    )

selection_key = f"ai:{selected_level}:{selected_interview_type}:{selected_session_label}"
if st.session_state.get("selection_key") != selection_key:
    st.session_state.selection_key = selection_key
    reset_session()
    initialize_ai_session_state()

if not st.session_state.get("ai_started"):
    st.subheader("Interview Session Summary")
    st.write(f"Interview Type: {selected_interview_type}")
    if selected_interview_type == "Interview Track":
        st.write(f"Track: {selected_track}")
        st.write("Domains: " + ", ".join(selected_track_domains))
    else:
        st.write(f"Domain: {selected_domain}")
    st.write(f"Level: {selected_level}")

    st.write("Interview Details:")
    st.write(f"- {MAX_QUESTIONS} Questions")
    st.write("- Estimated Time: 10-15 minutes")
    st.write("- Assessment Generated At End")
    st.write("- AI Evaluation Enabled" if gemini_ready else "- AI Evaluation Requires Setup")

    st.write("Question Mix:")
    st.write(f"- {get_question_mix_for_level(selected_level)}")

    can_start = has_curated_bank and (gemini_ready or not bank_needs_gemini)
    if selected_interview_type == "Domain Practice" and not has_curated_bank:
        can_start = gemini_ready

    col_start, col_back = st.columns(2)
    if col_start.button("Start Interview", disabled=not can_start):
        reset_session()
        initialize_ai_session_state()
        track_warnings = []
        if selected_interview_type == "Interview Track":
            session_questions, track_warnings = select_track_session_questions(
                selected_track,
                selected_level,
            )
            using_question_bank = True
            session_domain = selected_session_label
        else:
            session_questions = select_session_questions(selected_domain, selected_level, MAX_QUESTIONS)
            using_question_bank = bool(session_questions)
            session_domain = selected_domain

        using_question_bank = bool(session_questions)
        st.session_state.ai_started = True
        st.session_state.ai_complete = False
        st.session_state.ai_level = selected_level
        st.session_state.ai_domain = session_domain
        st.session_state.ai_interview_type = selected_interview_type
        st.session_state.ai_track = selected_track
        st.session_state.ai_track_domains = selected_track_domains
        st.session_state.ai_session_questions = session_questions
        st.session_state.ai_using_question_bank = using_question_bank
        warning_parts = list(track_warnings)
        if using_question_bank and len(session_questions) < MAX_QUESTIONS:
            warning_parts.append(
                f"Only {len(session_questions)} curated questions are available for this selection."
            )
        st.session_state.ai_bank_warning = " ".join(warning_parts)
        st.session_state.ai_interview = start_ai_interview(selected_level, session_domain)
        if using_question_bank:
            st.session_state.ai_current_question = session_questions[0]
        else:
            st.session_state.ai_current_question = generate_ai_question(selected_level, session_domain, [])
        st.session_state.ai_phase = "main_answer"
        st.rerun()

    if col_back.button("Back"):
        reset_session()
        initialize_ai_session_state()
        st.rerun()

    if not can_start:
        st.info(
            "Configure Gemini to use open-ended evaluations or generated interviews. "
            "Objective curated sessions can run locally when available."
        )
elif st.session_state.get("ai_complete"):
    history = st.session_state.get("ai_history", [])
    report = st.session_state.get("ai_final_report")
    if not report:
        report = generate_ai_final_report(history, st.session_state.ai_level, st.session_state.ai_domain)
        st.session_state.ai_final_report = report

    st.subheader("Final Interview Assessment")
    show_progress("Interview progress", len(history), get_active_ai_question_count())

    st.markdown("### Section 1: Overall Results")
    col_score, col_ready = st.columns(2)
    col_score.metric("Overall score", f"{report.get('total_score', report.get('overall_score', 0))}/100")
    col_ready.metric("Readiness", f"{report.get('readiness_percentage', 0)}%")

    recommendation = report.get("hiring_recommendation")
    if recommendation:
        st.write("Hiring Recommendation")
        st.write(recommendation)

    col1, col2, col3 = st.columns(3)
    col1.metric("Correct", report.get("correct_count", st.session_state.ai_correct_count))
    col2.metric("Partially correct", report.get("partial_count", st.session_state.ai_partial_count))
    col3.metric("Incorrect", report.get("incorrect_count", st.session_state.ai_incorrect_count))

    can_move = report.get("can_move_to_next_level") or report.get("ready_for_senior_interviews")
    if can_move:
        st.write("Move to next level")
        st.write(can_move)

    st.markdown("### Section 2: Strengths")
    for strength in report.get("strengths", []):
        st.write(f"- {strength}")

    st.markdown("### Section 3: Weak Areas")
    for gap in report.get("gaps", []):
        st.write(f"- {gap}")

    st.markdown("### Section 4: Concepts To Revise")
    concepts = report.get("concepts_to_revise") or report.get("recommended_learning_plan", [])
    domain_scores = report.get("domain_scores", {})
    if domain_scores:
        st.write("Domain-wise score")
        for score_domain, score in domain_scores.items():
            st.write(f"- {score_domain}: {score}/10")
        strongest_domain, weakest_domain = get_domain_score_extremes(domain_scores)
        if strongest_domain:
            st.write(f"Strongest domain: {strongest_domain[0]} ({strongest_domain[1]}/10)")
        if weakest_domain:
            st.write(f"Weakest domain: {weakest_domain[0]} ({weakest_domain[1]}/10)")

    dimension_scores = report.get("dimension_scores", {})
    if dimension_scores:
        st.write("Dimension-wise score")
        for dimension, score in dimension_scores.items():
            st.write(f"- {dimension}: {score}/10")

    for concept in concepts[:5]:
        st.write(f"- {concept}")

    st.markdown("### Section 5: Question Review")
    for index, item in enumerate(history, start=1):
        evaluation = item.get("evaluation", {})
        question = item.get("question", {})
        with st.expander(f"Question {index}: {question.get('question', '')}", expanded=index == 1):
            if question.get("scenario"):
                st.write(question["scenario"])
            st.write("Key Concept")
            st.write(question.get("concept") or question.get("category") or question.get("question_type") or "General data engineering")
            st.write("Your answer")
            st.write(item.get("answer", ""))
            st.write(f"Score: {evaluation.get('score', 0)}/10")
            if evaluation.get("dimension_scores"):
                st.write("Dimension scores")
                for dimension, score in evaluation["dimension_scores"].items():
                    st.write(f"- {dimension}: {score}/10")
            st.write("Explanation")
            st.write(evaluation.get("explanation", ""))
            st.write("Ideal answer")
            st.markdown(evaluation.get("ideal_answer", ""))
            if evaluation.get("missing_points"):
                st.write("Missing points")
                for point in evaluation["missing_points"]:
                    st.write(f"- {point}")

    st.markdown("### Section 6: Learning Plan")
    if report.get("recommended_learning_plan"):
        for item in report["recommended_learning_plan"]:
            st.write(f"- {item}")
    if can_move:
        st.write("Readiness recommendation")
        st.write(can_move)

    st.markdown("### Section 7: PDF Report")
    pdf_domain_label = get_ai_session_label()
    pdf_report = build_interview_report_pdf(
        report,
        history,
        st.session_state.ai_level,
        pdf_domain_label,
    )
    st.download_button(
        "Download PDF report",
        data=pdf_report,
        file_name="dailydehub_interview_report.pdf",
        mime="application/pdf",
    )

    if st.button("Start New Interview"):
        reset_session()
        initialize_ai_session_state()
        st.rerun()
else:
    level = st.session_state.ai_level
    domain = st.session_state.ai_domain
    question = st.session_state.get("ai_current_question")
    index = st.session_state.get("ai_question_index", 0)
    history = st.session_state.get("ai_history", [])
    active_question_count = get_active_ai_question_count()
    session_label = get_ai_session_label()

    if st.session_state.get("ai_phase") == "ready_for_assessment":
        answered_count = len(st.session_state.get("ai_pending_results", []))
        show_progress("Question", min(answered_count, active_question_count), active_question_count)
        st.caption(f"{level} • {session_label} • Assessment pending")
        st.success(f"All {answered_count} answers are recorded.")
        st.write("Generate the assessment when you are ready to see scores, explanations, ideal answers, and the learning plan.")
        if st.button("Generate Assessment"):
            with st.spinner("Evaluating answers and preparing your assessment..."):
                success, error = evaluate_pending_ai_answers()
            if not success:
                st.error(error)
            else:
                st.rerun()
        st.stop()

    show_progress("Question", index + 1, active_question_count)
    mode_label = "Curated bank + hybrid evaluation" if st.session_state.get("ai_using_question_bank") else "Gemini Flash"
    st.caption(f"{level} • {session_label} • {mode_label}")
    if st.session_state.get("ai_bank_warning"):
        st.warning(st.session_state.ai_bank_warning)

    if not isinstance(question, dict):
        st.error("No AI question is loaded. Restart the interview to generate a new question.")
        if st.button("Restart Interview"):
            reset_session()
            initialize_ai_session_state()
            st.rerun()
        st.stop()

    if question.get("error"):
        st.error(question["error"])
        if st.button("Try Again"):
            st.session_state.ai_current_question = generate_ai_question(level, domain, history)
            st.rerun()
        st.stop()

    if question.get("scenario"):
        st.write(question["scenario"])
    question_type_label = question.get("question_type") or question.get("type")
    if question_type_label:
        st.caption(f"{question_type_label} • {question.get('complexity') or question.get('difficulty', '')}")
    st.write(question.get("question", "No question available."))

    answer = render_ai_answer_input(question, index)
    button_label = "Finish Answers" if index + 1 >= active_question_count else "Next"
    if st.button(button_label):
        if is_empty_ai_answer(answer):
            st.warning("Please write an answer before submitting.")
        else:
            formatted_answer = format_ai_answer(answer)
            pending_result = {
                "question": question,
                "answer": formatted_answer,
                "raw_answer": answer,
            }
            st.session_state.ai_pending_results.append(pending_result)
            st.session_state.ai_answers.append(
                {"question_id": question.get("id"), "answer": formatted_answer}
            )

            next_index = index + 1
            st.session_state.ai_question_index = next_index
            st.session_state.ai_current_answer = ""

            if next_index >= active_question_count:
                st.session_state.ai_current_question = None
                st.session_state.ai_phase = "ready_for_assessment"
            else:
                session_questions = st.session_state.get("ai_session_questions", [])
                if st.session_state.get("ai_using_question_bank") and session_questions:
                    st.session_state.ai_current_question = session_questions[next_index]
                else:
                    st.session_state.ai_current_question = generate_ai_question(
                        level,
                        domain,
                        st.session_state.ai_pending_results,
                    )
            st.rerun()
