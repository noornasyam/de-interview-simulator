import streamlit as st

from app.config.levels import LEVELS
from app.config.platforms import PLATFORMS
from app.services.certification_engine import (
    evaluate_question,
    load_questions,
    load_taxonomy_questions,
    select_random_questions,
)


CERTIFICATION_QUESTION_LIMIT = 5
INTERVIEW_QUESTION_LIMIT = 5
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
    page_title="Data Engineering Career Accelerator",
    page_icon="🎯",
    layout="centered",
)

st.title("🎯 Data Engineering Career Accelerator")

mode = st.selectbox("Select mode", ["Learning Mode", "Exam Mode", "Interview Mode"])

if mode == "Interview Mode":
    role = st.selectbox("Select role", list(ROLE_LEVELS.keys()))
    interview_domain = st.selectbox("Select domain", INTERVIEW_DOMAINS)
    platform = "taxonomy"
    level = ROLE_LEVELS[role]
    st.caption("MVP interview content currently uses Senior-level banks for every role selection.")
else:
    role = None
    interview_domain = None
    platform = st.selectbox("Select cloud platform", PLATFORMS)
    level = st.selectbox("Select level", LEVELS)

if mode == "Exam Mode":
    explanation_mode = "At the end only"
    st.caption("Exam Mode shows explanations at the end only.")
else:
    default_explanation_mode = (
        "After each question" if mode == "Learning Mode" else "At the end only"
    )
    explanation_mode = st.radio(
        "Show explanation",
        ["After each question", "At the end only"],
        index=0 if default_explanation_mode == "After each question" else 1,
        horizontal=True,
    )

selection_key = f"{mode}:{platform}:{level}:{role}:{interview_domain}:{explanation_mode}"
if st.session_state.get("selection_key") != selection_key:
    st.session_state.selection_key = selection_key
    reset_session()


if mode in {"Learning Mode", "Exam Mode"}:
    st.subheader(mode)

    if "session_questions" not in st.session_state:
        if st.button("Start"):
            start_question_session(platform, level)
            st.rerun()
    else:
        questions = st.session_state.session_questions
        index = st.session_state.session_index
        results = st.session_state.session_results

        if not questions:
            st.warning("No certification questions available yet for this platform and level.")
        elif index < len(questions):
            question = questions[index]
            st.write(f"Question {index + 1} of {len(questions)}")

            if mode == "Learning Mode" and st.session_state.get("waiting_for_next_question"):
                if question.get("scenario"):
                    st.write(question["scenario"])
                st.write(question["question"])

                st.divider()
                show_learning_evaluation(question, results[-1]["evaluation"])

                if st.button("Continue to Next Question"):
                    st.session_state.session_index += 1
                    st.session_state.question_answered = False
                    st.session_state.explanation_shown = False
                    st.session_state.waiting_for_next_question = False
                    st.rerun()
            else:
                answer = show_question_input(question, "cert")

                if st.button("Submit Answer"):
                    if answer is None:
                        st.warning("This question is missing answer options and cannot be submitted.")
                        st.stop()

                    if question.get("type") == "fill_blank" and not str(answer).strip():
                        st.warning("Please enter an answer before submitting.")
                        st.stop()

                    result = evaluate_question(question, answer)
                    results.append(
                        {
                            "question": question,
                            "answer": answer,
                            "evaluation": result,
                        }
                    )

                    if result["is_correct"]:
                        st.session_state.session_score += 1

                    if mode == "Learning Mode":
                        st.session_state.question_answered = True
                        st.session_state.explanation_shown = True
                        st.session_state.waiting_for_next_question = True
                    else:
                        st.session_state.session_index += 1

                    st.rerun()

        else:
            st.subheader("Final Result")
            st.write(f"Score: {st.session_state.session_score}/{len(questions)}")

            percentage = (st.session_state.session_score / len(questions)) * 100
            st.write(f"Percentage: {percentage:.2f}%")

            st.divider()
            st.write("Review")
            for result in results:
                st.write(result["question"]["question"])
                show_basic_evaluation(result["evaluation"])

            report = build_text_report(platform, level, mode, results)
            st.download_button(
                "Download text report",
                data=report,
                file_name=f"{mode.lower().replace(' ', '_')}_report.txt",
                mime="text/plain",
            )

            if st.button("Restart"):
                reset_session()
                st.rerun()

else:
    st.subheader("Interview Mode")
    st.caption(f"{role} • {interview_domain} • {level}")

    if "interview_questions" not in st.session_state:
        st.write("You will answer 5 senior-style interview questions one at a time.")
        st.write("After each answer, you will see rubric feedback before continuing.")
        if st.button("Start Interview"):
            start_interview(interview_domain, level)
            st.rerun()
    elif st.session_state.interview_complete:
        history = st.session_state.interview_history

        if not history:
            st.warning("No interview questions available yet for this role and domain.")
        else:
            show_progress("Interview progress", len(history), len(st.session_state.interview_questions))
            show_final_interview_report(history)

            st.divider()
            st.write("Question-by-question breakdown")
            for result_index, result in enumerate(history, start=1):
                question = result["question"]
                st.write(f"Question {result_index}")
                st.caption(
                    f"{question.get('domain', 'unknown')} • "
                    f"{question.get('category', 'unknown')} • "
                    f"Difficulty {question.get('difficulty', 'n/a')}"
                )
                st.write(question["question"])
                show_interview_evaluation(result, key_suffix=f"review_{result_index}")
                st.divider()

            report = build_text_report(interview_domain, level, mode, history)
            st.download_button(
                "Download text report",
                data=report,
                file_name="interview_report.txt",
                mime="text/plain",
            )

        if st.button("Restart Interview"):
            reset_session()
            st.rerun()
    else:
        questions = st.session_state.interview_questions
        index = st.session_state.interview_index
        history = st.session_state.interview_history

        if index >= len(questions):
            st.session_state.interview_complete = True
            st.rerun()

        question = questions[index]
        show_progress("Question", index + 1, len(questions))
        st.caption(
            f"{question.get('domain', 'unknown')} • "
            f"{question.get('category', 'unknown')} • "
            f"Difficulty {question.get('difficulty', 'n/a')}"
        )

        if st.session_state.get("interview_waiting_for_next"):
            st.write("Current question")
            if question.get("scenario"):
                st.write(question["scenario"])
            st.write(question["question"])
            st.divider()
            st.write("Evaluation")
            show_interview_evaluation(history[-1], key_suffix="active")

            button_label = (
                "Finish Interview"
                if index + 1 >= len(questions)
                else "Continue to Next Question"
            )
            if st.button(button_label):
                st.session_state.interview_index += 1
                st.session_state.interview_waiting_for_next = False
                if st.session_state.interview_index >= len(questions):
                    st.session_state.interview_complete = True
                st.rerun()
        else:
            st.write("Question")
            answer = show_question_input(question, "interview")

            if st.button("Submit Answer"):
                if not answer.strip():
                    st.warning("Please write an answer before submitting.")
                else:
                    result = {
                        "question": question,
                        "answer": answer.strip(),
                        "evaluation": evaluate_question(question, answer.strip()),
                    }
                    history.append(result)
                    st.session_state.interview_waiting_for_next = True
                    st.rerun()
