# 🚀 Hirely

### AI-Powered Recruitment & Candidate Matching Platform

Hirely is an AI-powered recruitment platform designed to improve the way candidates discover opportunities and recruiters discover qualified talent.

The platform combines traditional recruitment workflows with Generative AI, semantic embeddings, deterministic skill matching, candidate ranking, and evidence-grounded AI explanations.

> **Project Status:** 🚧 Active Development  
> **Current Focus:** AI Matching API & Product Integration

---

## 📌 Overview

Traditional recruitment systems often rely heavily on keyword matching and manual candidate screening. This can make it difficult to identify candidates whose experience is relevant to a job but may be described using different terminology.

Hirely addresses this problem using a hybrid AI architecture.

Instead of relying entirely on an LLM, Hirely combines:

- Deterministic skill matching
- Semantic embeddings
- Weighted scoring
- Candidate ranking
- Generative AI explanations
- Structured data validation
- Traditional recruitment workflows

The goal is to build a recruitment system that is not only AI-powered, but also explainable, testable, maintainable, and production-oriented.

---

## 🎯 Problem Statement

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

Hirely aims to address these problems through a combination of conventional software engineering and AI.

---

## 💡 Core Idea

Hirely uses a hybrid matching architecture:

Candidate Resume
       ↓
Resume Parsing
       ↓
Candidate Representation
       ↓
Candidate Embedding
       │
       │
       ├──────────────────────┐
       ↓                      ↓
Skill Matching        Semantic Similarity
       │                      │
       └──────────┬───────────┘
                  ↓
           Hybrid Scoring
                  ↓
             Candidate
              Ranking
                  ↓
          AI Match Explanation

The system does not ask an LLM to make the entire hiring decision.

Instead:

- The database remains the source of truth.
- Deterministic logic handles structured matching.
- Embeddings capture semantic similarity.
- The matching engine combines measurable signals.
- Generative AI explains the evidence.

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
- PDF and DOCX validation
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

## 🏢 Recruiter Features

### Recruiter Profile

Recruiters have dedicated recruiter profiles and role-based access.

### Job Management

Recruiters can:

- Create jobs
- View jobs
- Manage active jobs
- Define required skills
- Define preferred skills

### Candidate Matching

Recruiters will be able to evaluate candidates using:

- Skill matching
- Semantic similarity
- Hybrid match scores
- Candidate ranking
- AI-generated match explanations

---

# 🤖 AI Features

## Resume Intelligence

Resume File
    ↓
Document Loader
    ↓
Document Processing
    ↓
Gemini
    ↓
Structured Resume Data

The parsed output is represented using validated structured schemas.

---

## Candidate Representation

Hirely creates a deterministic textual representation of a candidate using relevant information such as:

- Profile information
- Skills
- Experience
- Projects
- Education
- Certifications

Sensitive contact information such as email and phone numbers are excluded from the representation used for semantic matching.

---

## Job Representation

Jobs are represented using relevant information such as:

- Job title
- Description
- Location
- Employment type
- Experience level
- Required skills
- Preferred skills

Recruiter-specific and system metadata are excluded from the semantic representation.

---

## 🔢 Embeddings

Hirely uses Gemini embeddings to convert candidate and job representations into numerical vectors.

Candidate Representation
        ↓
     Embedding
        ↓
  Candidate Vector


Job Representation
        ↓
     Embedding
        ↓
     Job Vector

Semantic similarity is then calculated between the vectors.

The current embedding configuration uses a 768-dimensional vector representation.

---

# 🧩 Hybrid Matching Engine

Hirely does not depend on semantic similarity alone.

The matching engine combines deterministic skill matching with semantic similarity.

Current scoring configuration:

| Signal | Weight |
|---|---:|
| Required Skills | 50% |
| Preferred Skills | 20% |
| Semantic Similarity | 30% |

When a signal is unavailable, the available signals can be renormalized rather than inventing a score.

---

## 🎯 Skill Matching

The skill matching system distinguishes between:

### Required Skills

Skills that are explicitly required by a job.

### Preferred Skills

Skills that are useful but not mandatory.

The system identifies:

- Matched required skills
- Missing required skills
- Matched preferred skills
- Missing preferred skills

Skills are maintained as normalized shared entities.

Skill
├── CandidateSkill
│      └── Candidate
│
└── JobSkill
       └── Job

This allows the same skill to be reused across candidates and jobs.

---

# 🏆 Candidate Ranking

Multiple candidates can be evaluated against a job.

The ranking pipeline is:

Candidates
    ↓
Candidate Preparation
    ↓
Skill Matching
    ↓
Semantic Similarity
    ↓
Hybrid Scoring
    ↓
Sorting
    ↓
Ranked Candidates

Candidates are ranked by their final match score.

---

# 💬 AI Match Explanation

Hirely uses Generative AI to explain matching results.

The explanation system is evidence-grounded.

The LLM receives structured matching evidence instead of being asked to independently inspect the entire candidate and job.

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
- Hiring decisions

Structured AI output is validated using Pydantic schemas.

---

# 🧠 AI Architecture

Hirely follows a layered AI architecture:

                    AI ENGINE
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ↓              ↓              ↓
   Document       Representation   Embeddings
   Processing          │              │
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                Matching Engine
                       ↓
                    Ranking
                       ↓
                AI Explanation
                       ↓
                 Final Result

This architecture intentionally avoids building one large LLM call responsible for the entire recruitment decision.

---

# 🔐 Authentication & Authorization

Hirely uses JWT-based authentication with role-based access control.

Supported roles:

- Candidate
- Recruiter

