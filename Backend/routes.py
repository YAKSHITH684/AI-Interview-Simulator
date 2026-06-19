from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from database.database import SessionLocal
from database.models import User

router = APIRouter()


# ==========================
# MODELS
# ==========================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str
    new_password: str


# ==========================
# REGISTER
# ==========================

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
        return {
            "success": False,
            "message": "User already exists"
        }

    user = User(
        name=data.name,
        email=data.email,
        password=data.password
    )

    db.add(user)
    db.commit()
    db.close()

    return {
        "success": True,
        "message": "Registration Successful"
    }


# ==========================
# LOGIN
# ==========================

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

    if user:

        return {
            "success": True,
            "message": "Login Successful",
            "name": user.name
        }

    return {
        "success": False,
        "message": "Invalid Email or Password"
    }


# ==========================
# FORGOT PASSWORD
# ==========================

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

        return {
            "success": False,
            "message": "Email not found"
        }

    user.password = data.new_password

    db.commit()
    db.close()

    return {
        "success": True,
        "message": "Password Updated Successfully"
    }


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

    # AI OUTPUT
    "ai_skills_found": ai_skills_found,
    "ai_verdict": ai_verdict,
    "ai_feedback": ai_feedback,

    # PROGRESS DATA
    "resume_progress": ats,

    "interview_progress": 0,

    "overall_progress":
        int(
            (
                ats + 0
            ) / 2
        ),

    "level":
        "Excellent 🚀"
        if ats >= 80
        else "Good 👍"
        if ats >= 60
        else "Average ⚡"
        if ats >= 40
        else "Needs Improvement 📚"
}

@router.post("/chat")
def chat(data: dict):

    msg = data.get("message", "").strip().lower()
    step = data.get("step", 0)

    questions = [
        "Tell me about yourself (STRICT: answer in 3 lines only).",
        "What are your strengths?",
        "What are your weaknesses?",
        "Explain your best project.",
        "What challenges did you face in that project?",
        "What technologies did you use?",
        "Why did you choose this field?",
        "Describe a problem you solved recently.",
        "How do you handle pressure or deadlines?",
        "Why should we hire you?"
    ]

    feedback = [
        "Good introduction 👍",
        "Nice strength 👍",
        "Honest answer 👍",
        "Good project explanation 👨‍💻",
        "Strong problem solving 🔥",
        "Good technical clarity ⚙️",
        "Nice career reasoning 🎯",
        "Good real example 🧠",
        "Good pressure handling 💼",
        "Excellent final answer 🚀"
    ]

    # FIRST MESSAGE
    if step == 0:
        return {
            "reply": (
                "👋 Welcome to AI Interview!\n\n"
                "We will evaluate your communication and technical skills.\n\n"
                + questions[0]
            ),
            "next_step": 1
        }

    # STOP CONDITION
    if step >= len(questions):
        return {
            "reply": "🎉 Interview completed successfully!",
            "next_step": step
        }

    # NORMAL FLOW
    reply = (
        f"🤖 Feedback: {feedback[step - 1]}\n\n"
        f"➡️ Next Question:\n{questions[step]}"
    )

    return {
        "reply": reply,
        "next_step": step + 1
    }

@router.post("/chat")
def chat(data: dict):

    msg = data.get("message", "").strip().lower()
    step = data.get("step", 0)

    questions = [
        "Tell me about yourself (STRICT: answer in 3 lines only).",
        "What are your strengths?",
        "What are your weaknesses?",
        "Explain your best project.",
        "What challenges did you face in that project?",
        "What technologies did you use?",
        "Why did you choose this field?",
        "Describe a problem you solved recently.",
        "How do you handle pressure or deadlines?",
        "Why should we hire you?"
    ]

    feedback = [
        "Good introduction 👍",
        "Nice strength 👍",
        "Honest answer 👍",
        "Good project explanation 👨‍💻",
        "Strong problem solving 🔥",
        "Good technical clarity ⚙️",
        "Nice career reasoning 🎯",
        "Good real example 🧠",
        "Good pressure handling 💼",
        "Excellent final answer 🚀"
    ]

    # FIRST MESSAGE
    if step == 0:
        return {
            "reply": (
                "👋 Welcome to AI Interview!\n\n"
                "We will evaluate your communication, confidence, and technical skills.\n\n"
                "💡 Tip: Keep answers short and structured.\n\n"
                + questions[0]
            ),
            "next_step": 1
        }

    # STOP CONDITION
    if step >= len(questions):
        return {
            "reply": (
                "🎉 Interview completed successfully!\n\n"
                "📊 You can now review your performance and try again to improve."
            ),
            "next_step": step
        }

    # SIMPLE INTELLIGENT CHECK (NEW ADDITION)
    if len(msg) < 5:
        warning = "⚠️ Try to give a more detailed answer."
    else:
        warning = ""

    # NORMAL FLOW
    reply = (
        f"🧠 Your Answer Note: {warning}\n\n"
        f"🤖 Feedback: {feedback[step - 1]}\n\n"
        f"➡️ Next Question:\n{questions[step]}"
    )

    return {
        "reply": reply,
        "next_step": step + 1
    }
# ==========================
# STUDENT PROGRESS API
# ADD BELOW YOUR CODE
# ==========================

class ProgressRequest(BaseModel):
    ats_score: int = 0
    interview_step: int = 0


@router.post("/student-progress")
def student_progress(data: ProgressRequest):

    ats = data.ats_score
    interview = data.interview_step

    resume_progress = min(ats, 100)

    interview_progress = min(
        int((interview / 10) * 100),
        100
    )

    overall = int(
        (resume_progress + interview_progress) / 2
    )

    if overall >= 80:
        level = "Excellent 🚀"

    elif overall >= 60:
        level = "Good 👍"

    elif overall >= 40:
        level = "Average ⚡"

    else:
        level = "Needs Improvement 📚"

    return {

        "resume_progress": resume_progress,

        "interview_progress": interview_progress,

        "overall_progress": overall,

        "level": level
    }
