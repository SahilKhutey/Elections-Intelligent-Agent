# 🔧 Services & API Specification - EIA

## 🧠 Overview
The Election Assistant system is built using modular, lightweight services designed for speed and a <10MB footprint. All services are exposed via a **FastAPI** backend.

## 🧩 Service Architecture
```text
Client (Frontend)
        ↓
API Gateway (FastAPI)
        ↓
Core Services
 ├── Intent Detection Service
 ├── Election Knowledge Service
 ├── Timeline Engine
 ├── AI Assistant Service
 └── Session Service
```

## 1. Intent Detection Service
*   **Purpose**: Identify user intent using rule-based logic (No ML).
*   **Logic**:
    *   `if "vote" in query → voting_process`
    *   `if "timeline" in query → election_timeline`
    *   `if "eligible" in query → eligibility_check`

## 2. Election Knowledge Service
*   **Purpose**: Provide structured election data from `/data/*.json`.
*   **Data Sources**: `election_process.json`, `timelines.json`, `faq.json`.

## 3. Timeline Engine
*   **Purpose**: Generate dynamic election timelines using template-based generation.

## 4. AI Assistant Service
*   **Purpose**: Convert structured JSON into human-friendly explanations via external LLM APIs.
*   **Prompt**: "Explain the election process in simple steps for a first-time voter. Keep it short and clear."

## 5. Session Service
*   **Purpose**: Maintain lightweight user context via LocalStorage (Frontend) or In-memory cache (Backend).

## 🌐 API Endpoints (FastAPI)

### 🔹 1. Ask Query (`POST /api/query`)
*   **Input**: `{ "query": string, "location": string }`
*   **Output**: `{ "intent": string, "data": object, "ai_response": string }`

### 🔹 2. Get Timeline (`GET /api/timeline`)
*   **Output**: `{ "timeline": Array }`

### 🔹 3. Eligibility Check (`POST /api/eligibility`)
*   **Input**: `{ "age": integer, "citizenship": string }`
*   **Output**: `{ "eligible": boolean, "message": string }`

### 🔹 4. FAQ Endpoint (`GET /api/faq`)
*   **Output**: `{ "questions": Array }`

## 🔌 External Integrations
*   **LLM API**: Gemini / OpenAI (Response formatting).
*   **Data APIs**: Optional public datasets.

## 🔒 Security & Performance
*   **Validation**: FastAPI Pydantic schemas.
*   **Optimization**: In-memory JSON caching and async endpoints.
*   **Constraint**: Strict `.gitignore` to keep repo <10MB.
