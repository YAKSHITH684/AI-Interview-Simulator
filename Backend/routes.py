from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
import os
import anthropic

from database.database import SessionLocal
from database.models import User

router = APIRouter()

# ─────────────────────────────────────────
# Anthropic client (reads ANTHROPIC_API_KEY from env)
# ─────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def ask_claude(system: str, user: str, max_tokens: int = 1024) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}]
    )
    return message.content[0].text


# ─────────────────────────────────────────
# AUTH SCHEMAS
# ─────────────────────────────────────────
class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str
    new_password: str


# ─────────────────────────────────────────
# AUTH ROUTES
# ─────────────────────────────────────────
@router.post("/register")
def register(data: RegisterRequest):
    db = SessionLocal()
    exists = db.query(User).filter(User.email == data.email).first()
    if exists:
        db.close()
        return {"success": False, "message": "User already exists"}
    user = User(email=data.email, password=data.password)
    db.add(user)
    db.commit()
    db.close()
    return {"success": True, "message": "Registration Successful"}


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password
    ).first()
    db.close()
    return {"success": bool(user)}


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        db.close()
        return {"success": False, "message": "Email not found"}
    user.password = data.new_password
    db.commit()
    db.close()
    return {"success": True, "message": "Password Updated Successfully"}


# ─────────────────────────────────────────
# RESUME ANALYSIS
# ─────────────────────────────────────────
@router.post("/analyze-resume")
async def analyze_resume(resume: UploadFile = File(...)):
    import pdfplumber
    import docx as python_docx

    content = await resume.read()
    filename = resume.filename.lower()
    text = ""

    if filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(content)
        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif filename.endswith(".docx"):
        with open("temp.docx", "wb") as f:
            f.write(content)
        doc = python_docx.Document("temp.docx")
        for para in doc.paragraphs:
            text += para.text + " "

    else:
        try:
            text = content.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    if not text.strip():
        return {"error": "Could not extract text from resume."}

    # ── Claude AI Analysis ──
    system = """You are a professional ATS resume analyst and career coach.
Analyze the resume and respond ONLY with a valid JSON object — no markdown, no explanation.
Schema:
{
  "ats_score": integer 0-100,
  "resume_score": integer 0-100,
  "readiness": integer 0-100,
  "skills": integer (count of skills found),
  "ai_skills_found": ["skill1", "skill2", ...],
  "ai_verdict": "Strong Resume 💪 | Moderate Resume ⚖️ | Weak Resume ⚠️",
  "ai_feedback": "concise feedback string with suggestions separated by | ",
  "summary": "2-3 sentence professional summary of this candidate",
  "strengths": ["strength1", "strength2", "strength3"],
  "suggestions": ["suggestion1", "suggestion2", "suggestion3", "suggestion4"],
  "skill_breakdown": {
    "Technical Skills": integer 0-100,
    "Communication": integer 0-100,
    "Experience": integer 0-100,
    "Education": integer 0-100,
    "Projects": integer 0-100
  }
}"""

    try:
        import json
        raw = ask_claude(system, f"Analyze this resume:\n\n{text[:4000]}", max_tokens=1200)
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return result
    except Exception as e:
        # Fallback to keyword scoring if AI fails
        text_lower = text.lower()
        ats = 50
        skills_found = []
        skill_map = {
            "python": "Python", "machine learning": "Machine Learning",
            "deep learning": "Deep Learning", "sql": "SQL",
            "fastapi": "FastAPI", "docker": "Docker",
            "aws": "AWS", "django": "Django", "flask": "Flask",
            "javascript": "JavaScript", "react": "React",
            "node": "Node.js", "java": "Java", "c++": "C++"
        }
        for key, val in skill_map.items():
            if key in text_lower:
                skills_found.append(val)
                ats = min(ats + 5, 100)

        return {
            "ats_score": ats,
            "resume_score": max(ats - 5, 0),
            "readiness": max(ats - 10, 0),
            "skills": len(skills_found),
            "ai_skills_found": skills_found,
            "ai_verdict": "Moderate Resume ⚖️",
            "ai_feedback": "Could not run full AI analysis. Basic keyword scan used.",
            "summary": "Resume processed with basic analysis.",
            "strengths": skills_found[:3] or ["Skills detected"],
            "suggestions": ["Add more projects", "Include GitHub link", "Add metrics to achievements"],
            "skill_breakdown": {
                "Technical Skills": ats,
                "Communication": 60,
                "Experience": 55,
                "Education": 65,
                "Projects": 50
            }
        }


# ─────────────────────────────────────────
# AI INTERVIEW CHAT
# ─────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []   # [{"role": "user"|"assistant", "content": "..."}]
    mode: str = "technical"    # technical | hr | system | dsa


