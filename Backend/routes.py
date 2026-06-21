from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List
import random

from database.database import SessionLocal
from database.models import User

router = APIRouter()


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

    text_lower = text.lower()
    ats = 50
    skill_map = {
        "python": "Python", "machine learning": "Machine Learning",
        "deep learning": "Deep Learning", "sql": "SQL",
        "fastapi": "FastAPI", "docker": "Docker", "aws": "AWS",
        "django": "Django", "flask": "Flask", "javascript": "JavaScript",
        "react": "React", "node": "Node.js", "java": "Java",
        "c++": "C++", "tensorflow": "TensorFlow", "pytorch": "PyTorch",
        "git": "Git", "linux": "Linux", "mongodb": "MongoDB",
        "rest api": "REST API", "html": "HTML", "css": "CSS"
    }
    skills_found = []
    for key, val in skill_map.items():
        if key in text_lower:
            skills_found.append(val)
            ats = min(ats + 4, 100)

    if "project" in text_lower: ats = min(ats + 5, 100)
    if "experience" in text_lower: ats = min(ats + 5, 100)
    if "github" in text_lower: ats = min(ats + 3, 100)
    if "internship" in text_lower: ats = min(ats + 5, 100)

    feedback = []
    if "project" not in text_lower: feedback.append("Add real-world projects")
    if "github" not in text_lower: feedback.append("Include your GitHub profile")
    if "experience" not in text_lower: feedback.append("Mention internships or work experience")
    if len(skills_found) < 3: feedback.append("Add more technical skills")
    if not feedback: feedback.append("Well-structured resume ✅")

    if len(skills_found) >= 6:
        verdict = "Strong Resume 💪 (Great skill set)"
    elif len(skills_found) >= 3:
        verdict = "Moderate Resume ⚖️ (Needs improvement)"
    else:
        verdict = "Weak Resume ⚠️ (Add more skills)"

    return {
        "ats_score": ats,
        "resume_score": max(ats - 5, 0),
        "readiness": max(ats - 10, 0),
        "skills": len(skills_found),
        "ai_skills_found": skills_found,
        "ai_verdict": verdict,
        "ai_feedback": " | ".join(feedback),
        "summary": f"Candidate has {len(skills_found)} detected skills. ATS compatibility is {ats}%.",
        "strengths": skills_found[:3] if skills_found else ["Skills not detected"],
        "suggestions": feedback[:4],
        "skill_breakdown": {
            "Technical Skills": min(50 + len(skills_found) * 5, 100),
            "Communication": 65,
            "Experience": 60 if "experience" in text_lower else 40,
            "Education": 70 if "education" in text_lower or "degree" in text_lower else 50,
            "Projects": 75 if "project" in text_lower else 35
        }
    }


# ─────────────────────────────────────────
# AI INTERVIEW CHAT (smart rule-based)
# ─────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []
    mode: str = "technical"

QUESTIONS = {
    "technical": [
        "Tell me about yourself and your technical background.",
        "What programming languages are you most comfortable with?",
        "Explain the difference between a list and a tuple in Python.",
        "What is OOP and what are its main principles?",
        "Explain what a REST API is and how it works.",
        "What is the difference between SQL and NoSQL databases?",
        "How does Git version control work?",
        "What is time complexity and why does it matter?",
        "Describe a challenging technical problem you solved.",
        "Where do you see yourself in 5 years technically?"
    ],
    "hr": [
        "Tell me about yourself.",
        "What are your greatest strengths?",
        "What is your biggest weakness and how do you overcome it?",
        "Describe a time you worked in a team and faced a conflict.",
        "Tell me about a project you are most proud of.",
        "How do you handle pressure and tight deadlines?",
        "Why do you want to work at our company?",
        "Where do you see yourself in 5 years?",
        "What motivates you to do your best work?",
        "Why should we hire you over other candidates?"
    ],
    "system": [
        "How would you design a URL shortener like bit.ly?",
        "Design a scalable chat application like WhatsApp.",
        "How would you design a content delivery network (CDN)?",
        "Explain how you would design a ride-sharing system like Uber.",
        "How would you design a recommendation system?",
        "What are the trade-offs between SQL and NoSQL for a social media app?",
        "How would you ensure high availability in a distributed system?",
        "Explain load balancing and when you would use it.",
        "How would you design a notification system for millions of users?",
        "What is the CAP theorem and how does it affect system design?"
    ],
    "dsa": [
        "Reverse a string without using built-in functions.",
        "Find the largest element in an array.",
        "Check if a string is a palindrome.",
        "Find duplicates in an array.",
        "Implement a binary search algorithm.",
        "Explain how a linked list works and implement insertion.",
        "What is a stack and implement push/pop operations.",
        "Find the Fibonacci number at position N using dynamic programming.",
        "Explain BFS and DFS graph traversal.",
        "Find the two numbers in an array that add up to a target sum."
    ]
}

