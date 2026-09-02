# Software Design Document

## Introduction

This document defines the software architecture and component-level design of **Hirely**, an AI-powered recruitment platform.

The purpose of this document is to translate the requirements and research performed during the project into a practical, maintainable, scalable, and production-oriented software design.

Hirely is designed as a layered application in which traditional recruitment functionality forms the foundation and a dedicated Generative AI layer provides intelligent capabilities such as resume analysis, job description understanding, candidate-job matching, ranking, and explanations.

The architecture is intentionally designed to keep the core business logic independent from AI providers and models. This allows the AI capabilities to evolve without requiring major changes to the rest of the application.

The major architectural layers are:

- Presentation Layer
- API Layer
- Business Logic Layer
- Data Access Layer
- Database Layer
- AI/GenAI Layer

The architecture follows separation of concerns so that each layer has a clearly defined responsibility.

---

# System Architecture

## Architecture Overview

Hirely follows a layered architecture with a dedicated AI/GenAI layer.

The high-level architecture is:

    React Frontend
          |
          v
    FastAPI REST API
          |
          v
    Pydantic Validation
          |
          v
    Business Logic / Services
          |
          +----------------------+
          |                      |
          v                      v
    SQLAlchemy ORM          AI/GenAI Services
          |                      |
          v                      +----------------------+
      Database                  |                      |
                                v                      v
                             LLMs                Embedding Models

The traditional application flow handles authentication, candidates, recruiters, jobs, applications, and skills.

The AI layer operates alongside the business logic layer and interacts with structured application data as well as unstructured documents such as resumes and job descriptions.

The separation is important because not every recruitment operation requires AI.

For example:

- Authentication should be deterministic.
- Authorization should be deterministic.
- Application creation should be deterministic.
- Skill association should be deterministic.
- Resume understanding can use AI.
- Job description understanding can use AI.
- Semantic candidate-job matching can use embeddings and AI.
- Match explanations can use an LLM.

This prevents unnecessary LLM usage and makes the system easier to test and control.

---

## Architectural Principles

The Hirely architecture follows several important engineering principles.

### Separation of Concerns

Each layer is responsible for a specific category of work.

The API layer should not contain database-heavy business logic.

The service layer should not be responsible for HTTP-specific behavior.

The database layer should not contain AI prompting logic.

The AI layer should not directly control authentication or authorization.

This separation keeps components independently understandable and maintainable.

### Modular Design

Hirely is divided into domain-oriented modules such as:

- Authentication
- Candidate
- Recruiter
- Job
- Application
- Skill
- AI

Each domain can evolve independently while communicating through clearly defined interfaces.

### AI Provider Independence

The application should not tightly couple its business logic to a specific LLM provider.

Instead of placing provider-specific code throughout the application, AI interactions should be isolated behind AI services.

This allows the project to change models or providers without rewriting the entire application.

### Deterministic First

The system should use deterministic application logic whenever reliable structured information is already available.

For example, if the database states that a candidate has the skill `Python`, the system should not ask an LLM whether the candidate has Python.

AI should be used where interpretation, semantic understanding, or natural-language reasoning provides meaningful value.

### Explainability

Recruitment decisions can have significant consequences.

Therefore, Hirely should not only produce a match score.

The AI system should eventually provide supporting information such as:

- Matching skills
- Missing skills
- Relevant experience
- Related experience
- Strengths
- Potential gaps
- Explanation of the recommendation

The final design should therefore favor explainable matching rather than an unexplained numerical score.

### Testability

Traditional business logic should remain independently testable.

AI functionality should also be designed so that model-dependent behavior can be tested separately from deterministic application logic.

This allows Hirely to maintain reliable automated testing even when AI models change.

---

# Presentation Layer

## React Frontend

The frontend of Hirely will be implemented using **React**.

The React application is responsible for presenting the user interface and communicating with the backend through REST APIs.

The frontend should not directly communicate with the database.

It should also not contain sensitive AI provider credentials.

The frontend will eventually provide different experiences for candidates and recruiters.

### Candidate Experience

Candidates will be able to:

- Register and authenticate
- Manage their profile
- Add skills
- Upload resumes
- View jobs
- Apply for jobs
- View application status
- Receive AI-powered recommendations
- Understand why a job may be a good match

### Recruiter Experience

Recruiters will be able to:

- Register and authenticate
- Manage recruiter information
- Create jobs
- Define required and optional skills
- View applications
- Review candidates
- Receive AI-powered candidate rankings
- View candidate-job match explanations

The frontend communicates with the FastAPI backend through HTTP requests.

---

# API Layer

## FastAPI REST API

Hirely uses **FastAPI** as the backend API framework.

The API layer acts as the entry point into the application backend.

Its responsibilities include:

- Receiving HTTP requests
- Authentication handling
- Authorization enforcement
- Request validation
- Calling appropriate services
- Returning HTTP responses
- Translating application errors into appropriate HTTP status codes

The API layer should remain relatively thin.

Complex business operations should be delegated to service modules.

For example:

    POST /jobs/{job_id}/skills

The API route should:

1. Authenticate the user.
2. Verify recruiter authorization.
3. Validate the request.
4. Call the JobSkill service.
5. Return the result.

The route should not contain all the underlying database and business logic itself.

---

# Validation Layer

## Pydantic

Pydantic models are used to validate incoming and outgoing API data.

Examples include:

- Registration requests
- Login requests
- Job creation requests
- Skill creation requests
- Application requests
- AI service input/output schemas

Pydantic provides a boundary between external user input and internal application logic.

This is particularly important for AI systems because AI-generated output must eventually be validated before it is treated as structured application data.

The AI layer should therefore produce structured outputs that can be validated rather than allowing arbitrary model text to directly modify application state.

---

# Business Logic Layer

## Service Layer

The service layer contains the core application business logic.

Examples include:

- Authentication services
- Candidate services
- Recruiter services
- Job services
- Application services
- Skill services
- CandidateSkill services
- JobSkill services
- AI services

The service layer is independent from HTTP-specific concerns as much as practical.

For example:

    Candidate
        |
        +-- CandidateSkill
        |
        +-- Skill

and:

    Job
        |
        +-- JobSkill
        |
        +-- Skill

The service layer controls operations involving these relationships.

This architecture also provides a clean location for AI orchestration.

For example:

    Match Candidate To Job
            |
            +-- Retrieve candidate data
            +-- Retrieve job data
            +-- Perform deterministic matching
            +-- Generate embeddings
            +-- Calculate semantic similarity
            +-- Invoke LLM when required
            +-- Validate AI output
            +-- Generate explanation
            +-- Return structured result

---

# Data Access Layer

## SQLAlchemy

SQLAlchemy is used as the ORM and data access layer.

The application models represent the persistent entities in Hirely.

Current major entities include:

- User
- Candidate
- Recruiter
- Company
- Job
- Application
- Skill
- CandidateSkill
- JobSkill

SQLAlchemy provides the interface between application services and the relational database.

The service layer should interact with the database through SQLAlchemy rather than embedding raw database operations throughout API routes.

---

# Database Layer

## Relational Database

Hirely uses a relational database for structured application data.

The database stores information that requires reliable persistence, relationships, constraints, and transactional integrity.

Examples include:

### Users

Stores authentication and role information.

### Candidates

Stores candidate profile information.

### Recruiters

Stores recruiter information.

### Jobs

Stores job postings and their requirements.

### Applications

Stores candidate applications and application status.

### Skills

Stores the shared skill vocabulary.

### CandidateSkill

Connects candidates with skills.

### JobSkill

Connects jobs with required or optional skills.

The shared Skill model is particularly important for the future AI matching system.

Instead of storing skills independently inside candidates and jobs, Hirely maintains a shared vocabulary:

    Candidate
        |
        v
    CandidateSkill
        |
        v
      Skill
        ^
        |
      JobSkill
        ^
        |
       Job

This provides structured information that can be used by the matching engine.

---

# AI/GenAI Layer

## AI Layer Overview

The AI/GenAI layer is the primary intelligence layer of Hirely.

It is responsible for capabilities that require language understanding, semantic analysis, information extraction, or AI-assisted reasoning.

The AI layer should remain logically separated from the traditional recruitment business logic.

Its initial major responsibilities are:

- Resume Analysis
- Job Description Analysis
- Candidate Representation
- Job Representation
- Semantic Matching
- Candidate Ranking
- Match Explanation
- AI-powered Recommendations

The AI layer may use multiple technologies rather than relying on a single LLM.

A likely architecture is:

    Structured Data
          |
          v
    Deterministic Matching
          |
          +----------------+
          |                |
          v                v
     Embeddings           LLM
          |                |
          +-------+--------+
                  |
                  v
            Matching Engine
                  |
                  v
          Structured Result
                  |
                  v
             Explanation

The exact models and providers will be selected during the AI architecture and implementation phase.

---

# AI Responsibilities vs Traditional Responsibilities

A key design decision is that Hirely should not treat the LLM as the entire application.

Traditional backend logic should remain responsible for operations where deterministic behavior is appropriate.

| Responsibility | Traditional Backend | AI/GenAI |
|---|---|---|
| Authentication | Yes | No |
| Authorization | Yes | No |
| User roles | Yes | No |
| Application creation | Yes | No |
| Application status | Yes | No |
| Skill relationships | Yes | No |
| Database integrity | Yes | No |
| Resume understanding | No | Yes |
| Job description understanding | No | Yes |
| Semantic similarity | No | Yes / Embeddings |
| Candidate-job reasoning | Partially | Yes |
| Match explanation | No | Yes |
| Candidate recommendations | Partially | Yes |