Protected resources verify:

1. Authentication
2. User identity
3. User role
4. Resource ownership where required

Examples include:

Candidate → Candidate resources
Recruiter → Recruiter resources
Recruiter → Own jobs

Unauthorized operations are rejected by the API.

---

# 🏗️ System Architecture

The planned production architecture separates the frontend from the backend API.

┌──────────────────────┐
│    React Frontend    │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│    FastAPI REST API  │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Authentication / RBAC│
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│ Business Services    │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     ↓           ↓
 PostgreSQL     AI Layer
                   │
          ┌────────┼────────┐
          ↓        ↓        ↓
       Gemini  Embeddings  Matching

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL

## AI / GenAI

- Google Gemini
- Gemini Embeddings
- Generative AI structured outputs
- Semantic similarity
- Hybrid matching
- AI orchestration

## Document Processing

- Docling
- PDF processing
- DOCX processing

## Authentication

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

## Deployment

Planned:

- Docker
- Docker Compose
- AWS EC2
- Object storage
- Production environment configuration

---

# 📂 Project Structure

Hirely/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── embeddings/
│   │   │   ├── loaders/
│   │   │   ├── matching/
│   │   │   ├── parsers/
│   │   │   ├── representations/
│   │   │   └── services/
│   │   │
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── storage/
│   │
│   ├── tests/
│   ├── alembic/
│   └── requirements.txt
│
├── docs/
│   ├── 01_Project_Overview.md
│   ├── 02_Research_and_Analysis.md
│   └── 03_Software_Design_Document.md
│
└── README.md

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

During development, resumes are stored using local filesystem storage.

The database stores a reference to the stored file rather than storing the physical file itself.

Upload
   ↓
Validation
   ↓
Storage Service
   ↓
Filesystem
   │
   └── UUID-based physical filename

Database
   │
   └── Storage reference

The production architecture is planned to use object storage such as Amazon S3.

---

# 🧪 Testing

Hirely follows a test-driven verification approach across the backend.

The test suite covers:

- Authentication
- JWT
- RBAC
- Candidate APIs
- Recruiter APIs
- Job APIs
- Application APIs
- Candidate skills
- Job skills
- Resume APIs
- Resume activation
- Resume parsing
- Resume skill synchronization
- AI pipelines
- Matching components
- Matching orchestration
- Match explanation

### Current Regression Result

142 passed
0 failed

The complete backend regression suite currently passes successfully.

---

# 🚧 Project Status

Hirely is currently under active development.

## Completed

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

## In Progress

- [ ] Matching FastAPI API
- [ ] Matching API integration tests
- [ ] Candidate-facing AI features
- [ ] Recruiter-facing AI features
- [ ] React frontend
- [ ] Frontend/backend integration

## Planned

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
Matching API          ← CURRENT
    ↓
AI Candidate Features
    ↓
AI Recruiter Features
    ↓
React Frontend
    ↓
Integration
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

### Database as Source of Truth

Structured recruitment data remains in the database.

### Deterministic Logic Where Possible

Skills, relationships, permissions, and scoring rules should be predictable and testable.

### LLM for Language Understanding

Generative AI is used where natural-language understanding and generation provide value.

### Embeddings for Semantic Meaning

Embeddings provide semantic similarity between candidate and job representations.

### Evidence-Grounded AI

AI explanations should be based on actual matching evidence.

### Separation of Responsibilities

Different components handle:

- Authentication
- Data persistence
- Document processing
- Representation
- Embeddings
- Matching
- Ranking
- Explanation
- API orchestration

### Test Before Moving Forward

Each major backend capability is tested before becoming a dependency for the next layer.

---

# 🔮 Future Vision

The long-term goal is for Hirely to become an intelligent recruitment platform where:

### Candidates can

- Build professional profiles
- Upload and improve resumes
- Discover relevant jobs
- Understand their job match
- Identify skill gaps
- Generate cover letters
- Receive AI career guidance

### Recruiters can

- Create and analyze job descriptions
- Define required and preferred skills
- Discover relevant candidates
- Rank candidates automatically
- Understand why candidates match
- Manage applications efficiently

### The AI system can

- Understand resumes
- Understand job descriptions
- Represent candidates and jobs semantically
- Match candidates to opportunities
- Rank candidates
- Explain matching evidence
- Assist candidates with career development

---

# ⚠️ Responsible AI

Hirely is designed as a recruitment assistance system rather than an autonomous hiring decision-maker.

AI-generated results should be treated as decision-support information.

The system is designed to:

- Ground explanations in available evidence
- Avoid inventing candidate qualifications
- Separate deterministic signals from generated explanations
- Keep structured recruitment data as the source of truth

Human judgment remains important in recruitment decisions.

---

# 👨‍💻 Development Journey

Hirely is being built as a learning-in-public project with a focus on understanding production-oriented AI engineering rather than simply connecting an LLM to an application.

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

Current documentation includes:

- `01_Project_Overview.md`
- `02_Research_and_Analysis.md`
- `03_Software_Design_Document.md`

These documents cover the project vision, research, architecture, system design, AI architecture, matching engine, ranking, and explanation system.

---

# 🔗 Repository

GitHub:

https://github.com/Musharraf-Bubere/Hirely

---

# 📌 Disclaimer

Hirely is an actively developed portfolio and learning project.

Features, architecture, AI models, infrastructure, and production capabilities may continue to evolve as development progresses.

---

## ⭐ Hirely

**Building an AI-powered recruitment platform with GenAI, semantic matching, and production-oriented software engineering.**

🚀 **Build. Learn. Test. Improve.**
