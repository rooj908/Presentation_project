import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.nlp_utils import calculate_job_match
from utils.job_database import get_all_jobs
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Skill Gap Analysis", page_icon="📊", layout="wide")

st.markdown("# 📊 Skill Gap Analysis")
st.markdown("Compare your current skills against job requirements to identify what you need to learn.")
st.markdown("---")

# ── Input ──────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Your Current Skills")
    default_skills = st.session_state.get("user_skills", [])
    user_skills_input = st.text_area(
        "Enter your skills (comma-separated):",
        value=", ".join(default_skills) if default_skills else "",
        height=120,
        placeholder="python, machine learning, sql, pandas..."
    )

with col2:
    st.markdown("### Target Job Role")
    all_jobs = get_all_jobs()
    job_titles = [f"{j['title']} — {j['company']}" for j in all_jobs]
    selected_job_label = st.selectbox("Select a job to analyze:", job_titles)

    target_job = all_jobs[job_titles.index(selected_job_label)]

    st.info(f"**Experience required:** {target_job['experience']}\n\n**Location:** {target_job['location']}")

analyze_btn = st.button("🔍 Analyze Skill Gap", type="primary", use_container_width=True)

# ── Results ─────────────────────────────────────────
if analyze_btn:
    user_skills = [s.strip().lower() for s in user_skills_input.split(",") if s.strip()]

    if not user_skills:
        st.warning("Please enter your skills first.")
        st.stop()

    match_data = calculate_job_match(
        user_skills,
        target_job["required_skills"],
        target_job["preferred_skills"]
    )

    st.markdown("---")
    st.markdown(f"## Analysis: {target_job['title']} at {target_job['company']}")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Match Score", f"{match_data['match_percentage']}%", match_data['grade'])
    with col2:
        st.metric("Required Skills Matched", f"{len(match_data['required_matched'])}/{len(target_job['required_skills'])}")
    with col3:
        st.metric("Missing Required Skills", len(match_data['missing_required']))
    with col4:
        st.metric("Preferred Skills Matched", f"{len(match_data['preferred_matched'])}/{len(target_job['preferred_skills'])}")

    # Radar Chart
    st.markdown("### 🕸️ Skills Coverage Radar")

    all_required = target_job["required_skills"]
    user_lower = [s.lower() for s in user_skills]
    radar_labels = all_required
    radar_values = [1 if skill in user_lower else 0 for skill in radar_labels]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_values + [radar_values[0]],
        theta=radar_labels + [radar_labels[0]],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=2),
        name='Your Skills'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=[1] * (len(radar_labels) + 1),
        theta=radar_labels + [radar_labels[0]],
        fill='toself',
        fillcolor='rgba(220, 53, 69, 0.1)',
        line=dict(color='#dc3545', width=1, dash='dash'),
        name='Job Requirements'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=False, range=[0, 1])),
        showlegend=True,
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Skill breakdown columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ Skills You Have")
        if match_data["required_matched"]:
            for skill in match_data["required_matched"]:
                st.markdown(f"""<div style='background:#d4edda; color:#155724;
                    padding:6px 12px; border-radius:20px; margin:4px 0;
                    font-size:0.9rem'>✓ {skill}</div>""", unsafe_allow_html=True)
        else:
            st.warning("No required skills matched yet.")

        if match_data["preferred_matched"]:
            st.markdown("**Bonus preferred skills:**")
            for skill in match_data["preferred_matched"]:
                st.markdown(f"""<div style='background:#cce5ff; color:#004085;
                    padding:6px 12px; border-radius:20px; margin:4px 0;
                    font-size:0.9rem'>⭐ {skill}</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("### ❌ Skills to Learn (Required)")
        if match_data["missing_required"]:
            for skill in match_data["missing_required"]:
                st.markdown(f"""<div style='background:#f8d7da; color:#721c24;
                    padding:6px 12px; border-radius:20px; margin:4px 0;
                    font-size:0.9rem'>✗ {skill}</div>""", unsafe_allow_html=True)
        else:
            st.success("🎉 You have all required skills!")

    with col3:
        st.markdown("### 📚 Learning Recommendations")
        if match_data["missing_required"]:
            st.markdown("**Priority learning list:**")
            resources = {
                "python": "🔗 [Python.org](https://python.org) | [Real Python](https://realpython.com)",
                "machine learning": "🔗 [Coursera — Andrew Ng](https://coursera.org)",
                "sql": "🔗 [SQLZoo](https://sqlzoo.net) | [Mode SQL](https://mode.com/sql-tutorial)",
                "docker": "🔗 [Docker Docs](https://docs.docker.com)",
                "aws": "🔗 [AWS Free Tier](https://aws.amazon.com/free)",
                "react": "🔗 [React Docs](https://react.dev)",
                "django": "🔗 [Django Docs](https://djangoproject.com)",
                "tensorflow": "🔗 [TF Tutorials](https://tensorflow.org/tutorials)",
                "pytorch": "🔗 [PyTorch Tutorials](https://pytorch.org/tutorials)",
                "deep learning": "🔗 [fast.ai](https://fast.ai)",
            }
            for skill in match_data["missing_required"]:
                resource = resources.get(skill.lower(), f"🔗 [Search on Coursera](https://coursera.org/search?query={skill.replace(' ', '+')})")
                st.markdown(f"**{skill.title()}:** {resource}")
        else:
            st.success("You're qualified! Work on preferred skills next.")
            for skill in match_data.get("missing_preferred", [])[:5]:
                st.markdown(f"➕ Consider learning: **{skill}**")

    # Bar chart — skill match summary
    st.markdown("### 📊 Skills Match Overview")
    categories = ["Required Skills", "Preferred Skills"]
    matched = [len(match_data["required_matched"]), len(match_data["preferred_matched"])]
    missing = [len(match_data["missing_required"]), len(target_job["preferred_skills"]) - len(match_data["preferred_matched"])]

    fig_bar = go.Figure(data=[
        go.Bar(name="✅ Matched", x=categories, y=matched, marker_color="#28a745"),
        go.Bar(name="❌ Missing", x=categories, y=missing, marker_color="#dc3545")
    ])
    fig_bar.update_layout(
        barmode='group', height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)')
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # CTA
    if match_data["missing_required"]:
        st.info(f"📚 Go to **Career Roadmap** page to get a detailed learning plan for these skills!")
