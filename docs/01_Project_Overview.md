# Hirely — Project Overview

> **Version:** 0.2.0 (Active Development)<br>
> **Project Type:** Dual-Sided AI Recruitment & Career Intelligence Platform<br>
> **Status:** Core Platform & AI Intelligence Implemented<br>
> [← Back to Main Documentation (README.md)](../README.md) • [View Software Design Document (SDD)](./03_Software_Design_Document.md) • [View Docker Guide](./DOCKER.md)

---

# 🚀 Executive Summary & Elevator Pitch

**Hirely** is a startup-grade, dual-sided AI recruitment platform designed to connect **candidates** and **recruiters** through intelligent job discovery, structured application tracking, candidate-facing career assistance, recruiter talent intelligence, and a grounded AI matching engine.

By combining modern software engineering principles with Google Gemini models, Hirely delivers explainable, evidence-grounded AI capabilities while keeping critical business logic, security permissions, and numerical scoring under strict deterministic backend control.

---

# 💡 Problem Statement

Traditional recruitment workflows are fragmented and introduce substantial friction for both job seekers and hiring teams.

### 👤 Candidate Challenges
- **Blind Applications:** Candidates submit resumes without knowing whether their skills and experience genuinely align with role expectations.
- **ATS Black Boxes:** Job seekers struggle to identify why resumes fail automated screening or which specific keywords and qualifications are absent.
- **Application Fatigue:** Tailoring resumes and writing job-specific cover letters manually for dozens of positions is time-consuming and error-prone.
- **Lack of Guidance:** Professional career coaching is expensive, leaving applicants without structured feedback on interview readiness or skill gaps.

### 🏢 Recruiter Challenges
- **Application Overload:** Recruiters receive hundreds of resumes per opening, making manual review slow, exhausting, and inconsistent.
- **Unstructured Screening:** Manually cross-referencing candidate experience against complex job requirements is inefficient.
- **Hallucinated or Unverified Claims:** Keyword matches often fail to reflect depth of experience or contextual competency.
- **Inconsistent Decision-Making:** Comparing candidate pools objectively without clear scoring criteria or grounded citations leads to hiring bias and missed talent.

---

# 💡 The Hirely Solution

Hirely bridges candidates and recruiters within a single unified platform. Instead of operating as disjointed tools, Hirely coordinates the entire recruitment lifecycle through a hybrid deterministic and AI architecture:

```
                            ┌────────────────────────┐
                            │    HIRELY PLATFORM     │
                            └───────────┬────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 │                                             │
                 ▼                                             ▼
       👤 CANDIDATE EXPERIENCE                       🏢 RECRUITER EXPERIENCE
  ├── Profile & Skills Management               ├── Recruiter & Company Profile
  ├── Multi-Resume Storage & Docling Parsing    ├── Job Posting & Lifecycle Management
  ├── Active Resume Selection                   ├── Application Review Pipeline
  ├── Job Discovery & Direct Applications       ├── AI Job Description Analyzer
  ├── AI Resume ATS Analyzer (Hybrid)           ├── Recruiter Candidate Matching
  ├── AI Resume Improvement Assistant           ├── Candidate Intelligence & Search
  ├── AI Cover Letter Generator                 └── Candidate Evidence Assistant (RAG)
  └── AI Career Coach
                 │                                             │
                 └──────────────────────┬──────────────────────┘
                                        │
                                        ▼
                         🤖 CORE INTELLIGENCE LAYER
             ├── Deterministic Skill Scoring & Weight Calculations
             ├── Semantic Embeddings & Cosine Similarity
             ├── Evidence-Grounded Match Explanations
             ├── Privacy-Preserving Structured Observability
             └── AI Security Guardrails & Rate Limiting
```

---

# 🎯 Current Implementation Status

Unlike early conceptual drafts, Hirely has implemented its full-stack core across backend services, database migrations, AI pipelines, and frontend interfaces:

### 1. 🔐 Authentication, Authorization & Security
- Argon2 password hashing and JWT bearer authentication.
- Strict Role-Based Access Control (RBAC) isolating Candidate and Recruiter domains.
- In-memory sliding-window rate limiting protecting authentication routes (per IP) and AI endpoints (per user).
- Multi-layer upload security: magic byte inspection, ZIP-bomb protection, file size capping (10 MB), and uncompressed bounds (50 MB).

### 2. 👤 Candidate Platform
- Profile management (headline, bio, location, contact details).
- Candidate skill repository with CRUD capabilities.
- Multi-resume management supporting PDF uploads, Docling structured text extraction, active resume selection, and skill synchronization.
- Real-time job browsing, filtering, and single-click job applications.
- **AI ATS Analyzer:** Hybrid scoring evaluating required skill coverage (45%), preferred skill coverage (15%), semantic relevance (30%), and resume completeness (10%).
- **AI Resume Improvement:** Identifies missing competencies, provides structured bullet rewrite recommendations, and suggests actionable enhancements.
- **AI Cover Letter Generator:** Drafts targeted, context-aware cover letters grounded strictly in candidate resume experience and target job requirements.
- **AI Career Coach:** Contextual career mentoring and skill growth guidance.