This separation is critical for reliability.

An LLM should not be trusted to decide whether a user is authorized to modify a job.

Authorization must remain deterministic.

Similarly, an LLM should not be responsible for directly creating database records without validation.

---

# High-Level AI Data Flow

The eventual AI flow will follow a pipeline similar to:

    Resume
       |
       v
    Document Processing
       |
       v
    Resume Analysis
       |
       v
    Structured Candidate Representation
       |
       v
    Candidate Embedding
       |
       |
       +--------------------------+
                                  |
                                  v
    Job Description --> Job Analysis
                                  |
                                  v
                     Structured Job Representation
                                  |
                                  v
                            Job Embedding
                                  |
                                  v
                         Matching Engine
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             Structured Match             Semantic Match
                    |                           |
                    +-------------+-------------+
                                  |
                                  v
                            Final Match
                                  |
                                  v
                          Explanation Layer
                                  |
                                  v
                       Recruiter / Candidate

This pipeline will be refined during the detailed AI component design.

---

# AI Component Boundaries

The AI system should be divided into smaller components rather than implementing one large AI service.

The planned components are:

### Resume Analysis Component

Responsible for understanding resume content and extracting structured information.

### Job Analysis Component

Responsible for understanding job descriptions and extracting requirements.

### Candidate Representation Component

Creates a useful representation of the candidate for matching.

### Job Representation Component

Creates a useful representation of the job for matching.

### Matching Component

Combines structured and semantic signals to determine candidate-job compatibility.

### Ranking Component

Ranks multiple candidates for a particular job.

### Explanation Component

Generates human-readable explanations for matching and ranking results.

### AI Orchestration Component

Coordinates the execution of the different AI capabilities.

The detailed design of these components will be developed in the Component Design section.

---

# Communication Between Components

The major communication flow is:

    React
      |
      | HTTP/JSON
      v
    FastAPI
      |
      | validated request
      v
    Service Layer
      |
      +--------------------+
      |                    |
      v                    v
    Database          AI Services
                           |
                           +---- LLM
                           |
                           +---- Embedding Model
                           |
                           +---- AI Processing
      |                    |
      +---------+----------+
                |
                v
          Structured Result
                |
                v
             FastAPI
                |
                v
             React

Communication contracts should use structured schemas wherever possible.

This becomes especially important for AI-generated information.

---

# Security Boundary

The AI layer must not bypass the application's existing security model.

For example:

    User
      |
      v
    Authentication
      |
      v
    Authorization
      |
      v
    AI Endpoint
      |
      v
    AI Service

The AI service should receive only the information required for its task.

Sensitive information should not be unnecessarily sent to external AI providers.

API keys and model credentials must remain on the backend and should be supplied through environment variables or a secure secret-management mechanism.

Security considerations will be expanded in the dedicated Security section of the project.

---

# Scalability Considerations

The AI layer may require significantly more computational resources than traditional CRUD operations.

For example:

- Resume parsing may involve document processing.
- Embedding generation may be computationally expensive.
- LLM requests depend on external model infrastructure.
- Matching large numbers of candidates may require vector search.
- Batch candidate ranking may require asynchronous processing.

Therefore, the architecture should avoid tightly coupling expensive AI operations to ordinary synchronous CRUD operations.

The system can later evolve toward:

    FastAPI
       |
       +---- Synchronous API operations
       |
       +---- Background AI processing
                         |
                         v
                    AI Services
                         |
                         v
                  LLM / Embeddings

As Hirely grows, background workers, queues, caching, and vector databases can be introduced where justified.

These technologies should be added based on actual architectural requirements rather than prematurely.

---

# Architecture Decision

The selected architecture for Hirely is a **layered modular architecture with a dedicated AI/GenAI layer**.

The architecture consists of:

    React
      ↓
    FastAPI
      ↓
    Pydantic Validation
      ↓
    Business Services
      ↓
    SQLAlchemy
      ↓
    Relational Database

with AI services integrated alongside the business service layer:

    Business Services
          |
          +------ AI Services
                    |
                    +------ LLM
                    +------ Embeddings
                    +------ AI Processing

This architecture was selected because it provides:

- Clear separation of responsibilities
- Maintainability
- Testability
- AI provider flexibility
- Strong database integrity
- Secure API boundaries
- Future scalability
- Clear integration points for GenAI
- A strong foundation for AI-powered matching

---

# Mental Model

A useful mental model for Hirely is:

    Traditional Backend
            =
    Reliable Source of Truth

            +

    AI Layer
            =
    Intelligent Interpretation

