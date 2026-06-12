import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_utils import generate_interview_questions
from utils.job_database import get_all_jobs

st.set_page_config(page_title="Interview Prep", page_icon="🎤", layout="wide")

st.markdown("# 🎤 Interview Preparation")
st.markdown("Get role-specific interview questions with model answers to ace your interviews.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎯 Setup")
    all_jobs = get_all_jobs()
    job_titles = ["Custom Role"] + [f"{j['title']} — {j['company']}" for j in all_jobs]
    selected_label = st.selectbox("Select job role:", job_titles)

    if selected_label == "Custom Role":
        job_title_input = st.text_input("Enter job title:", placeholder="Data Scientist")
        exp_level = st.selectbox("Experience Level:", ["Fresh Graduate", "Mid-level", "Senior"])
        selected_skills = []
    else:
        selected_job = all_jobs[job_titles.index(selected_label) - 1]
        job_title_input = selected_job["title"]
        exp_level = selected_job["experience"]
        selected_skills = selected_job["required_skills"]
        st.info(f"📍 {selected_job['location']} | {selected_job['type']}")

with col2:
    st.markdown("### 🛠️ Focus Skills")
    default_skills = st.session_state.get("user_skills", selected_skills)
    skills_input = st.text_area(
        "Skills to focus on:",
        value=", ".join(default_skills[:8]) if default_skills else "",
        height=80
    )

    interview_type = st.multiselect(
        "Question types:",
        ["Technical", "Behavioral", "Problem Solving", "HR/General"],
        default=["Technical", "HR/General"]
    )

    difficulty = st.select_slider("Difficulty:", ["Easy", "Medium", "Hard"], value="Medium")

gen_btn = st.button("🎯 Generate Interview Questions", type="primary", use_container_width=True)

if gen_btn:
    job_title = job_title_input if selected_label == "Custom Role" else selected_job["title"]
    if not job_title:
        st.warning("Please select or enter a job role.")
        st.stop()

    user_skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    with st.spinner("Generating interview questions..."):
        questions = generate_interview_questions(job_title, user_skills, exp_level)

    st.markdown("---")
    st.markdown(f"## 📝 Interview Questions — {job_title}")
    st.markdown(f"*{len(questions)} questions | {difficulty} difficulty | {exp_level}*")

    # Practice mode toggle
    practice_mode = st.toggle("🎯 Practice Mode (hide answers first)", value=False)

    for i, q in enumerate(questions, 1):
        with st.expander(f"Q{i}: {q['question']}", expanded=(i == 1)):
            if practice_mode:
                st.markdown("*Think about your answer first...*")
                if st.button(f"💡 Show Answer Hint", key=f"ans_{i}"):
                    st.info(f"**Answer hint:** {q['answer_hint']}")
            else:
                st.info(f"**Answer hint:** {q['answer_hint']}")

            # Self-rating
            rating = st.select_slider(
                "How confident are you with this question?",
                options=["Not at all", "Somewhat", "Confident", "Very confident"],
                key=f"rating_{i}"
            )

            if rating in ["Not at all", "Somewhat"]:
                st.warning("💡 Practice this question — add it to your study list!")

    st.markdown("---")

    # STAR Method guide
    with st.expander("📚 STAR Method — Answer Framework"):
        st.markdown("""
        Use **STAR** for behavioral questions:

        - **S — Situation:** Set the context. What was happening?
        - **T — Task:** What was your responsibility?
        - **A — Action:** What did YOU specifically do?
        - **R — Result:** What was the outcome? (Quantify if possible)

        **Example:** "Tell me about a challenging project."

        > *"In my internship (S), I was tasked with building a churn prediction model (T).
        > I researched several algorithms, chose Random Forest, and tuned hyperparameters (A).
        > The final model achieved 87% accuracy, saving the company an estimated 15% in retention costs (R)."*
        """)

    # Tips
    with st.expander("🌟 General Interview Tips"):
        tips = [
            "Research the company thoroughly — know their products, tech stack, culture",
            "Prepare 3-4 questions to ask the interviewer — shows genuine interest",
            "Practice coding problems on LeetCode/HackerRank for technical roles",
            "Have your GitHub/portfolio ready with polished projects",
            "Arrive 10 minutes early (or log in 5 mins early for virtual)",
            "Follow up with a thank-you email within 24 hours",
            "Use the STAR method for behavioral questions",
            "Be specific — use numbers and metrics when describing achievements"
        ]
        for tip in tips:
            st.write(f"✅ {tip}")

    st.success("Good luck with your interview! Remember to practice out loud! 🎯")
