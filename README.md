````md
# 🤖 AI Interview Simulator

> Transform your interview preparation using Artificial Intelligence.
> Analyze resumes, practice interviews, and track your growth — all in one platform.

🔗 Live Demo:
https://ai-interview-simulator-1-xp6n.onrender.com/index.html

---

## ✨ Features

### 📄 Resume Intelligence
Upload resumes and receive:

- ATS Score
- Resume Score
- Skill Extraction
- Readiness Score
- AI Suggestions

Supported formats:
- PDF
- DOCX
- TXT

---

### 🤖 AI Interviewer

Experience realistic interview sessions.

Modes:
- Technical
- HR
- System Design
- DSA

Features:
- Dynamic questions
- Interview feedback
- Performance evaluation
- Multiple rounds

---

### 📊 Progress Tracking

Track:

- Interview readiness
- Performance growth
- Practice history
- Completion status

---

### 🎯 Practice Mode

Generate questions for:

- Python
- SQL
- Arrays
- DSA
- General CS Concepts

Receive instant AI feedback.

---

### 💬 Dashboard Assistant

Get help with:

- Resume Tips
- ATS Guidance
- Interview Preparation
- Salary Discussions
- Career Advice

---

## 🛠 Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- FastAPI
- Python

### Database
- SQLite

### Libraries
- Pydantic
- pdfplumber
- python-docx

---

# 📁 Project Structure

```bash
AI-Interview-Simulator
│
├── Backend
│   ├── app.py
│   ├── routes.py
│   ├── database
│   │    ├── database.py
│   │    └── models.py
│   │
│   └── requirements.txt
│
├── Frontend
│   ├── index.html
│   ├── dashboard.html
│   ├── interview.html
│   ├── progress.html
│   └── assets
│
└── README.md
````

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YAKSHITH684/AI-Interview-Simulator.git
cd AI-Interview-Simulator
```

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn app:app --reload
```

Open:

```bash
http://127.0.0.1:8000
```

Swagger:

```bash
http://127.0.0.1:8000/docs
```

---

# 🔌 API Routes

## Authentication

```http
POST /register
POST /login
POST /forgot-password
```

---

## Resume Analysis

```http
POST /analyze-resume
```

---

## Interview

```http
POST /chat
```

---

## Practice

```http
POST /practice/questions
POST /practice/feedback
```

---

## Assistant

```http
POST /assistant
```

---

# 📸 Screenshots

Add screenshots:

* Dashboard
* Upload Resume
* AI Analysis
* Interview Chat
* Progress
* Practice Page

---

# 🌟 Future Improvements

* LLM Integration
* Voice Interviews
* JWT Authentication
* Docker Support
* Cloud Deployment
* Analytics Dashboard

---

# 👨‍💻 Author

### Yakshith

⭐ Star the repository if you found it useful.

Made with ❤️ using FastAPI + Python

```
```