FEEDBACK = [
    "Good answer! You demonstrated clear thinking. 👍",
    "Nice response! Try to include a specific example next time. 💡",
    "Well explained! Adding metrics or numbers makes it stronger. 📊",
    "Good structure! Keep answers concise and to the point. ✅",
    "Great effort! Consider using the STAR method for behavioral questions. ⭐",
    "Solid answer! A real-world example would make it even better. 🔥",
    "Good thinking! Practice elaborating on your technical decisions. 🧠",
    "Nice work! Confidence in delivery is key in real interviews. 💼"
]

@router.post("/chat")
def chat(data: ChatRequest):
    mode = data.mode if data.mode in QUESTIONS else "technical"
    questions = QUESTIONS[mode]
    history = data.history
    msg = data.message.strip()

    # Count how many questions have been asked
    ai_turns = [h for h in history if h.get("role") == "assistant"]
    q_index = len(ai_turns)

    # First message — welcome + first question.
    # IMPORTANT: only an empty history should trigger the welcome message.
    # Previously this also fired whenever msg was empty, which silently
    # restarted the interview and discarded the user's real answer any
    # time the frontend sent a blank/whitespace message on a later turn.
    if not history:
        reply = (
            f"👋 Welcome to the AI Interview Simulator!\n\n"
            f"Mode: {'Technical' if mode == 'technical' else 'HR / Behavioral' if mode == 'hr' else 'System Design' if mode == 'system' else 'DSA'}\n\n"
            f"I'll ask you {len(questions)} questions. Take your time and answer clearly.\n\n"
            f"💡 Tip: Be specific, use examples, and stay confident!\n\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"Question 1/{len(questions)}:\n{questions[0]}"
        )
        history.append({"role": "assistant", "content": reply})
        return {"reply": reply, "history": history}

    # If we're mid-interview but the message is empty, ask for a real
    # answer instead of treating it as a fresh start.
    if not msg:
        reply = "⚠️ I didn't catch an answer there — could you type your response?"
        return {"reply": reply, "history": history}

    # Add user message to history
    history.append({"role": "user", "content": msg})

    # Interview complete
    if q_index >= len(questions):
        reply = (
            "🎉 Interview Complete!\n\n"
            "You answered all questions. Here's your summary:\n\n"
            f"✅ Questions answered: {len(questions)}\n"
            "📊 Visit the Progress page to see your scores.\n\n"
            "💪 Keep practicing to improve your confidence!\n"
            "Click 'New' to start another round."
        )
        history.append({"role": "assistant", "content": reply})
        return {"reply": reply, "history": history}

    # Validate answer length
    if len(msg) < 10:
        warning = "⚠️ Your answer seems too short. Try to elaborate more.\n\n"
    else:
        warning = ""

    # Pick feedback
    fb = random.choice(FEEDBACK)

    # Next question
    next_q_index = q_index
    if next_q_index < len(questions):
        next_question = (
            f"Question {next_q_index + 1}/{len(questions)}:\n{questions[next_q_index]}"
        )
    else:
        next_question = "That was the last question! Great job completing the interview."

    reply = (
        f"{warning}"
        f"🤖 Feedback: {fb}\n\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"➡️ {next_question}"
    )

    history.append({"role": "assistant", "content": reply})
    return {"reply": reply, "history": history}


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

