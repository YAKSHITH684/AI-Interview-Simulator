from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from database.database import SessionLocal
from database.models import User

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str
    new_password: str


@router.post("/register")
def register(data: RegisterRequest):

    db = SessionLocal()

    exists = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if exists:
        db.close()
        return {"message": "User already exists"}

    user = User(
        email=data.email,
        password=data.password
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "Registration Successful"}


@router.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.email == data.email,
            User.password == data.password
        )
        .first()
    )

    db.close()

    return {"success": bool(user)}


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        db.close()
        return {"message": "Email not found"}

    user.password = data.new_password

    db.commit()
    db.close()

    return {"message": "Password Updated Successfully"}


@router.post("/analyze-resume")
async def analyze_resume(resume: UploadFile = File(...)):

    import pdfplumber
    import docx

    content = await resume.read()
    filename = resume.filename.lower()

    text = ""

    # PDF file
    if filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(content)

        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    # DOCX file
    elif filename.endswith(".docx"):
        with open("temp.docx", "wb") as f:
            f.write(content)

        doc = docx.Document("temp.docx")
        for para in doc.paragraphs:
            text += para.text + " "

    # TXT fallback
    else:
        try:
            text = content.decode("utf-8", errors="ignore")
        except:
            text = ""

    text = text.lower()

    ats = 50
    skills = 0

    if "python" in text:
        ats += 10
        skills += 1

    if "machine learning" in text:
        ats += 15
        skills += 1

    if "sql" in text:
        ats += 10
        skills += 1

    if "project" in text:
        ats += 10
        skills += 1

    if "ai" in text:
        ats += 5
        skills += 1

    ats = min(ats, 100)

    # -------------------------
    # AI ANALYSIS (ONLY ADDED - NO LOGIC CHANGE)
    # -------------------------

    ai_skills_map = {
        "python": "Python",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "sql": "SQL Database",
        "ai": "Artificial Intelligence",
        "fastapi": "FastAPI",
        "docker": "Docker",
        "aws": "AWS Cloud",
        "django": "Django",
        "flask": "Flask"
    }

    ai_skills_found = []

    for key, value in ai_skills_map.items():
        if key in text:
            ai_skills_found.append(value)

    if len(ai_skills_found) >= 5:
        ai_verdict = "Strong Resume 💪 (AI Approved)"
    elif len(ai_skills_found) >= 3:
        ai_verdict = "Moderate Resume ⚖️ (Needs Improvement)"
    else:
        ai_verdict = "Weak Resume ⚠️ (Low Skill Match)"

    ai_feedback = []

    if "project" not in text:
        ai_feedback.append("Add more real-world projects")

    if "github" not in text:
        ai_feedback.append("Add GitHub profile")

    if "experience" not in text:
        ai_feedback.append("Mention internships or experience")

    if not ai_feedback:
        ai_feedback.append("Good structured resume")

    ai_feedback = " | ".join(ai_feedback)

    return {
        "ats_score": ats,
        "resume_score": max(ats - 5, 0),
        "readiness": max(ats - 10, 0),
        "skills": skills,

        # AI OUTPUT (ADDED ONLY)
        "ai_skills_found": ai_skills_found,
        "ai_verdict": ai_verdict,
        "ai_feedback": ai_feedback
    }