The database knows structured facts.

The AI understands unstructured information and semantic relationships.

The matching engine combines both.

For example:

    Database:
    Candidate has Python.

    Resume:
    Candidate developed production APIs using
    Python and FastAPI.

    Job:
    Requires Python and backend API development.

The deterministic layer can identify the explicit Python skill.

The AI layer can understand the broader context of the candidate's experience.

The matching system can then combine these signals into a more meaningful assessment.

---

# Key Takeaways

- Hirely uses a layered modular architecture.
- React is responsible for the user interface.
- FastAPI provides the REST API.
- Pydantic validates external and structured data.
- Services contain business logic.
- SQLAlchemy provides database access.
- The relational database remains the source of truth for structured recruitment data.
- Skills are represented using a shared Skill model with CandidateSkill and JobSkill relationships.
- The AI/GenAI layer is separated from traditional business logic.
- Deterministic logic should be used wherever structured information is sufficient.
- LLMs should be used for language understanding and reasoning tasks where they provide meaningful value.
- Embeddings will provide semantic representations for candidate-job matching.
- The eventual matching system will combine structured matching, semantic matching, and AI reasoning.
- AI-generated information should be validated before becoming trusted application data.
- The architecture is designed so AI providers and models can change without requiring major changes to the core application.
- The AI/GenAI component will be the primary intelligence layer of Hirely.

# Component Design

## Component Design Overview

The component design defines the internal responsibilities of the major Hirely components and how they interact with one another.

The most important component in Hirely is the AI/GenAI component because intelligent recruitment is the primary differentiating capability of the platform.

The AI component is not designed as a single monolithic LLM call.

Instead, it is divided into specialized components that work together:

    AI/GenAI Component
           |
           +-- Resume Analysis
           |
           +-- Job Description Analysis
           |
           +-- Candidate Representation
           |
           +-- Job Representation
           |
           +-- Embedding Generation
           |
           +-- Matching Engine
           |
           +-- Ranking Engine
           |
           +-- Explanation Engine
           |
           +-- AI Orchestration

This modular approach allows each capability to be developed, tested, improved, and replaced independently.

---

# AI/GenAI Component

## Purpose

The AI/GenAI component provides intelligent capabilities that cannot be efficiently implemented using traditional deterministic application logic alone.

Its primary purpose is to understand unstructured recruitment information and transform it into useful representations that can support candidate-job matching.

The AI component will work with information such as:

- Resumes
- Job descriptions
- Candidate experience
- Candidate projects
- Candidate skills
- Job requirements
- Job responsibilities
- Qualifications
- Technologies
- Semantic relationships between candidate experience and job requirements

The AI component should ultimately help answer questions such as:

- What skills does this candidate have?
- What experience does this candidate have?
- What does this job actually require?
- How closely does this candidate match the job?
- Which requirements are satisfied?
- Which requirements are missing?
- Does the candidate have related or transferable experience?
- Which candidates are strongest for this job?
- Why was a candidate ranked highly?

---

# AI Component Responsibilities

The AI component will initially have the following responsibilities:

### Resume Analysis

Understand uploaded resumes and extract meaningful candidate information.

### Job Description Analysis

Understand job descriptions and extract requirements and responsibilities.

### Candidate Representation

Create a structured and semantic representation of a candidate.

### Job Representation

Create a structured and semantic representation of a job.

### Embedding Generation

Convert candidate and job information into vector representations that can be compared semantically.

### Matching

Determine how well a candidate matches a job using multiple signals.

### Ranking

Rank multiple candidates against a specific job.

### Explanation

Generate human-readable reasoning explaining the match.

### AI Orchestration

Coordinate the different AI operations and ensure that the correct components are executed in the correct order.

---

# Resume Analysis Component

## Purpose

The Resume Analysis component converts unstructured resume content into structured candidate information.

A resume may be provided as:

- PDF
- DOCX
- Text
- Other supported document formats

The first step is document processing.

The high-level flow is:

    Resume File
         |
         v
    Document Loader
         |
         v
    Text Extraction
         |
         v
    Text Cleaning
         |
         v
    Resume Analyzer
         |
         v
    Structured Candidate Data

The extracted information may include:

- Name
- Contact information
- Skills
- Education
- Work experience
- Projects
- Certifications
- Technologies
- Achievements

The extracted information should not immediately be trusted as authoritative database information.

AI-generated information must pass through validation before it becomes part of the application's trusted structured data.

---

# Resume Analysis Using LLMs

Large Language Models are useful for interpreting the semantic meaning of resume content.

For example, a resume may contain:

    Developed REST APIs using FastAPI and PostgreSQL.
    Containerized services using Docker.

A simple keyword search could identify:

    FastAPI
    PostgreSQL
    Docker

