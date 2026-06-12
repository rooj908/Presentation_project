import streamlit as st
import sys, os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Application Tracker", page_icon="📌", layout="wide")

st.markdown("# 📌 Application Tracker")
st.markdown("Track all your job applications in one place — never lose track again.")
st.markdown("---")

# Initialize tracker
if "tracked_jobs" not in st.session_state:
    st.session_state["tracked_jobs"] = []

# ── Add Application Manually ─────────────────────────
with st.expander("➕ Add New Application", expanded=len(st.session_state["tracked_jobs"]) == 0):
    col1, col2, col3 = st.columns(3)
    with col1:
        new_title = st.text_input("Job Title*", placeholder="Data Scientist")
        new_company = st.text_input("Company*", placeholder="TechCorp")
    with col2:
        new_location = st.text_input("Location", placeholder="Karachi, Pakistan")
        new_salary = st.text_input("Salary Range", placeholder="PKR 80,000-120,000")
    with col3:
        new_status = st.selectbox("Status", ["Applied", "In Review", "Interview Scheduled",
                                              "Technical Test", "HR Round", "Offer Received",
                                              "Rejected", "Withdrawn"])
        new_date = st.date_input("Applied Date", datetime.today())

    new_notes = st.text_area("Notes:", placeholder="Key skills required, interview notes...", height=60)
    new_link = st.text_input("Job Link:", placeholder="https://linkedin.com/jobs/...")

    if st.button("➕ Add to Tracker", type="primary"):
        if new_title and new_company:
            entry = {
                "title": new_title,
                "company": new_company,
                "location": new_location or "N/A",
                "salary": new_salary or "N/A",
                "status": new_status,
                "date": str(new_date),
                "notes": new_notes,
                "link": new_link,
                "id": len(st.session_state["tracked_jobs"])
            }
            st.session_state["tracked_jobs"].append(entry)
            st.success(f"✅ Added: {new_title} at {new_company}")
            st.rerun()
        else:
            st.warning("Job Title and Company are required.")

# ── Load sample data ─────────────────────────────────
if st.button("📥 Load Sample Data (Demo)") and not st.session_state["tracked_jobs"]:
    sample = [
        {"id": 0, "title": "Data Scientist", "company": "TechCorp Solutions",
         "location": "Karachi", "salary": "PKR 90,000", "status": "Interview Scheduled",
         "date": "2024-01-10", "notes": "Good culture, strong ML team", "link": "#"},
        {"id": 1, "title": "ML Engineer", "company": "AI Startup Hub",
         "location": "Islamabad", "salary": "PKR 120,000", "status": "Applied",
         "date": "2024-01-12", "notes": "Requires PyTorch experience", "link": "#"},
        {"id": 2, "title": "Python Developer", "company": "Digital Ventures",
         "location": "Lahore", "salary": "PKR 85,000", "status": "Technical Test",
         "date": "2024-01-08", "notes": "Django + REST API focus", "link": "#"},
        {"id": 3, "title": "Data Analyst", "company": "Analytics Pro",
         "location": "Remote", "salary": "PKR 70,000", "status": "Rejected",
         "date": "2024-01-05", "notes": "Need more SQL practice", "link": "#"},
    ]
    st.session_state["tracked_jobs"] = sample
    st.rerun()

# ── Stats ─────────────────────────────────────────────
apps = st.session_state["tracked_jobs"]

if apps:
    status_counts = {}
    for app in apps:
        status_counts[app["status"]] = status_counts.get(app["status"], 0) + 1

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Applications", len(apps))
    with col2:
        st.metric("In Progress", sum(1 for a in apps if a["status"] not in ["Offer Received", "Rejected", "Withdrawn"]))
    with col3:
        st.metric("Interviews", sum(1 for a in apps if "Interview" in a["status"] or "HR" in a["status"]))
    with col4:
        st.metric("Offers", sum(1 for a in apps if a["status"] == "Offer Received"))
    with col5:
        st.metric("Rejected", sum(1 for a in apps if a["status"] == "Rejected"))

    st.markdown("---")

    # Filter & sort
    col1, col2 = st.columns([1, 2])
    with col1:
        filter_status = st.selectbox("Filter by Status:", ["All"] + list(set(a["status"] for a in apps)))
    with col2:
        search_company = st.text_input("Search by Company/Title:", placeholder="TechCorp...")

    filtered = apps
    if filter_status != "All":
        filtered = [a for a in filtered if a["status"] == filter_status]
    if search_company:
        filtered = [a for a in filtered if
                    search_company.lower() in a["company"].lower() or
                    search_company.lower() in a["title"].lower()]

    st.markdown(f"### 📋 Applications ({len(filtered)} shown)")

    # Display cards
    STATUS_COLORS = {
        "Applied": "#6c757d",
        "In Review": "#17a2b8",
        "Interview Scheduled": "#007bff",
        "Technical Test": "#fd7e14",
        "HR Round": "#6610f2",
        "Offer Received": "#28a745",
        "Rejected": "#dc3545",
        "Withdrawn": "#adb5bd"
    }

    for idx, app in enumerate(filtered):
        status_color = STATUS_COLORS.get(app["status"], "#6c757d")

        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            <div style='border-left:4px solid {status_color}; padding:0.8rem 1rem;
                        background:white; border-radius:8px; margin-bottom:0.8rem;
                        box-shadow: 0 1px 4px rgba(0,0,0,0.07)'>
                <div style='display:flex; justify-content:space-between; align-items:center'>
                    <div>
                        <strong style='font-size:1rem'>{app['title']}</strong>
                        <span style='color:#666; margin-left:0.5rem'>@ {app['company']}</span>
                    </div>
                    <span style='background:{status_color}; color:white; padding:3px 10px;
                                border-radius:12px; font-size:0.8rem'>{app['status']}</span>
                </div>
                <p style='color:#888; font-size:0.85rem; margin:0.3rem 0 0'>
                    📍 {app['location']} &nbsp;|&nbsp; 💰 {app['salary']} &nbsp;|&nbsp; 📅 {app['date']}
                    {'&nbsp;|&nbsp; 📝 ' + app['notes'][:50] + '...' if app.get('notes') else ''}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            new_status = st.selectbox(
                "Update",
                list(STATUS_COLORS.keys()),
                index=list(STATUS_COLORS.keys()).index(app["status"]) if app["status"] in STATUS_COLORS else 0,
                key=f"status_{idx}_{app.get('id', idx)}",
                label_visibility="collapsed"
            )
            if new_status != app["status"]:
                # Find and update in full list
                for a in st.session_state["tracked_jobs"]:
                    if a.get("id") == app.get("id") and a["title"] == app["title"]:
                        a["status"] = new_status
                st.rerun()

    # Delete all option
    st.markdown("---")
    if st.button("🗑️ Clear All Applications", help="Remove all tracked applications"):
        st.session_state["tracked_jobs"] = []
        st.rerun()

    # Export
    if apps:
        import json
        export_data = json.dumps(apps, indent=2)
        st.download_button(
            "⬇️ Export as JSON",
            data=export_data,
            file_name="job_applications.json",
            mime="application/json"
        )

else:
    st.info("📭 No applications tracked yet. Add your first application above or load sample data!")
    st.markdown("""
    **How to use:**
    1. Apply to jobs from the **Job Finder** page — they auto-add here
    2. Or manually add any job you've applied to
    3. Update status as your application progresses
    4. Never lose track of where you applied!
    """)
