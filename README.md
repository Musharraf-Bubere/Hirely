# 🚀 Hirely

### AI-Powered Recruitment & Candidate Matching Platform

Hirely is an AI-powered recruitment platform designed to improve how candidates discover opportunities and recruiters discover qualified talent.

The platform combines traditional recruitment workflows with:

- Generative AI
- Semantic embeddings
- Deterministic skill matching
- Hybrid scoring
- Candidate ranking
- Evidence-grounded AI explanations
- Structured data validation

> **Project Status:** 🚧 Active Development  
> **Current Focus:** AI Matching API & Product Integration

---

## 📌 Overview

Traditional recruitment systems often rely heavily on keyword matching and manual candidate screening. This can make it difficult to identify candidates whose experience is relevant to a job but described using different terminology.

Hirely addresses this problem using a **hybrid AI architecture**.

Instead of relying entirely on an LLM, Hirely combines deterministic software logic with AI capabilities.

### Core Approach

- **Database** → Source of truth
- **Deterministic matching** → Structured skill comparison
- **Embeddings** → Semantic understanding
- **Hybrid scoring** → Combines measurable signals
- **Ranking engine** → Orders candidates by match quality
- **Generative AI** → Explains matching evidence
- **Pydantic schemas** → Validates structured AI output

The goal is to build a recruitment system that is not only AI-powered, but also:

- Explainable
- Testable
- Maintainable
- Modular
- Production-oriented

---

# 🎯 Problem Statement

Recruiters often need to evaluate a large number of candidates against job requirements.

Traditional keyword-based approaches can struggle with:

- Different terminology for similar skills
- Large numbers of applicants
- Manual candidate screening
- Difficulty comparing candidates consistently
- Lack of meaningful explanations for matching decisions

Candidates also face challenges such as:

- Understanding how well their resume matches a job
- Identifying missing skills
- Improving their resume
- Generating job-specific application materials
- Understanding potential career improvements

Hirely aims to address these problems through a combination of **conventional software engineering and AI**.

---

# 💡 Core Idea

Hirely uses a hybrid candidate-matching architecture.

    Candidate Resume
           │
           ▼
    Resume Parsing
           │
           ▼
    Candidate Representation
           │
           ▼
    Candidate Embedding
           │
           ├────────────────────────┐
           ▼                        ▼
    Deterministic Skill       Semantic Similarity
        Matching
           │                        │
           └───────────┬────────────┘
                       ▼
                Hybrid Scoring
                       │
                       ▼
                Candidate Ranking
                       │
                       ▼
                AI Match Explanation
                       │
                       ▼
                  Final Result

The system does **not** ask an LLM to make the entire hiring decision.

Instead:

1. The database remains the source of truth.
2. Deterministic logic handles structured matching.
3. Embeddings capture semantic similarity.
4. The matching engine combines measurable signals.
5. Candidate ranking is based on the calculated score.
6. Generative AI explains the evidence.
7. Human judgment remains important in recruitment decisions.

---

# ✨ Features

## 👤 Candidate Features

### Candidate Profile

Candidates can maintain structured profile information including:

- Name
- Headline
- Bio
- Location
- Skills

### Resume Management

Hirely supports:

- Resume upload
- PDF validation
- DOCX validation
- Multiple resume versions
- Active resume selection
- Resume persistence
- Resume retrieval

### Resume Parsing

Uploaded resumes can be processed into structured information.

The parsing pipeline extracts information such as:

- Skills
- Experience
- Projects
- Education
- Certifications
- Resume summary

### Resume → Candidate Skills

Extracted skills can be synchronized with the normalized skill system.

This allows structured candidate skill matching while keeping the original parsed resume data.

---

# 🏢 Recruiter Features

## Recruiter Profile

Recruiters have dedicated recruiter profiles and role-based access.

## Job Management

Recruiters can:

- Create jobs
- View jobs
- Manage active jobs
- Define required skills
- Define preferred skills

## Candidate Matching

Recruiters will be able to evaluate candidates using:

