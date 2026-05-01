# 🗳️ Election Intelligence Assistant (EIA)

An elite, government-grade AI-powered election guidance system designed for high credibility, accessibility, and task-driven civic engagement. Aligned with **UX4G (User Experience for Government of India)** standards.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Framework: FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)](https://fastapi.tiangolo.com/)

---

## 🏛️ Project Vision
EIA is designed to bridge the information gap between the Election Commission and citizens. By leveraging multi-provider AI (OpenAI, Gemini, Claude), it transforms complex bureaucratic procedures into simple, actionable guidance tailored to the user's age, location, and eligibility status.

## 🚀 Key Features (v2.0 - Production Grade)

- 📴 **Offline Intelligence**: Resilient offline-first layer with fuzzy-matching logic for instant guidance without internet.
- ⚡ **Real-Time Streaming**: ChatGPT-style SSE (Server-Sent Events) for a high-engagement, "live typing" AI experience.
- 🗺️ **Polling Booth Locator**: Integrated Google Maps with Geolocation to find and navigate to nearby voting centers.
- 🔐 **Secure Sessions**: Stateless JWT-based authentication for persistent context and secure user journeys.
- 🌍 **Multilingual Mastery**: Native support for English and Hindi with dynamic Google Cloud Translation fallback.
- 🏛️ **UX4G Design System**: Premium, high-readability interface featuring the "Govt Blue" palette.
- 🛡️ **OWASP Hardening**: Advanced security headers, Pydantic input validation, and prompt injection guards.

## 🏗️ Architecture Deep Dive

- **Frontend**: Next.js 14 (App Router). State via Context API. Real-time stream processing via `ReadableStream`.
- **Backend**: FastAPI (Service-Oriented).
    - `AI Service`: Unified interface for OpenAI, Gemini, and Anthropic with streaming support.
    - `Security Layer`: JWT verification, Rate Limiting (SlowAPI), and OWASP Headers.
    - `Offline Service`: Robust word-intersection engine for local Q&A.
- **Data Layer**: Optimized JSON stores (`backend/data/`) for booths and offline knowledge.

## 🧪 Testing & Reliability
- **Backend**: Full `pytest` suite with **16+ test cases** covering Query Logic, Eligibility, Timeline, Offline Matching, and Security.
- **Frontend**: `Jest` + `React Testing Library` for component and utility verification.
- **Coverage**: Targets 80%+ critical path coverage.

## 🛡️ Security Protocol
- **A03: Injection**: Strict Pydantic Field validation + Regex patterns.
- **A05: Misconfig**: Custom Security Headers Middleware (CSP, XSS, HSTS).
- **Abuse Control**: IP-based rate limiting on all intelligence endpoints.
- **AI Safety**: Prompt injection filters and response length caps.

## 🛠️ Tech Stack
- **Frontend**: Next.js 14 + Vanilla CSS + Google Maps API
- **Backend**: FastAPI + Pydantic V2 + SSE-Starlette + python-jose
- **AI**: Gemini (Primary), OpenAI, Anthropic

## 🚀 Quick Start

### 1. Environment Setup
Create a `.env` in `backend/`:
```env
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
ADMIN_PASSWORD=your_secure_password
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_key
```

### 2. Launch
**Backend:**
```bash
cd backend && pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000
```
**Frontend:**
```bash
cd frontend && npm install && npm run dev
```

---
*Developed for the High-Impact Civic Intelligence Hackathon 2026.*
