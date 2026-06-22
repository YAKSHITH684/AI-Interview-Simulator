# 🤖 AI Interview Simulator

> **An intelligent interview preparation platform powered by Groq AI (Llama 3.3).**  
> Analyze resumes, practice with a real AI interviewer, and track your growth — all in one platform.

🔗 **Live Demo:** [https://ai-interview-simulator-1-xp6n.onrender.com](https://ai-interview-simulator-1-xp6n.onrender.com/index.html)  
🔧 **Backend API:** [https://ai-interview-simulator-316l.onrender.com](https://ai-interview-simulator-316l.onrender.com)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Intelligence** | Upload PDF/DOCX → AI gives ATS score, skills, strengths, suggestions |
| 🤖 **AI Interviewer** | Real Groq AI interview — Technical, HR, System Design, DSA modes |
| 🎯 **Practice Mode** | Topic-based questions with personalized AI feedback per answer |
| 📊 **Progress Tracking** | AI resume dashboard with skill breakdown and readiness score |
| 💬 **AI Assistant** | Floating chatbot on dashboard for instant interview tips |
| 🔐 **User Auth** | Register, Login, Forgot Password with SQLite database |

---

## 🚀 How It Works

```
01. Upload Resume  →  Groq AI scores ATS, extracts skills, gives suggestions
02. Get Insights   →  Skill breakdown, strengths, gaps, readiness score
03. Practice       →  Real AI interview with dynamic questions and feedback
04. Track Progress →  Monitor improvement and readiness over time
```

---

## 🛠️ Tech Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Glass morphism UI with background images
- Fully responsive design
- Hosted on **Render Static Site**

### Backend
- **Python 3** + **FastAPI**
- **SQLAlchemy** + **SQLite** for user database
- **Groq API** (Llama 3.3-70b-versatile) for all AI features
- **pdfplumber** + **python-docx** for resume parsing
- Hosted on **Render Web Service**

---

## 🗂️ Project Structure

```
AI-Interview-Simulator/
├── Frontend/
│   ├── index.html              # Dashboard + floating AI assistant
│   ├── resume.html             # Resume upload and AI analysis
│   ├── ai_analysis.html        # Deep AI resume analysis
│   ├── interview.html          # AI Interview Chat
│   ├── Practice.html           # Practice mode with AI feedback
│   ├── progress.html           # Progress tracking dashboard
│   ├── resources.html          # Interview resources
│   ├── 01_login.html           # Login page
│   ├── 02_register.html        # Register page
│   ├── 03_forgot_password.html # Forgot password
│   ├── style.css
│   └── script.js
│
└── Backend/
    ├── app.py                  # FastAPI entry point
    ├── routes.py               # All API routes with Groq AI
    ├── requirements.txt
    └── database/
        ├── database.py         # SQLAlchemy setup
        └── models.py           # User model
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | User registration |
| POST | `/login` | User login |
| POST | `/forgot-password` | Reset password |
| POST | `/analyze-resume` | AI resume analysis (Groq) |
| POST | `/chat` | AI interview chat (Groq) |
| POST | `/assistant` | Dashboard AI chatbot (Groq) |
| POST | `/practice/questions` | Generate practice questions |
| POST | `/practice/feedback` | AI feedback on answers (Groq) |
| POST | `/ai-analysis` | Deep resume analysis (Groq) |

---

## ⚙️ Local Setup

```bash
# Clone the repository
git clone https://github.com/YAKSHITH684/AI-Interview-Simulator.git
cd AI-Interview-Simulator/Backend

# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
# Windows:
set GROQ_API_KEY=your_groq_api_key_here
# Mac/Linux:
export GROQ_API_KEY=your_groq_api_key_here

# Run backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Open Frontend/index.html in your browser
```

---

## 🔑 Environment Variables

| Variable | Where to Get |
|---|---|
| `GROQ_API_KEY` | Free at [console.groq.com](https://console.groq.com) |

---

## 🌐 Deployment

- **Frontend** → Render Static Site
- **Backend** → Render Web Service
- **Start Command:** `uvicorn app:app --host 0.0.0.0 --port 10000`

---

## 🤖 AI Integration

All AI features are powered by **Groq API** using the **Llama 3.3-70b-versatile** model:

- **Resume Analysis** — reads uploaded PDF/DOCX and returns structured JSON with ATS score, skills, strengths, suggestions, skill breakdown
- **Interview Chat** — full conversation history sent on every request for context-aware dynamic questions and feedback
- **Practice Feedback** — evaluates candidate answers and gives specific improvement tips
- **Dashboard Assistant** — general interview coaching chatbot with fallback knowledge base

---

## 👨‍💻 About This Project

**AI Interview Simulator** was built to solve a real problem — most students and job seekers  
struggle with interview preparation because they lack access to realistic practice environments.

This platform brings together **Artificial Intelligence, Resume Analysis, and Mock Interviews**  
into one seamless experience, making quality interview prep accessible to everyone.

**What makes it stand out:**
- Real AI powered by **Groq Llama 3.3** — not hardcoded questions
- Live deployed and accessible from anywhere
- Full stack application: Python FastAPI backend + modern HTML/CSS/JS frontend
- Supports real resume parsing from PDF, DOCX, and TXT formats
- Interview questions dynamically adapt based on your answers
- Built with production-level practices: REST API, database, authentication, deployment

---


---

## 📅 Project Timeline (1 Month)

| Week | Phase | What Was Built |
|---|---|---|
| **Week 1** | Planning & Setup | Project structure, FastAPI backend setup, SQLite database, user authentication (register/login/forgot password) |
| **Week 2** | Core Features | Resume upload & parsing (PDF/DOCX), keyword-based ATS scoring, frontend pages (dashboard, resume, progress) |
| **Week 3** | AI Integration | Groq API integration (Llama 3.3), real AI interview chat, dynamic question generation, personalized feedback |
| **Week 4** | Polish & Deploy | AI assistant chatbot, UI improvements, bug fixes, deployment on Render, README and documentation |

---

## 📊 Project Statistics

| Metric | Count |
|---|---|
| 📁 Total Files | 20+ |
| 💻 Frontend Pages | 10 HTML pages |
| 🔌 API Endpoints | 9 REST endpoints |
| 🧠 AI Features | 5 (chat, resume, analysis, practice, assistant) |
| 🎯 Interview Modes | 4 (Technical, HR, System Design, DSA) |
| 📝 Lines of Code | 3000+ |
| 🗄️ Database Tables | 1 (Users) |
| ☁️ Deployments | 2 (Frontend + Backend on Render) |
| 🤖 AI Model | Llama 3.3-70b-versatile (Groq) |
| 📄 Resume Formats | PDF, DOCX, TXT |

---

## 🔮 Future Plans (Phase 2)

- [ ] Store interview history per user in database
- [ ] Score card at end of each interview session
- [ ] Voice interview mode (speech to text)
- [ ] Resume builder with AI suggestions
- [ ] Company-specific interview preparation
- [ ] Leaderboard and ranking system
- [ ] Email notifications and reminders
- [ ] Mobile app version

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

---

<p align="center">
  Made with ❤️ for placement preparation<br><br>
  <a href="https://ai-interview-simulator-1-xp6n.onrender.com/index.html">
    <strong>🚀 Try the Live Demo »</strong>
  </a>
</p>