However, an LLM can additionally understand contextual information such as:

- The candidate developed backend services.
- FastAPI was used for API development.
- PostgreSQL was used for persistence.
- Docker was used for containerization.

This semantic understanding can later contribute to candidate-job matching.

The LLM should therefore be used primarily for interpretation rather than as the application's source of truth.

---

# Structured Resume Output

The Resume Analysis component should produce structured output rather than relying solely on free-form text.

A conceptual representation is:

    CandidateProfile
        |
        +-- Skills
        +-- Experience
        +-- Education
        +-- Projects
        +-- Certifications
        +-- Technologies

A structured output allows the rest of the application to work with predictable data.

This also allows Pydantic validation to be applied before the result is persisted or used by other components.

---

# Job Description Analysis Component

## Purpose

The Job Description Analysis component converts an unstructured job description into structured requirements.

The input may contain:

- Job title
- Description
- Responsibilities
- Required qualifications
- Preferred qualifications
- Required technologies
- Optional technologies
- Experience requirements

The flow is:

    Job Description
          |
          v
    Text Processing
          |
          v
    Job Analyzer
          |
          v
    Structured Job Representation

The component should distinguish between required and optional requirements whenever the information can be reliably determined.

This distinction is important because a missing required skill should have a stronger effect on matching than a missing optional skill.

---

# Job Representation

A conceptual representation of a job is:

    JobRepresentation
        |
        +-- Job Title
        +-- Required Skills
        +-- Optional Skills
        +-- Experience Requirements
        +-- Responsibilities
        +-- Qualifications
        +-- Technologies
        +-- Semantic Representation

The structured requirements can be compared directly against candidate information.

The semantic representation can be compared using embeddings.

---

# Candidate Representation

## Purpose

The Candidate Representation component creates a consistent representation of the candidate for matching.

Candidate information can come from multiple sources:

    Candidate Database
           |
           +-- Profile
           +-- Skills
           +-- Experience
           +-- Education
           |
           v
        Resume
           |
           v
    Resume Analysis
           |
           v
    Candidate Representation

The candidate representation should combine trusted structured information with validated information extracted from unstructured documents.

This produces a richer representation than using either the database or resume alone.

---

# Job Representation

The Job Representation component performs a similar function for job postings.

The job representation can combine:

    Job Database
         |
         +-- Title
         +-- Description
         +-- JobSkill
         |
         v
    Job Description Analysis
         |
         v
    Job Representation

The result provides both structured and semantic information about the job.

---

# Embedding Component

## Purpose

Embeddings provide a numerical representation of semantic meaning.

Instead of representing a candidate or job only through exact keywords, the system can represent their meaning in vector form.

Conceptually:

    Candidate
       |
       v
    Text Representation
       |
       v
    Embedding Model
       |
       v
    Candidate Vector

and:

    Job
       |
       v
    Text Representation
       |
       v
    Embedding Model
       |
       v
    Job Vector

The two vectors can then be compared using a similarity measure.

---

# Why Embeddings Are Important

Keyword matching has limitations.

For example:

    Candidate:
    "Built scalable REST APIs using FastAPI."

    Job:
    "Experience developing backend web services."

There may not be an exact keyword match for every concept.

Semantic representations can identify that these statements are related.

Embeddings therefore provide a mechanism for measuring semantic similarity between candidate and job information.

However, embedding similarity should not be treated as the complete matching decision.

It should be one signal within a broader matching system.

---

# Matching Engine

## Purpose

The Matching Engine combines multiple signals to determine candidate-job compatibility.

The matching engine is one of the most important components of Hirely.

The initial conceptual architecture is:

    Candidate
       |
       +------------------+
       |                  |
       v                  v
    Structured        Semantic
    Matching          Matching
       |                  |
       |                  |
       v                  v
    Skill Match       Embedding
    Experience        Similarity
    Requirements
       |                  |
       +--------+---------+
                |
                v
         Matching Engine
                |
                v
           Final Score

The final implementation will determine the exact scoring methodology.

---

# Deterministic Matching

Deterministic matching uses structured application data and explicit rules.

For example:

    Candidate Skills:
    Python
    FastAPI
    SQL

    Job Requirements:
    Python REQUIRED
    FastAPI REQUIRED
    Docker REQUIRED
    SQL OPTIONAL

The deterministic matching layer can identify:

    Python   → Match
    FastAPI  → Match
    Docker   → Missing
    SQL      → Match

This information is reliable because it comes from structured data.

The deterministic layer should therefore be responsible for explicit requirements whenever reliable structured information is available.

---

# Semantic Matching

Semantic matching uses embeddings to identify relationships that may not be represented by exact keyword overlap.

For example:

    Candidate:
    "Developed production REST APIs using FastAPI."

    Job:
    "Experience building scalable backend web services."