INTERVIEW_SYSTEMS = {
    "technical": """You are a senior software engineer conducting a technical interview.
Ask one clear technical question at a time. After the candidate answers, give brief feedback (1-2 sentences), then ask the next question.
Focus on: coding, data structures, algorithms, system design basics.
Be professional but encouraging. Keep responses concise.""",

    "hr": """You are an experienced HR manager conducting a behavioral interview.
Ask one behavioral/situational question at a time (encourage STAR format).
After each answer give brief feedback and move to the next question.
Cover: teamwork, conflict, leadership, goals, motivation.
Be warm and professional. Keep responses concise.""",

    "system": """You are a principal engineer conducting a system design interview.
Ask one system design question at a time (e.g. design URL shortener, design Twitter).
Guide the candidate with hints if needed. Give brief feedback after each answer.
Keep responses concise and technical.""",

    "dsa": """You are a FAANG engineer conducting a DSA coding interview.
Present one algorithmic problem at a time. Evaluate correctness, time/space complexity, and clarity.
Give hints if asked. After each answer, give brief feedback and move to the next problem.
Keep responses concise."""
}


@router.post("/chat")
def chat(data: ChatRequest):
    mode = data.mode if data.mode in INTERVIEW_SYSTEMS else "technical"
    system = INTERVIEW_SYSTEMS[mode]

    # Build message history
    messages = []

    # If no history, start the interview
    if not data.history:
        messages.append({"role": "user", "content": "Start the interview. Greet me and ask the first question."})
    else:
        messages = data.history
        messages.append({"role": "user", "content": data.message})

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=system,
            messages=messages
        )
        reply = message.content[0].text
        messages.append({"role": "assistant", "content": reply})

        return {
            "reply": reply,
            "history": messages
        }
    except Exception as e:
        return {"reply": f"Error connecting to AI: {str(e)}", "history": data.history}


# ─────────────────────────────────────────
# PRACTICE QUESTIONS
# ─────────────────────────────────────────
class PracticeRequest(BaseModel):
    topic: str
    count: int = 3


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    topic: str


@router.post("/practice/questions")
def generate_questions(data: PracticeRequest):
    import json
    system = """You are an expert interviewer. Generate interview questions on the given topic.
Respond ONLY with a valid JSON array — no markdown, no extra text.
Format: [{"question": "...", "hint": "...", "difficulty": "Easy|Medium|Hard"}]"""

    try:
        raw = ask_claude(system, f"Generate {data.count} interview questions on: {data.topic}", max_tokens=800)
        clean = raw.replace("```json", "").replace("```", "").strip()
        questions = json.loads(clean)
        return {"success": True, "questions": questions}
    except Exception as e:
        return {"success": False, "error": str(e), "questions": []}


@router.post("/practice/feedback")
def get_feedback(data: FeedbackRequest):
    system = """You are an expert interviewer giving feedback on an interview answer.
Be constructive, specific, and encouraging.
Cover: what was good, what was missing, and a brief model answer outline.
Keep feedback to 4-5 sentences."""

    try:
        reply = ask_claude(
            system,
            f"Topic: {data.topic}\nQuestion: {data.question}\nCandidate's Answer: {data.answer}",
            max_tokens=600
        )
        return {"success": True, "feedback": reply}
    except Exception as e:
        return {"success": False, "feedback": f"Error: {str(e)}"}


# ─────────────────────────────────────────
# AI ANALYSIS (deep resume analysis)
# ─────────────────────────────────────────
class AnalysisRequest(BaseModel):
    resume_text: str


@router.post("/ai-analysis")
def ai_analysis(data: AnalysisRequest):
    import json
    system = """You are a professional resume analyst. Analyze the resume deeply.
Respond ONLY with valid JSON. Schema:
{
  "ats_score": integer,
  "readiness_score": integer,
  "skills": ["skill1", ...],
  "suggestions": ["s1","s2","s3","s4"],
  "summary": "string",
  "skill_breakdown": {
    "Technical Skills": integer,
    "Communication": integer,
    "Experience": integer,
    "Education": integer,
    "Projects": integer
  },
  "strengths": ["s1","s2","s3"],
  "gaps": ["g1","g2"]
}"""

    try:
        raw = ask_claude(system, data.resume_text[:4000], max_tokens=1000)
        clean = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return {"success": True, **result}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─────────────────────────────────────────
# DASHBOARD ASSISTANT CHATBOT
# ─────────────────────────────────────────
class AssistantRequest(BaseModel):
    message: str
    history: List[dict] = []


@router.post("/assistant")
def assistant(data: AssistantRequest):
    system = """You are a friendly and expert AI Interview Coach assistant.
Help users with: interview preparation tips, resume advice, common interview questions,
behavioral interview strategies, technical interview guidance, and career advice.
Keep answers concise and practical (3-5 sentences). Be encouraging and supportive.
If asked to start a full interview, tell them to click 'Interview Chat' in the navigation menu."""

    messages = data.history.copy()
    messages.append({"role": "user", "content": data.message})

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=system,
            messages=messages
        )
        reply = message.content[0].text
        messages.append({"role": "assistant", "content": reply})
        return {"reply": reply, "history": messages}
    except Exception as e:
        return {"reply": f"Error: {str(e)}", "history": data.history}
