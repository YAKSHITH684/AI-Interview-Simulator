# 🎯 AI Interview Simulator

An AI-powered interview preparation platform that helps students and job seekers practice technical and HR interviews through intelligent resume analysis, question generation, and performance feedback.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🚀 Features

✅ User Authentication (Register/Login)

✅ Resume Upload & Management

✅ AI Resume Analysis

✅ Technical Interview Simulation

✅ HR Interview Simulation

✅ Dynamic Question Generation

✅ Real-Time Performance Feedback

✅ Interview Score Tracking

✅ Secure Database Storage

✅ FastAPI REST APIs

---

## 🛠️ Tech Stack

### Backend

* 🐍 Python
* ⚡ FastAPI
* 🗄️ SQLAlchemy
* 💾 SQLite
* 🚀 Uvicorn

### Frontend

* 🌐 HTML5
* 🎨 CSS3
* ⚙️ JavaScript

### Version Control

* 🔧 Git
* 🐙 GitHub

---

## 📂 Project Structure

```text
AI-Interview-Simulator/
│
├── Backend/
│   ├── database/
│   │   ├── database.py
│   │   ├── models.py
│   │   └── schema.sql
│   │
│   ├── routes/
│   ├── app.py
│   ├── requirements.txt
│   └── users.db
│
├── Frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── Uploads/
├── Tests/
├── README.md
└── .gitignore
```

---

## 🎯 Project Workflow

```text
User Login/Register
          │
          ▼
 Resume Upload
          │
          ▼
 Resume Analysis
          │
          ▼
 AI Question Generation
          │
          ▼
 Mock Interview Session
          │
          ▼
 Answer Evaluation
          │
          ▼
 Feedback & Score
```

---

## 🗄️ Database Design

### 👤 Users Table

| Column        | Type     |
| ------------- | -------- |
| id            | Integer  |
| username      | String   |
| email         | String   |
| password_hash | String   |
| created_at    | DateTime |

### 🎤 Interview Sessions

| Column         | Type     |
| -------------- | -------- |
| id             | Integer  |
| user_id        | Integer  |
| interview_type | String   |
| score          | Integer  |
| feedback       | Text     |
| created_at     | DateTime |

---

## 🔗 API Endpoints

### 🔐 Authentication

| Method | Endpoint  |
| ------ | --------- |
| POST   | /register |
| POST   | /login    |

### 📄 Resume

| Method | Endpoint         |
| ------ | ---------------- |
| POST   | /upload-resume   |
| GET    | /resume-analysis |

### 🎯 Interview

| Method | Endpoint       |
| ------ | -------------- |
| GET    | /questions     |
| POST   | /submit-answer |
| GET    | /feedback      |

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YAKSHITH684/AI-Interview-Simulator.git
```

### 2️⃣ Navigate to Project

```bash
cd AI-Interview-Simulator
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run FastAPI Server

```bash
uvicorn app:app --reload
```

### 5️⃣ Open Browser

```text
http://127.0.0.1:8000
```

### 6️⃣ API Documentation

```text
http://127.0.0.1:8000/docs
```

---

## 🔒 Security Features

* 🔐 Password Hashing
* 🛡️ Input Validation
* 🚫 SQL Injection Protection
* 📂 Secure File Upload Handling
* 🔑 Authentication System

---

## 📈 Future Enhancements

### Version 2.0

* 🤖 Advanced AI Feedback
* 📊 Analytics Dashboard
* 📈 Performance Reports

### Version 3.0

* 🎙️ Voice Interviews
* 🎥 Video Interviews
* 🧠 AI Avatar Interviewer

### Version 4.0

* 🏢 Company-Specific Interview Prep
* 💻 Coding Interview Simulator
* 🌍 Multi-Language Support

---

## ☁️ Deployment Targets

* 🚀 Render
* 🚂 Railway
* ☁️ AWS
* 🔷 Azure
* 🌐 Google Cloud

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository 🍴
2. Create a feature branch 🌱
3. Commit changes 💾
4. Push to GitHub 🚀
5. Open a Pull Request 🎉

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

---

## 📜 License

This project is licensed under the MIT License.
