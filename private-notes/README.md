# 📚 Hirely — Private Technical Study Notes & Interview Preparation Kit

> **CONFIDENTIAL & PRIVATE STUDY MATERIAL**  
> *This directory is strictly for personal interview preparation and technical revision. It is excluded from Git tracking via `.gitignore` and must never be distributed publicly or committed to source control.*

---

## 🎯 Purpose of This Knowledge Base

This repository of notes is engineered to provide an exhaustive, evidence-based, end-to-end technical foundation for answering **Applied AI Engineer**, **AI Backend Engineer**, and **Full-Stack AI Developer** interview questions on the **Hirely** project.

Every architectural claim, data flow, formula, schema, and API endpoint documented across these modules is grounded in the actual codebase at `D:\Hirely` (FastAPI backend, PostgreSQL models, Google Gemini AI pipelines, RAG implementations, Docling document parser, and Docker Compose orchestration).

---

## 🗂️ Module Directory

| Module | File | Core Focus |
| :--- | :--- | :--- |
| **01** | [`01_project_story.md`](./01_project_story.md) | High-level project narrative, problem statement, business value, 60-second elevator pitch, 3-minute deep dive, and interviewer steering strategies. |
| **02** | [`02_project_explanation_hinglish.md`](./02_project_explanation_hinglish.md) | Intuitive Roman-English Hinglish breakdown of all concepts, workflows, and AI pipelines for conversational mastery and easy recall. |
| **03** | [`03_backend_architecture.md`](./03_backend_architecture.md) | Deep architectural dissection of FastAPI, request lifecycle, PostgreSQL schema, SQLAlchemy ORM, Alembic migrations, and RBAC. |
| **04** | [`04_ai_ml_and_rag.md`](./04_ai_ml_and_rag.md) | Comprehensive AI/ML guide: Gemini integration, Docling resume parsing, hybrid ATS scoring, semantic vector embeddings, and RAG Evidence Assistant. |
| **05** | [`05_security_and_reliability.md`](./05_security_and_reliability.md) | Production reliability, Argon2 hashing, JWT stateless auth, multi-layer upload validation, Cloudflare R2 vs local disk, rate limiting, and observability. |
| **06** | [`06_interview_questions.md`](./06_interview_questions.md) | 120 curated interview questions categorized across 15 engineering domains (Beginner $\to$ Intermediate $\to$ Advanced; strictly non-frontend). |
| **07** | [`07_interview_answers_hinglish.md`](./07_interview_answers_hinglish.md) | Matching 120 interview answers with 4-part structure: Simple Hinglish, Professional Technical English, Hirely Code Connection, and Follow-Up Concepts. |
| **08** | [`08_my_contribution_and_gaps.md`](./08_my_contribution_and_gaps.md) | Personal ownership boundaries, verified vs unverified components, honest answer scripts for unfamiliar areas, and a 1-week revision plan. |

*(Each Markdown file has an accompanying compiled `.pdf` document in this folder for portable offline study.)*

---

## 🗓️ Recommended Revision Schedules

### ⏱️ Option A: 1-Week Comprehensive Deep Dive
- **Day 1:** Module 01 (Project Story & 60s/3m pitches) + Module 02 (Conversational Hinglish overview).
- **Day 2:** Module 03 (FastAPI architecture, SQLAlchemy sessions, and Alembic migrations).
- **Day 3:** Module 04 (Hybrid ATS scoring mathematics, Docling parsing, Gemini embeddings, and RAG).
- **Day 4:** Module 05 (Security, Argon2, sliding-window rate limiters, Cloudflare R2, and Observability).
- **Day 5:** Module 06 & 07 (Questions 1 to 60: Backend, Architecture, Security, and Storage).
- **Day 6:** Module 06 & 07 (Questions 61 to 120: AI, LLMs, RAG, Embeddings, and Evaluation).
- **Day 7:** Module 08 (Ownership boundaries, honest gap scripts, mock interview rehearsing).

### ⚡ Option B: 2-Day Accelerated Review
- **Day 1:** Modules 01, 03, and 04 (Core Narrative + Backend Engine + AI/RAG Mechanics).
- **Day 2:** Modules 05, 07, and 08 (Security/Reliability + Questions/Answers review + Gap scripts).

### 🚀 Option C: 30-Minute Pre-Interview Warm-Up
1. Re-read the **60-Second Elevator Pitch** and **3-Minute Deep Dive** in [`01_project_story.md`](./01_project_story.md).
2. Scan the **Core AI Data Flow Diagrams** in [`04_ai_ml_and_rag.md`](./04_ai_ml_and_rag.md).
3. Review the **Honest Ownership Boundaries & Gap Scripts** in [`08_my_contribution_and_gaps.md`](./08_my_contribution_and_gaps.md).

---

## ⚠️ Integrity & Privacy Rules

1. **No External Secrets:** Real API keys, database connection strings, passwords, or personal credentials must never be added to these documents.
2. **Codebase Grounding:** All technical explanations represent the real implementation in `D:\Hirely`. Conceptual examples are explicitly labeled.
3. **No Frontend Ownership Claims:** The React 19 frontend is acknowledged as a consumer of the FastAPI backend, but frontend development is strictly excluded from personal ownership claims.
4. **Git Protection:** This directory is ignored by Git. Do not force-add or remove `.gitignore` protection.