These statements may be semantically related even if they do not contain identical words.

Semantic matching can therefore provide an additional signal for compatibility.

---

# AI Reasoning

Some matching situations require deeper interpretation.

For example:

    Candidate:
    "Built a recommendation system using
     machine learning and Python."

    Job:
    "Experience building intelligent ranking
     systems is preferred."

The relationship may be meaningful even if the candidate does not explicitly use the phrase "ranking system."

An LLM can be used to analyze such contextual relationships.

However, the result should be treated as an AI-derived signal rather than an unquestionable fact.

---

# Hybrid Matching Architecture

Hirely will use a hybrid matching architecture.

The conceptual model is:

    Candidate
        |
        +----------------------+
        |                      |
        v                      v
    Structured              Semantic
    Information             Information
        |                      |
        v                      v
    Deterministic          Embeddings
    Matching                   |
        |                      |
        +----------+-----------+
                   |
                   v
             Matching Engine
                   |
                   +------ AI Reasoning
                   |
                   v
              Final Result

This architecture combines:

- Exact structured matching
- Semantic similarity
- Contextual AI reasoning

This is more robust than depending entirely on keyword matching or an LLM.

---

# Match Score

The matching engine should eventually produce a structured result rather than only a single number.

A conceptual result is:

    MatchResult
        |
        +-- Overall Score
        +-- Skill Match
        +-- Experience Match
        +-- Semantic Match
        +-- Required Skill Matches
        +-- Missing Required Skills
        +-- Optional Skill Matches
        +-- Relevant Experience
        +-- Explanation

The exact scoring formula will be determined during implementation and experimentation.

The system should avoid presenting a score as an objective measurement of a person's worth.

The score should represent compatibility with the specific job according to the signals used by Hirely.

---

# Ranking Component

## Purpose

The Ranking Component ranks candidates for a particular job.

The flow is:

    Job
      |
      v
    Retrieve Candidates
      |
      v
    Candidate-Job Matching
      |
      v
    Match Scores
      |
      v
    Ranking Engine
      |
      v
    Ranked Candidates

For example:

    Job: Senior Python Developer

    Candidate A → 91
    Candidate B → 87
    Candidate C → 82
    Candidate D → 76

The ranking system should retain supporting match information so that recruiters can understand why candidates received their positions.

---

# Ranking and Explainability

A ranking without an explanation can be difficult for recruiters to trust.

Therefore, the ranking result should eventually provide information such as:

    Candidate A
    Overall Match: 91

    Strong matches:
    - Python
    - FastAPI
    - PostgreSQL

    Experience:
    - 5 years backend development

    Missing:
    - Kubernetes

    Reason:
    Strong alignment with the required backend
    technologies and experience requirements.

This makes the ranking more transparent.

---

# Explanation Component

## Purpose

The Explanation Component converts structured matching information into human-readable explanations.

The explanation should be grounded in the actual matching signals.

The system should not allow an LLM to invent candidate qualifications.

The preferred flow is:

    Structured Match Data
             |
             v
       Explanation LLM
             |
             v
       Human-readable
         explanation

The LLM should receive relevant evidence from the matching engine rather than being asked to independently evaluate the entire candidate.

This reduces the risk of unsupported claims.

---

# Evidence-Grounded Explanations

The explanation system should distinguish between:

### Observed Evidence

Information explicitly available in the candidate's profile, resume, or structured data.

### Derived Information

Information calculated by the matching engine.

### AI Interpretation

A semantic interpretation produced by the AI system.

For example:

    Observed:
    Candidate has Python skill.

    Derived:
    Python is a required skill for the job.

    AI Interpretation:
    Candidate's backend experience is relevant
    to the role.

This separation improves transparency and reduces hallucination risk.

---

# AI Orchestration Component

## Purpose

The AI Orchestration Component coordinates the AI workflow.

It determines:

- Which AI operation should run
- In what order components should execute
- Which information should be passed between components
- Which results require validation
- Which results should be persisted
- Which operations can be skipped because structured information is already available

A conceptual flow is:

    AI Orchestrator
          |
          +-- Resume Analysis
          |
          +-- Job Analysis
          |
          +-- Candidate Representation
          |
          +-- Job Representation
          |
          +-- Embedding Generation
          |
          +-- Matching
          |
          +-- Ranking
          |
          +-- Explanation

The orchestrator should coordinate these operations without containing all the implementation details itself.

---

# AI and Database Interaction

The AI layer should interact with the database through application services rather than bypassing the normal data-access architecture.

For example:

    AI Service
        |
        v
    Candidate Service
        |
        v
    SQLAlchemy
        |
        v
    Database

Similarly:

    AI Service
        |
        v
      Job Service
        |
        v
    SQLAlchemy
        |
        v
    Database