- Required skill matching
- Preferred skill matching
- Semantic similarity
- Hybrid match scores
- Candidate ranking
- AI-generated match explanations

---

# 🤖 AI Features

## Resume Intelligence

Resume processing follows this pipeline:

    Resume File
         │
         ▼
    Document Loader
         │
         ▼
    Document Processing
         │
         ▼
       Gemini
         │
         ▼
    Structured Resume Data
         │
         ▼
    Pydantic Validation

The parsed output is represented using validated structured schemas.

---

# 🧠 Candidate Representation

Hirely creates a deterministic textual representation of a candidate using relevant information such as:

- Profile information
- Skills
- Experience
- Projects
- Education
- Certifications

Sensitive contact information such as:

- Email
- Phone number

is excluded from the representation used for semantic matching.

This helps ensure that semantic similarity focuses on **professional relevance rather than personal contact information**.

---

# 💼 Job Representation

Jobs are represented using relevant information such as:

- Job title
- Job description
- Location
- Employment type
- Experience level
- Required skills
- Preferred skills

Recruiter-specific and system metadata are excluded from the semantic representation.

---

# 🔢 Embeddings

Hirely uses **Gemini Embeddings** to convert candidate and job representations into numerical vectors.

## Candidate Embedding

    Candidate Representation
             │
             ▼
          Embedding
             │
             ▼
       Candidate Vector

## Job Embedding

    Job Representation
             │
             ▼
          Embedding
             │
             ▼
          Job Vector

Semantic similarity is then calculated between the candidate and job vectors.

### Current Configuration

- Embedding provider: Google Gemini
- Vector dimensionality: 768

---

# 🧩 Hybrid Matching Engine

Hirely does not depend on semantic similarity alone.

The matching engine combines deterministic skill matching with semantic similarity.

## Current Scoring Configuration

| Signal | Weight |
|---|---:|
| Required Skills | 50% |
| Preferred Skills | 20% |
| Semantic Similarity | 30% |
| **Total** | **100%** |

### Scoring Principle

When all signals are available:

    Final Score =
        (Required Skill Score × 0.50)
      + (Preferred Skill Score × 0.20)
      + (Semantic Similarity Score × 0.30)

When a signal is unavailable, the available signals can be **renormalized** instead of inventing a score.

This ensures that missing information does not automatically become an artificial zero or fabricated value.

---

# 🎯 Skill Matching

The skill matching system distinguishes between two categories.

## Required Skills

Skills that are explicitly required by a job.

## Preferred Skills

Skills that are useful but not mandatory.

The matching engine identifies:

- Matched required skills
- Missing required skills
- Matched preferred skills
- Missing preferred skills

---

## Normalized Skill System

Skills are maintained as normalized shared entities.

    Skill
    ├── CandidateSkill
    │      └── Candidate
    │
    └── JobSkill
           └── Job

This allows the same skill to be reused across candidates and jobs.

It also reduces inconsistencies caused by storing skills as independent text values.

---

# 🏆 Candidate Ranking

Multiple candidates can be evaluated against a job.

The ranking pipeline is:

    Candidates
         │
         ▼
    Candidate Preparation
         │
         ▼
    Skill Matching
         │
         ▼
    Semantic Similarity
         │
         ▼
    Hybrid Scoring
         │
         ▼
    Sorting
         │
         ▼
    Ranked Candidates

Candidates are ranked according to their final hybrid match score.

---

# 💬 AI Match Explanation

Hirely uses Generative AI to explain matching results.

The explanation system is **evidence-grounded**.

The LLM receives structured matching evidence instead of being asked to independently inspect the entire candidate and job.

## Explanation Inputs

The AI can receive information such as:

- Final match score
- Required skill matches
- Missing required skills
- Preferred skill matches
- Missing preferred skills
- Semantic similarity
- Relevant candidate evidence
- Relevant job requirements

## Explanation Output

The explanation can communicate:

- Matching strengths
- Relevant skills
- Missing skills
- Semantic relevance
- Important matching evidence

The system is designed to prevent the model from inventing:

