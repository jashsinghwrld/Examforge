# <p align="center">🛠️ EXAMFORGE</p>

<p align="center">
  <img src="assets/hero.png" alt="Examforge Hero" width="800">
</p>

<p align="center">
  <strong>The Ultimate AI-Powered Study Companion for RGPV Students.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind">
  <img src="https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini">
</p>

---

## 🚀 Overview

**Examforge** is a sophisticated, data-driven web application designed to help students master the **RGPV Bhopal** syllabus (Engineering Physics focus). It bridges the gap between raw textbooks and exam-day performance by generating structured, high-scoring answers ground in curated academic datasets.

### ✨ Key Features

- **🎯 Exam-Ready Answers**: Generates structured, 7-mark style answers optimized for the RGPV pattern.
- **📚 Curated Datasets**: Grounding AI responses in verified syllabus-specific data to prevent hallucination.
- **⚡ Real-time Explanations**: Deep-dives into complex topics with simple, intuitive breakdowns.
- **🔍 Intelligent Search**: Quickly find any topic across the entire module library.
- **🛠️ Zero-Config Setup**: One-click startup script for local execution.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/), Python 3.11+, Uvicorn |
| **Frontend** | [React](https://reactjs.org/), [Vite](https://vitejs.dev/), [Tailwind CSS](https://tailwindcss.com/) |
| **AI Intelligence** | [Google Gemini Flash 1.5](https://aistudio.google.com/) |
| **State Management** | Context API & Hooks |

---

## 📂 Project Structure

```bash
├── 📁 backend/             # FastAPI Python Server
│   ├── 📁 dataset/         # Module-wise JSON grounding data
│   ├── 📁 routes/          # API endpoint logic (Explain, Ask, Search)
│   └── 📜 main.py          # Application entrypoint
├── 📁 frontend/            # React/Vite/Tailwind Application
│   └── 📁 src/             # UI Components & Logic
├── 📁 assets/              # Premium visual branding
├── 📜 start.bat            # Automated Windows startup script
└── 📜 stop.bat             # Graceful shutdown script
```

---

## 🏁 Getting Started (Windows)

### 1️⃣ Prerequisites
- **Python 3.11 or 3.12** installed and added to PATH.
- **Node.js (LTS)** installed.

### 2️⃣ Configure Gemini API
The app uses Google's Gemini AI. You'll need an API key:
1. Get a free key from [AI Studio](https://aistudio.google.com/app/apikey).
2. The `start.bat` script will create a `backend/.env` for you.
3. Open `backend/.env` and paste your key:
   ```env
   GEMINI_API_KEY=your_key_here
   ```

### 3️⃣ Launch
Simply double-click:
```bash
start.bat
```
This script handles virtual environment creation, dependency installation, and launches both servers automatically.

---

## 🧠 How it Works

Examforge isn't just a generic wrapper for AI. It uses a **Hybrid Grounding Architecture**:

1.  **Retrieval**: When you ask a question, the system searches its local **JSON datasets** (Module 1-5) for relevant technical context.
2.  **Context Injection**: This context is injected into a specialized "Exam-Expert" prompt.
3.  **Synthesis**: Gemini AI synthesizes the answer, ensuring it uses the correct terminology and structure required by RGPV examiners.
4.  **Fallback**: If the AI service is unavailable, the system gracefully switches to **Dataset-Only Mode**, providing the raw information from the verified modules.

---

<p align="center">
  <i>Developed with ❤️ for RGPV Students.</i>
</p>