### 3. 🏢 Recruiter Platform
- Recruiter profile management linked with dedicated company profiles.
- Job posting creation, updating, and lifecycle tracking.
- Application review pipeline with full status lifecycle (`applied` $\to$ `shortlisted` $\to$ `interview` $\to$ `hired` / `rejected`).
- **AI Job Description Analyzer:** Audits job postings for role clarity, structural completeness, missing expectations, and actionable improvements.
- **Recruiter Candidate Matching Engine:** Calculates deterministic score breakdowns and semantic relevance to rank applicant pools for specific openings.
- **Candidate Match Explanation:** Produces grounded qualitative summaries detailing candidate strengths, weaknesses, and hiring recommendations.
- **Candidate Intelligence:** Semantic search and filtering across applicants.
- **Candidate Evidence Assistant (RAG):** Interactive Retrieval-Augmented Generation assistant allowing recruiters to ask specific factual questions about a candidate's resume, returning answers supported by direct citations and quote verification.

### 4. ⚙️ Reliability, Storage & Observability
- **Dual Resume Storage:** Seamless support for local disk storage (`STORAGE_BACKEND=local`) or Cloudflare R2 / S3-compatible object storage (`STORAGE_BACKEND=r2`).
- **Privacy-Preserving Observability:** Request tracing via `X-Request-ID`, single-line structured JSON logging, automatic PII scrubbing, token usage and cost accounting, and in-memory latency percentiles ($p50, p90, p95$).
- **Deterministic AI Evaluation Suite:** Offline benchmark evaluation runner verifying RAG citation fidelity, retrieval precision, and answer correctness against curated datasets.
- **Containerized Development Stack:** Four-service Docker Compose environment orchestrating PostgreSQL, automatic Alembic migrations, FastAPI backend, and Nginx-served React frontend.

---

# 🏛️ Architecture & Core Principles

Hirely adheres to strict software engineering standards to avoid common generative AI pitfalls:

1. **Deterministic Business Logic:** Security checks, authorization decisions, status transitions, and numerical score weightings are executed purely in backend Python code—never delegated to language models.
2. **Grounded AI Generation:** AI prompts provide structured, bounded context. Models are strictly instructed to evaluate only provided facts and avoid hallucinating skills, metrics, or candidate experience.
3. **Structured Outputs:** All LLM completions adhere to strict Pydantic models with automated schema validation before reaching the user interface.
4. **Privacy First:** Raw resumes, prompt text, user credentials, and PII are never emitted to application logs or external telemetry providers.
5. **Separation of Concerns:** Independent domain modules encapsulate distinct AI tasks (`ats_analyzer`, `career_coach`, `cover_letter`, `resume_improvement`, `job_description_analyzer`, `candidate_intelligence`, `rag`).

---

# 📜 Evolution & Historical Background

Hirely began in August 2026 as a candidate-focused career suite concept ("AI-Powered Career Suite") aimed at helping applicants build resumes and prepare for interviews. The original planning documentation focused primarily on four initial candidate utilities (Resume Checker, Resume Scorer, Cover Letter Generator, and Career Coach).

During engineering development, the project evolved into a comprehensive, dual-sided recruitment ecosystem based on key architectural insights:
- Helping candidates optimize resumes without connecting them directly to live job opportunities created half a solution.
- Recruiters required equivalent intelligence tools to objectively evaluate applications, parse unstructured resumes, and extract factual evidence without human screening fatigue.
- Hybrid deterministic algorithms (combining exact skill matches with semantic vector similarity) proved far more reliable and reproducible than relying purely on LLM scoring.
- Adding full recruiter workflows, company entities, application pipelines, and RAG capabilities transformed Hirely into a realistic, production-oriented recruitment intelligence platform.

This evolution preserved the original candidate empowerment vision while expanding the software design into an end-to-end talent acquisition platform.

---

# 🔭 Future Roadmap

While Hirely's core recruitment platform and AI features are fully implemented, future engineering iterations will focus on:
- **Distributed Caching & Rate Limiting:** Transitioning in-memory rate limiting and embedding caches to a shared Redis cluster for multi-node deployments.
- **Asynchronous Task Queues:** Moving compute-heavy Docling resume parsing into isolated background worker processes (e.g., Celery / Redis Queue) with OS-level execution timeouts for enhanced denial-of-service resilience.
- **Dedicated Vector Stores:** Introducing pgvector or dedicated vector databases for cross-tenant candidate discovery across large document corpora.
- **Conversational Memory:** Enabling persistent multi-turn dialogues for the AI Career Coach and Recruiter Evidence Assistant.
- **Cloud Infrastructure & Managed Deployment:** Hardened production configurations for managed cloud databases (AWS RDS / Neon) and container orchestration.