- Skills
- Experience
- Qualifications
- Certifications
- Hiring decisions

Structured AI output is validated using **Pydantic schemas**.

---

# 🧠 AI Architecture

Hirely follows a layered AI architecture.

    ┌───────────────────────────────────┐
    │             AI ENGINE             │
    └─────────────────┬─────────────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
     Document     Candidate/Job  Embeddings
     Processing   Representation
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
               Matching Engine
                      │
                      ▼
                   Ranking
                      │
                      ▼
               AI Explanation
                      │
                      ▼
                 Final Result

This architecture intentionally avoids building one large LLM call responsible for the entire recruitment decision.

Each component has a clearly defined responsibility.

---

# 🔐 Authentication & Authorization

Hirely uses **JWT-based authentication** with **Role-Based Access Control (RBAC)**.

## Supported Roles

- Candidate
- Recruiter

Protected resources verify:

1. Authentication
2. User identity
3. User role
4. Resource ownership where required

### Authorization Examples

    Candidate
        │
        └── Candidate Resources

    Recruiter
        │
        ├── Recruiter Resources
        └── Own Jobs

Unauthorized operations are rejected by the API.

---

# 🏗️ System Architecture

The planned production architecture separates the frontend from the backend API.

    ┌──────────────────────────┐
    │      React Frontend      │
    └────────────┬─────────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │     FastAPI REST API      │
    └────────────┬─────────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │ Authentication / RBAC     │
    └────────────┬─────────────┘
                 │
                 ▼
    ┌──────────────────────────┐
    │    Business Services      │
    └────────────┬─────────────┘
                 │
          ┌──────┴──────┐
          │             │
          ▼             ▼
    ┌───────────┐   ┌───────────────┐
    │ PostgreSQL│   │    AI Layer   │
    └───────────┘   └───────┬───────┘
                            │
                   ┌────────┼────────┐
                   │        │        │
                   ▼        ▼        ▼
                Gemini  Embeddings Matching

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL

## AI / Generative AI

- Google Gemini
- Gemini Embeddings
- Structured AI outputs
- Semantic similarity
- Hybrid matching
- AI orchestration

## Document Processing

- Docling
- PDF processing
- DOCX processing

## Authentication & Security

- JWT
- Password hashing
- Role-Based Access Control

## Frontend

- React

## Testing

- Pytest
- FastAPI TestClient
- Unit tests
- API tests
- Integration tests
- AI pipeline tests

## DevOps & Deployment

### Planned

- Docker
- Docker Compose
- AWS EC2
- Object storage
- Production environment configuration
- Monitoring and observability

---

# 📂 Project Structure

