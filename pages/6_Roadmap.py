import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_utils import generate_roadmap
import plotly.graph_objects as go

st.set_page_config(page_title="Career Roadmap", page_icon="🗺️", layout="wide")

st.markdown("# 🗺️ Career Roadmap Generator")
st.markdown("Get a personalized, step-by-step learning path to reach your dream job.")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎯 Your Goal")
    target_roles = [
        "Data Scientist",
        "Machine Learning Engineer",
        "Python Developer",
        "Web Developer (Full Stack)",
        "Data Analyst",
        "DevOps Engineer",
        "NLP Engineer",
        "AI Research Engineer"
    ]
    target_role = st.selectbox("Target Role:", target_roles)
    custom_role = st.text_input("Or enter custom role:", placeholder="e.g., Blockchain Developer")
    final_role = custom_role if custom_role.strip() else target_role

with col2:
    st.markdown("### 📋 Your Current Status")
    experience_level = st.selectbox(
        "Current Level:",
        ["Complete Beginner", "Some Programming Knowledge", "CS Graduate", "Working Professional"]
    )

    default_skills = st.session_state.get("user_skills", [])
    current_skills = st.text_area(
        "Current Skills:",
        value=", ".join(default_skills) if default_skills else "",
        height=80,
        placeholder="python, sql, basic statistics..."
    )

    availability = st.slider("Hours per week available for learning:", 5, 40, 15)

gen_btn = st.button("🚀 Generate My Career Roadmap", type="primary", use_container_width=True)

if gen_btn:
    user_skills = [s.strip() for s in current_skills.split(",") if s.strip()]

    with st.spinner("Building your personalized roadmap..."):
        roadmap = generate_roadmap(final_role, user_skills, experience_level)

    st.markdown("---")
    st.markdown(f"## 🗺️ Roadmap: Become a {final_role}")

    # Timeline estimate
    weeks_per_phase = max(3, round((availability / 15) * 4))
    total_weeks = weeks_per_phase * len(roadmap["phases"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Estimated Duration", roadmap["duration"])
    with col2:
        st.metric("Learning Phases", len(roadmap["phases"]))
    with col3:
        st.metric("At Your Pace", f"~{total_weeks} weeks")

    # Progress tracker
    st.markdown("### 📊 Your Progress")
    completed_phases = st.session_state.get(f"roadmap_progress_{final_role}", [])
    progress_pct = len(completed_phases) / len(roadmap["phases"]) if roadmap["phases"] else 0
    st.progress(progress_pct, text=f"{int(progress_pct*100)}% Complete")

    st.markdown("---")

    # Phases
    for i, phase in enumerate(roadmap["phases"]):
        phase_num = i + 1
        is_completed = phase_num in completed_phases

        status_icon = "✅" if is_completed else ("🔵" if phase_num == min(
            [p for p in range(1, len(roadmap["phases"]) + 1) if p not in completed_phases], default=1
        ) else "⭕")

        with st.expander(f"{status_icon} {phase['phase']}", expanded=(i == 0)):
            col1, col2 = st.columns([1.5, 1])

            with col1:
                st.markdown("**📚 Topics to Learn:**")
                for topic in phase["topics"]:
                    checked = is_completed
                    st.checkbox(topic, value=checked, key=f"topic_{i}_{topic[:20]}")

                st.markdown("**🛠️ Projects to Build:**")
                for project in phase.get("projects", []):
                    st.write(f"  🔨 {project}")

            with col2:
                st.markdown("**🔗 Learning Resources:**")
                for resource in phase.get("resources", []):
                    st.write(f"  📖 {resource}")

                st.markdown(f"**⏱️ Estimated Time:**")
                st.write(f"~{weeks_per_phase} weeks at {availability}hrs/week")

            # Mark complete
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if not is_completed:
                    if st.button(f"✅ Mark Phase {phase_num} Complete", key=f"complete_{i}"):
                        if "roadmap_progress_" + final_role not in st.session_state:
                            st.session_state[f"roadmap_progress_{final_role}"] = []
                        st.session_state[f"roadmap_progress_{final_role}"].append(phase_num)
                        st.rerun()
                else:
                    st.success("Phase completed! 🎉")

    # Timeline Chart
    st.markdown("### 📅 Visual Timeline")

    phases = roadmap["phases"]
    fig = go.Figure()

    colors = ["#667eea", "#764ba2", "#f64f59", "#c471ed"]
    for i, phase in enumerate(phases):
        fig.add_trace(go.Bar(
            name=phase["phase"].split(":")[0],
            x=[weeks_per_phase],
            y=[phase["phase"].split("(")[0].strip()],
            orientation='h',
            marker_color=colors[i % len(colors)],
            text=f"{weeks_per_phase} weeks",
            textposition='inside',
        ))

    fig.update_layout(
        barmode='stack',
        height=200,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title="Weeks", gridcolor='rgba(0,0,0,0.1)'),
        margin=dict(l=180, r=20, t=20, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Key tips
    st.markdown("### 💡 Success Tips")
    tips = [
        "🏗️ **Build in public** — share your projects on GitHub from Day 1",
        "📝 **Document as you go** — write blog posts about what you learn",
        "🤝 **Join communities** — Discord, Reddit r/learnpython, LinkedIn groups",
        "💼 **Start applying early** — don't wait until 'perfect', apply after Phase 2",
        "🏆 **Kaggle competitions** — great for ML practice and portfolio",
        f"📱 **LinkedIn** — update your profile weekly, connect with {final_role}s",
    ]
    for tip in tips:
        st.markdown(tip)
