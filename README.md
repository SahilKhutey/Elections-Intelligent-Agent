# 🗳️ Election Intelligence Assistant (EIA)

An elite, government-grade AI-powered election guidance system designed for high credibility, accessibility, and task-driven civic engagement. Built to comply with **UX4G** standards and engineered for maximum code quality.

## 🏛️ Overview
EIA bridges the information gap between the Election Commission and citizens. By leveraging multi-provider AI (Gemini, OpenAI, Claude), it transforms complex bureaucratic procedures into simple, actionable guidance tailored to the user's age, location, and eligibility status.

## 🚀 Key Features
- 🎤 **Voice Assistant**: Integrated bilingual (English/Hindi) voice input and output for enhanced accessibility.
* 📴 **Offline Intelligence**: Robust offline-first layer with a local fuzzy-matching engine.
* 📱 **PWA Ready**: Installable application with advanced service-worker caching for rural resilience.
* ⚡ **Real-Time Streaming**: ChatGPT-style SSE for a high-engagement AI experience.
* 🗺️ **Polling Booth Locator**: Integrated Google Maps for locating nearby voting centers.
* 🛡️ **OWASP Hardened**: Advanced security headers, Pydantic V2 validation, and prompt injection guards.

## 🏗️ Architecture
The system follows a clean, service-oriented architecture:
- **Frontend**: Next.js 14 (App Router) with a task-first UI.
- **Backend**: FastAPI (Service-Oriented) with standardized API responses.
    - `core/`: Configuration and security protocols.
    - `services/`: Encapsulated business logic (AI, Intent, Notices, etc.).
    - `routes/`: Thin API endpoints with strict schema validation.
    - `models/`: Centralized Pydantic schemas.

## 🛠️ Tech Stack
- **Frontend**: Next.js 14, Vanilla CSS, Lucide Icons, Web Speech API.
- **Backend**: FastAPI, Pydantic V2, SSE-Starlette, SlowAPI, PyJWT.
- **AI**: Google Gemini (Primary), OpenAI GPT-3.5/4, Anthropic Claude 3.

## 🔧 Setup & Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Quality Standards
- **Docstrings**: All core functions and classes are documented using professional standards.
- **Type Hints**: 100% coverage of Python type hints for better maintainability.
- **Standardized Responses**: All API endpoints return a consistent `{"status": "success", "data": ...}` format.
- **Validation**: Strict schema enforcement using Pydantic V2.

---
*Developed for the High-Impact Civic Intelligence Hackathon 2026.*