The project is organized around clear separation of concerns between the backend API, AI components, database layer, business services, tests, documentation, and frontend.

    Hirely/
    │
    ├── backend/
    │   │
    │   ├── app/
    │   │   │
    │   │   ├── ai/
    │   │   │   ├── embeddings/
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── gemini.py
    │   │   │   │
    │   │   │   ├── loaders/
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── document_loader.py
    │   │   │   │
    │   │   │   ├── matching/
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── skill_matcher.py
    │   │   │   │   ├── semantic_matcher.py
    │   │   │   │   ├── hybrid_scorer.py
    │   │   │   │   └── ranker.py
    │   │   │   │
    │   │   │   ├── parsers/
    │   │   │   │   ├── __init__.py
    │   │   │   │   └── resume_parser.py
    │   │   │   │
    │   │   │   ├── representations/
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── candidate_representation.py
    │   │   │   │   └── job_representation.py
    │   │   │   │
    │   │   │   └── services/
    │   │   │       ├── __init__.py
    │   │   │       ├── resume_service.py
    │   │   │       ├── embedding_service.py
    │   │   │       ├── matching_service.py
    │   │   │       └── explanation_service.py
    │   │   │
    │   │   ├── api/
    │   │   │   ├── __init__.py
    │   │   │   ├── dependencies.py
    │   │   │   │
    │   │   │   └── routes/
    │   │   │       ├── __init__.py
    │   │   │       ├── auth.py
    │   │   │       ├── candidates.py
    │   │   │       ├── recruiters.py
    │   │   │       ├── jobs.py
    │   │   │       ├── applications.py
    │   │   │       ├── skills.py
    │   │   │       ├── resumes.py
    │   │   │       └── matching.py
    │   │   │
    │   │   ├── core/
    │   │   │   ├── __init__.py
    │   │   │   ├── config.py
    │   │   │   ├── security.py
    │   │   │   └── exceptions.py
    │   │   │
    │   │   ├── db/
    │   │   │   ├── __init__.py
    │   │   │   ├── base.py
    │   │   │   └── session.py
    │   │   │
    │   │   ├── models/
    │   │   │   ├── __init__.py
    │   │   │   ├── user.py
    │   │   │   ├── candidate.py
    │   │   │   ├── recruiter.py
    │   │   │   ├── job.py
    │   │   │   ├── application.py
    │   │   │   ├── skill.py
    │   │   │   ├── candidate_skill.py
    │   │   │   ├── job_skill.py
    │   │   │   └── resume.py
    │   │   │
    │   │   ├── schemas/
    │   │   │   ├── __init__.py
    │   │   │   ├── auth.py
    │   │   │   ├── candidate.py
    │   │   │   ├── recruiter.py
    │   │   │   ├── job.py
    │   │   │   ├── application.py
    │   │   │   ├── skill.py
    │   │   │   ├── resume.py
    │   │   │   └── matching.py
    │   │   │
    │   │   ├── services/
    │   │   │   ├── __init__.py
    │   │   │   ├── auth_service.py
    │   │   │   ├── candidate_service.py
    │   │   │   ├── recruiter_service.py
    │   │   │   ├── job_service.py
    │   │   │   ├── application_service.py
    │   │   │   ├── skill_service.py
    │   │   │   └── resume_service.py
    │   │   │
    │   │   ├── storage/
    │   │   │   ├── __init__.py
    │   │   │   ├── base.py
    │   │   │   └── local_storage.py
    │   │   │
    │   │   └── main.py
    │   │
    │   ├── tests/
    │   │   ├── unit/
    │   │   │   ├── ai/
    │   │   │   ├── services/
    │   │   │   └── matching/
    │   │   │
    │   │   ├── api/
    │   │   │   ├── test_auth.py
    │   │   │   ├── test_candidates.py
    │   │   │   ├── test_recruiters.py
    │   │   │   ├── test_jobs.py
    │   │   │   ├── test_applications.py
    │   │   │   ├── test_skills.py
    │   │   │   ├── test_resumes.py
    │   │   │   └── test_matching.py
    │   │   │
    │   │   └── integration/
    │   │       ├── test_resume_pipeline.py
    │   │       ├── test_matching_pipeline.py
    │   │       └── test_ai_pipeline.py
    │   │
    │   ├── alembic/
    │   │   ├── versions/
    │   │   └── env.py
    │   │
    │   ├── requirements.txt
    │   ├── .env.example
    │   └── Dockerfile
    │
    ├── frontend/
    │   ├── src/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   ├── services/
    │   │   ├── hooks/
    │   │   ├── context/
    │   │   └── utils/
    │   │
    │   ├── public/
    │   ├── package.json
    │   └── Dockerfile
    │
    ├── docs/
    │   ├── 01_Project_Overview.md
    │   ├── 02_Research_and_Analysis.md
    │   └── 03_Software_Design_Document.md
    │
    ├── .github/
    │   └── workflows/
    │       └── tests.yml
    │
    ├── docker-compose.yml
    ├── .gitignore
    ├── README.md
    └── LICENSE

---

# 🗄️ Database Design

The backend currently contains core entities such as:

    User
    ├── Candidate
    │     ├── Resume
    │     ├── CandidateSkill
    │     └── Application
    │
    └── Recruiter
          └── Job
                ├── JobSkill
                └── Application

    Skill
    ├── CandidateSkill
    └── JobSkill

