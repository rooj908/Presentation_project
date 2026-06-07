"""
AI Generation Utilities
Handles cover letter, interview questions, roadmap generation via LLM API
Falls back to template-based generation if API key not configured.
"""

import os
import streamlit as st

# ─────────────────────────────────────────────
# API SETUP (configure your key in .env or Streamlit secrets)
# ─────────────────────────────────────────────

def get_api_key():
    """Get API key from environment or streamlit secrets."""
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            pass
    return key


def call_openai(prompt: str, system: str = "You are a professional career coach.", max_tokens: int = 800) -> str:
    """Call OpenAI API. Falls back to template if key not set."""
    api_key = get_api_key()
    if not api_key:
        return None  # Signal to use fallback

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except ImportError:
        return None
    except Exception as e:
        return None


# ─────────────────────────────────────────────
# COVER LETTER GENERATION
# ─────────────────────────────────────────────

def generate_cover_letter(name: str, job_title: str, company: str,
                           user_skills: list, experience_level: str,
                           job_description: str = "") -> str:
    """Generate a tailored cover letter."""

    skills_str = ", ".join(user_skills[:8]) if user_skills else "Python, Machine Learning, Data Analysis"

    # Try AI generation
    prompt = f"""Write a professional cover letter for:
Name: {name}
Applying for: {job_title} at {company}
Experience Level: {experience_level}
Key Skills: {skills_str}
Job Description: {job_description[:500] if job_description else 'Not provided'}

Write a 3-paragraph cover letter that is professional, specific, and compelling.
Do not use generic phrases. Make it sound human and enthusiastic."""

    ai_result = call_openai(prompt)
    if ai_result:
        return ai_result

    # Template fallback
    skills_highlight = ", ".join(user_skills[:5]) if user_skills else "Python, Machine Learning, and Data Analysis"

    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. As a {experience_level.lower()} professional with hands-on experience in {skills_highlight}, I am excited about the opportunity to contribute to your team and help drive impactful results.

Throughout my academic and professional journey, I have developed solid expertise in {skills_highlight}. I have worked on end-to-end projects ranging from data preprocessing and model development to deployment and monitoring. I am particularly drawn to {company}'s reputation for innovation and technical excellence, and I believe my background aligns closely with what you are looking for in this role.

I am eager to bring my skills, passion for technology, and collaborative mindset to the {job_title} role. I would welcome the opportunity to discuss how my experience and enthusiasm can contribute to {company}'s continued success. Thank you for considering my application — I look forward to hearing from you.

