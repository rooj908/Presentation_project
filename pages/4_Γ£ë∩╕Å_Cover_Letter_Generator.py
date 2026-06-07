import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_utils import generate_cover_letter
from utils.job_database import get_all_jobs

st.set_page_config(page_title="Cover Letter Generator", page_icon="✉️", layout="wide")

st.markdown("# ✉️ AI Cover Letter Generator")
st.markdown("Generate a tailored, professional cover letter for any job in seconds.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 👤 Your Information")
    name = st.text_input("Full Name", placeholder="Ali Hassan")
    experience_level = st.selectbox(
        "Experience Level",
        ["Fresh Graduate", "Junior (1-2 years)", "Mid-level (2-5 years)", "Senior (5+ years)"]
    )

    default_skills = st.session_state.get("user_skills", [])
    skills_input = st.text_area(
        "Your Key Skills:",
        value=", ".join(default_skills[:10]) if default_skills else "",
        height=80,
        placeholder="python, machine learning, deep learning, sql..."
    )

    tone = st.selectbox("Letter Tone", ["Professional", "Enthusiastic", "Concise", "Creative"])

with col2:
    st.markdown("### 💼 Target Job")
    input_method = st.radio("Job source:", ["Select from database", "Enter manually"], horizontal=True)

    if input_method == "Select from database":
        all_jobs = get_all_jobs()
        # Check if job pre-selected
        selected_from_finder = st.session_state.get("selected_job")
        job_titles = [f"{j['title']} — {j['company']}" for j in all_jobs]
        default_idx = 0
        if selected_from_finder:
            for i, j in enumerate(all_jobs):
                if j["id"] == selected_from_finder.get("id"):
                    default_idx = i
                    break

        selected_label = st.selectbox("Choose a job:", job_titles, index=default_idx)
        selected_job = all_jobs[job_titles.index(selected_label)]
        job_title = selected_job["title"]
        company = selected_job["company"]
        job_desc = selected_job["description"]

        st.info(f"📍 {selected_job['location']} | 💼 {selected_job['type']}")
    else:
        job_title = st.text_input("Job Title", placeholder="Data Scientist")
        company = st.text_input("Company Name", placeholder="TechCorp Solutions")
        job_desc = st.text_area("Job Description (optional):", height=80,
                                placeholder="Paste job description for better tailoring...")

generate_btn = st.button("✍️ Generate Cover Letter", type="primary", use_container_width=True)

if generate_btn:
    if not name.strip():
        st.warning("Please enter your name.")
        st.stop()
    if not job_title.strip():
        st.warning("Please enter a job title.")
        st.stop()

    user_skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    with st.spinner("🤖 AI is writing your cover letter..."):
        letter = generate_cover_letter(
            name=name,
            job_title=job_title,
            company=company,
            user_skills=user_skills,
            experience_level=experience_level,
            job_description=job_desc
        )

    st.markdown("---")
    st.markdown("### 📄 Your Generated Cover Letter")

    # Display
    st.markdown(f"""
    <div style='background:white; border:1px solid #dee2e6; border-radius:10px;
                padding:2rem; font-family: Georgia, serif; line-height:1.8;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08)'>
        <p style='color:#999; font-size:0.85rem; margin-bottom:1rem'>
            {name} | {experience_level}<br>
            Applying for: {job_title} at {company}
        </p>
        <hr style='border-color:#eee'>
        <div style='margin-top:1rem; color:#333; white-space:pre-line'>{letter}</div>
    </div>
    """, unsafe_allow_html=True)

    # Edit & Copy
    st.markdown("### ✏️ Edit Your Letter")
    edited_letter = st.text_area("Edit if needed:", value=letter, height=300)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ Download as .txt",
            data=f"Cover Letter\n{'='*40}\n\nApplying for: {job_title} at {company}\n\n{edited_letter}",
            file_name=f"cover_letter_{company.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        if st.button("🔄 Regenerate Letter", use_container_width=True):
            st.rerun()

    st.success("✅ Cover letter generated! Remember to personalize it further before sending.")
    st.info("💡 **Tip:** Add specific achievements with numbers (e.g., 'improved accuracy by 15%') to make it stronger.")
