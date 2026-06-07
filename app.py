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
    evaluate_ai_answer,
    generate_ai_final_report,
    generate_ai_follow_up,
    generate_ai_question,
    is_adk_configured,
    start_ai_interview,
)


CERTIFICATION_QUESTION_LIMIT = 5
INTERVIEW_QUESTION_LIMIT = 5
AI_MODE = "AI Interview Mode"
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
    "ai_question_index": 0,
    "ai_current_question": None,
    "ai_current_answer": "",
    "ai_current_follow_up": None,
    "ai_history": [],
    "ai_answers": [],
    "ai_evaluations": [],
    "ai_final_report": None,
    "ai_explanations": [],
    "ai_phase": "main_answer",
    "ai_interview": None,
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
        "ai_question_index",
        "ai_current_question",
        "ai_current_answer",
        "ai_current_follow_up",
        "ai_history",
        "ai_answers",
        "ai_evaluations",
        "ai_final_report",
        "ai_explanations",
        "ai_phase",
        "ai_interview",
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
selected_domain = st.selectbox("Select domain", AI_DOMAINS, index=2)

selection_key = f"ai:{selected_level}:{selected_domain}"
if st.session_state.get("selection_key") != selection_key:
    st.session_state.selection_key = selection_key
    reset_session()
    initialize_ai_session_state()

if not st.session_state.get("ai_started"):
    st.write(f"Start a {MAX_QUESTIONS}-question AI interview. Gemini will evaluate each answer as you go.")
    if st.button("Start Interview", disabled=not gemini_ready):
        reset_session()
        initialize_ai_session_state()
        st.session_state.ai_started = True
        st.session_state.ai_complete = False
        st.session_state.ai_level = selected_level
        st.session_state.ai_domain = selected_domain
        st.session_state.ai_interview = start_ai_interview(selected_level, selected_domain)
        st.session_state.ai_current_question = generate_ai_question(selected_level, selected_domain, [])
        st.rerun()

    if not gemini_ready:
        st.info("AI interviews require Gemini. The old local modes remain in the repo but are no longer shown in the main UI.")
elif st.session_state.get("ai_complete"):
    history = st.session_state.get("ai_history", [])
    report = st.session_state.get("ai_final_report")
    if not report:
        report = generate_ai_final_report(history, st.session_state.ai_level, st.session_state.ai_domain)
        st.session_state.ai_final_report = report

    st.subheader("Final Interview Report")
    show_progress("Interview progress", len(history), MAX_QUESTIONS)
    st.metric("Final score", f"{report.get('overall_score', 0)}/100")

    can_move = report.get("can_move_to_next_level") or report.get("ready_for_senior_interviews")
    if can_move:
        st.write("Move to next level")
        st.write(can_move)

    st.write("Strengths")
    for strength in report.get("strengths", []):
        st.write(f"- {strength}")

    st.write("Weak areas")
    for gap in report.get("gaps", []):
        st.write(f"- {gap}")

    concepts = report.get("concepts_to_revise") or report.get("recommended_learning_plan", [])
    st.write("Concepts to revise")
    for concept in concepts:
        st.write(f"- {concept}")

    st.write("Question review")
    for index, item in enumerate(history, start=1):
        evaluation = item.get("evaluation", {})
        question = item.get("question", {})
        with st.expander(f"Question {index}: {question.get('question', '')}", expanded=index == 1):
            if question.get("scenario"):
                st.write(question["scenario"])
            st.write("Your answer")
            st.write(item.get("answer", ""))
            st.write(f"Score: {evaluation.get('score', 0)}/100")
            if evaluation.get("short_feedback"):
                st.write(evaluation["short_feedback"])
            st.write("Explanation")
            st.write(evaluation.get("explanation", ""))
            st.write("Ideal answer")
            st.markdown(evaluation.get("ideal_answer", ""))
            if evaluation.get("missing_points"):
                st.write("Missing points")
                for point in evaluation["missing_points"]:
                    st.write(f"- {point}")

    if report.get("recommended_learning_plan"):
        st.write("Recommended learning plan")
        for item in report["recommended_learning_plan"]:
            st.write(f"- {item}")

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

    show_progress("Question", index + 1, MAX_QUESTIONS)
    st.caption(f"{level} • {domain} • Gemini Flash")

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
    st.write(question.get("question", "No question available."))

    answer = st.text_area("Your answer", key=f"ai_answer_{index}", height=190)
    if st.button("Submit Answer"):
        if not answer.strip():
            st.warning("Please write an answer before submitting.")
        else:
            evaluation = evaluate_ai_answer(question, answer.strip(), level, domain, history)
            if evaluation.get("error"):
                st.error(evaluation["error"])
            else:
                result = {
                    "question": question,
                    "answer": answer.strip(),
                    "evaluation": evaluation,
                }
                st.session_state.ai_history.append(result)
                st.session_state.ai_answers.append(
                    {"question_id": question.get("id"), "answer": answer.strip()}
                )
                st.session_state.ai_evaluations.append(evaluation)
                if evaluation.get("explanation"):
                    st.session_state.ai_explanations.append(evaluation["explanation"])

                next_index = index + 1
                st.session_state.ai_question_index = next_index
                if next_index >= MAX_QUESTIONS:
                    st.session_state.ai_complete = True
                    st.session_state.ai_final_report = generate_ai_final_report(
                        st.session_state.ai_history,
                        level,
                        domain,
                    )
                else:
                    st.session_state.ai_current_question = generate_ai_question(
                        level,
                        domain,
                        st.session_state.ai_history,
                    )
                st.rerun()