Warm regards,
{name}"""


# ─────────────────────────────────────────────
# INTERVIEW QUESTIONS GENERATION
# ─────────────────────────────────────────────

INTERVIEW_QUESTIONS_DB = {
    "python": [
        ("What are Python decorators? Give an example.", "Decorators are functions that modify other functions using @syntax. Example: @property, @staticmethod, or custom decorators for logging/timing."),
        ("Explain the difference between a list and a tuple.", "Lists are mutable (can be modified), tuples are immutable. Lists use [], tuples use (). Tuples are faster and used for fixed data."),
        ("What is the GIL in Python?", "Global Interpreter Lock — prevents multiple threads from executing Python bytecode simultaneously. Use multiprocessing for CPU-bound tasks instead."),
        ("How does memory management work in Python?", "Python uses reference counting + garbage collector. Objects are deallocated when reference count reaches 0. gc module handles cyclic references."),
        ("What are generators and when would you use them?", "Generators use yield to produce values lazily. Use them for large datasets to save memory — e.g., reading large files line by line."),
    ],
    "machine learning": [
        ("What is the bias-variance tradeoff?", "Bias = underfitting (model too simple), Variance = overfitting (model too complex). Goal is to find the sweet spot. Regularization helps manage this."),
        ("Explain overfitting and how to prevent it.", "Overfitting = model memorizes training data, performs poorly on new data. Fix: regularization (L1/L2), dropout, cross-validation, more data, simpler model."),
        ("What is cross-validation and why is it important?", "CV splits data into k folds, trains on k-1, tests on 1, repeats k times. Gives reliable performance estimate and helps detect overfitting."),
        ("How does gradient descent work?", "Iteratively updates model parameters in direction of steepest loss descent. Step size = learning rate. Variants: SGD, Adam, RMSProp."),
        ("Explain precision vs recall.", "Precision = TP/(TP+FP) — of predicted positives, how many are correct. Recall = TP/(TP+FN) — of actual positives, how many did we catch. F1 = harmonic mean."),
    ],
    "sql": [
        ("What is the difference between INNER JOIN and LEFT JOIN?", "INNER JOIN returns only matching rows. LEFT JOIN returns all rows from left table + matching rows from right (NULLs where no match)."),
        ("Explain GROUP BY vs HAVING.", "GROUP BY groups rows for aggregation. HAVING filters on aggregated results (like WHERE but after grouping). WHERE filters before grouping."),
        ("What are indexes and when should you use them?", "Indexes speed up SELECT queries by creating lookup structures. Use on frequently queried columns. Downsides: slower INSERTs/UPDATEs, more storage."),
    ],
    "deep learning": [
        ("Explain how backpropagation works.", "Computes gradients of loss w.r.t. each weight using chain rule, flowing backwards through the network. These gradients update weights via gradient descent."),
        ("What is the vanishing gradient problem?", "In deep networks, gradients become tiny as they propagate backward, making early layers learn very slowly. Fixed by ReLU activations, batch norm, residual connections."),
        ("What are transformers and why are they powerful?", "Attention-based architecture that processes sequences in parallel. Self-attention allows each token to attend to all others. Powers BERT, GPT, etc."),
    ],
    "django": [
        ("Explain Django's MVT architecture.", "Model (database), View (business logic), Template (HTML). Django handles URL routing, ORM, admin, auth, forms out-of-the-box."),
        ("What is Django ORM? How does it work?", "Object-Relational Mapper — lets you interact with DB using Python objects instead of SQL. MyModel.objects.filter(name='Ali') generates SQL automatically."),
    ],
    "react": [
        ("What is the virtual DOM?", "React keeps a lightweight copy of the DOM. On state change, it diffs virtual DOM vs real DOM and only updates changed parts — very efficient."),
        ("Explain useState and useEffect hooks.", "useState manages component state. useEffect handles side effects (API calls, subscriptions) after renders. useEffect with [] runs once on mount."),
    ],
    "general": [
        ("Tell me about yourself.", "Structure: 1) Current role/background, 2) Key skills and achievements, 3) Why you're interested in this role. Keep it concise — 90 seconds."),
        ("Where do you see yourself in 5 years?", "Show ambition but align with company growth. Example: 'I see myself growing into a senior/lead role, taking on more responsibility and mentoring others.'"),
        ("What is your greatest weakness?", "Be genuine but strategic. Choose a real weakness you're actively improving. Show self-awareness and growth mindset."),
        ("Why do you want to work here?", "Research the company. Mention specific: their tech stack, culture, products, or mission. Show you're excited about their specific work, not just any job."),
        ("Describe a challenging project you worked on.", "Use STAR method: Situation, Task, Action, Result. Quantify results where possible."),
    ]
}


def generate_interview_questions(job_title: str, skills: list, experience_level: str) -> list:
    """Generate relevant interview questions."""

    # Try AI generation
    prompt = f"""Generate 10 interview questions for a {job_title} position at {experience_level} level.
