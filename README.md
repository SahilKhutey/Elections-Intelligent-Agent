# 🗳️ Election Intelligence Assistant (EIA)

An elite, government-grade AI-powered election guidance system designed for high credibility, accessibility, and task-driven civic engagement. Aligned with **UX4G (User Experience for Government of India)** standards.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

---

## 🏛️ Project Vision
EIA is designed to bridge the information gap between the Election Commission and citizens. By leveraging multi-provider AI (OpenAI, Gemini, Claude), it transforms complex bureaucratic procedures into simple, actionable guidance tailored to the user's age, location, and eligibility status.

## 🚀 Key Features

- 🏛️ **UX4G Design System**: Professional, high-readability light interface featuring "Govt Blue" palette and task-first hierarchy.
- 🧠 **Context-Aware Intelligence**: Specialized AI personas for **Eligible Voters** vs. **Future Voters** (under 18).
- 📍 **Location Intelligence**: Region-specific announcements (e.g., Bhopal, Delhi, Mumbai) with national-level fallbacks.
- 📋 **Structured Eligibility**: Robust checks for Age, Citizenship, and Residency status.
- 🌍 **Native Multilingualism**: Seamless English and Hindi integration throughout the entire stack.
- 📅 **Interactive Roadmap**: Visualized election timeline and step-by-step registration guides.
- 🛡️ **Admin Portal**: Secure interface for officials to publish urgent public notices.

## 🏗️ Architecture Deep Dive

The system follows a **Modular Monolith** architecture optimized for a <10MB repository footprint:

- **Frontend**: Next.js 14 with App Router. State management via Context API. Components are built using Vanilla CSS tokens to ensure strict UX4G compliance.
- **Backend**: FastAPI with a Service-Oriented architecture. 
    - `AI Service`: Unified interface for OpenAI, Gemini, and Anthropic.
    - `Intent Service`: Rule-based classification for zero-latency routing.
    - `Knowledge Service`: High-speed retrieval from structured JSON repositories.
- **Data Layer**: Optimized JSON stores located in `backend/data/`, ensuring high portability and low overhead.

## 🛠️ Tech Stack

- **Frontend**: Next.js 14 + Vanilla CSS + Lucide Icons
- **Backend**: FastAPI + Pydantic V2 + Anthropic/OpenAI/Google SDKs
- **Infrastructure**: Docker + Docker Compose + Vercel (Frontend)

## 🚀 Quick Start

### 1. Environment Setup
Create a `.env` file in the `backend/` directory:
```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
CLAUDE_API_KEY=your_key
ADMIN_PASSWORD=your_secure_password
ENVIRONMENT=production
```

### 2. Deployment via Docker (Recommended)
```bash
docker-compose up --build
```
The application will be available at `http://localhost:3000`.

### 3. Manual Launch

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run build
npm run start
```

## ✅ Compliance & Standards
- **Accessibility**: WCAG 2.1 AA compliant.
- **Design**: UX4G (Government of India) design tokens.
- **Security**: PII-blind AI processing; secure admin notice publishing.

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created for the High-Impact Civic Intelligence Hackathon 2026.*