This keeps the database access architecture consistent throughout the application.

---

# AI Output Validation

AI output should never automatically become trusted application data.

The flow should be:

    LLM
      |
      v
    Raw AI Output
      |
      v
    Structured Schema
      |
      v
    Validation
      |
      +---- Invalid → Reject / Retry
      |
      v
    Valid AI Result
      |
      v
    Application Logic

Pydantic schemas can be used to validate structured AI outputs.

This is particularly important when AI output is later used for:

- Candidate profiles
- Job requirements
- Match results
- Rankings
- Recommendations

---

# Hallucination Control

LLMs can generate information that was not present in the source material.

Hirely should therefore use several strategies to reduce hallucinations.

### Ground AI Analysis in Source Documents

The model should analyze the actual resume or job description rather than relying on assumptions.

### Use Structured Output

AI results should be returned in predictable schemas.

### Validate Output

Generated results should be validated before being used by application logic.

### Use Deterministic Data Where Available

Known database facts should not be unnecessarily regenerated by an LLM.

### Ground Explanations in Match Evidence

Explanations should be generated from structured matching evidence.

### Avoid Unsupported Claims

The system should not claim that a candidate possesses a skill or experience unless there is supporting evidence.

---

# AI Component Communication

The AI components should communicate through structured interfaces.

A conceptual interface is:

    ResumeAnalyzer
        |
        v
    CandidateRepresentation

    JobAnalyzer
        |
        v
    JobRepresentation

    CandidateRepresentation
        +
    JobRepresentation
        |
        v
    MatchingEngine
        |
        v
    RankingEngine
        |
        v
    ExplanationEngine

This makes each component independently testable.

---

# Synchronous vs Asynchronous AI Processing

Not every AI operation should necessarily run synchronously inside an HTTP request.

Some operations may be computationally expensive or dependent on external model APIs.

For example:

    Resume Upload
          |
          v
    Create Processing Job
          |
          v
    Background AI Processing
          |
          v
    Resume Analysis
          |
          v
    Embedding Generation
          |
          v
    Store Result

The frontend can later retrieve the processing status.

For smaller operations, synchronous processing may initially be acceptable.

The architecture should therefore support asynchronous processing as Hirely grows.

---

# AI Component Security

The AI layer must follow the same security boundaries as the rest of Hirely.

Sensitive credentials such as:

- LLM API keys
- Embedding provider credentials
- Database credentials

must never be exposed to the frontend.

AI provider credentials must remain on the backend.

The AI service should receive only the minimum information required for a particular operation.

Candidate resumes and personal information should be handled carefully because recruitment data can contain sensitive personal information.

Detailed security and privacy controls will be addressed in the dedicated Security section.

---

# AI Provider Abstraction

The application should avoid tightly coupling business logic to a specific AI provider.

Instead of:

    JobService
        |
        v
    SpecificLLMProvider

the architecture should prefer:

    JobService
        |
        v
    AI Service Interface
        |
        +---- Provider A
        +---- Provider B
        +---- Local Model

This allows Hirely to change models or providers without rewriting the entire application.

The exact provider and model selection will be determined during implementation and experimentation.

---

# Vector Storage Consideration

As semantic matching grows, Hirely may require persistent vector storage.

A conceptual architecture is:

    Candidate Representation
            |
            v
        Embedding
            |
            v
       Vector Storage

    Job Representation
            |
            v
        Embedding
            |
            v
       Vector Storage

The system can then perform semantic similarity searches.

A vector database or a relational database with vector capabilities may eventually be introduced.

The final choice should depend on:

- Dataset size
- Search requirements
- Infrastructure complexity
- Performance
- Cost
- Operational requirements

Vector storage should not be introduced merely because it is an AI technology.

It should be introduced when the application's retrieval and matching requirements justify it.

---

# End-to-End AI Matching Flow

