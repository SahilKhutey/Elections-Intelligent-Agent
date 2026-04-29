# 🧠 Overview - Election Intelligence Assistant (EIA)

The Election Assistant System is a lightweight, AI-powered web application designed to help users understand:
*   Election processes (step-by-step)
*   Timelines and phases
*   Eligibility and participation steps

The system is built with a minimal, scalable architecture using external APIs and static data to ensure the GitHub repository remains under 10MB.

## 🏗️ High-Level Architecture
```text
                ┌──────────────────────┐
                │      Frontend        │
                │  (Next.js / React)   │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │     API Gateway      │
                │      (FastAPI)       │
                └─────────┬────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Knowledge    │  │ Timeline     │  │ AI Assistant │
│ Service      │  │ Engine       │  │ Service      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
 ┌────────────────────────────────────────────┐
 │     Static JSON / External APIs / LLM API  │
 └────────────────────────────────────────────┘
```

## 🧩 Core Components

### 1. Frontend Layer
*   **Tech Stack**: Next.js / React, Tailwind CSS.
*   **Responsibilities**: User interaction (chat + guided flows), display structured responses (steps, timelines), manage session locally.

### 2. API Gateway (FastAPI)
*   **Purpose**: Central orchestrator between frontend and services.
*   **Responsibilities**: Route user requests, perform lightweight validation, call internal services, aggregate responses.

### 3. Knowledge Service
*   **Purpose**: Provides structured election-related information.
*   **Data Source**: Static JSON files (lightweight, <500KB total).
*   **Examples**: Voting steps, required documents, eligibility rules.

### 4. Timeline Engine
*   **Purpose**: Generates election timelines dynamically.
*   **Approach**: Template-based generation, configurable for different regions.

### 5. AI Assistant Service
*   **Purpose**: Transforms structured data into natural, easy-to-understand responses.
*   **Implementation**: External LLM APIs (Gemini / OpenAI) via prompt engineering.

### 6. Intent Detection Layer
*   **Type**: Rule-based (lightweight) to avoid heavy ML models.
*   **Examples**: "How do I vote?" → `voting_process`, "Election dates?" → `timeline_query`.

### 7. Data Layer
*   **Structure**: `/data` directory containing `election_process.json`, `timelines.json`, `faq.json`.

## 🔁 Data Flow
1.  User inputs a query (e.g., “How do I vote?”).
2.  **API Gateway**: Detects intent and routes to relevant services.
3.  **Knowledge Service**: Fetches structured data from JSON.
4.  **AI Service**: Enhances the explanation with natural language.
5.  **Response**: Returned as step-by-step guidance + optional timeline visualization.

## 📦 Repository Size Optimization (<10MB)
*   ❌ No large datasets or local ML models.
*   ❌ No heavy assets (images/videos).
*   ✅ Use external APIs and CDN-hosted libraries.
*   ✅ Strict `.gitignore` (exclude `node_modules`, `.env`).

## 🔒 Security Considerations
*   Input validation via FastAPI.
*   Rate limiting middleware.
*   No sensitive data storage; API keys in environment variables.

## ✅ Summary
This architecture is optimized for hackathon constraints: lightweight, fast, easy to deploy, and scalable for future growth.
