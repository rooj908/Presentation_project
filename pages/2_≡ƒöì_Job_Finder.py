import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.job_database import get_all_jobs, search_jobs
from utils.nlp_utils import calculate_job_match, estimate_salary

st.set_page_config(page_title="Job Finder", page_icon="🔍", layout="wide")

st.markdown("# 🔍 AI Job Finder")
st.markdown("Enter your skills and let AI match you to the best job opportunities.")
st.markdown("---")

# Sidebar Filters 
with st.sidebar:
    st.markdown("### 🎯 Search Filters")

    search_query = st.text_input("🔎 Search jobs", placeholder="e.g., Data Scientist, Python")

    location_filter = st.selectbox(
        "📍 Location",
        ["All", "Karachi", "Lahore", "Islamabad", "Remote"]
    )

    job_type_filter = st.selectbox(
        "💼 Job Type",
        ["All", "Full-time", "Part-time", "Contract", "Internship"]
    )

    experience_filter = st.selectbox(
        "📊 Experience Level",
        ["All", "Fresh Graduate", "1-3 years", "3-5 years", "5+ years"]
    )

    st.markdown("---")
    st.markdown("### 🛠️ Your Skills")
    st.markdown("*Auto-filled from Resume Analyzer*")

    default_skills = st.session_state.get("user_skills", [])
    skills_input = st.text_area(
        "Enter your skills (comma-separated):",
        value=", ".join(default_skills) if default_skills else "",
        height=100,
        placeholder="python, machine learning, sql, django..."
    )

    sort_by = st.selectbox("📋 Sort by", ["Match %", "Date Posted", "Salary"])

search_btn = st.button("🚀 Find Matching Jobs", type="primary", use_container_width=True)

# Job Results
user_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()] if skills_input else []

if search_btn or True:  # Always show jobs
    all_jobs = get_all_jobs()

    # Filter
    filtered_jobs = search_jobs(
        query=search_query,
        skills=user_skills if user_skills else None,
        location=location_filter,
        job_type=job_type_filter
    )

    # Calculate match for each job
    jobs_with_match = []
    for job in filtered_jobs:
        if user_skills:
            match_data = calculate_job_match(
                user_skills,
                job["required_skills"],
                job["preferred_skills"]
            )
        else:
            match_data = {"match_percentage": 0, "grade": "N/A — Add skills",
                          "missing_required": [], "required_matched": [], "preferred_matched": []}
        jobs_with_match.append({**job, "match": match_data})

    # Sort
    if sort_by == "Match %" and user_skills:
        jobs_with_match.sort(key=lambda x: x["match"]["match_percentage"], reverse=True)

    st.markdown(f"### 📋 {len(jobs_with_match)} Jobs Found")

    if not jobs_with_match:
        st.warning("No jobs found. Try adjusting your filters.")
    else:
        for job in jobs_with_match:
            match_pct = job["match"]["match_percentage"]
            grade = job["match"]["grade"]

            # Color based on match
            if match_pct >= 75:
                border_color = "#28a745"
            elif match_pct >= 50:
                border_color = "#ffc107"
            elif match_pct > 0:
                border_color = "#dc3545"
            else:
                border_color = "#6c757d"

            with st.container():
                st.markdown(f"""
                <div style='border-left: 4px solid {border_color}; padding: 0.8rem 1rem;
                            background: white; border-radius: 8px; margin-bottom: 1rem;
                            box-shadow: 0 2px 6px rgba(0,0,0,0.07)'>
                    <div style='display:flex; justify-content:space-between; align-items:flex-start'>
                        <div>
                            <h3 style='margin:0; color:#1a1a2e'>{job['title']}</h3>
                            <p style='margin:0.2rem 0; color:#555'>
                                🏢 {job['company']} &nbsp;|&nbsp;
                                📍 {job['location']} &nbsp;|&nbsp;
                                💼 {job['type']} &nbsp;|&nbsp;
                                🕐 {job['posted']}
                            </p>
                            <p style='margin:0.2rem 0; color:#28a745; font-weight:600'>
                                💰 {job['salary']}
                            </p>
                        </div>
                        <div style='text-align:center; min-width:100px'>
                            <div style='font-size:1.6rem; font-weight:700; color:{border_color}'>
                                {match_pct:.0f}%
                            </div>
                            <div style='font-size:0.75rem; color:#666'>{grade}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"📖 View Details — {job['title']} at {job['company']}"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown("**Job Description:**")
                        st.write(job["description"])

                        st.markdown("**Responsibilities:**")
                        for resp in job["responsibilities"]:
                            st.write(f"• {resp}")

                        st.markdown("**Required Skills:**")
                        req_skills_html = " ".join([
                            f"<span style='background:#667eea; color:white; padding:2px 8px; border-radius:10px; font-size:0.8rem; margin:2px; display:inline-block'>{s}</span>"
                            for s in job["required_skills"]
                        ])
                        st.markdown(req_skills_html, unsafe_allow_html=True)

                        if job["preferred_skills"]:
                            st.markdown("**Preferred Skills:**")
                            pref_html = " ".join([
                                f"<span style='background:#764ba2; color:white; padding:2px 8px; border-radius:10px; font-size:0.8rem; margin:2px; display:inline-block'>{s}</span>"
                                for s in job["preferred_skills"]
                            ])
                            st.markdown(pref_html, unsafe_allow_html=True)

                    with col2:
                        if user_skills:
                            match = job["match"]
                            st.markdown("**Match Analysis:**")
                            st.metric("Match Score", f"{match_pct:.0f}%")

                            if match["required_matched"]:
                                st.markdown("✅ **You have:**")
                                for s in match["required_matched"]:
                                    st.write(f"  ✓ {s}")

                            if match["missing_required"]:
                                st.markdown("❌ **Missing required:**")
                                for s in match["missing_required"]:
                                    st.write(f"  ✗ {s}")

                        # Salary estimate
                        sal = estimate_salary(job["title"], job["experience"], "Pakistan")
                        st.markdown("**💰 Salary Estimate:**")
                        st.write(f"{sal['min']} — {sal['max']}")
                        st.caption(sal['note'])

                    # Action buttons
                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    with btn_col1:
                        st.link_button("🔗 Apply on LinkedIn", job["apply_link"])
                    with btn_col2:
                        if st.button(f"📝 Generate Cover Letter", key=f"cl_{job['id']}"):
                            st.session_state["selected_job"] = job
                            st.info("Go to **Cover Letter Generator** page!")
                    with btn_col3:
                        if st.button(f"📌 Track Application", key=f"track_{job['id']}"):
                            if "tracked_jobs" not in st.session_state:
                                st.session_state["tracked_jobs"] = []
                            if job not in st.session_state["tracked_jobs"]:
                                st.session_state["tracked_jobs"].append({**job, "status": "Applied", "date": "Today"})
                                st.success("Added to tracker!")
                            else:
                                st.info("Already tracked!")
