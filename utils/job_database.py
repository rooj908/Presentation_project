"""
Job Database — Sample job listings for demo/testing
In production, this would be replaced by LinkedIn scraper data.
"""

JOBS_DATABASE = [
    {
        "id": 1,
        "title": "Data Scientist",
        "company": "TechCorp Solutions",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "experience": "0-2 years",
        "posted": "2 days ago",
        "salary": "PKR 80,000 - 120,000/month",
        "description": "We are looking for a talented Data Scientist to join our growing team. You will work on exciting ML projects and help drive data-driven decisions.",
        "required_skills": ["python", "machine learning", "pandas", "numpy", "sql", "data analysis"],
        "preferred_skills": ["tensorflow", "deep learning", "tableau", "aws"],
        "responsibilities": [
            "Build and deploy ML models",
            "Analyze large datasets to extract insights",
            "Create data visualizations and dashboards",
            "Collaborate with engineering teams"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 2,
        "title": "Python Developer",
        "company": "Digital Ventures",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "experience": "1-3 years",
        "posted": "1 day ago",
        "salary": "PKR 70,000 - 100,000/month",
        "description": "Join our backend team to build scalable Python applications. You'll work on RESTful APIs, database optimization, and cloud deployments.",
        "required_skills": ["python", "django", "rest api", "postgresql", "git"],
        "preferred_skills": ["docker", "aws", "redis", "celery"],
        "responsibilities": [
            "Develop and maintain Django/FastAPI applications",
            "Design and optimize database schemas",
            "Write clean, testable code",
            "Code review and mentoring juniors"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 3,
        "title": "Machine Learning Engineer",
        "company": "AI Startup Hub",
        "location": "Islamabad, Pakistan",
        "type": "Full-time",
        "experience": "2-4 years",
        "posted": "3 days ago",
        "salary": "PKR 100,000 - 160,000/month",
        "description": "Build production-grade ML systems from research to deployment. Work with state-of-the-art models including transformers and LLMs.",
        "required_skills": ["python", "pytorch", "tensorflow", "machine learning", "deep learning", "docker"],
        "preferred_skills": ["kubernetes", "aws", "mlflow", "transformers", "bert"],
        "responsibilities": [
            "Design ML pipelines end-to-end",
            "Fine-tune and deploy LLMs",
            "Optimize model performance",
            "Monitor model drift in production"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 4,
        "title": "Full Stack Web Developer",
        "company": "WebSolutions Pvt Ltd",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "experience": "1-3 years",
        "posted": "Today",
        "salary": "PKR 60,000 - 90,000/month",
        "description": "Build end-to-end web applications using React and Node.js. Work in an agile team delivering quality products.",
        "required_skills": ["javascript", "react", "node.js", "html", "css", "sql"],
        "preferred_skills": ["typescript", "mongodb", "docker", "aws"],
        "responsibilities": [
            "Develop responsive React frontends",
            "Build RESTful APIs with Node.js",
            "Manage databases and deployments",
            "Participate in sprint planning"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 5,
        "title": "Data Analyst",
        "company": "Analytics Pro",
        "location": "Remote (Pakistan)",
        "type": "Full-time",
        "experience": "0-2 years",
        "posted": "5 days ago",
        "salary": "PKR 55,000 - 85,000/month",
        "description": "Analyze business data and create insightful reports and dashboards. Help stakeholders make data-driven decisions.",
        "required_skills": ["python", "sql", "excel", "data analysis", "data visualization"],
        "preferred_skills": ["tableau", "power bi", "pandas", "statistics"],
        "responsibilities": [
            "Collect, clean and analyze data",
            "Build dashboards in Tableau/Power BI",
            "Present findings to management",
            "Automate reporting pipelines"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 6,
        "title": "NLP / AI Engineer",
        "company": "FinTech Innovations",
        "location": "Lahore, Pakistan",
        "type": "Full-time",
        "experience": "1-3 years",
        "posted": "4 days ago",
        "salary": "PKR 90,000 - 140,000/month",
        "description": "Work on cutting-edge NLP systems for financial document processing, chatbots, and text analytics.",
        "required_skills": ["python", "nlp", "transformers", "bert", "scikit-learn", "sql"],
        "preferred_skills": ["pytorch", "spacy", "fastapi", "docker", "gpt"],
        "responsibilities": [
            "Build NLP pipelines for text classification",
            "Fine-tune transformer models",
            "Deploy AI microservices",
            "Research new NLP techniques"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 7,
        "title": "Cloud DevOps Engineer",
        "company": "CloudBase Systems",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "experience": "2-5 years",
        "posted": "1 week ago",
        "salary": "PKR 110,000 - 170,000/month",
        "description": "Manage our cloud infrastructure on AWS. Implement CI/CD pipelines and ensure high availability of production systems.",
        "required_skills": ["aws", "docker", "kubernetes", "linux", "ci/cd", "git"],
        "preferred_skills": ["terraform", "ansible", "python", "jenkins", "monitoring"],
        "responsibilities": [
            "Maintain AWS infrastructure",
            "Build and optimize CI/CD pipelines",
            "Implement security best practices",
            "Monitor system performance"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 8,
        "title": "Junior Data Scientist (Fresher)",
        "company": "StartUp Karachi",
        "location": "Karachi, Pakistan",
        "type": "Full-time",
        "experience": "Fresh Graduate",
        "posted": "Today",
        "salary": "PKR 45,000 - 65,000/month",
        "description": "Great opportunity for fresh graduates! Join our data team and learn on the job while working on real ML projects.",
        "required_skills": ["python", "pandas", "numpy", "sql", "statistics"],
        "preferred_skills": ["scikit-learn", "data visualization", "machine learning"],
        "responsibilities": [
            "Assist with data cleaning and EDA",
            "Build simple ML models under supervision",
            "Create reports and visualizations",
            "Learn and grow with the team"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 9,
        "title": "React Frontend Developer",
        "company": "UX Masters",
        "location": "Remote (Pakistan)",
        "type": "Contract",
        "experience": "1-2 years",
        "posted": "2 days ago",
        "salary": "PKR 50,000 - 80,000/month",
        "description": "Build beautiful, responsive web interfaces using React and modern CSS frameworks.",
        "required_skills": ["react", "javascript", "html", "css", "git"],
        "preferred_skills": ["typescript", "tailwind", "next.js", "figma", "rest api"],
        "responsibilities": [
            "Implement UI/UX designs in React",
            "Ensure cross-browser compatibility",
            "Optimize frontend performance",
            "Work closely with designers"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
    {
        "id": 10,
        "title": "Senior Python / ML Engineer",
        "company": "Global Tech Corp",
        "location": "Islamabad, Pakistan",
        "type": "Full-time",
        "experience": "4+ years",
        "posted": "3 days ago",
        "salary": "PKR 160,000 - 250,000/month",
        "description": "Lead a team of ML engineers to build next-generation AI products. Architecture, mentoring, and delivery responsibility.",
        "required_skills": ["python", "machine learning", "deep learning", "docker", "aws", "leadership"],
        "preferred_skills": ["kubernetes", "mlflow", "pytorch", "tensorflow", "agile"],
        "responsibilities": [
            "Lead ML team and set technical direction",
            "Design scalable AI systems",
            "Mentor junior engineers",
            "Communicate with stakeholders"
        ],
        "apply_link": "https://www.linkedin.com/jobs/"
    },
]


def get_all_jobs():
    return JOBS_DATABASE


def search_jobs(query: str = "", skills: list = None, location: str = "", job_type: str = ""):
    """Filter jobs based on criteria."""
    results = JOBS_DATABASE.copy()

    if query:
        query_lower = query.lower()
        results = [j for j in results if
                   query_lower in j["title"].lower() or
                   query_lower in j["company"].lower() or
                   query_lower in j["description"].lower()]

    if skills:
        skills_lower = [s.lower() for s in skills]
        def has_skill_overlap(job):
            all_job_skills = job["required_skills"] + job["preferred_skills"]
            return any(s in all_job_skills for s in skills_lower)
        results = [j for j in results if has_skill_overlap(j)]

    if location and location != "All":
        results = [j for j in results if location.lower() in j["location"].lower()]

    if job_type and job_type != "All":
        results = [j for j in results if job_type.lower() in j["type"].lower()]

    return results


def get_job_by_id(job_id: int):
    for job in JOBS_DATABASE:
        if job["id"] == job_id:
            return job
    return None
