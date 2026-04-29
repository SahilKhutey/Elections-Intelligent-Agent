# 🚀 Production Deployment Guide - EIA

This guide provides step-by-step instructions for deploying the **Election Intelligence Assistant (EIA)** to a production environment using **Vercel** (Frontend) and **Render** (Backend).

## 📋 Prerequisites
- A [GitHub](https://github.com/) account with the repository pushed.
- A [Vercel](https://vercel.com/) account for the frontend.
- A [Render](https://render.com/) or [Railway](https://railway.app/) account for the backend.
- API Keys for OpenAI, Google Gemini, and Anthropic Claude.

---

## 🛠️ Step 1: Deploy the Backend (API Core)
The backend is containerized and ready for Docker-based deployment.

1.  **Log in to [Render.com](https://render.com/)**.
2.  Click **New +** > **Web Service**.
3.  Connect your GitHub repository: `SahilKhutey/Elections-Intelligent-Agent`.
4.  **Configuration**:
    *   **Name**: `eia-backend`
    *   **Root Directory**: `backend` (Important)
    *   **Runtime**: `Docker`
5.  **Environment Variables**:
    Add the following in the "Environment" tab:
    - `OPENAI_API_KEY`: `your_openai_key`
    - `GEMINI_API_KEY`: `your_gemini_key`
    - `CLAUDE_API_KEY`: `your_anthropic_key`
    - `ADMIN_PASSWORD`: `your_secure_password`
    - `ENVIRONMENT`: `production`
    - `CORS_ORIGINS`: `["https://your-frontend-domain.vercel.app"]`
6.  **Deploy**: Click **Create Web Service**.
7.  **Copy the URL**: Once deployed, copy the service URL (e.g., `https://eia-backend.onrender.com`).

---

## 💻 Step 2: Deploy the Frontend (UI)
The frontend is a Next.js application optimized for Vercel.

1.  **Log in to [Vercel.com](https://vercel.com/)**.
2.  Click **Add New** > **Project**.
3.  Import the repository: `SahilKhutey/Elections-Intelligent-Agent`.
4.  **Project Settings**:
    *   **Framework Preset**: `Next.js`
    *   **Root Directory**: `frontend` (Important: Click "Edit" and select the `frontend` folder).
5.  **Environment Variables**:
    Add the following:
    - `NEXT_PUBLIC_API_URL`: `https://eia-backend.onrender.com` (Use your actual backend URL).
6.  **Deploy**: Click **Deploy**.
7.  **Verification**: Your app should now be live at `https://your-project-name.vercel.app`.

---

## ✅ Step 3: Final Integration Check
1.  Open your frontend URL.
2.  Type a test query (e.g., "Am I eligible to vote?").
3.  Ensure the AI response loads correctly.
4.  Verify the **Admin Portal** by publishing a test notice with your `ADMIN_PASSWORD`.

## 🛡️ Security Best Practices
- **Restrict CORS**: Update `CORS_ORIGINS` in the backend settings to only allow your Vercel domain.
- **Key Rotation**: Regularly update your API keys in the respective cloud dashboards.
- **Health Monitoring**: Use the `validate_backend.py` script locally to check system health if you make changes.

---
*Status: Ready for Launch*