Applications connect candidates with jobs.

    Candidate ───── Application ───── Job

This supports the recruitment workflow while keeping skills normalized and reusable.

---

# 📄 Resume Storage Architecture

During development, resumes are stored using **local filesystem storage**.

The database stores a reference to the stored file rather than storing the physical file itself.

    Upload
       │
       ▼
    Validation
       │
       ▼
    Storage Service
       │
       ▼
    Local Filesystem
       │
       └── UUID-based physical filename

    Database
       │
       └── Storage reference

The production architecture is planned to use object storage such as **Amazon S3**.

---

# 🧪 Testing

Hirely follows a **test-driven verification approach** across the backend.

The test suite covers:

### Authentication & Security

- Authentication
- JWT
- RBAC
- Authorization
- Resource ownership

### Core APIs

- Candidate APIs
- Recruiter APIs
- Job APIs
- Application APIs
- Candidate skills
- Job skills

### Resume System

- Resume upload
- Resume APIs
- Resume activation
- Resume parsing
- Resume skill synchronization

### AI System

- AI pipelines
- Candidate representation
- Job representation
- Embeddings
- Matching components
- Matching orchestration
- Match explanation

---

## 📊 Current Regression Result

    142 passed
    0 failed

The complete backend regression suite currently passes successfully.

---

# 🚧 Project Status

Hirely is currently under active development.

## ✅ Completed

- [x] Project architecture
- [x] Database foundation
- [x] Authentication
- [x] JWT
- [x] Role-Based Access Control
- [x] Candidate profile
- [x] Recruiter profile
- [x] Job management
- [x] Applications
- [x] Skill management
- [x] Resume upload
- [x] Resume storage
- [x] Multiple resume versions
- [x] Active resume
- [x] Resume parsing
- [x] Resume → candidate skills
- [x] Candidate representation
- [x] Job representation
- [x] Gemini embeddings
- [x] Semantic similarity
- [x] Deterministic skill matching
- [x] Hybrid scoring
- [x] Candidate ranking
- [x] AI match explanation
- [x] AI orchestration
- [x] Backend regression testing

## 🚧 In Progress

- [ ] Matching FastAPI API
- [ ] Matching API integration tests
- [ ] Candidate-facing AI features
- [ ] Recruiter-facing AI features
- [ ] React frontend
- [ ] Frontend/backend integration

## 🔮 Planned

- [ ] Resume ATS checker
- [ ] Resume improvement
- [ ] AI career coach
- [ ] Cover letter generator
- [ ] Job description analyzer
- [ ] Advanced candidate search
- [ ] Docker deployment
- [ ] AWS deployment
- [ ] Security hardening
- [ ] Production optimization
- [ ] Monitoring and observability

---

# 🗺️ Development Roadmap

    Foundation
        ↓
    Research & Analysis
        ↓
    Software Design
        ↓
    Backend Architecture
        ↓
    Authentication & RBAC
        ↓
    Candidate / Recruiter / Jobs
        ↓
    Applications
        ↓
    Skills
        ↓
    Resume Management
        ↓
    Resume Parsing
        ↓
    Candidate & Job Representation
        ↓
    Embeddings
        ↓
    Semantic Matching
        ↓
    Skill Matching
        ↓
    Hybrid Scoring
        ↓
    Candidate Ranking
        ↓
    AI Match Explanation
        ↓
    Matching API                  ← CURRENT
        ↓
    AI Candidate Features
        ↓
    AI Recruiter Features
        ↓
    React Frontend
        ↓
    Frontend / Backend Integration
        ↓
    Testing & Optimization
        ↓
    Docker
        ↓
    AWS Deployment
        ↓
    Security Hardening
        ↓
    Production Release

---

# 🔬 Engineering Principles

Hirely is being developed around several core engineering principles.

## 1. Database as Source of Truth

Structured recruitment data remains in the database.

The AI layer should not become the authoritative source for structured candidate or job information.

---

## 2. Deterministic Logic Where Possible

Skills, relationships, permissions, and scoring rules should be:

