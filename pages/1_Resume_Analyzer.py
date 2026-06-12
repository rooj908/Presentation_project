import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.nlp_utils import (
    extract_email, extract_phone, extract_skills,
    extract_experience_years, extract_education,
    calculate_ats_score, get_ats_suggestions
)

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.markdown("# 📄 Resume Analyzer")
st.markdown("Upload your CV and get an instant ATS score, skill extraction, and improvement tips.")
st.markdown("---")

# ── Input ──────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Upload or Paste Your Resume")

    upload_method = st.radio("Input method:", ["📋 Paste Text", "📁 Upload .txt file"], horizontal=True)

    resume_text = ""

    if upload_method == "📋 Paste Text":
        resume_text = st.text_area(
            "Paste your resume content here:",
            height=350,
            placeholder="Paste your full resume text here...\n\nInclude: Contact info, Skills, Experience, Education, Projects"
        )
    else:
        uploaded_file = st.file_uploader("Upload resume (.txt)", type=["txt"])
        if uploaded_file:
            resume_text = uploaded_file.read().decode("utf-8", errors="ignore")
            st.success(f"✅ File loaded: {uploaded_file.name} ({len(resume_text)} characters)")
            with st.expander("Preview uploaded text"):
                st.text(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))

    # Sample resume for demo
    if st.button("📝 Load Sample Resume (Demo)"):
        resume_text = """
Ali Hassan
Email: ali.hassan@gmail.com | Phone: +92-300-1234567 | LinkedIn: linkedin.com/in/alihassan | GitHub: github.com/alihassan

OBJECTIVE
Passionate Data Science graduate seeking opportunities to apply machine learning and Python skills to real-world problems.

EDUCATION
Bachelor of Science in Computer Science — FAST-NUCES, Karachi (2020-2024) CGPA: 3.5/4.0
Intermediate (FSc Pre-Engineering) — DJ Science College, Karachi (2018-2020) 85%

SKILLS
Programming: Python, SQL, R, Java
Machine Learning: scikit-learn, TensorFlow, Keras, PyTorch
Data Analysis: Pandas, NumPy, Matplotlib, Seaborn
NLP: SpaCy, NLTK, Transformers, BERT
Tools: Git, GitHub, Jupyter, VS Code, Docker, Tableau
Databases: MySQL, PostgreSQL, MongoDB

EXPERIENCE
Data Science Intern — TechSolutions Pvt Ltd (June 2023 - Sept 2023)
- Developed customer churn prediction model with 87% accuracy using Random Forest
- Analyzed 500K+ records and built Tableau dashboards for management
- Implemented automated data pipeline reducing processing time by 40%
- Collaborated with cross-functional teams to deliver insights

PROJECTS
1. AI Resume Screening System (FYP)
   - Built NLP-based system to match resumes to job descriptions
   - Achieved 91% match accuracy using BERT fine-tuning
   - Technologies: Python, HuggingFace, FastAPI, PostgreSQL

2. Stock Price Prediction
   - Developed LSTM model for stock price forecasting
   - Achieved RMSE of 2.3% on test data
   - Technologies: Python, TensorFlow, Pandas

3. Sentiment Analysis Web App
   - Built real-time sentiment analyzer for Twitter data
   - Deployed on Heroku with Flask REST API
   - Technologies: Python, Flask, SpaCy, Twitter API

CERTIFICATIONS
- Machine Learning Specialization — Coursera (Andrew Ng)
- Data Science Professional Certificate — IBM
- Deep Learning Nanodegree — Udacity

ACHIEVEMENTS
- 1st place, FAST Hackathon 2023 (AI category)
- Dean's List — 4 consecutive semesters
"""
        st.session_state["resume_text"] = resume_text
        st.rerun()

    if "resume_text" in st.session_state and not resume_text:
        resume_text = st.session_state["resume_text"]

analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)

# ── Analysis Output ─────────────────────────────────
if analyze_btn and resume_text.strip():
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")

    with st.spinner("Analyzing your resume..."):
        # Extract data
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        years_exp = extract_experience_years(resume_text)
        education = extract_education(resume_text)
        skills_found = extract_skills(resume_text)
        ats_data = calculate_ats_score(resume_text, skills_found)
        suggestions = get_ats_suggestions(resume_text, skills_found, ats_data)

    # ATS Score & Contact
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        score = ats_data["total"]
        color = "#28a745" if score >= 70 else "#ffc107" if score >= 50 else "#dc3545"
        st.markdown(f"""
        <div style='text-align:center; padding:1.5rem; background:white;
                    border-radius:12px; border: 2px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1)'>
            <h1 style='color:{color}; margin:0; font-size:3rem'>{score}</h1>
            <p style='color:#666; margin:0'>ATS Score / 100</p>
            <p style='color:{color}; font-weight:600; margin:0.5rem 0 0'>{ats_data['grade']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("**📋 Contact Info**")
        st.write(f"📧 Email: `{email}`")
        st.write(f"📱 Phone: `{phone}`")
        st.write(f"🎓 Education: `{', '.join(education) if education else 'Not detected'}`")
        st.write(f"⏱️ Est. Experience: `{years_exp} years`")

    with col3:
        st.markdown("**📈 Score Breakdown**")
        breakdown = ats_data["breakdown"]
        for key, val in breakdown.items():
            max_val = {"skills_count": 30, "contact_info": 15, "education": 15,
                       "experience_keywords": 20, "resume_length": 10, "formatting_keywords": 10}.get(key, 10)
            label = key.replace("_", " ").title()
            st.write(f"{label}: **{val}/{max_val}**")
            st.progress(val / max_val)

    # Skills
    st.markdown("### 🛠️ Skills Detected")
    if skills_found:
        for category, skills in skills_found.items():
            cat_label = category.replace("_", " ").title()
            st.markdown(f"**{cat_label}:**")
            cols = st.columns(min(len(skills), 6))
            for i, skill in enumerate(skills):
                with cols[i % 6]:
                    st.markdown(f"""<span style='background:#667eea; color:white;
                        padding:3px 10px; border-radius:12px; font-size:0.8rem;
                        display:inline-block; margin:2px'>{skill}</span>""",
                        unsafe_allow_html=True)
            st.write("")
    else:
        st.warning("No skills detected. Make sure your resume contains recognizable skill names.")

    # Save to session
    all_skills = []
    for skills in skills_found.values():
        all_skills.extend(skills)
    st.session_state["user_skills"] = all_skills
    st.session_state["resume_analyzed"] = True

    # Suggestions
    st.markdown("### 💡 Improvement Suggestions")
    for suggestion in suggestions:
        st.info(suggestion)

    st.success("✅ Resume analyzed! Go to **Job Finder** to find matching jobs.")

elif analyze_btn:
    st.warning("⚠️ Please paste your resume text or upload a file first.")