PRACTICE_QUESTIONS = {
    "arrays": [
        {"question": "Find the maximum subarray sum (Kadane's Algorithm).", "hint": "Keep a running sum, reset when negative.", "difficulty": "Medium"},
        {"question": "Remove duplicates from a sorted array in-place.", "hint": "Use two pointers.", "difficulty": "Easy"},
        {"question": "Rotate an array to the right by K steps.", "hint": "Reverse the whole array, then parts.", "difficulty": "Medium"},
    ],
    "python": [
        {"question": "What is the difference between a list and a tuple?", "hint": "Think mutability.", "difficulty": "Easy"},
        {"question": "Explain decorators in Python with an example.", "hint": "Functions that wrap other functions.", "difficulty": "Medium"},
        {"question": "What are Python generators and when would you use them?", "hint": "Think memory efficiency and yield.", "difficulty": "Medium"},
    ],
    "sql": [
        {"question": "Write a query to find the second highest salary.", "hint": "Use LIMIT/OFFSET or subquery.", "difficulty": "Medium"},
        {"question": "Explain the difference between INNER JOIN and LEFT JOIN.", "hint": "Think about what rows are included.", "difficulty": "Easy"},
        {"question": "What is database indexing and why is it important?", "hint": "Think about query speed.", "difficulty": "Easy"},
    ],
    "default": [
        {"question": "Explain the concept of recursion with an example.", "hint": "Think base case and recursive case.", "difficulty": "Easy"},
        {"question": "What is the difference between stack and queue?", "hint": "Think LIFO vs FIFO.", "difficulty": "Easy"},
        {"question": "Explain time complexity with an example.", "hint": "Think Big O notation.", "difficulty": "Medium"},
    ]
}

@router.post("/practice/questions")
def generate_questions(data: PracticeRequest):
    topic_lower = data.topic.lower()
    if "array" in topic_lower or "string" in topic_lower:
        questions = PRACTICE_QUESTIONS["arrays"]
    elif "python" in topic_lower or "oop" in topic_lower:
        questions = PRACTICE_QUESTIONS["python"]
    elif "sql" in topic_lower or "database" in topic_lower:
        questions = PRACTICE_QUESTIONS["sql"]
    else:
        questions = PRACTICE_QUESTIONS["default"]

    return {"success": True, "questions": questions[:data.count]}


@router.post("/practice/feedback")
def get_feedback(data: FeedbackRequest):
    ans = data.answer.strip()
    if len(ans) < 10:
        feedback = "⚠️ Your answer is too short. Please elaborate with examples and details."
    elif len(ans) < 50:
        feedback = "📝 Decent start! Try to expand your answer with a concrete example or code snippet."
    elif len(ans) < 150:
        feedback = "✅ Good answer! You covered the basics. Adding real-world examples would make it stronger."
    else:
        feedback = "🔥 Excellent detailed answer! You demonstrated strong understanding. Keep it up!"
    return {"success": True, "feedback": feedback}


# ─────────────────────────────────────────
# DASHBOARD ASSISTANT CHATBOT
# ─────────────────────────────────────────
class AssistantRequest(BaseModel):
    message: str
    history: List[dict] = []

