import re


# =========================================================
# SKILL DATABASE
# =========================================================

SKILLS = {

    # Programming
    "Python": "Programming",
    "Java": "Programming",
    "C++": "Programming",
    "C": "Programming",
    "JavaScript": "Programming",
    "TypeScript": "Programming",

    # Web Development
    "HTML": "Web Development",
    "CSS": "Web Development",
    "React": "Web Development",
    "Node.js": "Web Development",
    "Angular": "Web Development",
    "Bootstrap": "Web Development",

    # Database
    "SQL": "Database",
    "MySQL": "Database",
    "PostgreSQL": "Database",
    "MongoDB": "Database",
    "Oracle": "Database",

    # AI / ML
    "Machine Learning": "AI/ML",
    "Deep Learning": "AI/ML",
    "Artificial Intelligence": "AI/ML",
    "TensorFlow": "AI/ML",
    "PyTorch": "AI/ML",
    "Scikit-learn": "AI/ML",
    "NLP": "AI/ML",
    "Natural Language Processing": "AI/ML",
    "Computer Vision": "AI/ML",
    "OpenCV": "AI/ML",
    "Neural Networks": "AI/ML",
    "CNN": "AI/ML",
    "RNN": "AI/ML",
    "LSTM": "AI/ML",

    # Data Science
    "Pandas": "Data Science",
    "NumPy": "Data Science",
    "Matplotlib": "Data Science",
    "Seaborn": "Data Science",
    "Plotly": "Data Science",
    "Power BI": "Data Science",
    "Tableau": "Data Science",
    "Data Analysis": "Data Science",
    "Data Visualization": "Data Science",

    # Backend
    "Flask": "Backend",
    "Django": "Backend",
    "FastAPI": "Backend",
    "REST API": "Backend",

    # Cloud
    "AWS": "Cloud",
    "Azure": "Cloud",
    "Google Cloud": "Cloud",
    "GCP": "Cloud",

    # Tools
    "Git": "Tools",
    "GitHub": "Tools",
    "Docker": "Tools",
    "Kubernetes": "Tools",
    "Streamlit": "Tools",
    "Jupyter": "Tools",

    # Soft Skills
    "Communication": "Soft Skills",
    "Leadership": "Soft Skills",
    "Teamwork": "Soft Skills",
    "Problem Solving": "Soft Skills",
    "Time Management": "Soft Skills"
}


# =========================================================
# EXTRACT SKILLS
# =========================================================

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        skill_lower = skill.lower()

        # Escape special characters like + and .
        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(
        list(set(found_skills))
    )


# =========================================================
# GET SKILL CATEGORY
# =========================================================

def get_skill_category(skill):

    return SKILLS.get(
        skill,
        "Other"
    )