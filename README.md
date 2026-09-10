<div align="center">
  
# 🎬 Videa-AI: Cinematic AI Video Studio

[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-Wan_2.2-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-Prompt_Enhancer-4285F4?style=for-the-badge&logo=google)](https://deepmind.google/technologies/gemini/)

*A highly polished, production-ready AI Video Generation Platform. Built as a full-stack microservice architecture, Videa-AI empowers users to generate stunning cinematic videos from simple text prompts using state-of-the-art open-source diffusion models.*

</div>

---

## ✨ Enterprise-Grade Features

*   🎥 **Cinematic UI/UX:** A gorgeous, Netflix-style glassmorphism interface built with Next.js and Tailwind CSS. Features dynamic 3D tilt cards, live video galleries, and seamless asynchronous state transitions.
*   🧠 **LLM Prompt Enhancement Pipeline:** Simple user prompts are automatically intercepted by **Google Gemini 3.6 Flash**. The LLM intelligently rewrites basic ideas into highly detailed, cinematic prompt structures before hitting the video generator.
*   🚀 **State-of-the-Art Video AI:** Powered by the open-source **Wan-AI/Wan2.2-TI2V-5B** model via Hugging Face Serverless Inference.
*   ⚙️ **Robust Asynchronous Architecture:** A FastAPI backend seamlessly manages asynchronous long-running background tasks. This completely eliminates HTTP timeout bottlenecks commonly found in standard synchronous REST APIs.
*   💾 **Production Database:** A fully Dockerized PostgreSQL database meticulously tracks the entire video generation lifecycle (**Queued** → **Processing** → **Completed** / **Failed** / **Timeout**).
*   🛡️ **Graceful Error Handling:** 360-degree UI/UX protection against empty inputs, API billing limits (e.g., `402 Payment Required`), SSL network drops, and generation timeouts.

---

## 🏗️ Architecture & Tech Stack

### 🎨 Frontend Layer
*   **Framework:** Next.js 14 (App Router)
*   **Styling:** Tailwind CSS, Framer Motion, Vanilla CSS Modules
*   **State & Data Fetching:** React Query (TanStack), Axios
*   **Animations:** GSAP, custom CSS transitions

### 🧠 Backend Layer
*   **Framework:** FastAPI (Python 3.12)
*   **Database:** PostgreSQL (asyncpg), SQLAlchemy ORM, Alembic Migrations
*   **AI Integrations:** 
    *   `huggingface_hub` (AsyncInferenceClient) for video generation.
    *   `google-genai` SDK for prompt enhancement.

### 🐳 Infrastructure Layer
*   **Containerization:** Docker & Docker Compose
*   **Microservices:** Isolated containers for the Frontend, Backend API, and Database.

---

## 📝 Design Decisions & Constraints

**Why Hugging Face & Wan 2.2?**
During research, many premium video APIs (like Kling or Luma) required expensive upfront subscriptions to access their developer endpoints. To build a robust, cost-effective prototype, Videa-AI integrates the open-source **Wan-AI/Wan2.2-TI2V-5B** model via Hugging Face Serverless Inference, funded via a small  credit allocation. 

**Why is it not hosted live on Vercel?**
While the application is fully Dockerized and inherently ready for cloud production, it is currently not hosted on a public URL. Because the video generation API relies on a strictly limited  budget, leaving the platform publicly accessible would expose the API keys to exhaustion by public traffic. The project is designed to be easily spun up locally via Docker.

---

## 🚀 Quick Start Guide

### Prerequisites
*   Docker and Docker Compose installed on your machine.
*   A [Google Gemini API Key](https://aistudio.google.com/app/apikey).
*   A [Hugging Face](https://huggingface.co/) account with inference credits (Minimum  balance recommended) and a Fine-grained Access Token.

### 1. Environment Setup
Create a `.env` file in the root directory and populate it with your credentials:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/ai_video_studio

# Gemini API Key (Prompt Enhancement)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# Hugging Face Configuration (Video Generation)
VIDEO_PROVIDER=huggingface
HF_TOKEN=your_hugging_face_finegrained_token_here
```

### 2. Launch the Platform
Start the entire microservice stack (PostgreSQL database, FastAPI backend, and Next.js frontend) with a single command:

```bash
docker-compose up --build
```

### 3. Access the Application
*   **Frontend Web App:** [http://localhost:3000](http://localhost:3000)
*   **Backend API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💡 How It Works (The Lifecycle)

1.  **Prompt Entry:** The user enters a basic prompt on the `CREATE` tab (e.g., "A glowing butterfly").
2.  **LLM Intercept:** The backend routes the input to Gemini 3.6 Flash, which expands it based on the user's selected style (e.g., *"Cinematic, ultra-realistic slow motion shot of a glowing blue butterfly landing on a bright red rose. High quality, 4k, volumetric lighting."*).
3.  **Background Generation:** FastAPI spawns an asynchronous background worker that submits the enhanced prompt to the Hugging Face serverless API.
4.  **State Machine Polling:** The frontend gracefully polls the API for status updates, displaying a live progress skeleton. 
5.  **Video Delivery:** Once the MP4 bytes are returned and saved to local storage, the state machine hits `completed`, and the video slides seamlessly into the user's browser for playback or download.

---

## 📜 Assessment Requirements Fulfilled

| Requirement | Implementation Details | Status |
|-------------|------------------------|--------|
| **Prompt Input** | Clean, validated text box with intelligent error states. | ✅ Complete |
| **Video Generation** | Hugging Face Serverless API running `Wan-AI/Wan2.2` model. | ✅ Complete |
| **Display Output** | Beautiful seamless video player with native Download functionality. | ✅ Complete |
| **History Gallery** | PostgreSQL-backed live background-playing video gallery (Last 5 videos). | ✅ Complete |
| **Error Handling** | 360-degree protection: Empty prompts, API timeouts, and Provider failures. | ✅ Complete |
| *(Bonus)* **Styles** | Dynamically driven by Gemini LLM. | 🌟 Complete |
| *(Bonus)* **Loading State** | Asynchronous polling state machine with progress indicators. | 🌟 Complete |

---

<div align="center">
  <i>Designed and engineered by Sanket Shakya for the AI/ML Engineer Internship Assessment.</i>
</div>