The complete conceptual workflow is:

    ┌──────────────────┐
    │ Candidate Resume │
    └────────┬─────────┘
             |
             v
    ┌──────────────────┐
    │ Document Process  │
    └────────┬─────────┘
             |
             v
    ┌──────────────────┐
    │ Resume Analysis  │
    │      LLM         │
    └────────┬─────────┘
             |
             v
    ┌────────────────────────┐
    │ Candidate Representation│
    └───────────┬────────────┘
                |
                v
         ┌─────────────┐
         │  Embedding  │
         └──────┬──────┘
                |
                |
                |       ┌──────────────────┐
                |       │  Job Description │
                |       └────────┬─────────┘
                |                |
                |                v
                |       ┌──────────────────┐
                |       │   Job Analysis   │
                |       │       LLM        │
                |       └────────┬─────────┘
                |                |
                |                v
                |       ┌──────────────────┐
                |       │ Job Representation│
                |       └────────┬─────────┘
                |                |
                |                v
                |         ┌─────────────┐
                |         │  Embedding  │
                |         └──────┬──────┘
                |                |
                +-------+--------+
                        |
                        v
                ┌─────────────────┐
                │ Matching Engine │
                └────────┬────────┘
                         |
             +-----------+-----------+
             |                       |
             v                       v
    ┌─────────────────┐     ┌─────────────────┐
    │ Structured Match│     │ Semantic Match  │
    └────────┬────────┘     └────────┬────────┘
             |                       |
             +-----------+-----------+
                         |
                         v
                 ┌──────────────┐
                 │ AI Reasoning │
                 └──────┬───────┘
                        |
                        v
                 ┌──────────────┐
                 │ Final Match  │
                 └──────┬───────┘
                        |
                        v
                 ┌──────────────┐
                 │    Ranking   │
                 └──────┬───────┘
                        |
                        v
                 ┌──────────────┐
                 │ Explanation  │
                 └──────┬───────┘
                        |
                        v
                 Recruiter UI

---

# Advantages

The proposed AI architecture provides several advantages.

### Hybrid Intelligence

Combines deterministic application logic with semantic AI capabilities.

### Better Explainability

Matching results can be supported by explicit evidence.

### Reduced LLM Dependency

Not every operation requires an LLM call.

### Provider Flexibility

AI providers and models can be changed independently.

### Testability

AI components can be tested separately from traditional backend components.

### Scalability

Expensive AI operations can eventually be moved to background processing.

### Better Data Quality

Structured validation prevents arbitrary AI output from directly entering the system.

### Stronger Matching

Combining skill overlap, semantic similarity, and contextual reasoning provides richer signals than simple keyword matching.

---

# Limitations

The AI architecture also has limitations.

### Model Errors

LLMs and embedding models can produce incorrect or incomplete results.

### Hallucinations

AI-generated information may contain unsupported claims.

### Cost

External LLM and embedding APIs can introduce operational costs.

### Latency

AI processing may take longer than normal database operations.

### Model Dependency

Results can vary between models and model versions.

### Bias

Recruitment AI systems can reproduce or amplify biases present in data or models.

### Explainability Limitations

Even when an explanation is generated, it may not fully represent the internal reasoning of an AI model.

### Privacy

Resume and candidate information may contain sensitive personal data and must be handled appropriately.

These limitations must be considered during implementation and testing.

---

# Design Decision

Hirely will use a **modular hybrid AI architecture**.

The system will combine:

    Deterministic Rules
            +
       Embeddings
            +
           LLM
            +
       Structured Data
            |
            v
       Matching Engine
            |
            v
      Explainable Result

The LLM will not be treated as the application's source of truth.

Structured application data will remain authoritative for known facts.

Embeddings will provide semantic similarity.

LLMs will provide language understanding and contextual reasoning.

The matching engine will combine these signals into a structured result.

This design provides a balance between:

- Reliability
- Intelligence
- Explainability
- Flexibility
- Cost control
- Testability

---

# Mental Model

The simplest way to understand Hirely's AI architecture is:

    Database
        =
    What Hirely knows

    LLM
        =
    What Hirely can understand

    Embeddings
        =
    How Hirely represents meaning

    Matching Engine
        =
    How Hirely combines evidence

    Explanation
        =
    How Hirely communicates the result

Therefore:

    Structured Facts
          +
    Semantic Meaning
          +
    AI Reasoning
          |
          v
    Intelligent Recruitment

The goal is not to make the LLM responsible for the entire recruitment process.

The goal is to use each technology where it is strongest.

---

# Key Takeaways

- GenAI is the primary intelligence layer of Hirely.
- The AI system is designed as multiple specialized components rather than one large LLM call.
- Resume Analysis converts unstructured resumes into structured information.
- Job Analysis converts job descriptions into structured requirements.
- Candidate and job representations combine structured and semantic information.
- Embeddings provide semantic representations.
- Deterministic matching handles reliable structured requirements.
- Semantic matching handles meaning beyond exact keywords.
- LLM reasoning can provide contextual interpretation.
- The Matching Engine combines these signals.
- The Ranking Engine ranks candidates for specific jobs.
- The Explanation Engine produces evidence-grounded explanations.
- AI output must be validated before being trusted.
- The LLM should not be used for authentication, authorization, or other deterministic responsibilities.
- AI provider integrations should remain replaceable.
- Expensive AI processing can eventually move to background workers.
- Vector storage may be introduced when semantic retrieval requirements justify it.
- Security, privacy, cost, latency, and bias must be considered throughout the AI architecture.
- The overall design follows a hybrid approach: structured data + deterministic logic + embeddings + LLM reasoning.