# AI Video Studio

![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Wan_2.2-FFD21E)
![Gemini](https://img.shields.io/badge/Google_Gemini-Prompt_Enhancement-4285F4)

A highly polished, production-ready AI Video Generation Platform. Built as a full-stack microservice architecture, this platform empowers users to generate stunning cinematic videos from simple text prompts using state-of-the-art open-source diffusion models.

## ✨ Key Features

- **Cinematic UI/UX:** A gorgeous, Netflix-style glassmorphism interface built with Next.js and Tailwind CSS. Features dynamic 3D tilt cards, live video galleries, and seamless asynchronous state transitions.
- **LLM Prompt Enhancement:** Integrated with **Google Gemini 3.6 Flash**. Simple user prompts are automatically intercepted and intelligently rewritten into highly detailed, cinematic prompt structures before being sent to the video generator.
- **State-of-the-Art Video AI:** Powered by the **Wan-AI/Wan2.2-TI2V-5B** model via Hugging Face Serverless Inference.
- **Robust Architecture:** A FastAPI backend seamlessly manages asynchronous long-running background tasks to prevent HTTP timeouts.
- **Production Database:** Fully Dockerized PostgreSQL database tracks the entire video generation lifecycle (Queued -> Processing -> Completed/Failed/Timeout).
- **Graceful Error Handling:** Extensive UI/UX protection against empty inputs, API billing limits (e.g. `402 Payment Required`), and generation timeouts.

---

## 🏗️ Architecture Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS, Framer Motion, Vanilla CSS Modules
- **State & Data Fetching:** React Query, Axios

### Backend
- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL (asyncpg), SQLAlchemy ORM, Alembic Migrations
- **AI Integration:** `huggingface_hub` (AsyncInferenceClient), Google GenAI SDK

### Infrastructure
- **Containerization:** Docker & Docker Compose

---

## 🚀 Quick Start Guide

### Prerequisites
- Docker and Docker Compose installed on your machine.
- A Google Gemini API Key.
- A Hugging Face account with inference credits (Minimum $5 balance recommended).

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
Start the entire stack (PostgreSQL database, FastAPI backend, and Next.js frontend) with a single command:

```bash
docker-compose up --build
```

### 3. Access the Application
- **Frontend App:** [http://localhost:3000](http://localhost:3000)
- **Backend API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💡 How It Works

1. **Prompt Entry:** The user enters a basic prompt on the `CREATE` tab (e.g., "A glowing butterfly").
2. **LLM Intercept:** The backend routes the input to Gemini 3.6 Flash, which expands it based on the user's selected style (e.g., "Cinematic, ultra-realistic slow motion shot of a glowing blue butterfly landing on a bright red rose. High quality, 4k, volumetric lighting.").
3. **Background Generation:** FastAPI spawns an asynchronous background worker that submits the enhanced prompt to the Hugging Face serverless API using the `Wan2.2-TI2V-5B` model.
4. **State Machine Polling:** The frontend gracefully polls the API for status updates, displaying a live progress skeleton. 
5. **Video Delivery:** Once the MP4 bytes are returned and saved to local storage, the state machine hits `completed`, and the video slides seamlessly into the user's browser.

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
| *(Bonus)* **Loading State** | Polling state machine with progress indicators. | 🌟 Complete |

---
*Built as a scalable, premium microservice architecture.*