ASSISTANT_KB = {
    "tell me about yourself": "Structure your answer in 3 parts: 1) Who you are, 2) Your key skills/experience, 3) Why you're excited about this role. Keep it under 2 minutes. Example: 'I'm a computer science graduate with strong Python and ML skills. I've built 3 projects including an AI chatbot. I'm passionate about solving real problems with AI.'",
    "ats": "ATS (Applicant Tracking System) score measures how well your resume matches a job description. Tips to improve: use keywords from the job posting, use standard section headings like 'Experience' and 'Education', avoid tables/graphics, and save as PDF.",
    "technical interview": "To prepare for technical interviews: 1) Practice DSA on LeetCode daily, 2) Review core CS concepts (OOP, OS, Networks, DB), 3) Build projects to discuss, 4) Practice explaining your thought process out loud, 5) Do mock interviews.",
    "weakness": "When answering 'What is your weakness?': Choose a real weakness that isn't critical to the job. Show self-awareness and explain steps you're taking to improve. Example: 'I sometimes spend too much time perfecting code. I've learned to set time limits and prioritize delivery.'",
    "strength": "For strengths: Pick 2-3 relevant to the role. Back each with a specific example. Example: 'My strength is problem-solving — in my last project I debugged a critical API issue that was blocking the team by using systematic logging.'",
    "salary": "For salary negotiation: Research market rates on Glassdoor/LinkedIn first. Give a range based on your research. Say: 'Based on my research and experience, I'm looking for ₹X-Y. I'm open to discussion based on the full package.'",
    "resume": "Resume tips: Keep it to 1 page, use action verbs (built, designed, improved), add metrics (increased performance by 30%), include GitHub link, list relevant skills, and tailor it for each job.",
    "hr interview": "For HR interviews use the STAR method: Situation, Task, Action, Result. Be honest, show enthusiasm, research the company beforehand, and prepare 3-5 stories that demonstrate your skills.",
    "project": "When explaining your project: 1) What problem it solves, 2) Technologies used, 3) Your specific role/contribution, 4) Challenges faced and how you solved them, 5) Results/impact.",
    "pressure": "To answer 'How do you handle pressure?': Give a real example. 'In my final year project, we had a 48-hour deadline. I broke the task into smaller chunks, prioritized critical features, and communicated progress to my team. We delivered on time.'",
}

@router.post("/assistant")
def assistant(data: AssistantRequest):
    msg = data.message.lower().strip()
    history = data.history.copy()
    history.append({"role": "user", "content": data.message})

    # Match keywords to knowledge base
    reply = None
    for key, answer in ASSISTANT_KB.items():
        if any(word in msg for word in key.split()):
            reply = f"💡 {answer}"
            break

    # Generic responses
    if not reply:
        if any(w in msg for w in ["hi", "hello", "hey"]):
            reply = "👋 Hello! I'm your AI Interview Assistant. Ask me about interview tips, resume advice, or practice questions!"
        elif any(w in msg for w in ["thank", "thanks"]):
            reply = "😊 You're welcome! Best of luck with your interview. You've got this! 💪"
        elif any(w in msg for w in ["interview", "prepare", "preparation"]):
            reply = "🎯 Interview Preparation Tips:\n\n1. Research the company thoroughly\n2. Practice common questions out loud\n3. Prepare 5-6 STAR stories\n4. Review your resume and projects\n5. Dress professionally and arrive early\n6. Ask thoughtful questions at the end"
        elif any(w in msg for w in ["nervous", "anxiety", "scared", "fear"]):
            reply = "😌 Interview nerves are completely normal! Tips to calm down:\n\n1. Prepare thoroughly — confidence comes from preparation\n2. Take deep breaths before entering\n3. Remember they want you to succeed\n4. Treat it as a conversation, not an exam\n5. Practice mock interviews with friends"
        elif any(w in msg for w in ["dsa", "algorithm", "leetcode", "coding"]):
            reply = "💻 DSA Interview Tips:\n\n1. Start with easy LeetCode problems\n2. Master arrays, strings, hashmaps first\n3. Learn binary search and two pointers\n4. Practice trees and graphs\n5. Always explain your approach before coding\n6. Discuss time/space complexity"
        elif any(w in msg for w in ["system design", "design"]):
            reply = "🏗️ System Design Tips:\n\n1. Clarify requirements first\n2. Estimate scale (users, requests/sec)\n3. Draw high-level architecture\n4. Discuss database choices (SQL vs NoSQL)\n5. Talk about caching, load balancing\n6. Address failure scenarios"
        else:
            reply = "🤖 I can help you with:\n\n• Tell me about yourself\n• Technical interview tips\n• Resume & ATS advice\n• HR & behavioral questions\n• Salary negotiation\n• DSA & System Design tips\n• Handling interview nerves\n\nWhat would you like to know?"

    history.append({"role": "assistant", "content": reply})
    return {"reply": reply, "history": history}