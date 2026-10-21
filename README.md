# 🚀 Hirely — AI-Powered Recruitment & Career Intelligence Platform

> **Hirely is a startup-grade, dual-sided AI recruitment platform connecting candidates and recruiters through intelligent job discovery, structured application management, candidate-facing career tools, recruiter talent intelligence, and an evidence-grounded AI matching engine.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite)](https://vitejs.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.19-1F2937)](https://alembic.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2.13-E92063)](https://docs.pydantic.dev/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)](https://ai.google.dev/)
[![Docling](https://img.shields.io/badge/Docling-Parser-FF6F00)](https://github.com/DS4SD/docling)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Unspecified-lightgrey)](#-license)

---

## 📌 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Key Features & Implementation Status](#-key-features--implementation-status)
- [🏗️ System Architecture](#️-system-architecture)
- [💼 Recruitment Workflows](#-recruitment-workflows)
- [🤖 AI Capabilities & Architecture](#-ai-capabilities--architecture)
  - [📊 Hybrid ATS Analyzer](#-hybrid-ats-analyzer)
  - [🛠️ AI Resume Improvement](#️-ai-resume-improvement)
  - [📝 AI Cover Letter Generator](#-ai-cover-letter-generator)
  - [🎓 AI Career Coach](#-ai-career-coach)
  - [📋 AI Job Description Analyzer](#-ai-job-description-analyzer)
  - [🔍 Recruiter Candidate Intelligence & Matching](#-recruiter-candidate-intelligence--matching)
  - [📑 Candidate Resume Evidence Assistant (RAG)](#-candidate-resume-evidence-assistant-rag)
- [🔐 Security, Observability & Reliability](#-security-observability--reliability)
- [🗄️ Database Architecture](#️-database-architecture)
- [📂 Project Structure](#-project-structure)
- [🛠️ Technology Stack](#️-technology-stack)
- [🐳 Docker Compose Quickstart](#-docker-compose-quickstart)
- [⚙️ Local Manual Setup](#️-local-manual-setup)
- [🔑 Environment Variables](#-environment-variables)
- [🧪 Testing & Quality Assurance](#-testing--quality-assurance)
- [🔌 API Reference](#-api-reference)
- [🎨 Frontend Overview](#-frontend-overview)
- [🔒 Security & Production Limitations](#-security--production-limitations)
- [🗺️ Future Roadmap](#️-future-roadmap)
- [📚 Documentation](#-documentation)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

# 🎯 Project Overview

**Hirely** is a dual-sided AI-assisted recruitment platform built to bridge candidates and recruiters within a unified, interactive recruitment ecosystem.

Traditional hiring platforms often separate job applications, ATS screening, resume optimization, and recruiter candidate evaluation. Hirely unifies these operations by coupling deterministic business logic and role-based permissions with assistive generative AI, semantic vector embeddings, and Retrieval-Augmented Generation (RAG).

```
                             ┌─────────────────────┐
                             │       HIRELY        │
                             │ AI Recruitment      │
                             │     Platform        │
                             └──────────┬──────────┘
                                        │
                       ┌────────────────┴────────────────┐
                       │                                 │
                       ▼                                 ▼
                 👤 CANDIDATE                      🏢 RECRUITER
                       │                                 │
           ┌───────────┴───────────┐         ┌───────────┴───────────┐
           ▼                       ▼         ▼                       ▼
      Find Jobs               AI Career  Post & Manage          AI Talent
     & Direct App              Tools     Open Roles           Intelligence
           │                       │         │                       │
           └───────────┬───────────┘         └───────────┬───────────┘
                       │                                 │
                       └────────────────┬────────────────┘
                                        │
                                        ▼
                             🤖 AI & MATCHING ENGINE
                               Deterministic Scoring
                               Semantic Embeddings
                               RAG Evidence Extraction
                               Grounded Match Explanations
```

### Core Engineering Principles
- **Deterministic Critical Logic:** Authorization, security, application state machines, and numerical scoring remain deterministic in backend code. Language models never make authorization or hiring decisions.
- **Grounded AI Generation:** AI prompts are supplied with bounded, structured context. Models are instructed to evaluate only provided evidence, avoiding hallucinated credentials or experience.
- **Structured Pydantic Validation:** All LLM outputs are validated against strict Pydantic schemas before reaching the client.
- **Privacy-Preserving Telemetry:** User resumes, raw prompt text, credentials, and PII are strictly excluded from logging statements.
- **Defense-in-Depth:** Input validation, sliding-window rate limiting, and multi-layer file upload checks protect service boundaries.

---

# ✨ Key Features & Implementation Status

### ✅ Implemented & Fully Verified in Source Code

| Domain | Implemented Features | Source Evidence |
| :--- | :--- | :--- |
| **Authentication & RBAC** | Argon2 password hashing, JWT bearer tokens, role separation (`candidate`, `recruiter`), sliding-window auth rate limiting per IP. | [`backend/app/api/auth.py`](file:///D:/Hirely/backend/app/api/auth.py), [`backend/app/core/rate_limit.py`](file:///D:/Hirely/backend/app/core/rate_limit.py) |
| **Candidate Core** | Profile management, skill tags CRUD, PDF resume upload, file validation, Docling text/skill parsing, active resume selection, job discovery, direct application. | [`backend/app/api/candidate.py`](file:///D:/Hirely/backend/app/api/candidate.py), [`backend/app/api/resumes.py`](file:///D:/Hirely/backend/app/api/resumes.py) |
| **Candidate AI Suite** | **ATS Resume Analyzer V1** (hybrid 45/15/30/10 scoring), **AI Resume Improvement**, **AI Cover Letter Generator**, **AI Career Coach**. | [`backend/app/ai/ats_analyzer`](file:///D:/Hirely/backend/app/ai/ats_analyzer), [`backend/app/ai/resume_improvement`](file:///D:/Hirely/backend/app/ai/resume_improvement) |
| **Recruiter Core** | Recruiter profile, company association, job creation & management, application pipeline, status transitions (`applied` $\to$ `shortlisted` $\to$ `interview` $\to$ `hired` / `rejected`). | [`backend/app/api/recruiter.py`](file:///D:/Hirely/backend/app/api/recruiter.py), [`backend/app/api/applications.py`](file:///D:/Hirely/backend/app/api/applications.py) |
| **Recruiter AI Suite** | **AI Job Description Analyzer**, **Candidate Intelligence & Search**, **Two-Sided Matching Engine**, **Match Explanation**, **Candidate Evidence Assistant (RAG)**. | [`backend/app/ai/job_description_analyzer`](file:///D:/Hirely/backend/app/ai/job_description_analyzer), [`backend/app/ai/rag`](file:///D:/Hirely/backend/app/ai/rag) |
| **Dual Storage** | Local filesystem storage (`STORAGE_BACKEND=local`) or Cloudflare R2 / S3-compatible object storage (`STORAGE_BACKEND=r2`) via `boto3`. | [`backend/app/storage/storage_service.py`](file:///D:/Hirely/backend/app/storage/storage_service.py) |
| **AI Observability** | Single-line JSON logging, request tracing via `X-Request-ID`, PII regex scrubbing, token usage & cost accounting, in-memory latency percentiles ($p50, p90, p95$). | [`backend/app/core/observability`](file:///D:/Hirely/backend/app/core/observability) |
| **AI Evaluation** | Offline benchmark evaluation runner assessing RAG retrieval precision and citation correctness against curated test datasets. | [`backend/app/ai/eval/runner.py`](file:///D:/Hirely/backend/app/ai/eval/runner.py) |
| **Docker Stack** | 4 orchestrated Compose services: `hirely-postgres`, `hirely-migration`, `hirely-backend`, and `hirely-frontend`. | [`docker-compose.yml`](file:///D:/Hirely/docker-compose.yml), [`docs/DOCKER.md`](file:///D:/Hirely/docs/DOCKER.md) |
| **Frontend UI** | 19 React 19 pages with React Router 7, authentication context, responsive UI cards, and loading/error states. | [`frontend/src/App.jsx`](file:///D:/Hirely/frontend/src/App.jsx) |

### 🟡 Partially Implemented / Architectural Scope Limitations
- **In-Memory Rate Limiting:** Sliding-window rate limiters are stored in-memory per worker process. Effective for single instances, but requires a Redis backend for distributed multi-instance clusters.
- **In-Memory AI Metrics Collector:** Telemetry is tracked in process memory and resets on restart. For distributed metrics, logs should be ingested by log collectors or exposed via Prometheus.
- **In-Process Resume Parsing:** Parsing runs synchronously in-process via Docling. Protected by upload limits (10 MB, 10 pages), but true multi-tenant DoS isolation requires asynchronous workers (e.g. Celery) with OS-level execution timeouts.

### 🗺️ Planned Roadmap Features (Not Yet Implemented)
- Distributed Redis caching & shared rate limiting.
- Asynchronous Celery / Redis Queue workers for background document processing.
- Persistent multi-turn conversational memory for AI Career Coach and RAG Assistant.
- Dedicated vector database (e.g. pgvector or Pinecone) for cross-tenant resume semantic search.
- Managed cloud production deployment pipelines (AWS / Render with automated TLS).

---

# 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React 19 + Vite)                     │
│                                                                             │
│   Candidate Views                      Recruiter Views                      │
│   ├── Dashboard & Profile              ├── Dashboard & Company Profile      │
│   ├── Resume Upload & Parsing          ├── Job Creation & Management        │
│   ├── Job Search & Application         ├── Application Review Pipeline      │
│   ├── AI ATS Analyzer                  ├── AI Job Description Analyzer      │
│   ├── AI Resume Improvement            ├── Recruiter Candidate Matching     │
│   ├── AI Cover Letter Generator        └── Candidate Evidence Assistant     │
│   └── AI Career Coach                      (Interactive RAG Q&A)            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / REST (JWT Bearer)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (FastAPI + Python 3.12)                   │
│                                                                             │
│  [Middleware Pipeline]                                                      │
│  ├── CorrelationIdMiddleware (X-Request-ID tracing)                         │
│  └── CORSMiddleware (Dynamic origins with wildcard credential protection)   │
│                                                                             │
│  [API Routers]                                                              │
│  ├── /auth          ├── /candidate    ├── /recruiter    ├── /jobs           │
│  ├── /resumes       ├── /applications ├── /health       └── /skills         │
│                                                                             │
│  [Domain & Core Services]                                                   │
│  ├── Auth & RBAC Security (Argon2 + JWT)                                    │
│  ├── In-Memory Sliding-Window Rate Limiter (IP auth / User AI limits)       │
│  ├── File Validation (Magic numbers, ZIP bombs, 10MB upload limit)          │
│  ├── Structured JSON Logging & In-Memory Latency Metrics ($p50, p90, p95$)  │
│  └── Dual Storage Provider: Local Filesystem ⟷ Cloudflare R2 (S3 API)      │
│                                                                             │
│  [AI Domain Layer]                                                          │
│  ├── ATS Analyzer          ├── Cover Letter Generator                       │
│  ├── Career Coach          ├── Resume Improvement Assistant                 │
│  ├── Job Description AI    ├── Recruiter Matching & Explanation Engine      │
│  └── Candidate Evidence Assistant (RAG Chunker, Retriever & Citation Verifier)
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
        SQLAlchemy ORM │                               │ Google GenAI SDK
                       ▼                               ▼
       ┌───────────────────────────────┐       ┌──────────────────────────────┐
       │     PostgreSQL Database       │       │        Google Gemini         │
       │  Users, Candidates, Companies │       │  gemini-2.5-flash            │
       │  Recruiters, Jobs, Resumes    │       │  gemini-embedding-2          │
       │  Applications, Skills         │       │  Pydantic Structured Outputs │
       └───────────────────────────────┘       └──────────────────────────────┘
```

---

# 💼 Recruitment Workflows

### 👤 Candidate Journey
```
Register ➔ Login ➔ Create Profile ➔ Add Skills ➔ Upload Resume ➔ Docling Auto-Parse
   │
   ▼
Browse Jobs ➔ Run ATS Analysis ➔ Review AI Resume Improvements ➔ Generate Cover Letter
   │
   ▼
Apply to Job ➔ Track Application Status (`applied` ➔ `shortlisted` ➔ `interview` ➔ `hired`)
```

### 🏢 Recruiter Journey
```
Register ➔ Login ➔ Setup Company & Profile ➔ Create Job Posting ➔ Run AI JD Analyzer
   │
   ▼
Receive Applications ➔ Run Recruiter Candidate Matching ➔ Read AI Match Explanations
   │
   ▼
Open Candidate Intelligence ➔ Ask Specific Resume Questions (RAG Evidence Assistant)
   │
   ▼
Advance Application Status (`applied` ➔ `shortlisted` ➔ `interview` ➔ `hired` / `rejected`)
```

---

# 🤖 AI Capabilities & Architecture

Hirely organizes AI into isolated domain modules rather than a monolithic service. Each module maintains its own context assemblers, prompts, and Pydantic schemas:

### 📊 Hybrid ATS Analyzer
Answers: *"How well does my active resume match this job, and what should I improve?"*
- **Required Skill Coverage (45%):** Exact string matching against mandatory job skills.
- **Preferred Skill Coverage (15%):** Exact string matching against nice-to-have skills.
- **Semantic Relevance (30%):** Cosine similarity between Gemini embeddings of resume experience and job requirements.
- **Resume Completeness (10%):** Deterministic check verifying contact information, experience depth, and education sections.
- **Qualitative Summary:** Gemini generates structured strengths, weaknesses, and targeted advice grounded in the analysis.

### 🛠️ AI Resume Improvement
- Analyzes candidate resume text against target job requirements.
- Identifies critical missing competencies and weak phrasing.
- Generates structured before-and-after bullet rewrites with explainable rationales.

### 📝 AI Cover Letter Generator
- Produces job-specific, professional cover letters.
- Context is strictly bounded to the candidate's active parsed resume and job description.
- Enforces grounded generation to prevent fabricating accomplishments or dates.

### 🎓 AI Career Coach
- Delivers contextual, candidate-specific career guidance.
- Analyzes candidate profile skills and experience to recommend targeted learning paths, interview preparation strategies, and career milestones.

### 📋 AI Job Description Analyzer
- Recruiter-facing tool auditing job postings before publication.
- Checks clarity, structural completeness, missing expectations, and skill precision.
- Returns actionable recommendations to improve job posting quality.

### 🔍 Recruiter Candidate Intelligence & Matching
- **Two-Sided Matching Engine:** Ranks candidate pools for a specific job posting using combined skill match scoring and vector similarity.
- **AI Match Explanation:** Translates raw scores into recruiter-friendly qualitative assessments detailing strengths, risks, and interview questions.

### 📑 Candidate Resume Evidence Assistant (RAG)
- Interactive Q&A system for recruiters reviewing a specific candidate.
- Resumes are parsed, sanitized, chunked, and retrieved based on query similarity.
- Gemini answers the recruiter's inquiry and includes direct quote citations from the resume.
- Citation verifier checks that quoted excerpts exist verbatim in the source chunks.

---

# 🔐 Security, Observability & Reliability

### 🛡️ Security Guardrails
- **Argon2 Password Hashing & JWT Authentication:** Secure credential handling with active-user validation.
- **Role-Based Access Control:** Recruiter endpoints strictly reject candidates; candidate endpoints reject recruiters.
- **Upload File Validation:** Magic number byte verification, ZIP bomb mitigation, 10 MB upload cap, and 50 MB uncompressed limit.
- **Sliding-Window Rate Limiting:** In-memory sliding-window limits protect auth endpoints against brute force and AI endpoints against abuse.

### 📊 Privacy-Preserving AI Observability
- **Request Tracing:** `CorrelationIdMiddleware` assigns or sanitizes incoming `X-Request-ID` headers across all operations.
- **Structured JSON Logging:** Emits machine-parsable, single-line JSON records formatted for log forwarders (e.g., Datadog, Vector).
- **Zero PII & Prompt Leakage:** Raw prompts, model completions, candidate resumes, and contact info are regex-scrubbed.
- **Token & Cost Telemetry:** Automatically extracts token usage from model responses and tracks estimated operational costs.
- **In-Memory Latency Percentiles:** Tracks rolling $p50, p90, p95$ operational latencies per feature using bounded queues.

### 🧪 Offline AI Evaluation Framework
- Benchmark runner ([`app.ai.eval.runner`](file:///D:/Hirely/backend/app/ai/eval/runner.py)) tests RAG performance against curated ground-truth datasets ([`candidate_evidence_eval_v1.json`](file:///D:/Hirely/backend/app/ai/eval/datasets/candidate_evidence_eval_v1.json)).
- Evaluates retrieval precision, citation validity, and hallucination bounds in CI without live API dependency.

---

# 🗄️ Database Architecture

Hirely uses PostgreSQL 15 managed via SQLAlchemy 2.0 ORM and Alembic migrations.

```
                         ┌──────────────┐
                         │    users     │
                         └──────┬───────┘
                                │ 1:1
              ┌─────────────────┴─────────────────┐
              ▼                                   ▼
       ┌──────────────┐                    ┌──────────────┐
       │  candidates  │                    │  recruiters  │
       └──────┬───────┘                    └──────┬───────┘
              │                                   │ N:1
              ├─────────────────────┐             ▼
              │ 1:N                 │ 1:N  ┌──────────────┐
              ▼                     ▼      │  companies   │
       ┌──────────────┐      ┌───────────┐ └──────────────┘
       │   resumes    │      │ candidate │        │
       └──────────────┘      │  _skills  │        │ 1:N
              │              └─────┬─────┘        ▼
              │                    │       ┌──────────────┐
              │                    │ N:1   │     jobs     │
              │                    ▼       └──────┬───────┘
              │             ┌────────────┐        │
              │             │   skills   │        ├────────────────┐
              │             └────────────┘        │ 1:N            │ 1:N
              │                    ▲              ▼                ▼
              │                    │ N:1   ┌──────────────┐ ┌──────────────┐
              │             ┌────────────┐ │ applications │ │  job_skills  │
              │             │ job_skills │ └──────────────┘ └──────────────┘
              │             └────────────┘
              ▼
   (Dual Storage: Local Disk / Cloudflare R2)
```

### Main Tables
- `users`: Core account identity, email, role (`candidate` or `recruiter`), password hash.
- `candidates`: Profile information (first name, last name, headline, bio, location).
- `companies`: Company metadata associated with recruiters.
- `recruiters`: Recruiter profile linked to a user account and company.
- `jobs`: Job postings with title, description, location, job type, active status.
- `resumes`: Uploaded resumes with file path/key, active status, parsed JSON data.
- `applications`: Applications linking candidate to job with state lifecycle.
- `skills`: Canonical skill dictionary.
- `candidate_skills`: Many-to-many relationship linking candidates to skills.
- `job_skills`: Many-to-many relationship linking jobs to required/preferred skills.

A unique database constraint on `(candidate_id, job_id)` prevents duplicate applications.

---

# 📂 Project Structure

```
Hirely/
├── .github/
│   └── workflows/
│       └── backend-ci.yml           # CI: PostgreSQL service, Pytest, AI Eval, Frontend Lint & Build
├── backend/
│   ├── alembic/                     # Alembic migration environment and versions
│   │   ├── versions/                # 7 database migrations
│   │   └── env.py
│   ├── app/
│   │   ├── ai/                      # AI domain modules
│   │   │   ├── ats_analyzer/        # ATS scoring engine, prompts, schemas
│   │   │   ├── candidate_intelligence/ # Candidate filtering & semantic intelligence
│   │   │   ├── career_coach/        # Career advice service & prompts
│   │   │   ├── cover_letter/        # Grounded cover letter generator
│   │   │   ├── embeddings/          # Vector embedding service
│   │   │   ├── eval/                # Deterministic AI eval runner & datasets
│   │   │   ├── job_description_analyzer/ # JD structural analysis service
│   │   │   ├── matching/            # Two-sided matching orchestrator & ranker
│   │   │   ├── parsers/             # Docling resume parser & structured extraction
│   │   │   ├── rag/                 # RAG candidate evidence assistant
│   │   │   ├── resume_improvement/  # Bullet rewrite & gap analysis service
│   │   │   └── services/            # Gemini client & provider abstraction
│   │   ├── api/                     # FastAPI route controllers
│   │   │   ├── applications.py      # Candidate & recruiter application endpoints
│   │   │   ├── auth.py              # Register, login, me endpoints
│   │   │   ├── candidate.py         # Profile & candidate AI endpoints
│   │   │   ├── candidate_skills.py  # Candidate skill management
│   │   │   ├── dependencies.py      # Auth & RBAC FastAPI dependencies
│   │   │   ├── health.py            # API & DB health checks
│   │   │   ├── jobs.py              # Jobs CRUD & matching endpoints
│   │   │   ├── job_skills.py        # Job skill requirements
│   │   │   ├── recruiter.py         # Recruiter profile & AI endpoints
│   │   │   └── resumes.py           # Resume upload, parse, activate, delete
│   │   ├── core/                    # Core configuration, security, rate limiting, observability
│   │   │   ├── observability/       # Correlation ID, structured JSON logging, metrics
│   │   │   ├── config.py            # Pydantic BaseSettings configuration
│   │   │   ├── rate_limit.py        # In-memory sliding-window rate limiter
│   │   │   └── security.py          # Argon2 hashing & JWT creation/verification
│   │   ├── db/                      # SQLAlchemy session & Base model
│   │   ├── models/                  # 10 SQLAlchemy ORM models
│   │   ├── schemas/                 # Pydantic request & response models
│   │   ├── services/                # Business logic services
│   │   ├── storage/                 # File validation & Dual Storage (Local / Cloudflare R2)
│   │   └── main.py                  # FastAPI application entry point
│   ├── tests/                       # Complete Pytest test suite (50+ test files)
│   ├── alembic.ini                  # Alembic configuration
│   ├── Dockerfile                   # Python 3.12-slim backend container
│   └── pytest.ini                   # Pytest configuration with pythonpath and markers
├── frontend/
│   ├── src/
│   │   ├── components/              # Shared UI cards, layout shell, navbar, protected route
│   │   ├── context/                 # AuthContext & token management
│   │   ├── pages/                   # 19 React view pages
│   │   ├── services/                # Axios API client & endpoint bindings
│   │   ├── App.jsx                  # React Router 7 route definitions
│   │   └── main.jsx                 # Application mount
│   ├── Dockerfile                   # Multi-stage Node 20 builder + Nginx runner
│   ├── nginx.conf                   # Nginx reverse proxy, static caching & SPA fallback
│   └── package.json                 # React 19, Vite 8, React Router 7
├── docs/
│   ├── 01_Project_Overview.md       # High-level architecture & project evolution
│   ├── 02_Research_and_Analysis.md  # Detailed technical research log
│   ├── 03_Software_Design_Document.md # Exhaustive software design document (Days 1–34)
│   └── DOCKER.md                    # Detailed Docker Compose operations guide
├── .dockerignore
├── .env.example                     # Environment template with sensible defaults
├── .gitignore
├── docker-compose.yml               # Multi-container orchestration (db, migration, backend, frontend)
├── LICENSE                          # License file
├── README.md                        # Primary project documentation
└── requirements.txt                 # Backend Python dependencies (at repository root)
```

---

# 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend Framework** | Python 3.12, FastAPI, Uvicorn, Pydantic v2, Pydantic-Settings |
| **Database & ORM** | PostgreSQL 15, SQLAlchemy 2.0, Alembic, Psycopg 3 |
| **Authentication & Security** | Argon2-cffi, PyJWT, In-memory Sliding-Window Rate Limiting |
| **AI / Machine Learning** | Google Gemini (`gemini-2.5-flash`), Gemini Embeddings, Google GenAI SDK |
| **Document Processing** | Docling (`langchain-docling`, `docling-parse`) |
| **Cloud Storage** | Cloudflare R2 (S3-compatible) via `boto3` / Local disk fallback |
| **Frontend Framework** | React 19, Vite 8, React Router 7, Axios, CSS3 Modules |
| **Observability** | Structured JSON Logging, `contextvars`, Correlation IDs (`X-Request-ID`) |
| **Testing & CI** | Pytest, Pytest-cov, Node Test Runner, GitHub Actions |
| **Containerization** | Docker, Docker Compose, Nginx Alpine |

---

# 🐳 Docker Compose Quickstart

Hirely includes a full multi-container development environment configured in [`docker-compose.yml`](file:///D:/Hirely/docker-compose.yml). For detailed operational instructions, consult the [Hirely Docker Desktop & Compose Guide](docs/DOCKER.md).

### Orchestrated Services
1. **`db` (`hirely-postgres`)**: PostgreSQL 15 on host port `5433` (mapped to internal `5432` to avoid host conflicts).
2. **`migration` (`hirely-migration`)**: Runs `alembic upgrade head` automatically on container launch, then exits cleanly.
3. **`backend` (`hirely-backend`)**: FastAPI application on host port `8000`, starts after migrations succeed.
4. **`frontend` (`hirely-frontend`)**: Production React SPA served via Nginx on host port `3000`, starts once backend is healthy.

### Run the Stack

```bash
# 1. Start all services in the background (builds images on first run)
docker compose up --build -d

# 2. Verify container statuses (db, backend, and frontend should show healthy)
docker compose ps

# 3. View live logs
docker compose logs -f backend

# 4. Stop all services (preserving database volume)
docker compose down
```

- **Web Application:** [http://localhost:3000](http://localhost:3000)
- **Interactive Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Backend Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

---

# ⚙️ Local Manual Setup

If running without Docker, follow these steps:

### Prerequisites
- Python 3.12
- Node.js 20+ & npm
- PostgreSQL 15 running locally

### 1. Clone & Setup Environment
```bash
git clone https://github.com/Musharraf-Bubere/Hirely.git
cd Hirely

# Create and activate Python virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install backend dependencies from ROOT-LEVEL requirements.txt
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy template from repository root
cp .env.example .env
```
Open `.env` and configure your database credentials, `JWT_SECRET_KEY`, and `GEMINI_API_KEY`.

### 3. Run Database Migrations
Migrations must be executed from the `backend/` directory where `alembic.ini` is located:
```bash
cd backend
alembic upgrade head
```

### 4. Start the FastAPI Backend
From the `backend/` directory:
```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Start the React Frontend
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
Access the application at [http://localhost:5173](http://localhost:5173).

---

# 🔑 Environment Variables

Configuration is driven by Pydantic settings from `.env`. See [`.env.example`](.env.example) for placeholder values:

| Variable | Default / Example | Purpose |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql+psycopg://...` | PostgreSQL connection string |
| `JWT_SECRET_KEY` | *(Required in prod)* | Secret key for signing JWT tokens ($\ge 32$ chars) |
| `JWT_ALGORITHM` | `HS256` | JWT signature algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifespan |
| `GEMINI_API_KEY` | *(Required for AI)* | Google AI Gemini API Key |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Primary Gemini model for generation and analysis |
| `GEMINI_FALLBACK_MODEL` | `gemini-2.0-flash` | Fallback model activated during upstream 503 errors |
| `STORAGE_BACKEND` | `local` | Resume storage mode: `local` or `r2` |
| `RESUME_STORAGE_DIR` | `app/storage/resumes` | Filesystem upload directory (when `STORAGE_BACKEND=local`) |
| `R2_ACCOUNT_ID` | *(Optional)* | Cloudflare R2 Account ID (when `STORAGE_BACKEND=r2`) |
| `R2_ACCESS_KEY_ID` | *(Optional)* | Cloudflare R2 S3 Access Key |
| `R2_SECRET_ACCESS_KEY` | *(Optional)* | Cloudflare R2 S3 Secret Access Key |
| `R2_BUCKET_NAME` | `hirely-resumes` | Cloudflare R2 Bucket Name |
| `DB_POOL_SIZE` | `5` | SQLAlchemy base connection pool size per worker |
| `DB_MAX_OVERFLOW` | `10` | SQLAlchemy maximum overflow connections |
| `CORS_ORIGINS` | `http://localhost:3000,...` | Allowed CORS origins list |

---

# 🧪 Testing & Quality Assurance

Hirely maintains an extensive automated testing suite across backend services, AI pipelines, and frontend components.

### Run Backend Unit & Service Tests
Backend tests must be run from the `backend/` directory to ensure `pytest.ini` properly resolves the Python path:
```bash
cd backend

# Run all deterministic tests (excluding live external API calls)
pytest -m "not integration and not eval_live" -v

# Run full test suite
pytest
```

### Run Offline AI Evaluation Suite
Evaluates RAG evidence retrieval precision and citation adherence without calling live external APIs:
```bash
cd backend
python -m app.ai.eval.runner --dataset app/ai/eval/datasets/candidate_evidence_eval_v1.json
```

### Run Frontend Automated Tests
```bash
cd frontend

# Run Node test runner for API clients
npm test

# Run ESLint
npm run lint

# Verify production Vite build
npm run build
```

### Continuous Integration (CI)
GitHub Actions workflow ([`.github/workflows/backend-ci.yml`](.github/workflows/backend-ci.yml)) automatically executes on push and pull requests to `main`:
1. Spawns a PostgreSQL 15 service container.
2. Applies Alembic schema migrations.
3. Runs all deterministic Pytest suites.
4. Executes the AI Evaluation benchmark runner.
5. Runs frontend linting, tests, and production build.

---

# 🔌 API Reference

### 🏥 Health Checks
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Lightweight service liveness check |
| `GET` | `/health/db` | Database connectivity check (`SELECT 1`) |

### 🔐 Authentication (`/auth`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Register new user as `candidate` or `recruiter` |
| `POST` | `/auth/login` | Authenticate and obtain JWT bearer access token |
| `GET` | `/auth/me` | Fetch currently authenticated user profile |

### 👤 Candidate (`/candidate`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/candidate/profile` | Create candidate profile |
| `GET` | `/candidate/profile` | Retrieve candidate profile |
| `PATCH` | `/candidate/profile` | Update candidate profile details |
| `POST` | `/candidate/skills` | Add skill to candidate profile |
| `GET` | `/candidate/skills` | List skills on candidate profile |
| `DELETE` | `/candidate/skills/{skill_id}` | Remove skill from candidate profile |
| `POST` | `/candidate/career-coach` | Get AI career guidance and recommendations |
| `POST` | `/candidate/cover-letter` | Generate targeted cover letter for a job |
| `POST` | `/candidate/ats-analysis` | Run hybrid deterministic & semantic ATS analysis |
| `POST` | `/candidate/resume-improvement` | Generate bullet rewrite & skill gap suggestions |

### 📄 Resume Management (`/resumes`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/resumes` | Upload resume file (PDF) |
| `GET` | `/resumes` | List uploaded resumes for current candidate |
| `PATCH` | `/resumes/{resume_id}/activate` | Set resume as active for job applications |
| `POST` | `/resumes/{resume_id}/parse` | Parse resume with Docling & sync skills |
| `DELETE` | `/resumes/{resume_id}` | Delete resume record and associated file |

### 💼 Jobs & Applications (`/jobs` & `/applications`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/jobs` | List active job postings |
| `GET` | `/jobs/{job_id}` | Get specific job details |
| `POST` | `/jobs` | Create new job posting *(Recruiter only)* |
| `POST` | `/jobs/{job_id}/apply` | Apply to job using active resume *(Candidate only)* |
| `POST` | `/jobs/{job_id}/skills` | Add required/preferred skill to job *(Recruiter only)* |
| `GET` | `/jobs/{job_id}/skills` | List skills associated with job |
| `DELETE` | `/jobs/{job_id}/skills/{skill_id}` | Remove skill from job *(Recruiter only)* |
| `POST` | `/jobs/{job_id}/match` | Evaluate candidate match against job *(Candidate only)* |
| `POST` | `/jobs/{job_id}/candidates/match` | Rank applicant pool for job *(Recruiter only)* |
| `POST` | `/jobs/{job_id}/candidates/match/explain` | Generate AI match explanation *(Recruiter only)* |
| `GET` | `/applications/me` | List candidate's submitted applications |
| `GET` | `/applications/recruiter` | List applications received by recruiter |
| `PATCH` | `/applications/{app_id}/status` | Update application status *(Recruiter only)* |

### 🏢 Recruiter AI & Operations (`/recruiter`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/recruiter/profile` | Retrieve recruiter profile and company details |
| `GET` | `/recruiter/jobs` | List jobs posted by current recruiter |
| `POST` | `/recruiter/jobs/{job_id}/description-analysis` | Run AI audit on job description |
| `POST` | `/recruiter/jobs/{job_id}/candidate-intelligence` | Semantic search & filter across candidates |
| `POST` | `/recruiter/jobs/{job_id}/candidates/{id}/ask-evidence` | Ask candidate resume questions via RAG |

---

# 🎨 Frontend Overview

The Hirely frontend is built with **React 19**, **Vite 8**, and **React Router 7**, featuring dedicated, role-protected portals:

- **Public Experience:** Landing page, user registration, user login, and public job board.
- **Candidate Portal:**
  - **Dashboard:** Career health summary, active resume status, and quick action cards.
  - **Profile & Skills:** Headline, bio, location, and interactive skill tag management.
  - **Resume Center:** Upload, activate, inspect Docling parse outputs, and delete resumes.
  - **ATS Analyzer:** Detailed breakdown of skill coverage, semantic similarity, and improvement tips.
  - **Resume Improvement:** Interactive before/after bullet rewrites and gap analysis.
  - **Cover Letter Studio:** One-click job-grounded cover letter generation with copy/regenerate.
  - **Career Coach:** Context-aware career advice interface.
- **Recruiter Portal:**
  - **Dashboard:** Job metrics, active applicants, and recent activity.
  - **Job Studio:** Job creation and requirement definition.
  - **Job Description Analyzer:** Real-time AI recommendations on job posting clarity.
  - **Candidate Matching & Intelligence:** Ranked candidate pools with score breakdowns.
  - **Evidence Assistant:** Interactive RAG interface to query candidate resumes with verified quote citations.

---

# 🔒 Security & Production Limitations

Hirely is engineered with production-minded patterns, but operating in a live multi-tenant production environment requires acknowledging current architectural boundaries:

1. **Process-Local Rate Limiting:** The sliding-window rate limiters ([`app/core/rate_limit.py`](file:///D:/Hirely/backend/app/core/rate_limit.py)) and candidate embedding cache reside in process memory. In multi-worker or clustered deployments, rate limit states are not shared across workers. Clustered deployments require a shared Redis backplane.
2. **Synchronous Document Parsing:** Docling C++ document parsing runs synchronously within the application worker. While bounded by file size limits (10 MB) and page limits (10 pages), true multi-tenant DoS immunity requires offloading parsing to isolated worker processes (e.g. Celery) with OS-level execution timeouts.
3. **Process-Local Observability Metrics:** In-memory operational metrics reset on process restarts. Production telemetry should ingest the emitted single-line structured JSON logs via log collectors (e.g. FluentBit, Promtail) into centralized APM systems.
4. **Secret Hygiene:** Never commit `.env` files or API credentials to source control. In production environments, credentials should be injected via secret managers (e.g. AWS Secrets Manager, HashiCorp Vault).
5. **Production Readiness Caution:** Healthy Docker containers and passing test suites represent a robust development foundation, but true production readiness requires a managed PostgreSQL cluster, object storage (Cloudflare R2), an external Redis cache, and TLS termination behind an ingress reverse proxy.

---

# 🗺️ Future Roadmap

- [ ] **Distributed Infrastructure:** Replace in-memory rate limiting and embedding caches with Redis.
- [ ] **Asynchronous Task Queue:** Move Docling document parsing to Celery / RabbitMQ background workers.
- [ ] **Dedicated Vector Database:** Integrate pgvector or Pinecone for cross-tenant resume indexing and search.
- [ ] **Conversational Memory:** Add multi-turn dialogue persistence for Career Coach and Recruiter RAG.
- [ ] **Cloud CI/CD & Infrastructure as Code:** Terraform / CloudFormation templates for AWS ECS or Render cloud deployment.

---

# 📚 Documentation

Detailed architectural and operational documentation is maintained in the [`docs/`](docs/) directory:

- [01_Project_Overview.md](docs/01_Project_Overview.md): High-level system overview, dual-sided platform design, and historical evolution.
- [DOCKER.md](docs/DOCKER.md): Complete guide for multi-container Docker Compose setup, networking, volumes, and troubleshooting.
- [03_Software_Design_Document.md](docs/03_Software_Design_Document.md): Detailed software design specifications covering system architecture, domain models, RAG implementation, security guardrails, and observability.
- [02_Research_and_Analysis.md](docs/02_Research_and_Analysis.md): Comprehensive 25,000+ line technical research log covering ATS behavior, career coaching, and design tradeoffs.

---

# 📄 License

This repository is maintained as a personal software engineering portfolio project. A formal open-source license has not yet been specified.

---

# 👨‍💻 Author

**Musharraf Bubère**<br>
*Data Science & AI Developer*

- **Repository:** [https://github.com/Musharraf-Bubere/Hirely](https://github.com/Musharraf-Bubere/Hirely)
