"""
NLP Utility Functions
Handles resume parsing, skill extraction, ATS scoring, job matching
"""

import re
import json
from collections import Counter

# ─────────────────────────────────────────────
# SKILLS DATABASE
# ─────────────────────────────────────────────

SKILLS_DB = {
    "programming": [
        "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
        "go", "rust", "kotlin", "swift", "php", "ruby", "matlab", "sql", "bash"
    ],
    "web": [
        "html", "css", "react", "angular", "vue", "node.js", "django", "flask",
        "fastapi", "express", "spring boot", "rest api", "graphql", "bootstrap",
        "tailwind", "next.js", "gatsby"
    ],
    "data_science": [
        "machine learning", "deep learning", "nlp", "computer vision",
        "data analysis", "data visualization", "statistics", "pandas", "numpy",
        "scikit-learn", "tensorflow", "pytorch", "keras", "xgboost",
        "random forest", "neural networks", "transformers", "bert", "gpt"
    ],
    "databases": [
        "mysql", "postgresql", "mongodb", "sqlite", "redis", "cassandra",
        "oracle", "sql server", "firebase", "elasticsearch", "dynamodb"
    ],
    "cloud_devops": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git",
        "github", "gitlab", "ci/cd", "terraform", "ansible", "linux",
        "devops", "microservices", "agile", "scrum"
    ],
    "tools": [
        "tableau", "power bi", "excel", "jupyter", "vs code", "pycharm",
        "postman", "jira", "confluence", "figma", "photoshop"
    ],
    "soft_skills": [
        "communication", "teamwork", "leadership", "problem solving",
        "critical thinking", "time management", "project management",
        "presentation", "analytical"
    ]
}

ALL_SKILLS = []
for category, skills in SKILLS_DB.items():
    ALL_SKILLS.extend(skills)

SKILL_CATEGORY_MAP = {}
for category, skills in SKILLS_DB.items():
    for skill in skills:
        SKILL_CATEGORY_MAP[skill] = category


# ─────────────────────────────────────────────
# RESUME PARSING
# ─────────────────────────────────────────────

def extract_text_from_string(text: str) -> str:
    """Clean and normalize text."""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def extract_email(text: str) -> str:
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not found"


def extract_phone(text: str) -> str:
    pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not found"


def extract_skills(text: str) -> dict:
    """Extract skills from text and categorize them."""
    text_lower = text.lower()
    found_skills = {}

    for skill in ALL_SKILLS:
        # Match whole word/phrase
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            category = SKILL_CATEGORY_MAP.get(skill, "other")
            if category not in found_skills:
                found_skills[category] = []
            found_skills[category].append(skill)

    return found_skills


