SKILLS_DB = [
    "python", "machine learning", "deep learning",
    "sql", "flask", "fastapi", "pandas",
    "numpy", "tensorflow", "opencv"
]

def extract_skills(text):
    text = text.lower()
    return list({skill for skill in SKILLS_DB if skill in text})


def extract_projects(text):
    lines = text.split("\n")
    return [line.strip() for line in lines if "project" in line.lower()]