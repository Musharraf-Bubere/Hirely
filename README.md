# 🚀 Hirely — AI-Powered Recruitment Platform

> **Hirely is a startup-grade AI recruitment platform that connects candidates and recruiters through intelligent job discovery, application management, AI-assisted career tools, resume analysis, and an evolving AI matching engine.**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-Migrations-1F2937)](https://alembic.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063)](https://docs.pydantic.dev/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)](https://ai.google.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-Core-1C3C3C)](https://www.langchain.com/)
[![Git](https://img.shields.io/badge/Git-Version_Control-F05032?logo=git)](https://git-scm.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](#-license)

---

## 📌 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [💡 Problem Statement](#-problem-statement)
- [🚀 Vision](#-vision)
- [👥 Target Users](#-target-users)
- [✨ Key Features](#-key-features)
- [🤖 AI Capabilities](#-ai-capabilities)
- [🧠 AI Architecture](#-ai-architecture)
- [📊 ATS Analyzer](#-ats-analyzer)
- [📝 Cover Letter Generator](#-cover-letter-generator)
- [🎓 AI Career Coach](#-ai-career-coach)
- [🔐 Authentication & Authorization](#-authentication--authorization)
- [💼 Recruitment Workflow](#-recruitment-workflow)
- [🗄️ Database Architecture](#️-database-architecture)
- [🏗️ System Architecture](#️-system-architecture)
- [📂 Project Structure](#-project-structure)
- [🛠️ Technology Stack](#️-technology-stack)
- [⚙️ Local Setup](#️-local-setup)
- [🔑 Environment Variables](#-environment-variables)
- [▶️ Running the Application](#️-running-the-application)
- [🧪 Testing](#-testing)
- [🔌 API Overview](#-api-overview)
- [🎨 Frontend](#-frontend)
- [🧩 Design Principles](#-design-principles)
- [🗺️ Product Roadmap](#️-product-roadmap)
- [📈 Engineering Progress](#-engineering-progress)
- [📚 Documentation](#-documentation)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👨‍💻 Author](#-author)

---

# 🎯 Project Overview

**Hirely** is a startup-grade AI-powered recruitment platform built to connect candidates and recruiters through a unified recruitment ecosystem.

The platform combines traditional recruitment workflows with AI-powered assistance, semantic analysis, and intelligent recruitment capabilities while keeping security and business-critical calculations under deterministic backend control.

                         ┌─────────────────────┐
                         │       HIRELY        │
                         │ AI Recruitment      │
                         │     Platform        │
                         └──────────┬──────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
             👤 Candidate      🏢 Recruiter      🤖 AI Engine
                   │                │                │
                   ▼                ▼                ▼
              Find Jobs        Create Jobs       Intelligence
              Apply            Manage Jobs       Analysis
              Track Status     Review Apps       Matching
              AI Assistance    Candidate Data    Recommendations

Hirely is being developed as a production-oriented portfolio project with a focus on:

- Clean architecture
- Modular backend services
- Secure authentication
- Role-based access control
- AI-assisted workflows
- Explainable AI
- Deterministic business logic
- Structured AI outputs
- Testing
- Documentation
- Git/GitHub-based development
- Future production deployment

---

# 💡 Problem Statement

Traditional recruitment platforms often separate job discovery, applications, resume optimization, candidate evaluation, and recruiter workflows.

This creates friction for both candidates and recruiters.

## 👤 Candidate Challenges

Candidates may struggle with:

- Finding relevant job opportunities
- Understanding whether their resume matches a job
- Identifying missing skills
- Improving resume quality
- Writing job-specific cover letters
- Understanding career development needs
- Tracking application progress

## 🏢 Recruiter Challenges

Recruiters may struggle with:

- Creating effective job descriptions
- Managing large numbers of applications
- Evaluating candidate-job alignment
- Identifying relevant candidates efficiently
- Understanding candidate strengths and gaps
- Reducing repetitive screening work
- Making recruitment decisions efficiently

## 💡 Hirely's Approach

Hirely brings these workflows together:

    Candidate
        │
        ▼
    Profile + Skills + Resume
        │
        ▼
    Job Discovery
        │
        ├───────────────┐
        ▼               ▼
    ATS Analysis    AI Assistance
        │               │
        └───────┬───────┘
                ▼
             Application
                │
                ▼
        Application Tracking
                │
                ▼
           Recruiter Review
                │
                ▼
       Recruitment Intelligence

---

# 🚀 Vision

The long-term vision of Hirely is to evolve from a conventional recruitment platform into an **AI-native recruitment intelligence system**.

                         ┌───────────────┐
                         │    HIRELY     │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
         👤 Candidate       🏢 Recruiter       🤖 AI Engine
         Experience         Experience         Intelligence
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
                         Intelligent Matching
                                 │
                                 ▼
                         Semantic Analysis
                                 │
                                 ▼
                       Explainable Insights
                                 │
                                 ▼
                      Better Hiring Outcomes

The goal is not to replace candidates or recruiters.

The goal is to **augment human decision-making with useful, grounded, explainable AI capabilities.**

---

# 👥 Target Users

## 👤 Candidates

Candidates can:

- Register and authenticate
- Create and manage professional profiles
- Manage skills
- Upload resumes
- Maintain an active resume
- Discover active jobs
- View job details
- Analyze resume-job alignment
- Generate job-specific cover letters
- Receive AI career guidance
- Apply to jobs
- Track application progress
- Improve their resume based on identified gaps

## 🏢 Recruiters

Recruiters can:

- Register and authenticate
- Create recruiter profiles
- Create job postings
- Manage jobs
- Review applications
- Update application statuses
- Evaluate candidates
- Use future AI-powered recruitment intelligence features

---

# ✨ Key Features

## 🔐 Authentication & Security

- Candidate registration
- Recruiter registration
- Secure login
- JWT-based authentication
- Argon2 password hashing
- Current-user endpoint
- Role-based access control
- Protected API routes
- Candidate-specific authorization
- Recruiter-specific authorization

## 👤 Candidate Platform

- Candidate profile management
- Candidate skills
- Resume upload
- Resume parsing
- Active resume selection
- Job discovery
- Job details
- Job applications
- Application history
- Application status tracking

## 🏢 Recruiter Platform

- Recruiter profile
- Job creation
- Job management
- Application management
- Candidate review
- Application lifecycle management

## 🤖 AI Features

### ✅ Implemented

- 🧑‍🏫 AI Career Coach
- ✍️ AI Cover Letter Generator
- 📊 AI Resume ATS Analyzer

### 🚧 Planned

- 🛠️ AI Resume Improvement
- 📋 AI Job Description Analyzer
- 🧠 Advanced Candidate Intelligence
- 🔎 Retrieval-Augmented Generation (RAG)
- 🔗 Advanced AI workflows
- 📈 AI evaluation and observability
- ☁️ Production deployment

---

# 🤖 AI Capabilities

Hirely uses independent AI domain modules instead of placing all AI logic into a single service.

                              Candidate
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
          Career Coach      Cover Letter      ATS Analyzer
                │                 │                 │
                ▼                 ▼                 ▼
        Career Guidance     Job-specific      Resume–Job
                             Drafting           Analysis

Each AI capability has its own:

- Context construction
- Prompt design
- Pydantic schemas
- Service layer
- API integration

This keeps the AI architecture modular and maintainable.

---

# 🧠 AI Architecture

Hirely follows a hybrid AI architecture.

                         User Request
                              │
                              ▼
                       FastAPI Endpoint
                              │
                              ▼
                       Domain Service
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Structured Data   Deterministic     AI Context
                           Logic          Construction
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                       Gemini AI Services
                              │
                              ▼
                     Structured AI Output
                              │
                              ▼
                       Pydantic Validation
                              │
                              ▼
                           Frontend

## AI Architecture Principles

### Deterministic Business Logic

Business rules, authorization, numerical scoring, and other critical calculations remain in backend code.

### Provider Abstraction

Gemini communication is isolated inside shared AI service infrastructure.

### Context Separation

Context construction is separated from prompt construction.

### Structured Output

AI responses are validated using Pydantic schemas.

### Grounded Generation

AI models are instructed to use only the supplied information and avoid unsupported claims.

### Minimum Necessary Context

Only information required for the specific AI task is provided.

### Controlled Complexity

RAG, vector databases, agents, and advanced orchestration are introduced only when a genuine product requirement exists.

---

# 📊 ATS Analyzer

The **AI Resume ATS Analyzer V1** is a candidate-facing feature designed to answer:

> **"How well does my current resume match this job, and what should I improve?"**

The ATS Analyzer combines deterministic evaluation, semantic embeddings, and Gemini-powered qualitative analysis.

                 Candidate Resume
                        │
                        ▼
              ┌──────────────────┐
              │ Resume Context    │
              └────────┬─────────┘
                       │
                       │
                 Target Job
                       │
                       ▼
              ┌──────────────────┐
              │ Job Context       │
              └────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
      Skill Match  Completeness  Embeddings
          │            │            │
          │            │            ▼
          │            │      Semantic Relevance
          │            │            │
          └────────────┼────────────┘
                       ▼
                 ATS Score
                       │
                       +
                       ▼
                 Gemini Analysis
                       │
                       ▼
          Strengths / Improvements
          Suggestions / Summary

## 📐 ATS Score

The final ATS score uses:

| Component | Weight |
|---|---:|
| Required Skill Coverage | 45% |
| Preferred Skill Coverage | 15% |
| Semantic Relevance | 30% |
| Resume Completeness | 10% |

The final score is calculated by backend logic rather than delegated to the language model.

This makes the numerical evaluation deterministic and reproducible.

## 🔎 Deterministic Skill Analysis

The ATS Analyzer evaluates:

- Required skills matched
- Required skills missing
- Preferred skills matched
- Preferred skills missing
- Resume completeness

Candidate profile skills and active parsed resume skills are combined before skill matching.

## 🧠 Semantic Relevance

Gemini embeddings are used to generate semantic representations for:

    Candidate Resume Representation
                  ↕
          Semantic Similarity
                  ↕
           Job Representation

Cosine similarity is calculated and normalized into the semantic relevance score.

## ✨ Gemini Qualitative Analysis

Gemini provides:

- Strengths
- Improvement areas
- Actionable suggestions
- Overall summary

The model is instructed to:

- Use only supplied information
- Avoid inventing experience
- Avoid inventing skills
- Avoid unsupported achievements
- Provide evidence-based insights
- Avoid keyword stuffing
- Avoid generating a numerical ATS score

## 📋 Structured Output

The ATS response contains:

- ATS score
- Score breakdown
- Required skills matched
- Required skills missing
- Preferred skills matched
- Preferred skills missing
- Strengths
- Improvement areas
- Suggestions
- Summary

Pydantic schemas validate the structured response.

## 📄 Resume Requirement

ATS analysis operates on the candidate's active parsed resume.

The resume must have completed parsing before ATS analysis can be performed.

## 🔌 ATS API

    POST /candidate/ats-analysis

Request:

    {
      "job_id": "JOB_UUID"
    }

## 🧱 ATS V1 Scope

The V1 ATS Analyzer intentionally does not use:

- RAG
- Vector databases
- LangGraph
- Autonomous agents
- Background workers
- Resume rewriting
- PDF generation
- Persistent ATS history

These capabilities can be introduced later when product requirements justify them.

---

# 📝 Cover Letter Generator

The **AI Cover Letter Generator V1** creates a job-specific cover letter using relevant candidate and job context.

    Candidate Profile
           +
    Candidate Skills
           +
    Active Resume
           +
    Target Job
           │
           ▼
         Gemini
           │
           ▼
    Job-specific Cover Letter

The generated letter is grounded in:

- Candidate profile
- Candidate skills
- Active resume
- Job description
- Job requirements
- Employment information

## V1 Features

- Candidate-facing generation
- Job-specific cover letter
- Structured API response
- Copy functionality
- Regenerate functionality
- Grounded generation

## V1 Exclusions

- Automatic email sending
- PDF generation
- Persistent cover-letter history
- Autonomous agent workflows

---

# 🎓 AI Career Coach

The **AI Career Coach** provides contextual career guidance to candidates.

It can assist with areas such as:

- Career direction
- Skill development
- Learning paths
- Interview preparation
- Professional development
- Career decisions

The Career Coach uses:

- Dedicated AI domain module
- Structured request/response schemas
- Gemini
- Context-aware prompts
- Backend API integration

The feature is designed as an assistive career guidance capability rather than a replacement for human career decision-making.

---

# 🔐 Authentication & Authorization

Hirely uses JWT-based authentication with role-based authorization.

                         User
                          │
                          ▼
                      Register
                          │
                          ▼
                        Login
                          │
                          ▼
                      JWT Token
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
          Candidate                Recruiter
              │                       │
              ▼                       ▼
      Candidate APIs          Recruiter APIs

## Security Components

- JWT authentication
- Argon2 password hashing
- Role-based access control
- Protected API endpoints
- Active-user validation
- Candidate-only dependencies
- Recruiter-only dependencies

AI is not responsible for authentication or authorization decisions.

---

# 💼 Recruitment Workflow

## 👤 Candidate Workflow

    Register
       ↓
    Login
       ↓
    Create Profile
       ↓
    Add Skills
       ↓
    Upload Resume
       ↓
    Resume Parsing
       ↓
    Find Jobs
       ↓
    View Job
       ↓
    ATS Analysis
       ↓
    Resume Improvement
       ↓
    Generate Cover Letter
       ↓
    Apply
       ↓
    Track Application

## 🏢 Recruiter Workflow

    Register
       ↓
    Login
       ↓
    Create Recruiter Profile
       ↓
    Create Job
       ↓
    Manage Job
       ↓
    Receive Applications
       ↓
    Review Applications
       ↓
    Evaluate Candidates
       ↓
    Update Application Status

## 📈 Application Lifecycle

    Applied
       ↓
    Shortlisted
       ↓
    Interview
       ↓
    Hired

Alternative terminal path:

    Applied / Shortlisted / Interview
                    ↓
                 Rejected

`Hired` and `Rejected` are terminal application states.

---

# 🗄️ Database Architecture

Hirely uses PostgreSQL with SQLAlchemy ORM and Alembic migrations.

## Core Entities

                              User
                         ┌──────┴──────┐
                         │             │
                         ▼             ▼
                    Candidate      Recruiter
                         │             │
             ┌───────────┼───────┐     │
             │           │       │     ▼
             ▼           ▼       ▼    Job
      CandidateSkill   Resume  Application
             │                   ▲       │
             ▼                   │       │
           Skill                 │       ▼
             ▲                   └── Application
             │
          JobSkill

## Main Tables

- `users`
- `candidates`
- `recruiters`
- `jobs`
- `applications`
- `skills`
- `candidate_skills`
- `job_skills`
- `resumes`

## Important Relationships

### User → Candidate

    User.id → Candidate.user_id

### User → Recruiter

    User.id → Recruiter.user_id

### Recruiter → Job

    Recruiter.id → Job.recruiter_id

### Candidate → Application

    Candidate.id → Application.candidate_id

### Job → Application

    Job.id → Application.job_id

### Candidate → Skill

    Candidate → CandidateSkill → Skill

### Job → Skill

    Job → JobSkill → Skill

A unique candidate-job application constraint prevents duplicate applications.

---

# 🏗️ System Architecture

    ┌───────────────────────────────────────────────────────────────┐
    │                       HIRELY FRONTEND                         │
    │                         React + Vite                          │
    │                                                               │
    │  Candidate UI                       Recruiter UI              │
    │  ├── Dashboard                      ├── Dashboard              │
    │  ├── Profile                        ├── Jobs                   │
    │  ├── Resume                         ├── Applications            │
    │  ├── Find Jobs                      └── Candidate Review        │
    │  ├── Applications                                             │
    │  ├── Career Coach                                             │
    │  ├── Cover Letter                                             │
    │  └── ATS Analyzer                                             │
    └──────────────────────────────┬────────────────────────────────┘
                                   │
                                   │ REST API
                                   ▼
    ┌───────────────────────────────────────────────────────────────┐
    │                       FASTAPI BACKEND                         │
    │                                                               │
    │  ┌────────────┐  ┌────────────┐  ┌─────────────────────────┐ │
    │  │ Auth APIs  │  │ Candidate  │  │ Recruiter APIs          │ │
    │  └────────────┘  └────────────┘  └─────────────────────────┘ │
    │                                                               │
    │  ┌───────────────────────────────────────────────────────────┐│
    │  │                    Domain Services                        ││
    │  └───────────────────────────────────────────────────────────┘│
    │                                                               │
    │  ┌───────────────────────────────────────────────────────────┐│
    │  │                       AI Layer                             ││
    │  │ Career Coach │ Cover Letter │ ATS │ Embeddings │ Parsers  ││
    │  └───────────────────────────────────────────────────────────┘│
    └──────────────────────────────┬────────────────────────────────┘
                                   │
                     ┌─────────────┴──────────────┐
                     ▼                            ▼
            ┌─────────────────┐          ┌──────────────────┐
            │   PostgreSQL    │          │   Google Gemini  │
            │    Database     │          │ LLM + Embeddings │
            └─────────────────┘          └──────────────────┘

---

# 📂 Project Structure

    Hirely/
    │
    ├── backend/
    │   │
    │   ├── app/
    │   │   │
    │   │   ├── ai/
    │   │   │   ├── ats_analyzer/
    │   │   │   ├── career_coach/
    │   │   │   ├── cover_letter/
    │   │   │   ├── embeddings/
    │   │   │   ├── parsers/
    │   │   │   ├── services/
    │   │   │   └── config.py
    │   │   │
    │   │   ├── api/
    │   │   │   ├── auth.py
    │   │   │   ├── candidate.py
    │   │   │   ├── recruiter.py
    │   │   │   └── dependencies.py
    │   │   │
    │   │   ├── models/
    │   │   ├── schemas/
    │   │   ├── services/
    │   │   ├── db/
    │   │   └── main.py
    │   │
    │   ├── alembic/
    │   ├── tests/
    │   ├── requirements.txt
    │   └── .env
    │
    ├── frontend/
    │   │
    │   ├── src/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   │   ├── ATSAnalyzer.jsx
    │   │   │   ├── CareerCoach.jsx
    │   │   │   ├── CoverLetter.jsx
    │   │   │   ├── JobDetail.jsx
    │   │   │   └── ...
    │   │   │
    │   │   ├── services/
    │   │   │   ├── atsAnalyzer.js
    │   │   │   ├── candidate.js
    │   │   │   └── ...
    │   │   │
    │   │   ├── App.jsx
    │   │   └── main.jsx
    │   │
    │   ├── package.json
    │   └── .env
    │
    ├── docs/
    │   ├── 01_...
    │   ├── 02_...
    │   ├── 03_Software_Design_Document.md
    │   └── ...
    │
    ├── .gitignore
    └── README.md

> The exact project structure may evolve as Hirely grows.

---

# 🛠️ Technology Stack

## 🐍 Backend

| Technology | Purpose |
|---|---|
| Python | Core backend language |
| FastAPI | REST API framework |
| Pydantic | Request/response validation |
| SQLAlchemy | ORM |
| PostgreSQL | Relational database |
| Alembic | Database migrations |
| JWT | Authentication |
| Argon2 | Password hashing |

## 🤖 AI / ML

| Technology | Purpose |
|---|---|
| Google Gemini | LLM-powered generation and analysis |
| Gemini Embeddings | Semantic representations |
| LangChain Core | AI workflow primitives |
| Docling | Resume/document parsing |
| Scikit-learn | Machine learning utilities |
| NumPy | Numerical operations |

## ⚛️ Frontend

| Technology | Purpose |
|---|---|
| React | UI framework |
| Vite | Frontend build tool |
| React Router | Client-side routing |
| CSS | UI styling |

## 🔧 Development Tools

| Tool | Purpose |
|---|---|
| Git | Version control |
| GitHub | Source control |
| Pytest | Backend testing |
| Jupyter | Experimentation and documentation |
| VS Code | Development environment |

---

# ⚙️ Local Setup

## 1️⃣ Clone the Repository

    git clone https://github.com/Musharraf-Bubere/Hirely.git
    cd Hirely

## 2️⃣ Backend Setup

Navigate to the backend:

    cd backend

Create a virtual environment:

    python -m venv venv

Activate it on Windows:

    venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

## 3️⃣ PostgreSQL Setup

Create a PostgreSQL database for Hirely.

Example:

    Database: hirely

Configure the connection using backend environment variables.

## 4️⃣ Database Migration

Run:

    alembic upgrade head

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

Example:

    DATABASE_URL=postgresql://username:password@localhost:5432/hirely
    SECRET_KEY=your_secret_key
    GEMINI_API_KEY=your_gemini_api_key

> ⚠️ **Never commit `.env` files, passwords, API keys, JWT secrets, or other credentials to GitHub.**

For public repositories, use a `.env.example` file containing placeholder values only.

Example:

    DATABASE_URL=
    SECRET_KEY=
    GEMINI_API_KEY=

---

# ▶️ Running the Application

## 🖥️ Backend

From the `backend` directory:

    uvicorn app.main:app --reload

FastAPI interactive documentation:

    http://127.0.0.1:8000/docs

ReDoc:

    http://127.0.0.1:8000/redoc

## 🌐 Frontend

Navigate to the frontend:

    cd frontend

Install dependencies:

    npm install

Start development server:

    npm run dev

Build production frontend:

    npm run build

---

# 🧪 Testing

Hirely uses Pytest for backend testing.

## Run Complete Backend Tests

    pytest

## Run Non-Integration Tests

    pytest -m "not integration"

## Run ATS Tests

    pytest tests/test_ats_analyzer.py
    pytest tests/test_ats_analyzer_api.py
    pytest tests/test_ats_analyzer_service.py

## Frontend Production Build

    npm run build

Testing focuses on:

- Authentication
- Authorization
- Candidate workflows
- Recruiter workflows
- Job management
- Applications
- AI services
- ATS analysis
- API behavior
- Regression safety

---

# 🔌 API Overview

## 🔐 Authentication

    POST /auth/register
    POST /auth/login
    GET  /auth/me

## 👤 Candidate

    POST  /candidate/profile
    GET   /candidate/profile
    PATCH /candidate/profile

    POST /candidate/career-coach
    POST /candidate/cover-letter
    POST /candidate/ats-analysis

## 💼 Jobs

    GET  /jobs
    GET  /jobs/{job_id}
    POST /jobs

## 📄 Applications

    POST /applications
    GET  /applications

## 🏢 Recruiter

Recruiter APIs support:

- Recruiter profile management
- Job management
- Application review
- Candidate evaluation
- Application status updates

> API routes may evolve as the platform continues development.

---

# 🎨 Frontend

Hirely's frontend is designed around a polished recruitment experience.

## Candidate Experience

    Candidate Dashboard
            │
            ├── 👤 Profile
            ├── 📄 Resume
            ├── 🔎 Find Jobs
            ├── 📋 Applications
            ├── 🧑‍🏫 Career Coach
            ├── ✍️ Cover Letter
            └── 📊 ATS Analyzer

## Frontend Design Goals

- Clean UI
- Responsive layouts
- Consistent visual language
- Clear user flows
- Action-oriented interfaces
- Useful loading states
- Useful error states
- Protected routes
- Minimal friction between recruitment actions

---

# 🧩 Design Principles

## 1. 🏗️ Modular Architecture

Features are separated into domain modules.

For example:

    ai/
    ├── career_coach/
    ├── cover_letter/
    └── ats_analyzer/

This keeps AI capabilities independently maintainable.

## 2. 🔒 Security First

Authentication and authorization are handled by deterministic backend mechanisms.

AI is never responsible for deciding whether a user is authorized to perform an action.

## 3. 🎯 Grounded AI

AI systems should use only relevant information supplied through structured context.

The model should not invent:

- Skills
- Experience
- Qualifications
- Achievements
- Candidate history

## 4. 📊 Deterministic Where Possible

Numerical and business-critical calculations should remain deterministic.

For example, ATS scoring is calculated using backend-controlled weights.

## 5. 🧠 Structured AI Output

AI responses are validated using Pydantic schemas wherever structured output is required.

    LLM
     ↓
    Structured Response
     ↓
    Pydantic Validation
     ↓
    Application

## 6. 🧹 Minimum Necessary Context

Only information relevant to the current AI task should be provided to the model.

This improves:

- Relevance
- Reliability
- Privacy
- Maintainability
- Cost control

## 7. 🚫 No Premature Complexity

Hirely does not introduce advanced AI infrastructure simply because it is available.

RAG, vector databases, agents, orchestration frameworks, and other infrastructure should be introduced only when they solve a genuine product or engineering problem.

## 8. 👨‍💼 Human Review

AI-generated content and recommendations are assistive.

They should support candidates and recruiters rather than being treated as unquestionable sources of truth.

---

# 🗺️ Product Roadmap

Hirely is being developed incrementally.

## Phase 1 — Core Platform

- Authentication
- Authorization
- Candidate profiles
- Recruiter profiles
- Skills
- Jobs
- Applications
- Application lifecycle
- Resume management

## Phase 2 — Candidate AI

- ✅ AI Career Coach
- ✅ AI Cover Letter Generator
- ✅ AI Resume ATS Analyzer
- 🚧 AI Resume Improvement

## Phase 3 — Recruiter AI

- 📋 AI Job Description Analyzer
- 🧠 Candidate intelligence
- 📊 Advanced candidate insights
- 🔎 Semantic candidate discovery

## Phase 4 — RAG & Advanced AI

RAG will be introduced where it provides genuine value.

Potential architecture:

    Knowledge Sources
            │
            ▼
       Document Processing
            │
            ▼
         Chunking
            │
            ▼
        Embeddings
            │
            ▼
       Vector Store
            │
            ▼
        Retrieval
            │
            ▼
     Relevant Context
            │
            ▼
          Gemini
            │
            ▼
    Grounded AI Response

Potential RAG use cases may include:

- Recruitment knowledge
- Company hiring guidelines
- Job-related knowledge
- Career resources
- Internal recruitment documentation
- Candidate intelligence context

RAG will not be added merely for technology demonstration. It will be introduced when the application requires retrieval from a growing knowledge base.

## Phase 5 — Advanced AI Engineering

Potential future capabilities:

- Hybrid search
- Reranking
- Agentic workflows
- Advanced orchestration
- AI evaluation
- Guardrails
- Observability
- Prompt/version management
- AI quality monitoring

## Phase 6 — Production Engineering

- Docker
- Production configuration
- CI/CD
- Cloud deployment
- AWS infrastructure
- Database production setup
- Logging
- Monitoring
- Security hardening
- Performance optimization
- Production testing

---

# 📈 Engineering Progress

Hirely is being developed incrementally with every feature following a structured engineering workflow.

    Research
        ↓
    Understand
        ↓
    Design
        ↓
    Implement
        ↓
    Test
        ↓
    Debug
        ↓
    Refactor
        ↓
    Document
        ↓
    Git
        ↓
    GitHub
        ↓
    LinkedIn
        ↓
    Next Feature

## Completed Milestones

### 🔐 Foundation

- Authentication
- JWT security
- Argon2 password hashing
- Role-based authorization
- Candidate and recruiter separation

### 💼 Recruitment Core

- Candidate profiles
- Recruiter profiles
- Job creation
- Job discovery
- Applications
- Application history
- Application status lifecycle

### 📄 Resume Infrastructure

- Resume management
- Resume parsing
- Structured resume data
- Active resume support

### 🤖 Candidate AI

- AI Career Coach
- AI Cover Letter Generator
- AI Resume ATS Analyzer

### 📊 ATS Analyzer Validation

The ATS Analyzer has been tested through:

- Unit tests
- Service tests
- API tests
- Backend regression testing
- Frontend production build
- Real Gemini browser integration
- Re-analysis flow

---

# 📚 Documentation

Detailed engineering documentation is maintained inside the `docs/` directory.

Documentation covers areas such as:

- Project requirements
- Software architecture
- Software design
- Database design
- API design
- AI architecture
- Feature design
- Development decisions
- Testing
- Future architecture

The primary software design documentation includes:

    docs/03_Software_Design_Document.md

---

# 🧪 Quality & Engineering Standards

Hirely follows several engineering practices:

- Modular architecture
- Separation of concerns
- Strong request/response validation
- Automated testing
- Regression testing
- Database migrations
- Secure credential handling
- Git-based version control
- Documentation alongside implementation
- Incremental feature development
- Deterministic business logic
- Grounded AI generation
- Structured AI outputs

The objective is to build Hirely as a **realistic production-oriented system**, not simply a collection of AI demos.

---

# 🔭 Future Architecture

The long-term Hirely architecture is expected to evolve toward:

    ┌─────────────────────────────────────────────┐
    │                 Hirely Platform             │
    └──────────────────────┬──────────────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         Candidate     Recruiter      AI Engine
         Experience    Experience     Platform
              │            │            │
              └────────────┼────────────┘
                           ▼
                  Matching Intelligence
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          Embeddings     RAG       AI Agents
              │            │            │
              └────────────┼────────────┘
                           ▼
                  Grounded Intelligence
                           │
                           ▼
                    Human-in-the-loop
                           │
                           ▼
                   Better Recruitment

Advanced components will be introduced incrementally rather than all at once.

---

# 🔒 Security Considerations

Hirely treats security as a backend responsibility.

Security considerations include:

- Secure password hashing
- JWT authentication
- Role-based access control
- Protected routes
- Input validation
- Database constraints
- Environment-based secrets
- No credentials in source control
- Controlled AI context
- Grounded AI prompts
- Human review for AI-assisted outputs

AI-generated content should never be treated as a security authorization mechanism.

---

# ⚠️ Current Project Status

Hirely is an actively developed portfolio project.

The platform already contains a functional recruitment foundation and multiple candidate-facing AI capabilities.

Current status:

    Core Recruitment Platform       ✅
    Authentication                  ✅
    Candidate Workflow               ✅
    Recruiter Workflow               ✅
    Resume Infrastructure            ✅
    AI Career Coach                  ✅
    AI Cover Letter Generator        ✅
    AI Resume ATS Analyzer           ✅
    AI Resume Improvement            🚧
    Recruiter AI                     🚧
    RAG                              🗺️ Planned
    Advanced Candidate Intelligence  🗺️ Planned
    Production Deployment             🗺️ Planned

---

# 🤝 Contributing

Hirely is primarily a personal portfolio project, but suggestions and discussions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement the change.
4. Add or update tests.
5. Verify the application.
6. Commit your changes.
7. Open a pull request.

Example:

    git checkout -b feature/your-feature
    git add .
    git commit -m "feat: add your feature"
    git push origin feature/your-feature

---

# 📄 License

This project is currently maintained as a personal portfolio and learning project.

If a formal open-source license is added, this section will be updated accordingly.

---

# 👨‍💻 Author

## Musharraf Bubère

Data Science & AI Developer focused on:

- Python
- SQL
- Machine Learning
- Deep Learning
- NLP
- Generative AI
- LLM Applications
- RAG
- Agentic AI
- FastAPI
- Data Analytics
- AI Engineering

### 🔗 Project Repository

GitHub:

https://github.com/Musharraf-Bubere/Hirely

---

# ⭐ Support

If you find this project interesting:

- ⭐ Star the repository
- 🍴 Fork the project
- 💡 Share feedback
- 🐛 Report issues
- 🤝 Contribute ideas

---

# 🚀 Hirely

> **From job discovery to intelligent recruitment — building a smarter hiring ecosystem with AI.**

**Built with Python, FastAPI, React, PostgreSQL, Gemini, and a production-oriented engineering mindset.**