def extract_experience_years(text: str) -> int:
    """Try to estimate years of experience."""
    patterns = [
        r'(\d+)\+?\s*years?\s*of\s*experience',
        r'experience\s*of\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s*exp',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return int(matches[0])

    # Count year mentions
    years = re.findall(r'\b(20\d{2})\b', text)
    if len(years) >= 2:
        years_int = [int(y) for y in years]
        span = max(years_int) - min(years_int)
        return min(span, 15)

    return 0


def extract_education(text: str) -> list:
    """Extract education qualifications."""
    degrees = []
    degree_patterns = [
        r'\b(B\.?S\.?C?\.?|Bachelor[\w\s]*?(?:Science|Arts|Engineering|Technology|Computer))',
        r'\b(M\.?S\.?C?\.?|Master[\w\s]*?(?:Science|Arts|Engineering|Technology|Business))',
        r'\b(Ph\.?D\.?|Doctor[\w\s]*?Philosophy)',
        r'\b(MBA|MCA|BCA|B\.?Tech|M\.?Tech|BE|ME)\b',
        r'\b(Intermediate|Matric|O-Level|A-Level|FSc|FA|ICS)\b',
    ]
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        degrees.extend([m if isinstance(m, str) else m[0] for m in matches])

    return list(set(degrees))


# ─────────────────────────────────────────────
# ATS SCORING
# ─────────────────────────────────────────────

ATS_WEIGHTS = {
    "skills_count": 30,
    "contact_info": 15,
    "education": 15,
    "experience_keywords": 20,
    "resume_length": 10,
    "formatting_keywords": 10,
}

EXPERIENCE_KEYWORDS = [
    "developed", "designed", "implemented", "managed", "led", "created",
    "built", "analyzed", "improved", "optimized", "deployed", "architected",
    "collaborated", "coordinated", "delivered", "achieved", "increased",
    "reduced", "spearheaded", "mentored", "automated"
]

FORMATTING_KEYWORDS = [
    "objective", "summary", "experience", "education", "skills",
    "projects", "achievements", "certifications", "references", "internship"
]


def calculate_ats_score(text: str, skills_found: dict) -> dict:
    """Calculate ATS score with breakdown."""
    text_lower = text.lower()
    scores = {}
    details = {}

    # Skills score (30 pts)
    total_skills = sum(len(v) for v in skills_found.values())
    skill_score = min(30, total_skills * 2)
    scores["skills_count"] = skill_score
    details["skills"] = f"{total_skills} skills found"

    # Contact info (15 pts)
    has_email = bool(re.search(r'\b[\w.-]+@[\w.-]+\.\w{2,}\b', text))
    has_phone = bool(re.search(r'[\+\d][\d\s\-\(\)]{8,}', text))
    has_linkedin = 'linkedin' in text_lower
    contact_score = (5 if has_email else 0) + (5 if has_phone else 0) + (5 if has_linkedin else 0)
    scores["contact_info"] = contact_score
    details["contact"] = f"Email: {'✓' if has_email else '✗'} | Phone: {'✓' if has_phone else '✗'} | LinkedIn: {'✓' if has_linkedin else '✗'}"

    # Education (15 pts)
    edu = extract_education(text)
    edu_score = min(15, len(edu) * 5)
    scores["education"] = edu_score
    details["education"] = f"{len(edu)} qualification(s) found"

    # Experience keywords (20 pts)
    exp_found = [kw for kw in EXPERIENCE_KEYWORDS if kw in text_lower]
    exp_score = min(20, len(exp_found) * 2)
    scores["experience_keywords"] = exp_score
    details["experience_keywords"] = f"{len(exp_found)} action verbs found"

    # Resume length (10 pts)
    word_count = len(text.split())
    if 300 <= word_count <= 1000:
        len_score = 10
    elif word_count < 300:
        len_score = 5
    else:
        len_score = 7
    scores["resume_length"] = len_score
    details["length"] = f"{word_count} words"

    # Formatting (10 pts)
    fmt_found = [kw for kw in FORMATTING_KEYWORDS if kw in text_lower]
    fmt_score = min(10, len(fmt_found) * 2)
    scores["formatting_keywords"] = fmt_score
    details["formatting"] = f"{len(fmt_found)} standard sections found"

    total = sum(scores.values())
    return {
        "total": total,
        "breakdown": scores,
        "details": details,
        "grade": get_ats_grade(total)
    }


def get_ats_grade(score: int) -> str:
    if score >= 85:
        return "Excellent ✅"
    elif score >= 70:
        return "Good 👍"
    elif score >= 55:
        return "Average ⚠️"
    else:
        return "Needs Work ❌"


def get_ats_suggestions(text: str, skills_found: dict, score_data: dict) -> list:
    """Generate actionable ATS improvement suggestions."""
    suggestions = []
    text_lower = text.lower()

    if score_data["breakdown"]["contact_info"] < 15:
        if 'linkedin' not in text_lower:
            suggestions.append("🔗 Add your LinkedIn profile URL")
        if not re.search(r'\b[\w.-]+@[\w.-]+\.\w{2,}\b', text):
            suggestions.append("📧 Add your email address")
        if not re.search(r'[\+\d][\d\s\-\(\)]{8,}', text):
            suggestions.append("📱 Add your phone number")

    if score_data["breakdown"]["skills_count"] < 20:
        suggestions.append("💡 Add more technical skills (aim for 15-20+ skills)")

    if score_data["breakdown"]["experience_keywords"] < 15:
        suggestions.append("✍️ Use more action verbs (e.g., 'developed', 'implemented', 'led')")

    if score_data["breakdown"]["formatting_keywords"] < 8:
        suggestions.append("📑 Add clear section headers: Skills, Experience, Education, Projects")

    if 'objective' not in text_lower and 'summary' not in text_lower:
        suggestions.append("📝 Add a professional summary/objective at the top")

    if 'github' not in text_lower and 'portfolio' not in text_lower:
        suggestions.append("💻 Add your GitHub profile or portfolio link")

    if not suggestions:
        suggestions.append("🌟 Your resume is well-optimized! Keep it updated.")

    return suggestions


# ─────────────────────────────────────────────
# JOB MATCHING
# ─────────────────────────────────────────────

def calculate_job_match(user_skills: list, job_required_skills: list, job_preferred_skills: list = None) -> dict:
    """Calculate match percentage between user skills and job requirements."""
    if job_preferred_skills is None:
        job_preferred_skills = []

    user_skills_lower = [s.lower() for s in user_skills]
    required_lower = [s.lower() for s in job_required_skills]
    preferred_lower = [s.lower() for s in job_preferred_skills]

    # Required skills match (70% weight)
    required_matched = [s for s in required_lower if s in user_skills_lower]
    required_pct = (len(required_matched) / len(required_lower) * 100) if required_lower else 100

    # Preferred skills match (30% weight)
    preferred_matched = [s for s in preferred_lower if s in user_skills_lower]
    preferred_pct = (len(preferred_matched) / len(preferred_lower) * 100) if preferred_lower else 0

    # Weighted total
    if preferred_lower:
        total = (required_pct * 0.7) + (preferred_pct * 0.3)
    else:
        total = required_pct

    missing_required = [s for s in required_lower if s not in user_skills_lower]
    missing_preferred = [s for s in preferred_lower if s not in user_skills_lower]

    return {
        "match_percentage": round(total, 1),
        "required_matched": required_matched,
        "preferred_matched": preferred_matched,
        "missing_required": missing_required,
        "missing_preferred": missing_preferred,
        "grade": get_match_grade(total)
    }


def get_match_grade(pct: float) -> str:
    if pct >= 85:
        return "🟢 Excellent Match"
    elif pct >= 70:
        return "🟡 Good Match"
    elif pct >= 50:
        return "🟠 Partial Match"
    else:
        return "🔴 Low Match"


# ─────────────────────────────────────────────
# SALARY ESTIMATION
# ─────────────────────────────────────────────

SALARY_DATA = {
    "fresher": {
        "data scientist": (60000, 90000),
        "software engineer": (55000, 85000),
        "web developer": (45000, 75000),
        "ml engineer": (65000, 95000),
        "data analyst": (50000, 75000),
        "python developer": (55000, 80000),
        "default": (45000, 70000),
    },
    "mid": {
        "data scientist": (90000, 140000),
        "software engineer": (85000, 130000),
        "web developer": (75000, 120000),
        "ml engineer": (100000, 150000),
        "data analyst": (75000, 110000),
        "python developer": (80000, 120000),
        "default": (70000, 110000),
    },
    "senior": {
        "data scientist": (140000, 200000),
        "software engineer": (130000, 190000),
        "web developer": (120000, 170000),
        "ml engineer": (150000, 210000),
        "data analyst": (110000, 160000),
        "python developer": (120000, 175000),
        "default": (110000, 170000),
    }
}


def estimate_salary(job_title: str, experience_level: str, location: str = "US") -> dict:
    """Estimate salary range for a job."""
    level_key = experience_level.lower()
    if "fresh" in level_key or "entry" in level_key or "junior" in level_key:
        level = "fresher"
    elif "senior" in level_key or "lead" in level_key or "principal" in level_key:
        level = "senior"
    else:
        level = "mid"

    job_lower = job_title.lower()
    salary_range = SALARY_DATA[level].get("default")
    for key, val in SALARY_DATA[level].items():
        if key in job_lower:
            salary_range = val
            break

    # Pakistan adjustment
    if "pakistan" in location.lower() or "pk" in location.lower():
        factor = 0.08  # PKR rough approximation
        return {
            "min": f"PKR {salary_range[0]*factor*83:,.0f}",
            "max": f"PKR {salary_range[1]*factor*83:,.0f}",
            "currency": "PKR",
            "note": "Estimated based on market data"
        }

    return {
        "min": f"${salary_range[0]:,}",
        "max": f"${salary_range[1]:,}",
        "currency": "USD",
        "note": "Estimated based on market data"
    }
