import streamlit as st

st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .sidebar .sidebar-content {
        background: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 AI-Powered Career Guidance System</h1>
    <p style="font-size:1.1rem; opacity:0.9;">
        Smart Job Recommendations • Resume Analysis • Career Roadmap
    </p>
    <p style="font-size:0.85rem; opacity:0.7;">
        FYP Project — AI & Data Science
    </p>
</div>
""", unsafe_allow_html=True)

# Feature Overview
st.markdown("## 🚀 What This System Does")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2>📄</h2>
        <h4>CV Analysis</h4>
        <p style="font-size:0.85rem">Upload your resume and get instant ATS score & feedback</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2>🔍</h2>
        <h4>Job Matching</h4>
        <p style="font-size:0.85rem">AI matches your profile to relevant job listings</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h2>📚</h2>
        <h4>Skill Roadmap</h4>
        <p style="font-size:0.85rem">Personalized learning path to close skill gaps</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h2>✉️</h2>
        <h4>Cover Letter</h4>
        <p style="font-size:0.85rem">AI-generated cover letters tailored to each job</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Stats
st.markdown("## 📊 System Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jobs in Database", "2,500+", "↑ Updated Daily")
with col2:
    st.metric("Skills Tracked", "500+", "Across all domains")
with col3:
    st.metric("ATS Accuracy", "92%", "Industry standard")
with col4:
    st.metric("Users Helped", "Demo Mode", "Ready to launch")

st.markdown("---")

# Navigation Guide
st.markdown("## 📌 How to Use — Navigate from the Sidebar")

steps = [
    ("1️⃣", "Resume Analyzer", "Upload your CV → Get ATS score, skill extraction & improvement tips"),
    ("2️⃣", "Job Finder", "Enter your skills → AI finds matching jobs with match percentage"),
    ("3️⃣", "Skill Gap Analysis", "Compare your skills vs job requirements → See what's missing"),
    ("4️⃣", "Cover Letter Generator", "Select a job → AI writes a custom cover letter for you"),
    ("5️⃣", "Interview Prep", "Choose job role → Get relevant interview questions & model answers"),
    ("6️⃣", "Career Roadmap", "Set your goal → Get step-by-step learning path with resources"),
    ("7️⃣", "Application Tracker", "Track all your job applications in one place"),
]

for icon, title, desc in steps:
    col1, col2 = st.columns([1, 8])
    with col1:
        st.markdown(f"<h2 style='text-align:center'>{icon}</h2>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"**{title}** — {desc}")

st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; font-size:0.85rem'>
    AI-Powered Intelligent Career Guidance and Job Recommendation System<br>
    Using Resume Analysis and LinkedIn Job Mining<br>
    Built with Python • Streamlit • NLP • Machine Learning
</div>
""", unsafe_allow_html=True)