- Predictable
- Testable
- Reproducible
- Easy to debug

---

## 3. LLM for Language Understanding

Generative AI is used where natural-language understanding and generation provide value.

Examples include:

- Resume understanding
- Structured extraction
- Match explanations
- Future candidate assistance
- Future recruiter assistance

---

## 4. Embeddings for Semantic Meaning

Embeddings are used to capture semantic relationships between candidate and job representations.

This helps identify relevant matches even when terminology differs.

---

## 5. Evidence-Grounded AI

AI-generated explanations should be based on actual matching evidence.

The LLM should explain the system's evidence rather than independently deciding whether a candidate should be hired.

---

## 6. Separation of Responsibilities

Different components handle different responsibilities:

- Authentication
- Authorization
- Data persistence
- Document processing
- Resume parsing
- Representation
- Embeddings
- Skill matching
- Semantic matching
- Scoring
- Ranking
- Explanation
- API orchestration

---

## 7. Test Before Moving Forward

Each major backend capability is tested before becoming a dependency for the next layer.

This reduces regressions and makes the system easier to evolve.

---

# 🔮 Future Vision

The long-term goal is for Hirely to become an intelligent recruitment platform where candidates, recruiters, and AI-assisted workflows work together.

## 👤 Candidates Can

- Build professional profiles
- Upload resumes
- Manage multiple resume versions
- Improve resumes
- Discover relevant jobs
- Understand their job match
- Identify skill gaps
- Generate cover letters
- Receive AI career guidance

---

## 🏢 Recruiters Can

- Create job descriptions
- Analyze job descriptions
- Define required skills
- Define preferred skills
- Discover relevant candidates
- Rank candidates automatically
- Understand why candidates match
- Manage applications efficiently

---

## 🤖 The AI System Can

- Understand resumes
- Understand job descriptions
- Extract structured information
- Represent candidates semantically
- Represent jobs semantically
- Generate embeddings
- Match candidates to opportunities
- Rank candidates
- Explain matching evidence
- Identify skill gaps
- Assist candidates with career development
- Assist recruiters with candidate discovery

---

# ⚠️ Responsible AI

Hirely is designed as a **recruitment assistance system** rather than an autonomous hiring decision-maker.

AI-generated results should be treated as **decision-support information**.

The system is designed to:

- Ground explanations in available evidence
- Avoid inventing candidate qualifications
- Separate deterministic signals from generated explanations
- Keep structured recruitment data as the source of truth
- Make matching logic measurable and testable

### Human-in-the-Loop

Human judgment remains important in recruitment decisions.

Hirely should assist recruiters and candidates rather than making irreversible hiring decisions autonomously.

---

# 👨‍💻 Development Journey

Hirely is being built as a **learning-in-public project** with a focus on understanding production-oriented AI engineering rather than simply connecting an LLM to an application.

The development process follows:

    Learn
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
    Document
      ↓
    Git
      ↓
    GitHub
      ↓
    Build in Public

The goal is to understand not only **what** is being built, but also **why** each architectural and engineering decision is made.

---

# 📚 Documentation

Project documentation is maintained in the `docs/` directory.

## Current Documentation

- `01_Project_Overview.md`
- `02_Research_and_Analysis.md`
- `03_Software_Design_Document.md`

These documents cover:

- Project vision
- Research
- Requirements
- Architecture
- System design
- AI architecture
- Database design
- Matching engine
- Candidate ranking
- AI explanation system

---

# 🔗 Repository

**GitHub:**  
https://github.com/Musharraf-Bubere/Hirely

---

# 📌 Disclaimer

Hirely is an actively developed **portfolio and learning project**.

Features, architecture, AI models, infrastructure, and production capabilities may continue to evolve as development progresses.

The current implementation and roadmap represent the project's development state and may change as new engineering requirements are identified.

---

# ⭐ Hirely

**Building an AI-powered recruitment platform with GenAI, semantic matching, and production-oriented software engineering.**

> 🚀 **Build. Learn. Test. Improve.**