Skills focus: {', '.join(skills[:6])}
Format: Return as a numbered list. For each question, provide:
Q: [Question]
A: [Brief model answer hint]
---"""

    ai_result = call_openai(prompt, max_tokens=1200)
    if ai_result:
        # Parse AI response
        questions = []
        blocks = ai_result.split("---")
        for block in blocks:
            if "Q:" in block and "A:" in block:
                lines = block.strip().split("\n")
                q = ""
                a = ""
                for line in lines:
                    if line.startswith("Q:"):
                        q = line[2:].strip()
                    elif line.startswith("A:"):
                        a = line[2:].strip()
                if q:
                    questions.append({"question": q, "answer_hint": a})
        if questions:
            return questions

    # Template fallback
    all_questions = []

    # Add skill-specific questions
    skills_lower = [s.lower() for s in skills]
    for skill, questions in INTERVIEW_QUESTIONS_DB.items():
        if skill in skills_lower or any(skill in s for s in skills_lower):
            all_questions.extend([{"question": q, "answer_hint": a} for q, a in questions])

    # Always add general questions
    all_questions.extend([{"question": q, "answer_hint": a} for q, a in INTERVIEW_QUESTIONS_DB["general"]])

    # Deduplicate and limit
    seen = set()
    unique = []
    for q in all_questions:
        if q["question"] not in seen:
            seen.add(q["question"])
            unique.append(q)

    return unique[:12]


# ─────────────────────────────────────────────
# LEARNING ROADMAP GENERATION
# ─────────────────────────────────────────────

ROADMAP_DB = {
    "data scientist": {
        "duration": "6-9 months",
        "phases": [
            {
                "phase": "Phase 1: Foundations (Month 1-2)",
                "topics": ["Python basics & OOP", "Statistics & Probability", "NumPy & Pandas", "SQL fundamentals"],
                "resources": ["Python.org tutorials", "Khan Academy Statistics", "Kaggle Pandas course", "Mode SQL Tutorial"],
                "projects": ["EDA on any public dataset", "SQL query exercises"]
            },
            {
                "phase": "Phase 2: Machine Learning (Month 3-4)",
                "topics": ["Scikit-learn", "Regression & Classification", "Model evaluation", "Feature engineering"],
                "resources": ["Andrew Ng ML Course (Coursera)", "Scikit-learn docs", "Kaggle Learn ML"],
                "projects": ["Titanic prediction", "House price regression", "Customer churn model"]
            },
            {
                "phase": "Phase 3: Deep Learning & NLP (Month 5-6)",
                "topics": ["Neural Networks", "TensorFlow/PyTorch", "NLP with Transformers", "Computer Vision basics"],
                "resources": ["Fast.ai course", "HuggingFace tutorials", "Deep Learning Specialization"],
                "projects": ["Sentiment analysis", "Image classifier", "Text summarizer"]
            },
            {
                "phase": "Phase 4: Production & Portfolio (Month 7-9)",
                "topics": ["MLOps basics", "Docker & deployment", "API development", "Portfolio building"],
                "resources": ["MLflow docs", "Docker tutorial", "FastAPI docs"],
                "projects": ["Deploy a model as API", "End-to-end ML pipeline", "Kaggle competition"]
            }
        ]
    },
    "web developer": {
        "duration": "4-6 months",
        "phases": [
            {
                "phase": "Phase 1: HTML, CSS & JS (Month 1-2)",
                "topics": ["HTML5 semantic markup", "CSS Flexbox & Grid", "JavaScript ES6+", "Responsive design"],
                "resources": ["freeCodeCamp", "MDN Web Docs", "The Odin Project"],
                "projects": ["Personal portfolio", "Landing page", "To-do app"]
            },
            {
                "phase": "Phase 2: React & Backend (Month 3-4)",
                "topics": ["React fundamentals", "State management", "Node.js & Express", "REST APIs"],
                "resources": ["React docs", "Node.js docs", "The Odin Project", "Traversy Media YouTube"],
                "projects": ["Todo app in React", "CRUD API with Node", "Full-stack auth app"]
            },
            {
                "phase": "Phase 3: Databases & Deployment (Month 5-6)",
                "topics": ["SQL & PostgreSQL", "MongoDB", "Docker basics", "Cloud deployment"],
                "resources": ["PostgreSQL tutorial", "MongoDB University", "Docker docs", "Vercel/Railway"],
                "projects": ["Full-stack MERN app", "Blog platform", "E-commerce prototype"]
            }
        ]
    },
    "python developer": {
        "duration": "4-5 months",
        "phases": [
            {
                "phase": "Phase 1: Python Mastery (Month 1-2)",
                "topics": ["Advanced Python", "OOP", "File I/O", "Error handling", "Testing"],
                "resources": ["Real Python", "Python docs", "Corey Schafer YouTube"],
                "projects": ["CLI tools", "File automation scripts"]
            },
            {
                "phase": "Phase 2: Web with Python (Month 2-3)",
                "topics": ["Django or Flask", "REST APIs with FastAPI", "Authentication", "ORM"],
                "resources": ["Django docs", "FastAPI docs", "TestDriven.io"],
                "projects": ["REST API project", "Django blog", "Authentication system"]
            },
            {
                "phase": "Phase 3: Databases & DevOps (Month 4-5)",
                "topics": ["PostgreSQL", "Redis", "Docker", "CI/CD", "AWS basics"],
                "resources": ["Docker docs", "AWS Free Tier", "DigitalOcean tutorials"],
                "projects": ["Containerized Django app", "Deployed API on AWS/Railway"]
            }
        ]
    },
    "default": {
        "duration": "4-6 months",
        "phases": [
            {
                "phase": "Phase 1: Core Skills (Month 1-2)",
                "topics": ["Python programming", "Git & GitHub", "SQL basics", "Problem solving"],
                "resources": ["Python.org", "GitHub Learning Lab", "SQLZoo"],
                "projects": ["Python scripts", "GitHub profile setup"]
            },
            {
                "phase": "Phase 2: Specialization (Month 3-4)",
                "topics": ["Choose your domain", "Domain-specific frameworks", "Projects & practice"],
                "resources": ["Coursera", "Udemy", "YouTube tutorials"],
                "projects": ["2-3 domain projects", "Kaggle or open source contribution"]
            },
            {
                "phase": "Phase 3: Portfolio & Jobs (Month 5-6)",
                "topics": ["Portfolio website", "LinkedIn optimization", "Interview prep", "Networking"],
                "resources": ["GitHub Pages", "LinkedIn Learning"],
                "projects": ["Final capstone project", "Open source contribution"]
            }
        ]
    }
}


def generate_roadmap(target_role: str, current_skills: list, experience_level: str) -> dict:
    """Generate a personalized learning roadmap."""

    target_lower = target_role.lower()
    roadmap_key = "default"
    for key in ROADMAP_DB:
        if key in target_lower or any(word in target_lower for word in key.split()):
            roadmap_key = key
            break

    roadmap = ROADMAP_DB[roadmap_key].copy()
    roadmap["target_role"] = target_role
    roadmap["experience_level"] = experience_level
    return roadmap
