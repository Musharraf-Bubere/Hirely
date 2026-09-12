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

## Candidate Ranking

### Purpose

Candidate matching determines how well an individual candidate matches a specific job.

However, recruiters usually need to evaluate multiple candidates for the same job. Hirely therefore requires a dedicated ranking component that can compare the match results of multiple candidates and arrange them from strongest to weakest match.

The ranking component does not recalculate the candidate-job match. It consumes the overall match scores produced by the Matching Engine.

---

### Ranking Flow

The candidate ranking workflow follows this sequence:

1. Evaluate candidate-job match
2. Generate MatchScoreResult
3. Collect multiple candidate match results
4. Convert results into ranking inputs
5. Sort candidates by overall match score
6. Assign rank positions
7. Return ranked candidate results

The conceptual flow is:

Candidate + Job  
↓  
Matching Engine  
↓  
MatchScoreResult  
↓  
Matching Service  
↓  
CandidateMatch  
↓  
Candidate Ranker  
↓  
RankedCandidate

---

### Ranking Input

The ranking process requires only the information necessary to compare candidates:

- Candidate ID
- Overall Match Score

The detailed matching evidence remains inside the MatchScoreResult produced by the Matching Engine.

This keeps the ranking component independent from the internal implementation of skill matching, semantic similarity, embeddings, and scoring.

---

### Ranking Output

Each ranked candidate contains:

- Rank
- Candidate ID
- Overall Match Score

For example:

| Rank | Candidate | Overall Match Score |
|------|-----------|--------------------:|
| 1 | Candidate B | 0.94 |
| 2 | Candidate D | 0.88 |
| 3 | Candidate A | 0.82 |
| 4 | Candidate C | 0.71 |

The ranking system orders candidates by descending overall match score.

---

### Separation of Responsibilities

Hirely separates matching and ranking into independent responsibilities.

**Matching**

Determines:

> How well does this candidate match this job?

The Matching Engine evaluates structured and semantic evidence and produces an overall match score.

**Ranking**

Determines:

> Among all candidates for this job, who matches best?

The Candidate Ranker orders existing match results without recalculating their scores.

**Matching Service**

Acts as the orchestration layer between matching and ranking components.

It converts MatchScoreResult objects into the smaller CandidateMatch representation required by the ranking component and coordinates the ranking workflow.

This separation prevents the Matching Engine and Candidate Ranker from becoming tightly coupled.

---

### Data Validation

Match scores are normalized to the range:

0.0 ≤ overall_score ≤ 1.0

Both MatchScoreResult and CandidateMatch validate this constraint.

Invalid values are rejected instead of silently corrected.

For example:

- 0.0 → valid
- 0.5 → valid
- 1.0 → valid
- -0.1 → invalid
- 1.1 → invalid

Failing validation early helps identify errors in upstream scoring logic rather than hiding them through automatic correction.

---

### Tie Handling

Multiple candidates may receive the same overall match score.

Hirely's initial ranking implementation preserves the original order of candidates when scores are equal.

For example:

Candidate A → 0.91  
Candidate B → 0.91  
Candidate C → 0.85

The result becomes:

| Rank | Candidate | Score |
|------|-----------|------:|
| 1 | Candidate A | 0.91 |
| 2 | Candidate B | 0.91 |
| 3 | Candidate C | 0.85 |

More advanced tie-breaking strategies may be introduced later using additional matching evidence such as required skill score.

---

### Architecture Decision

Hirely will implement Candidate Ranking as a deterministic component separate from the Matching Engine.

The architecture will follow:

Matching Engine
→ MatchScoreResult
→ Matching Service
→ CandidateMatch
→ Candidate Ranker
→ RankedCandidate

The Ranking component will not use an LLM because ranking existing numerical match results is a deterministic business operation.

This provides:

- Predictable behavior
- Fast execution
- Low computational cost
- Easy testing
- Clear separation of responsibilities
- Easier future optimization

---

### AI and Ranking Relationship

AI contributes to candidate evaluation through resume understanding, job understanding, semantic representations, embeddings, and other matching signals.

However, the final candidate ordering is performed deterministically using the resulting match scores.

Therefore:

**AI/GenAI → produces semantic evidence**

**Matching Engine → combines evidence**

**Ranking → orders candidates**

This architecture avoids using a single LLM call as the complete hiring decision mechanism.

---

### Limitations

The initial ranking implementation has several limitations:

- Ranking depends on the quality of the underlying match score.
- Equal scores currently use input order as the tie behavior.
- Ranking does not independently evaluate candidate qualifications.
- The current ranking model does not learn optimal ordering from historical hiring outcomes.
- Match-score weights are configurable but have not yet been scientifically learned or optimized.

These limitations can be addressed in future versions through evaluation datasets, recruiter feedback, additional ranking signals, and machine-learning-based ranking approaches.

---

### Decision for Hirely

Hirely will use a deterministic Candidate Ranker after the Matching Engine.

The system will first evaluate each candidate against the job using structured and semantic evidence. The resulting match scores will then be passed through the Matching Service and ordered by the Candidate Ranker.

The ranking system will remain independent from the underlying AI models so that the AI and ranking components can evolve independently.

---

### Mental Model

The complete candidate evaluation system can be remembered as:

**Matching = Evaluate**

**Scoring = Combine Evidence**

**Ranking = Order**

**Explanation = Communicate Why**

This separation forms the foundation for Hirely's recruiter-facing AI candidate discovery workflow.

---

### Key Takeaways

- Matching evaluates one candidate against one job.
- Ranking compares multiple candidates for the same job.
- Ranking uses the existing overall match score.
- Candidate identity must remain attached to the match result.
- Matching and ranking are separated into independent components.
- MatchingService provides orchestration between the components.
- Match scores are validated between 0.0 and 1.0.
- Ranking is deterministic and does not require an LLM.
- Equal scores preserve their original input order in the initial implementation.
- Future ranking improvements can introduce additional signals or learned ranking models.

# Match Explanation

## Purpose

The Match Explanation component converts the structured evidence produced by the matching system into a concise, human-readable explanation.

The purpose is not to make a new hiring decision.

The purpose is to communicate **why the matching system produced its result** using the evidence that has already been calculated.

The Match Explanation component therefore follows the core Hirely principle:

**Deterministic System → Calculates Evidence**

**LLM → Explains Evidence**

The explanation layer should not independently evaluate the entire resume or job description when the required matching evidence is already available.

---

## Why Hirely Needs Match Explanation

A numerical match score alone is difficult for recruiters to interpret.

For example:

Candidate A → 0.78

The score indicates the degree of compatibility calculated by Hirely, but it does not immediately communicate:

- Which required skills matched
- Which required skills are missing
- Which preferred skills matched
- Which preferred skills are missing
- How strong the semantic similarity signal was
- What the recruiter should understand from the result

A recruiter therefore needs supporting information alongside the score.

The Match Explanation component provides this supporting information in a human-readable form.

---

## Explanation Architecture

The implemented explanation workflow is:

    Matching Engine

            |

            v

    CompleteMatchResult

        +-----------+

        |           |

        v           v

      Score       Skills

        |           |

        +-----+-----+

              |

              v

    MatchExplanationInput

              |

              v

    ExplanationPromptBuilder

              |

              v

        GeminiService

              |

              v

       MatchExplanation

The Matching Engine calculates the matching evidence once.

The CompleteMatchResult keeps both the score information and skill-matching information together.

The explanation layer then consumes this existing evidence instead of recalculating it.

---

## Complete Match Result

The Matching Engine produces a `CompleteMatchResult`.

The result contains two major categories of information:

### Match Score

The score portion contains:

- Candidate ID
- Overall match score
- Required skill score
- Preferred skill score
- Semantic similarity

### Skill Evidence

The skill portion contains:

- Matched required skills
- Missing required skills
- Matched preferred skills
- Missing preferred skills

Conceptually:

    CompleteMatchResult

            |

            +-- MatchScoreResult

            |      +-- Candidate ID

            |      +-- Overall Score

            |      +-- Required Skill Score

            |      +-- Preferred Skill Score

            |      +-- Semantic Similarity

            |

            +-- SkillMatchResult

                   +-- Required Matched

                   +-- Required Missing

                   +-- Preferred Matched

                   +-- Preferred Missing

This provides the explanation system with a single structured source of matching evidence.

---

## Match Explanation Input

The explanation layer uses a dedicated `MatchExplanationInput`.

The input contains the evidence required to generate an explanation:

- Candidate ID
- Overall match score
- Required skill score
- Preferred skill score
- Semantic similarity
- Required matched skills
- Required missing skills
- Preferred matched skills
- Preferred missing skills

The explanation input intentionally does not contain the complete raw resume or complete job description.

This is an important architectural decision.

The explanation model does not need to independently rediscover the matching evidence because the Matching Engine has already calculated it.

---

## Why the LLM Does Not Receive the Entire Resume and Job Description

A possible design would be:

    Resume

       +

    Job Description

       |

       v

      LLM

       |

       v

    Match Explanation

Hirely does not use this as the primary explanation design.

Instead, Hirely uses:

    Matching Evidence

          |

          v

    Explanation LLM

          |

          v

    Human-readable Explanation

This provides stronger grounding.

The LLM is given the information that the deterministic matching system has already established.

This reduces unnecessary re-evaluation and lowers the risk that the explanation introduces unsupported claims.

---

## Evidence-Grounded Explanation

The explanation must be grounded in the actual matching evidence.

The LLM should use:

- Overall match score
- Required skill score
- Preferred skill score
- Semantic similarity
- Matched required skills
- Missing required skills
- Matched preferred skills
- Missing preferred skills

The explanation should not introduce unsupported candidate information.

For example, if the evidence says:

    Required matched:
    Python
    FastAPI

the explanation can state that Python and FastAPI are matched required skills.

It should not automatically claim:

    The candidate is an expert in Python.

A matched skill indicates that the skill is present in the matching evidence.

It does not automatically establish:

- Proficiency
- Expertise
- Depth of knowledge
- Years of experience

This distinction is important for preventing unsupported AI claims.

---

## Explanation Prompt Builder

Hirely uses a dedicated `ExplanationPromptBuilder`.

Its responsibility is to transform the structured matching evidence into a controlled prompt for the LLM.

The prompt provides:

- Matching evidence
- Grounding rules
- Explanation requirements
- Output expectations

The prompt explicitly instructs the model to use only the supplied evidence.

This keeps prompt construction separate from the Gemini provider implementation.

The architecture is therefore:

    MatchExplanationInput

            |

            v

    ExplanationPromptBuilder

            |

            v

          Prompt

            |

            v

       GeminiService

---

## Grounding Rules

The explanation system follows several grounding rules.

### Do Not Recalculate the Match Score

The LLM must not calculate or modify the overall match score.

The score is produced by the deterministic Matching Engine.

The explanation layer communicates that score.

### Use Only Provided Evidence

The model must use the evidence supplied in `MatchExplanationInput`.

It should not invent additional candidate or job information.

### Do Not Invent Skills

The model must not introduce skills that are not present in the supplied matching evidence.

### Do Not Invent Experience

The model must not invent:

- Years of experience
- Job responsibilities
- Achievements
- Qualifications
- Expertise
- Seniority

unless such information is explicitly supported by the supplied evidence.

### Matched Skills Do Not Establish Proficiency

A matched skill only indicates skill presence.

It does not prove that the candidate is:

- Expert
- Highly skilled
- Proficient
- Advanced

unless such information is explicitly supported.

### Missing Skills Must Remain Missing

If a required skill is missing from the matching evidence, the explanation should communicate that gap rather than attempting to justify or hide it.

### Unavailable Signals Are Not Zero

If a signal is unavailable, it must not automatically be interpreted as a score of zero.

For example:

    Preferred Skill Score = Unavailable

is different from:

    Preferred Skill Score = 0.0

The explanation should preserve this distinction.

### Do Not Make Hiring Decisions

The LLM should explain the match.

It should not independently decide:

- Hire
- Reject
- Interview
- Promote
- Disqualify

The recruiter remains responsible for the final recruitment decision.

---

## Structured Explanation Output

The LLM produces a structured `MatchExplanation`.

The output contains:

- Summary
- Strengths
- Gaps
- Evidence
- Caveats

Conceptually:

    MatchExplanation

        |

        +-- Summary

        +-- Strengths

        +-- Gaps

        +-- Evidence

        |     +-- Required Skill Score

        |     +-- Preferred Skill Score

        |     +-- Semantic Similarity

        |

        +-- Caveats

This output is validated using Pydantic before it is treated as a valid application result.

---

## Summary

The summary provides a concise explanation of the candidate-job match.

It should communicate the overall matching situation using the supplied evidence.

For example, it may describe:

- Strong required skill alignment
- Partial required skill alignment
- Strong semantic similarity
- Missing requirements

The summary should remain factual and concise.

---

## Strengths

Strengths should be derived from positive matching evidence.

Examples include:

- Matched required skills
- Matched preferred skills
- Strong semantic similarity

The system should not transform a matched skill into an unsupported claim about expertise.

---

## Gaps

Gaps should be derived from missing matching evidence.

Examples include:

- Missing required skills
- Missing preferred skills

Required skill gaps should remain clearly distinguishable from preferred skill gaps.

This distinction helps recruiters understand which gaps are more important according to the job requirements.

---

## Evidence

The explanation output includes the numerical evidence used by the matching system:

- Required skill score
- Preferred skill score
- Semantic similarity

These values should correspond to the values supplied to the explanation model.

The LLM is therefore not responsible for creating a new score.

The explanation preserves the evidence calculated by the Matching Engine.

---

## Caveats

The explanation may contain caveats that help prevent overinterpretation.

For example:

- Matched skills indicate skill presence only.
- Skill matching does not establish proficiency level.
- Missing required skills should be considered when reviewing the candidate.
- Semantic similarity is a matching signal rather than a hiring probability.

Caveats are especially useful because recruitment matching results should not be interpreted as absolute judgments about a candidate.

---

## Pydantic Validation

The Match Explanation output is validated through a Pydantic schema.

The flow is:

    Gemini

       |

       v

    Structured JSON

       |

       v

    MatchExplanation Schema

       |

       v

    Validation

       |

       +---- Invalid → Reject

       |

       v

    Valid MatchExplanation

This prevents arbitrary model output from being accepted as a valid structured explanation.

The explanation schema also validates numerical evidence ranges.

Scores must remain within:

    0.0 ≤ score ≤ 1.0

The summary must contain meaningful content.

---

## Separation of Responsibilities

Hirely separates matching, ranking, and explanation.

### Matching Engine

Determines:

> How well does this candidate match this job?

It calculates the matching evidence and produces `CompleteMatchResult`.

### Ranking Component

Determines:

> Among multiple candidates, who ranks higher?

It orders candidates using the existing match scores.

### Explanation Component

Determines:

> How should the matching result be communicated to the recruiter?

It converts existing structured evidence into a human-readable explanation.

### Gemini

Gemini is responsible for language generation and explanation.

It is not responsible for:

- Authentication
- Authorization
- Database integrity
- Final numerical scoring
- Candidate ranking
- Final hiring decisions

This separation keeps the architecture deterministic where possible and uses GenAI where it provides meaningful value.

---

## One Source of Matching Evidence

The implementation intentionally avoids calculating the same matching evidence multiple times.

The Matching Engine produces:

    CompleteMatchResult

            |

            +-- score

            +-- skills

Both components are then reused by downstream systems.

For example:

    CompleteMatchResult

        |

        +------> Ranking

        |

        +------> Explanation

This provides a single source of matching evidence.

It also prevents inconsistencies where one component could calculate a different skill result from another component.

---

## Explanation and Ranking Relationship

Ranking and explanation have different responsibilities.

The flow is:

    Candidate A

        |

        v

    Matching Engine

        |

        v

    CompleteMatchResult

        |

        +------> Ranking

        |

        +------> Explanation

The ranking system determines candidate ordering.

The explanation system communicates the reasoning behind the matching evidence.

Therefore:

**Matching = Evaluate**

**Scoring = Combine Evidence**

**Ranking = Order**

**Explanation = Communicate Why**

This separation allows the ranking system to remain deterministic while still providing recruiters with understandable results.

---

## Hallucination Control

The explanation architecture uses several mechanisms to reduce hallucination risk.

### Structured Input

The LLM receives structured matching evidence instead of relying on unrestricted interpretation.

### Grounded Prompt

The prompt explicitly restricts the model to the provided evidence.

### Structured Output

The model must return a defined explanation schema.

### Pydantic Validation

The generated output is validated before being accepted.

### Deterministic Evidence

Skills and numerical matching signals are calculated outside the LLM.

### Restricted Scope

The explanation model is asked to explain the match rather than independently evaluate the candidate.

These controls do not guarantee that an LLM will never make an incorrect statement, but they reduce the opportunity for unsupported reasoning.

---

## AI Provider Interaction

The Match Explanation component does not directly implement provider-specific API calls.

Instead, it uses the existing `GeminiService`.

The flow is:

    MatchExplanationService

            |

            v

    ExplanationPromptBuilder

            |

            v

        GeminiService

            |

            v

          Gemini

This keeps provider-specific communication isolated.

If the AI provider changes in the future, the explanation component should require minimal modification.

---

## Match Explanation Service

The `MatchExplanationService` acts as the service-level coordinator for explanation generation.

Its responsibilities are:

- Receive `MatchExplanationInput`
- Build the explanation prompt
- Call the Gemini service
- Request structured output
- Return a validated `MatchExplanation`

It does not calculate the match score.

It does not perform skill matching.

It does not rank candidates.

This keeps the service focused on explanation generation.

---

## End-to-End Match Explanation Flow

The complete implemented flow is:

    Candidate Data
          +
    Job Data
          |
          v
    Candidate / Job Representation
          |
          v
       Embeddings
          |
          v
    Matching Engine
          |
          v
    CompleteMatchResult
          |
          +------------------+
          |                  |
          v                  v
       Score              Skills
          |                  |
          +--------+---------+
                   |
                   v
       MatchExplanationInput
                   |
                   v
       ExplanationPromptBuilder
                   |
                   v
              GeminiService
                   |
                   v
                 Gemini
                   |
                   v
          Structured Response
                   |
                   v
          MatchExplanation
                   |
                   v
             Recruiter UI

This architecture ensures that the explanation is generated from the same evidence used by the matching system.

---

## Example

Suppose the matching engine produces:

    Required Skills:
    Python
    FastAPI
    SQL
    Docker

    Candidate Skills:
    Python
    FastAPI
    SQL
    AWS

The deterministic matching system produces:

    Required Skill Score:
    0.75

    Required Matched:
    Python
    FastAPI
    SQL

    Required Missing:
    Docker

Suppose the preferred skills are:

    AWS
    Kubernetes

The system produces:

    Preferred Skill Score:
    0.50

    Preferred Matched:
    AWS

    Preferred Missing:
    Kubernetes

The explanation model receives this evidence.

It can generate an explanation such as:

    Summary:
    Strong alignment with the required skills, with Docker
    remaining as a required gap.

    Strengths:
    Python, FastAPI, and SQL match the required skills.
    AWS matches a preferred skill.

    Gaps:
    Docker is missing from the required skills.
    Kubernetes is missing from the preferred skills.

The important point is that the LLM did not discover these facts independently.

The deterministic matching system supplied the evidence.

The LLM communicated that evidence in natural language.

---

## Architecture Decision

Hirely will use an **evidence-grounded Match Explanation architecture**.

The architecture will follow:

    Matching Engine

          ↓

    CompleteMatchResult

          ↓

    MatchExplanationInput

          ↓

    ExplanationPromptBuilder

          ↓

    GeminiService

          ↓

    Structured MatchExplanation

The LLM will not be treated as the source of truth for matching evidence.

The Matching Engine remains responsible for calculating structured matching signals.

The Explanation Component remains responsible for communicating those signals.

This provides:

- Better explainability
- Reduced hallucination risk
- Clear separation of responsibilities
- Reusable matching evidence
- Structured AI output
- Easier testing
- Provider flexibility
- Better control over AI behavior

---

## Advantages

### Evidence Grounding

The explanation is based on structured matching evidence rather than unrestricted LLM evaluation.

### Reduced Duplication

Matching evidence is calculated once and reused by ranking and explanation.

### Better Explainability

Recruiters can understand the strengths and gaps behind a match score.

### Deterministic Matching

The LLM does not control the underlying numerical matching calculation.

### Structured Output

The explanation has a predictable schema.

### Validation

Pydantic validates the generated explanation.

### Provider Flexibility

The explanation service communicates through the existing AI service abstraction.

### Testability

Prompt construction, schema validation, service behavior, and real Gemini integration can be tested independently.

### Clear Responsibility Boundaries

Matching, ranking, and explanation remain separate components.

---

## Limitations

### LLM Output Can Still Be Incorrect

Grounding reduces hallucination risk but does not guarantee perfect language generation.

### Explanation Quality Depends on Matching Evidence

If the underlying matching signals are incomplete or incorrect, the explanation may also be incomplete.

### Semantic Similarity Is Not a Qualification Probability

A high semantic similarity score does not mean that the candidate has a corresponding probability of being qualified or hired.

### Skill Presence Does Not Establish Proficiency

A matched skill should not automatically be interpreted as expertise or years of experience.

### Model Variability

Different models or model versions may produce different wording while using the same evidence.

### External API Dependency

Gemini-based explanations depend on external model availability, latency, and cost.

### Recruitment Bias

AI-generated explanations may still reflect limitations or biases of the underlying model.

### Human Oversight

The explanation should support recruiter decision-making rather than replace human judgment.

---

## Testing Strategy

The Match Explanation implementation is tested at multiple levels.

### Schema Tests

Verify that:

- Valid explanation input is accepted.
- Invalid scores are rejected.
- Unavailable preferred scores are supported.
- Valid explanations are accepted.
- Empty summaries are rejected.

### Prompt Tests

Verify that:

- Matching evidence is included.
- Unavailable values are represented correctly.
- Empty skill lists are handled.
- Grounding rules are included.
- Unsupported proficiency claims are prohibited.

### Service Tests

Verify that:

- The service builds the prompt.
- Gemini is called with the expected structured schema.
- A valid `MatchExplanation` is returned.

### Integration Test

The real integration test verifies the complete flow:

    MatchingEngine

          ↓

    CompleteMatchResult

          ↓

    MatchExplanationInput

          ↓

    ExplanationPromptBuilder

          ↓

    GeminiService

          ↓

    Real Gemini Model

          ↓

    MatchExplanation

The integration test also verifies that the numerical evidence in the generated explanation corresponds to the deterministic matching result.

---

## Mental Model

The simplest way to understand Match Explanation is:

    Matching Engine

        =

    What the system calculated

        +

    Explanation Layer

        =

    How the system communicates it

The complete Hirely AI matching mental model is:

    Database

        =

    What Hirely knows

    Embeddings

        =

    How Hirely represents meaning

    Matching Engine

        =

    How Hirely combines evidence

    Ranking

        =

    How Hirely orders candidates

    Explanation

        =

    How Hirely communicates why

    Gemini

        =

    Natural-language explanation

The LLM is therefore one component of the system, not the entire recruitment decision engine.

---

## Key Takeaways

- Match Explanation converts structured matching evidence into human-readable language.
- The Matching Engine remains responsible for calculating matching evidence.
- `CompleteMatchResult` contains both score information and skill evidence.
- The explanation layer consumes `CompleteMatchResult` rather than recalculating matching evidence.
- `MatchExplanationInput` provides a controlled input boundary for the LLM.
- `ExplanationPromptBuilder` converts structured evidence into a grounded prompt.
- Gemini is used for language generation and explanation.
- The LLM must not recalculate or modify the match score.
- The LLM must not invent skills, experience, qualifications, achievements, or expertise.
- Matched skill presence does not automatically establish proficiency or years of experience.
- Missing required skills should be clearly communicated.
- Unavailable signals must not be treated as zero.
- The explanation output is structured using `MatchExplanation`.
- Pydantic validates the generated explanation.
- Ranking and explanation are separate responsibilities.
- Matching evidence is calculated once and reused by downstream components.
- The architecture reduces unnecessary duplicate computation.
- Evidence-grounded prompting reduces hallucination risk.
- The explanation supports recruiter understanding but does not make the final hiring decision.
- The overall architecture follows the principle:

**Deterministic System → Calculates Evidence**

**LLM → Explains Evidence**

# Recruiter Candidate Matching API

## Purpose

The Recruiter Candidate Matching API exposes Hirely's candidate-job matching and ranking system to recruiters through a FastAPI endpoint.

The endpoint allows an authenticated recruiter to request a ranked list of eligible candidates for one of their active jobs.

The implemented endpoint is:

    POST /jobs/{job_id}/candidates/match

The API acts as the integration boundary between the traditional recruitment backend and Hirely's AI matching system.

---

## API Responsibilities

The recruiter matching endpoint is responsible for:

- Authenticating the requester
- Verifying recruiter authorization
- Retrieving the requested job
- Verifying that the job is active
- Verifying recruiter ownership of the job
- Retrieving candidates
- Filtering candidates based on resume eligibility
- Preparing candidate representations
- Preparing the job representation
- Generating candidate and job embeddings
- Assembling matching inputs
- Executing the Matching Engine
- Ranking candidates
- Returning structured ranked results

The API should coordinate these operations rather than implement the underlying AI algorithms itself.

---

## Endpoint Contract

### Endpoint

    POST /jobs/{job_id}/candidates/match

### Path Parameter

    job_id

The `job_id` identifies the job for which candidates should be matched.

### Request Body

No request body is required.

The authenticated recruiter is determined from the JWT token.

The backend retrieves the job and candidate information from trusted application data.

The frontend must not provide:

- Candidate embeddings
- Job embeddings
- Match scores
- Candidate ranking
- Recruiter ownership information

These values are generated and validated by the backend.

---

## Authentication Flow

The endpoint requires a valid JWT token.

The authentication flow is:

    HTTP Request
        |
        v
    JWT Token
        |
        v
    Authentication
        |
        +---- Invalid → 401 Unauthorized
        |
        v
    Current User
        |
        v
    Recruiter Authorization
        |
        +---- Not Recruiter → 403 Forbidden
        |
        v
    Recruiter Matching

Authentication and authorization remain deterministic backend responsibilities.

The AI layer is never responsible for deciding whether the requester is allowed to access the endpoint.

---

## Job Validation

After authentication, the API retrieves the requested job.

The job must satisfy two conditions:

    Job exists
        +
    Job is active

If the job does not exist or is inactive, the endpoint returns:

    404 Not Found

The API does not expose inactive jobs through the recruiter matching workflow.

---

## Recruiter Ownership Validation

A recruiter must only be able to match candidates for their own jobs.

The ownership rule is:

    job.recruiter_id
            ==
    authenticated_recruiter.id

If the job belongs to another recruiter, the endpoint returns:

    403 Forbidden

This creates an explicit authorization boundary around recruiter data.

The flow is:

    Authenticated Recruiter
            |
            v
        Requested Job
            |
            v
      Ownership Check
            |
      +-----+-----+
      |           |
      v           v
    Owner      Not Owner
      |           |
      v           v
 Continue       403

---

## Candidate Eligibility

Not every candidate should enter the AI matching pipeline.

Hirely first checks whether the candidate has an eligible resume.

A candidate is eligible when:

- An active resume exists
- The active resume has completed parsing
- Parsed resume data is available and valid

Candidates without an eligible resume are skipped.

The flow is:

    Candidate
        |
        v
    Active Resume?
        |
        +---- No → Skip
        |
        v
    Parsing Status = COMPLETED?
        |
        +---- No → Skip
        |
        v
    Valid Parsed Data?
        |
        +---- No → Skip
        |
        v
    Eligible Candidate

Skipping ineligible candidates allows one incomplete candidate record to exist without causing the entire recruiter matching request to fail.

---

## Empty Eligible Candidate Pool

If no candidates satisfy the eligibility requirements, the API returns:

    200 OK

with:

    []

This represents a valid matching request where no candidates are currently eligible.

It is different from an API or authentication failure.

The distinction is:

    Invalid Request / Unauthorized
            ↓
          Error

    Valid Job + No Eligible Candidates
            ↓
          []

---

## Recruiter Matching Architecture

The implemented recruiter matching flow is:

    POST /jobs/{job_id}/candidates/match
                |
                v
        Authentication
                |
                v
        Recruiter Authorization
                |
                v
          Retrieve Job
                |
                v
          Active Job Check
                |
                v
        Ownership Validation
                |
                v
        Retrieve Job Skills
                |
                v
        Prepare Job Once
                |
                v
        Retrieve Candidates
                |
                v
       Resume Eligibility
                |
                v
    Prepare Eligible Candidates
                |
                v
      MatchingInputAssembler
                |
                v
       Matching Orchestrator
                |
                v
         Matching Engine
                |
                v
          Match Results
                |
                v
             Ranking
                |
                v
       RankedMatchResult[]
                |
                v
           FastAPI Response

---

## Job Preparation

The job is prepared once for the entire recruiter matching request.

This is an important optimization.

If a recruiter has 100 eligible candidates, the system should not generate the same job embedding 100 separate times.

The flow is:

    Job
      |
      v
    Job Skills
      |
      v
    JobPreparationService
      |
      +---- Job Representation
      |
      +---- Job Embedding
      |
      v
    JobPreparationResult

The resulting job preparation data is reused for candidate matching.

---

## Candidate Preparation

Each eligible candidate is prepared individually.

The candidate preparation process is:

    Candidate
        |
        v
    Active Resume
        |
        v
    Parsed ResumeData
        |
        v
    CandidateRepresentationBuilder
        |
        +---- Candidate Representation
        |
        v
    EmbeddingService
        |
        v
    Candidate Embedding
        |
        v
    CandidatePreparationResult

The candidate representation provides the semantic text used to generate the candidate embedding.

---

## Matching Input Assembly

The candidate and job preparation results are converted into a common matching input.

The `MatchingInputAssembler` combines:

- Candidate ID
- Candidate skills
- Required job skills
- Preferred job skills
- Candidate embedding
- Job embedding

The flow is:

    CandidatePreparationResult
                +
          Candidate Skills
                +
      JobPreparationResult
                +
        Required Skills
                +
        Preferred Skills
                |
                v
      MatchingInputAssembler
                |
                v
          MatchingInput

This creates a clean boundary between preparation and matching.

---

## Matching Orchestrator

The `MatchingOrchestrator` coordinates execution of the matching workflow.

For each candidate:

    MatchingInput
          |
          v
    MatchingOrchestrator
          |
          v
      MatchingEngine
          |
          v
    CompleteMatchResult

The orchestrator does not implement the underlying similarity or scoring mathematics.

Instead, it coordinates the specialized matching components.

---

## Multiple Candidate Matching

For recruiter matching, multiple candidates must be evaluated against the same job.

The conceptual flow is:

    Candidate A + Job
            |
            v
      CompleteMatchResult A

    Candidate B + Job
            |
            v
      CompleteMatchResult B

    Candidate C + Job
            |
            v
      CompleteMatchResult C

            |

            v

    CompleteMatchResult[]

The results can then be passed to the ranking system.

---

## Ranking Integration

Once all eligible candidates have been matched, Hirely ranks the candidates using the existing deterministic ranking system.

The flow is:

    CompleteMatchResult[]
            |
            v
    MatchingService
            |
            v
      Candidate Ranker
            |
            v
    RankedMatchResult[]

The ranking system orders candidates using their calculated overall match scores.

The ranking component does not ask an LLM to decide the ordering.

This follows the established Hirely architecture:

    AI/GenAI
        ↓
    Semantic Evidence

    Matching Engine
        ↓
    Combined Match Score

    Ranking
        ↓
    Candidate Ordering

This preserves deterministic ranking behavior.

---

## Ranked Match Result

The recruiter API returns a structured `RankedMatchResult`.

Each result contains:

- Rank
- Candidate ID
- Overall score
- Required skill score
- Preferred skill score
- Semantic similarity
- Required matched skills
- Required missing skills
- Preferred matched skills
- Preferred missing skills

Conceptually:

    RankedMatchResult
        |
        +-- Rank
        +-- Candidate ID
        +-- Overall Score
        +-- Required Skill Score
        +-- Preferred Skill Score
        +-- Semantic Similarity
        +-- Required Matched
        +-- Required Missing
        +-- Preferred Matched
        +-- Preferred Missing

This allows the recruiter interface to display both the ranking and the evidence behind the ranking.

---

## Example API Response

A successful response may look conceptually like:

    [
        {
            "rank": 1,
            "candidate_id": "...",
            "overall_score": 0.975,
            "required_skill_score": 1.0,
            "preferred_skill_score": 1.0,
            "semantic_similarity": 0.918,
            "required_matched": [],
            "required_missing": [],
            "preferred_matched": [],
            "preferred_missing": []
        },
        {
            "rank": 2,
            "candidate_id": "...",
            "overall_score": 0.969,
            "required_skill_score": 1.0,
            "preferred_skill_score": 1.0,
            "semantic_similarity": 0.898,
            "required_matched": [],
            "required_missing": [],
            "preferred_matched": [],
            "preferred_missing": []
        }
    ]

The exact values depend on the candidate data, job requirements, skill information, and embedding model output.

---

## Security Boundaries

The recruiter matching endpoint was designed with explicit security boundaries.

### Unauthenticated User

Request without a valid authentication token:

    401 Unauthorized

### Candidate User

Candidate attempting to access recruiter matching:

    403 Forbidden

### Recruiter Accessing Another Recruiter's Job

Recruiter attempting to match candidates for a job they do not own:

    403 Forbidden

### Inactive Job

Matching request for an inactive job:

    404 Not Found

### Nonexistent Job

Matching request for a nonexistent job:

    404 Not Found

These checks occur before the AI matching workflow.

This prevents unauthorized requests from unnecessarily triggering AI processing.

---

## Why Security Happens Before AI Processing

AI operations can involve external model APIs, latency, and cost.

Therefore the system should validate:

    Authentication
        ↓
    Authorization
        ↓
    Ownership
        ↓
    Job Eligibility
        ↓
    Candidate Eligibility
        ↓
    AI Processing

rather than:

    AI Processing
        ↓
    Security Check

The first design is safer and avoids unnecessary model usage.

---

## AI Provider Boundary

The recruiter API does not directly implement Gemini API calls.

Instead, it uses the existing AI services:

    Recruiter Matching API
            |
            v
    CandidatePreparationService
            |
            v
      EmbeddingService
            |
            v
           Gemini

and:

    Recruiter Matching API
            |
            v
      JobPreparationService
            |
            v
      EmbeddingService
            |
            v
           Gemini

This keeps provider-specific implementation isolated from the API layer.

---

## Client Trust Boundary

The frontend is considered an untrusted client.

The frontend can request:

    Match candidates for job X

but it cannot decide:

    Candidate embedding
    Job embedding
    Match score
    Candidate rank
    Recruiter ownership
    Candidate eligibility

The backend generates and validates these values.

This prevents manipulation of the matching system from the client side.

---

## Performance Considerations

The current implementation generates embeddings during the matching request.

For a small candidate pool, this provides a straightforward synchronous architecture.

However, at larger scale, repeatedly generating embeddings can become expensive.

For example:

    1 Job
      +
    500 Candidates

could require many embedding operations.

A future production implementation can introduce:

- Cached candidate embeddings
- Cached job embeddings
- Embedding persistence
- Batch embedding generation
- Background processing
- Vector retrieval
- Candidate pre-filtering

The current implementation intentionally keeps the architecture simple until scale requires additional infrastructure.

---

## Current Embedding Strategy

Hirely currently uses Gemini embeddings for semantic representation.

Candidate information is converted into a candidate embedding.

Job information is converted into a job embedding.

The matching engine then calculates semantic similarity between these vectors.

Conceptually:

    Candidate Representation
            |
            v
    Gemini Embedding Model
            |
            v
    Candidate Vector


    Job Representation
            |
            v
    Gemini Embedding Model
            |
            v
    Job Vector


    Candidate Vector
            +
        Job Vector
            |
            v
    Semantic Similarity

Semantic similarity is only one component of the final matching score.

---

## Deterministic and Semantic Signals

The recruiter matching workflow combines two important categories of evidence.

### Deterministic Evidence

Examples include:

- Required skill matches
- Required skill gaps
- Preferred skill matches
- Preferred skill gaps

These signals come from structured application data.

### Semantic Evidence

Semantic similarity is calculated using embeddings.

This allows Hirely to capture relationships that may not be represented by exact keyword overlap.

The final score combines these signals according to the matching configuration.

---

## Why Ranking Is Not Performed by the LLM

An LLM could theoretically be asked:

    "Rank these candidates from best to worst."

However, Hirely does not use this as the primary ranking mechanism.

The ranking system instead uses:

    Candidate Match Scores
            |
            v
    Deterministic Candidate Ranker
            |
            v
    Ranked Candidates

This provides:

- Predictable ordering
- Reproducibility
- Lower cost
- Lower latency
- Easier testing
- Easier debugging
- Clearer explanation of ranking behavior

The LLM can still be used for explanation after ranking.

---

## Match Explanation Integration

The recruiter matching endpoint currently returns deterministic matching and ranking evidence.

The existing Match Explanation component can consume the resulting ranked match data later.

The eventual flow is:

    RankedMatchResult
            |
            v
    MatchExplanationInput
            |
            v
    ExplanationPromptBuilder
            |
            v
       GeminiService
            |
            v
     MatchExplanation

This preserves the established Hirely principle:

    Deterministic System → Calculates Evidence

    LLM → Explains Evidence

The explanation should not override the numerical score or candidate ranking.

---

## Testing Strategy

The recruiter matching API is tested at multiple levels.

### Authentication Test

Verify that unauthenticated requests return:

    401

### Role Authorization Test

Verify that candidates cannot access the recruiter endpoint.

Expected result:

    403

### Job Existence Test

Verify that a nonexistent job returns:

    404

### Active Job Test

Verify that an inactive job cannot be matched.

Expected result:

    404

### Ownership Test

Verify that recruiter A cannot match candidates for recruiter B's job.

Expected result:

    403

### Resume Eligibility Tests

Verify that candidates without an active resume are skipped.

Verify that candidates with pending resumes are skipped.

### Ranking Test

Use deterministic mocked embeddings to verify that:

    Strong Candidate
          >
    Weak Candidate

and therefore:

    Strong Candidate → Rank 1
    Weak Candidate   → Rank 2

This keeps the ranking test deterministic and avoids unnecessary external API calls.

### Real Gemini Integration Test

A separate integration test uses the real Gemini embedding service.

The test verifies:

    Candidate Resume
          |
          v
    Candidate Representation
          |
          v
    Real Gemini Embedding

    Job
          |
          v
    Job Representation
          |
          v
    Real Gemini Embedding

          |
          v
    Matching Engine
          |
          v
    Ranking
          |
          v
    API Response

This validates the real AI integration while keeping the deterministic tests independent from external model availability.

---

## Test Results

The recruiter matching API test suite passed:

    8 passed

The deterministic ranking correctness test passed:

    1 passed

The real Gemini recruiter matching integration test passed:

    1 passed

The complete non-integration regression suite passed:

    151 passed
    8 deselected

The deselected tests are integration tests excluded during the normal regression run.

The normal regression command is:

    pytest tests -m "not integration" -q -v -s

The complete test command remains:

    pytest tests -q -v -s

---

## Regression and Compatibility

During implementation, the existing `MatchingOrchestrator` test suite exposed an interface compatibility issue.

The recruiter workflow needed to rank already-computed `CompleteMatchResult` objects, while the existing orchestrator workflow expected `MultiCandidateMatchingInput`.

The orchestrator was therefore designed to support both workflows.

Conceptually:

    MultiCandidateMatchingInput
            |
            v
      match_candidates()
            |
            v
    CompleteMatchResult[]
            |
            v
          Ranking


    CompleteMatchResult[]
            |
            v
          Ranking

This preserves the existing behavior while allowing the recruiter endpoint to avoid unnecessary recomputation.

The full regression suite confirmed that the compatibility change did not introduce additional failures.

---

## Architectural Decision

Hirely will expose recruiter candidate matching through:

    POST /jobs/{job_id}/candidates/match

The endpoint will:

- Require authentication
- Require recruiter role
- Require an active job
- Require recruiter ownership
- Filter candidates by resume eligibility
- Generate AI representations server-side
- Generate embeddings server-side
- Use the existing Matching Engine
- Use deterministic candidate ranking
- Return structured ranked results
- Keep AI explanation as a separate layer

The API will not accept client-generated embeddings or match scores.

---

## Advantages

### Secure

Authentication, authorization, and ownership are enforced before AI processing.

### Explainable

The API returns structured matching evidence rather than only a ranking number.

### Deterministic Ranking

Candidate ordering is controlled by the deterministic ranking component.

### AI-Powered

Semantic embeddings allow Hirely to identify meaningful relationships between candidate and job information.

### Modular

Candidate preparation, job preparation, matching, ranking, and explanation remain separate components.

### Testable

Security, eligibility, ranking, and AI integration can be tested independently.

### Provider-Aware

The API communicates through AI services rather than embedding Gemini-specific implementation throughout the route.

---

## Limitations

### Synchronous AI Processing

Embedding generation currently occurs during the API request.

### Embedding Cost

A large number of eligible candidates can result in many embedding requests.

### No Persistent Embedding Cache

Candidate and job embeddings are not yet persisted as a dedicated optimization layer.

### Limited Candidate Retrieval

The current workflow does not yet use vector retrieval to reduce the candidate search space.

### Skill Normalization

Deterministic skill matching currently depends on normalized skill names rather than a complete semantic skill ontology.

### Explanation Not Yet Attached

The recruiter ranking endpoint currently returns matching evidence without generating an explanation for every candidate.

This is intentional so that ranking remains independent from LLM generation.

---

## Future Improvements

The recruiter matching system can later evolve toward:

    Recruiter Request
          |
          v
    Authorization
          |
          v
    Candidate Pre-filtering
          |
          v
    Vector Retrieval
          |
          v
    Top Candidate Pool
          |
          v
    Deterministic Matching
          |
          v
    Candidate Ranking
          |
          v
    Top Ranked Candidates
          |
          v
    Evidence-Grounded Explanation
          |
          v
    Recruiter UI

Potential future optimizations include:

- Persistent embeddings
- Embedding caching
- Vector search
- Candidate pre-filtering
- Batch processing
- Background workers
- Ranking evaluation datasets
- Learned ranking models
- Recruiter feedback signals
- Semantic skill normalization
- Match explanation caching

These improvements should be introduced when actual performance, scale, or product requirements justify them.

---

## Mental Model

The recruiter matching workflow can be remembered as:

    Authenticate
        ↓
    Authorize
        ↓
    Validate Job
        ↓
    Filter Candidates
        ↓
    Prepare
        ↓
    Embed
        ↓
    Match
        ↓
    Score
        ↓
    Rank
        ↓
    Explain

The most important architectural principle remains:

    Backend
        =
    Security + Source of Truth

    Embeddings
        =
    Semantic Representation

    Matching Engine
        =
    Evidence Combination

    Ranking
        =
    Candidate Ordering

    LLM
        =
    Natural-Language Understanding / Explanation

---

## Key Takeaways

- Hirely now exposes candidate-job matching through a recruiter-facing FastAPI endpoint.
- The endpoint is protected by authentication and recruiter role authorization.
- Recruiters can only match candidates for their own jobs.
- Inactive and nonexistent jobs are rejected.
- Candidates without eligible resumes are skipped.
- Candidate and job embeddings are generated server-side.
- The frontend cannot manipulate embeddings, scores, or rankings.
- The job embedding is prepared once and reused across candidate matching.
- Candidate preparation is performed for each eligible candidate.
- MatchingInputAssembler provides a clean boundary between preparation and matching.
- MatchingOrchestrator coordinates the matching workflow.
- MatchingEngine calculates the actual matching evidence.
- MatchingService and CandidateRanker perform deterministic ranking.
- The recruiter endpoint returns structured RankedMatchResult objects.
- Ranking does not depend on an LLM.
- Match Explanation remains a separate evidence-grounded AI layer.
- The real Gemini embedding integration has been verified.
- The ranking correctness test has been verified independently using mocked embeddings.
- Authentication, authorization, ownership, job status, and resume eligibility have been tested.
- The full non-integration regression suite remains green.
- The current implementation is suitable as an MVP foundation and can later evolve toward cached embeddings, vector retrieval, asynchronous processing, and learned ranking.

---

## Recruiter Matching Service

### Purpose

Hirely's recruiter-facing candidate matching workflow requires evaluating multiple candidates against the same job.

Initially, this workflow was implemented directly inside the FastAPI job routes. This resulted in duplicated workflow logic between:

- Recruiter candidate ranking
- Recruiter candidate ranking with AI explanations

To improve separation of concerns and maintainability, the recruiter matching workflow was moved into a dedicated service:

`RecruiterMatchingService`

The API layer is now responsible for:

- Authentication
- Recruiter authorization
- Job lookup
- Job ownership verification
- Calling the appropriate service method
- Returning the result

The matching workflow itself is handled by the service layer.

---

### Architecture

The recruiter matching architecture follows:

    React
       |
       | HTTP/JSON
       v
    FastAPI
       |
       v
    Jobs API
       |
       | authorization + job ownership
       v
    RecruiterMatchingService
       |
       +-----------------------------+
       |                             |
       v                             v
    Job Preparation          Candidate Preparation
       |                             |
       |                             |
       +-------------+---------------+
                     |
                     v
              Matching Input
                     |
                     v
              Matching Engine
                     |
                     v
             MatchScoreResult
                     |
                     v
              Matching Service
                     |
                     v
              Candidate Ranker
                     |
                     v
             RankedMatchResult
                     |
                     v
              Top-N Selection
                     |
                     v
             Match Explanation
                     |
                     v
                  Gemini
                     |
                     v
             FinalMatchResult

This architecture keeps HTTP-specific concerns separate from the candidate matching workflow.

---

### Recruiter Matching Workflow

The recruiter matching workflow is implemented as a multi-stage process.

#### Job Preparation

The job is prepared only once for a recruiter matching request.

The service retrieves:

- Job title
- Job description
- Location
- Employment type
- Experience level
- Required skills
- Preferred skills

The information is converted into a `JobRepresentation` and an embedding is generated.

The prepared job is then reused for every eligible candidate.

This avoids unnecessarily generating the same job embedding repeatedly.

---

### Candidate Eligibility

The service retrieves candidates and evaluates whether each candidate can participate in matching.

A candidate is currently considered eligible when:

- An active resume exists.
- The resume has completed parsing.
- Parsed resume data exists.
- Parsed resume data passes `ResumeData` validation.

Candidates that do not satisfy these conditions are skipped.

This allows the matching system to continue processing valid candidates without failing the entire ranking operation because of one incomplete candidate record.

---

### Candidate Preparation

For each eligible candidate, Hirely retrieves:

- Candidate skills
- Active parsed resume data

The resume data is converted into a `CandidateRepresentation`.

The candidate representation contains relevant information such as:

- Profile information
- Location
- Headline
- Summary
- Skills
- Professional experience
- Projects
- Education
- Certifications

The candidate representation is then converted into an embedding.

The candidate embedding is used together with the prepared job embedding for semantic similarity.

---

### Matching Input Assembly

The prepared candidate and prepared job are combined with structured skill information.

The resulting `MatchingInput` contains:

- Candidate ID
- Candidate skills
- Required job skills
- Preferred job skills
- Candidate embedding
- Job embedding

`MatchingInputAssembler` is responsible for constructing this input.

This keeps the recruiter workflow independent from the internal structure of the preparation services.

---

### Candidate Matching

Each eligible candidate is evaluated by the existing `MatchingEngine`.

The Matching Engine combines:

- Required skill matching
- Preferred skill matching
- Semantic similarity

The result is represented as a `CompleteMatchResult`.

The underlying scoring system remains deterministic.

The LLM is not responsible for calculating the final match score.

---

### Candidate Ranking

After all eligible candidates have been matched, their results are passed to the existing ranking workflow.

The process is:

    CompleteMatchResult
            |
            v
    MatchScoreResult
            |
            v
    MatchingService
            |
            v
    CandidateMatch
            |
            v
    CandidateRanker
            |
            v
    RankedCandidate
            |
            v
    RankedMatchResult

The ranking component orders candidates by their overall match score.

Ranking remains deterministic and does not require an LLM.

This preserves the separation already established between:

**Matching = Evaluate**

**Scoring = Combine Evidence**

**Ranking = Order**

---

### Recruiter Matching API

Hirely exposes a recruiter-facing endpoint for candidate ranking:

    POST /jobs/{job_id}/candidates/match

The endpoint requires recruiter authentication.

The recruiter must also own the requested job.

The API route performs:

1. Authentication
2. Recruiter profile lookup
3. Active job lookup
4. Job ownership verification
5. Delegation to `RecruiterMatchingService`
6. Returning ranked results

The route does not perform candidate preparation, embedding generation, matching, or ranking itself.

This keeps the API layer thin.

---

### AI Match Explanation

Recruiters may also request explanations for ranked candidates.

The explanation endpoint is:

    POST /jobs/{job_id}/candidates/match/explain

The endpoint accepts:

    explanation_limit

The default explanation limit is:

    5

The explanation workflow first performs candidate matching and ranking.

Only the top N ranked candidates are then sent to the explanation workflow.

For example:

    100 candidates
          |
          v
    Match 100 candidates
          |
          v
    Rank 100 candidates
          |
          v
    Select top 5
          |
          v
    Generate 5 explanations

This avoids generating an expensive LLM explanation for every candidate.

---

### Evidence-Grounded Explanation

The explanation system does not send the complete resume and job description to the LLM for every explanation.

Instead, the explanation workflow uses structured matching evidence such as:

- Overall match score
- Required skill score
- Preferred skill score
- Semantic similarity
- Required matched skills
- Required missing skills
- Preferred matched skills
- Preferred missing skills

The LLM receives this structured evidence and generates a human-readable explanation.

The resulting output is validated using the defined Pydantic explanation schema.

This reduces the risk of unsupported claims and keeps the explanation grounded in the actual matching result.

---

### Explanation Output

The explanation endpoint returns `FinalMatchResult` objects.

Each result contains:

- Ranked match information
- Optional AI explanation

For candidates outside the explanation limit:

    explanation = None

For candidates within the explanation limit:

    explanation = MatchExplanation

Therefore, the API can return the complete ranked candidate list while limiting expensive AI explanation generation to the most relevant candidates.

---

### Separation of Responsibilities

The final recruiter matching architecture separates responsibilities across several components.

**Jobs API**

Responsible for:

- HTTP requests
- Authentication
- Authorization
- Job ownership
- HTTP responses

**RecruiterMatchingService**

Responsible for:

- Coordinating recruiter candidate matching
- Preparing the job
- Preparing eligible candidates
- Assembling matching inputs
- Executing candidate matching
- Ranking candidates
- Coordinating optional explanations

**CandidatePreparationService**

Responsible for:

- Building candidate representations
- Generating candidate embeddings

**JobPreparationService**

Responsible for:

- Building job representations
- Generating job embeddings

**MatchingInputAssembler**

Responsible for:

- Combining prepared candidate and job information into `MatchingInput`

**MatchingEngine**

Responsible for:

- Structured skill matching
- Semantic similarity
- Match score calculation

**MatchingService**

Responsible for:

- Converting match results into ranking inputs
- Coordinating ranking

**CandidateRanker**

Responsible for:

- Deterministically ordering candidates

**MatchExplanationService**

Responsible for:

- Building explanation prompts
- Calling Gemini
- Validating structured explanation output

This separation allows each component to be tested and changed independently.

---

### Why a Dedicated Recruiter Matching Service?

The dedicated service provides several engineering benefits.

#### Reduced Duplication

The recruiter ranking endpoint and recruiter explanation endpoint previously contained the same candidate preparation and ranking workflow.

The shared workflow now exists in one service.

#### Thin API Layer

The API route focuses on HTTP and authorization concerns rather than implementing the entire matching pipeline.

#### Reusability

The same recruiter matching workflow can later be used by:

- Recruiter dashboards
- Background jobs
- Batch matching
- Scheduled candidate recommendations
- Administrative tools

without duplicating the workflow.

#### Testability

The workflow can be tested independently from FastAPI routes.

Individual AI and matching components can also continue to be tested separately.

#### Maintainability

Changes to candidate eligibility, preparation, matching, or ranking can be implemented in the service without modifying multiple API endpoints.

---

### Performance Considerations

The service currently performs synchronous candidate preparation and embedding generation.

For a small candidate pool, this is acceptable for the initial implementation.

However, as the number of candidates grows, the workflow may become expensive because candidate embeddings are generated during the request.

Potential future improvements include:

- Persisting candidate embeddings
- Persisting job embeddings
- Caching embeddings
- Batch embedding generation
- Vector database search
- Background processing
- Asynchronous candidate matching
- Precomputed candidate representations

These optimizations should be introduced when actual performance requirements justify them.

---

### Security Boundary

The AI matching workflow does not bypass Hirely's authentication and authorization system.

The request flow is:

    Recruiter
        |
        v
    Authentication
        |
        v
    Recruiter Authorization
        |
        v
    Job Ownership Verification
        |
        v
    RecruiterMatchingService
        |
        v
    AI Matching Components

A recruiter cannot use the matching endpoint for another recruiter's job.

The AI service therefore operates behind the existing application security boundary.

---

### Architecture Decision

Hirely will use `RecruiterMatchingService` as the orchestration layer for recruiter-facing multi-candidate matching.

The architecture follows:

    FastAPI
       |
       v
    Authorization
       |
       v
    RecruiterMatchingService
       |
       +---- Job Preparation
       |
       +---- Candidate Preparation
       |
       +---- Matching Input Assembly
       |
       +---- Matching Engine
       |
       +---- Ranking
       |
       +---- Optional Top-N Explanation

This design maintains the project's core architectural principle:

**Use deterministic application logic where deterministic logic is sufficient, and use AI where semantic understanding or natural-language reasoning provides meaningful value.**

---

### Testing

The recruiter matching workflow is covered by automated API tests.

The implemented test coverage includes:

- Recruiter can match candidates for an owned job
- Candidate cannot access recruiter matching
- Unauthenticated requests are rejected
- Nonexistent jobs are rejected
- Inactive jobs are rejected
- Cross-recruiter access is rejected
- Candidates without eligible resumes are skipped
- Pending resumes are skipped
- Candidate ranking is returned correctly
- Recruiter explanation endpoint works
- Top-N explanation behavior works
- Candidate access to explanation endpoint is rejected
- Unauthenticated explanation requests are rejected
- Cross-recruiter explanation requests are rejected
- Invalid explanation limits are rejected

The full normal test suite currently passes:

    157 passed
    8 deselected

Integration tests involving external AI services remain separately marked so that normal regression testing does not depend on external model availability or quota.

---

### Mental Model

The recruiter-facing Hirely workflow can be remembered as:

    Prepare
       ↓
    Match
       ↓
    Score
       ↓
    Rank
       ↓
    Explain Top N

Or more simply:

**Recruiter Matching = Prepare + Evaluate + Rank + Explain**

The LLM is not the complete recruitment decision maker.

Instead:

**Structured Data → reliable facts**

**Embeddings → semantic meaning**

**Matching Engine → evidence combination**

**Ranking → deterministic ordering**

**LLM Explanation → human-readable reasoning**

This keeps Hirely's recruitment intelligence explainable, testable, and modular.

---

### Key Takeaways

- Recruiter matching is implemented as a dedicated service workflow.
- `RecruiterMatchingService` removes duplicated matching logic from API routes.
- The FastAPI layer remains thin.
- The job is prepared once and reused across candidates.
- Only eligible candidates participate in matching.
- Candidate preparation and job preparation remain separate services.
- `MatchingInputAssembler` provides a clean boundary between preparation and matching.
- The Matching Engine combines structured and semantic evidence.
- Candidate ranking remains deterministic.
- LLM explanations are generated only for the top N candidates.
- Explanation output is structured and validated.
- Authentication and authorization remain outside the AI workflow.
- The architecture can later support caching, vector search, batch processing, and background AI processing.
- The final design follows Hirely's hybrid approach: structured data + deterministic logic + embeddings + LLM reasoning.

---

# Implemented AI Features

The initial AI capabilities of Hirely have been implemented as focused, domain-specific AI services rather than as a single monolithic AI component.

The currently implemented candidate-facing AI features are:

- AI Career Coach
- AI Cover Letter Generator

Each feature follows the same architectural principles established for the Hirely AI layer:

- Dedicated AI module
- Structured context
- Controlled prompt construction
- Backend-only LLM interaction
- Structured AI output
- Pydantic validation
- Evidence-grounded generation
- Separation between application logic and AI provider logic

The purpose of this design is to make each AI capability independently testable, maintainable, and replaceable.

---

# AI Career Coach

## Purpose

The AI Career Coach provides candidates with contextual career guidance based on information already available within Hirely.

The feature is designed to provide useful career-oriented responses while grounding the AI in the candidate's actual profile, skills, resume information, job context, and application information where applicable.

The Career Coach is implemented as a dedicated AI module rather than placing prompt construction and Gemini interaction directly inside the API route.

The architecture follows:

    Candidate
        |
        v
    Candidate Context
        |
        +---- Profile
        +---- Skills
        +---- Resume
        +---- Job / Application Context
        |
        v
    Career Coach Context
        |
        v
    Prompt Builder
        |
        v
    Gemini Service
        |
        v
    Structured Response
        |
        v
    Pydantic Validation
        |
        v
    Candidate UI

---

## Career Coach Component Structure

The Career Coach is organized into dedicated components:

    career_coach/
        |
        +-- schemas.py
        |
        +-- context.py
        |
        +-- prompts.py
        |
        +-- service.py

Each component has a focused responsibility.

### Schemas

Defines the request and response contracts used by the Career Coach API.

Structured schemas ensure that the AI response follows a predictable application-level contract.

### Context Builder

The context builder prepares the information required by the Career Coach.

This keeps context preparation separate from prompt construction and model communication.

### Prompt Builder

The prompt builder converts the structured context into a controlled prompt.

Prompt construction is isolated from the Gemini provider implementation.

### Career Coach Service

The service coordinates:

1. Context preparation
2. Prompt construction
3. Gemini invocation
4. Structured response validation

The API route therefore remains thin and delegates the AI workflow to the service layer.

---

## Career Coach API

The candidate-facing Career Coach is exposed through a protected API endpoint.

The request must pass through Hirely's authentication and candidate authorization boundary before the AI service is invoked.

The request flow is:

    Candidate
        |
        v
    Authentication
        |
        v
    Candidate Authorization
        |
        v
    Career Coach API
        |
        v
    Career Coach Service
        |
        v
    Gemini Service
        |
        v
    Structured Response

The AI service does not bypass the existing authentication or authorization system.

---

## Career Coach Grounding

The Career Coach should use the information supplied by Hirely rather than inventing candidate-specific facts.

The model should not create unsupported:

- Skills
- Work experience
- Qualifications
- Projects
- Achievements
- Employment history
- Candidate accomplishments

The application's structured information remains the source of truth for known candidate facts.

This follows the broader Hirely architecture principle:

**Database and validated application data → reliable facts**

**LLM → interpretation and natural-language guidance**

The Career Coach therefore acts as an AI assistant rather than an authoritative source of candidate information.

---

## Career Coach Output Validation

The Career Coach uses structured AI output rather than relying on uncontrolled free-form model responses.

The flow is:

    Gemini
       |
       v
    AI Output
       |
       v
    Pydantic Schema
       |
       v
    Validation
       |
       +---- Invalid → Reject / Error
       |
       v
    Valid Career Coach Response
       |
       v
    Candidate UI

This keeps the AI provider response behind a predictable application boundary.

---

## Career Coach Provider Abstraction

The Career Coach does not communicate directly with Gemini-specific implementation details throughout the application.

Instead, it uses the shared Hirely Gemini service.

The architecture follows:

    Career Coach Service
            |
            v
       Gemini Service
            |
            v
          Gemini

This keeps provider-specific communication isolated and allows the underlying AI provider or model to evolve without requiring changes throughout the Career Coach feature.

---

# AI Cover Letter Generator

## Purpose

The AI Cover Letter Generator creates a job-specific cover letter for a candidate using the candidate's available Hirely information and the selected job's requirements.

The feature is intentionally designed as a focused generation workflow.

It does not attempt to become a complete application-management system.

The initial implementation supports:

- Job-specific cover letter generation
- Candidate profile context
- Candidate skills context
- Active resume context
- Job description context
- Required job skills
- Preferred job skills
- Structured AI response
- Copy functionality
- Regeneration

The generated document is presented as an editable draft that the candidate can review and personalize before using it.

---

## Cover Letter Architecture

The implemented cover letter workflow follows:

    Candidate
        |
        +-- Profile
        |
        +-- Skills
        |
        +-- Active Resume
        |
        v
    Candidate Context
        |
        +----------------------+
                               |
    Selected Job              |
        |                      |
        +-- Title              |
        +-- Description        |
        +-- Location           |
        +-- Employment Type    |
        +-- Experience Level   |
        +-- Required Skills    |
        +-- Preferred Skills   |
                               |
        +----------+-----------+
                   |
                   v
        Cover Letter Context
                   |
                   v
          Prompt Builder
                   |
                   v
             Gemini LLM
                   |
                   v
        Structured Response
                   |
                   v
        Pydantic Validation
                   |
                   v
        Cover Letter Response
                   |
                   v
            Candidate UI

---

## Cover Letter Component Structure

The Cover Letter Generator is implemented as a dedicated AI module:

    cover_letter/
        |
        +-- schemas.py
        |
        +-- context.py
        |
        +-- prompts.py
        |
        +-- service.py

The components have separate responsibilities.

### Request and Response Schemas

`CoverLetterRequest` accepts the selected job identifier.

The generated result is returned through `CoverLetterResponse`.

The API contract is therefore intentionally small:

    Request
        |
        +-- job_id

    Response
        |
        +-- cover_letter

This keeps the feature simple while allowing the backend to derive the candidate from the authenticated user.

---

## Candidate Context

The Cover Letter Generator builds a candidate context from information already stored in Hirely.

The candidate context may contain:

- Candidate name
- Headline
- Bio
- Location
- Candidate skills
- Active parsed resume

The active resume is treated as supporting candidate context.

Resume information is converted into the existing structured `ResumeData` representation before being passed to the cover letter context.

The context therefore combines structured profile information with validated resume information.

---

## Job Context

The selected job provides the source of truth for the target opportunity.

The job context contains:

- Job title
- Job description
- Location
- Employment type
- Experience level
- Required skills
- Preferred skills

Required and preferred skills are kept separate.

This distinction allows the prompt to prioritize genuine alignment with required requirements without treating optional requirements as mandatory.

---

## Context Construction

Candidate and job information are assembled into a dedicated `CoverLetterContext`.

The architecture is:

    Candidate Data
          |
          v
    Candidate Context
          |
          |
    Job Data
          |
          v
      Job Context
          |
          +--------+
                   |
                   v
        CoverLetterContext

The context builder also normalizes skill collections by removing empty values and duplicate skill names.

This keeps prompt input predictable and reduces unnecessary duplication.

---

## Prompt Builder

The `CoverLetterPromptBuilder` converts the structured `CoverLetterContext` into a controlled generation prompt.

Candidate and job information are serialized separately.

The prompt explicitly establishes grounding rules for the generated cover letter.

The model is instructed to:

- Use only supplied candidate information
- Use the selected job as the target opportunity
- Prioritize genuine candidate-job overlap
- Avoid unsupported claims
- Avoid inventing skills
- Avoid inventing experience
- Avoid inventing companies
- Avoid inventing projects
- Avoid inventing achievements
- Avoid inventing qualifications
- Avoid claiming a missing required skill
- Avoid inventing company culture or products
- Avoid including internal identifiers
- Avoid including authentication information
- Avoid mentioning the AI generation process

The model should produce only the final professional cover letter.

---

## Hallucination Control

Cover letter generation presents a particular hallucination risk because a language model may attempt to make a candidate sound stronger by adding unsupported qualifications.

Hirely therefore applies explicit grounding rules.

For example:

    Candidate Skills:
    Python
    FastAPI
    PostgreSQL

    Job Required Skills:
    Python
    FastAPI
    Docker

The generated letter may highlight Python and FastAPI.

It must not claim that the candidate has Docker experience unless supporting candidate information exists.

Similarly, the model must not invent:

- Years of experience
- Previous employers
- Job titles
- Projects
- Responsibilities
- Achievements
- Certifications
- Education
- Technical expertise

This follows Hirely's broader principle:

**AI should interpret available evidence, not manufacture candidate qualifications.**

---

## Cover Letter API

The feature is exposed through:

    POST /candidate/cover-letter

The request contains the selected job identifier.

The candidate is derived from the authenticated request rather than being supplied by the frontend.

The request flow is:

    Candidate
        |
        v
    Authentication
        |
        v
    Candidate Authorization
        |
        v
    Cover Letter API
        |
        v
    Active Job Validation
        |
        v
    Cover Letter Service
        |
        v
    Context Construction
        |
        v
    Prompt Construction
        |
        v
    Gemini Service
        |
        v
    Structured Response
        |
        v
    Candidate UI

Only an active job can be used by the current implementation.

If the selected job cannot be found or is inactive, the API returns an appropriate HTTP error instead of invoking the AI service.

---

## Cover Letter AI Provider Flow

The Cover Letter Service communicates with the shared Gemini service.

The architecture is:

    CoverLetterService
           |
           v
    GeminiService
           |
           v
        Gemini
           |
           v
    CoverLetterResponse

The Cover Letter Service is therefore independent from the low-level Gemini communication implementation.

This preserves the project's AI provider abstraction principle.

---

## Structured AI Response

The Cover Letter Generator requests a structured response matching `CoverLetterResponse`.

The expected structure is:

    CoverLetterResponse
        |
        +-- cover_letter: string

The generated result is validated before being returned by the API.

The application also verifies that the generated cover letter is not empty before presenting it to the candidate.

---

## Candidate User Experience

The candidate can access the Cover Letter Generator from the Job Detail page.

The frontend workflow is:

    Job Detail
        |
        v
    Generate Cover Letter
        |
        v
    Cover Letter Page
        |
        v
    Generate
        |
        v
    AI-generated Draft
        |
        +---- Copy
        |
        +---- Regenerate

The generated cover letter is displayed in a document-style interface.

The candidate can copy the generated text and review or personalize it before sending it to an employer.

The current implementation intentionally does not automatically send the cover letter to recruiters.

---

## Frontend Architecture

The frontend uses a dedicated service module for communication with the backend:

    frontend
        |
        +-- services/
        |      |
        |      +-- coverLetter.js
        |
        +-- pages/
               |
               +-- CoverLetter.jsx
               +-- CoverLetter.css

`coverLetter.js` is responsible for the API request.

`CoverLetter.jsx` manages:

- Job loading
- Generation state
- Generated content
- Error state
- Copy state
- Regeneration

`CoverLetter.css` contains the presentation layer for the cover letter workspace.

The AI provider is never called directly from the frontend.

---

## Security Boundary

The Cover Letter Generator follows the existing Hirely security model.

The request must pass through:

    Candidate
        |
        v
    Authentication
        |
        v
    Candidate Authorization
        |
        v
    Cover Letter Endpoint
        |
        v
    Cover Letter Service
        |
        v
    Gemini Service

The Gemini API credentials remain on the backend.

The frontend does not receive or store the Gemini API key.

Only the information required for cover letter generation is assembled into the AI context.

---

## Privacy Considerations

Candidate resumes and profiles may contain personal information.

The Cover Letter Generator therefore follows a minimum-context approach.

The AI context is constructed specifically for cover letter generation rather than sending unrelated application information.

Sensitive contact information such as internal authentication data is not included in the cover letter generation prompt.

The generated cover letter is intended for the candidate's review and should not be treated as an independently verified representation of the candidate.

---

## Why RAG Is Not Used

The initial Cover Letter Generator does not use Retrieval-Augmented Generation.

The feature currently operates on a small, well-defined context:

    Candidate Profile
        +
    Candidate Skills
        +
    Active Resume
        +
    Selected Job

This information can be assembled directly without requiring semantic retrieval from a large external knowledge base.

Therefore, introducing a vector database or retrieval pipeline at this stage would add architectural complexity without providing a necessary benefit.

RAG may become valuable later for capabilities involving larger knowledge collections, such as:

- Recruitment knowledge bases
- Company-specific hiring policies
- Large collections of job descriptions
- Historical candidate information
- Internal recruitment documentation

Such technologies should be introduced when actual retrieval requirements justify them.

---

## Testing

The implemented Cover Letter Generator has been validated through the Hirely application workflow.

The feature was tested with:

- Candidate authentication
- Job selection
- Job detail navigation
- Cover letter generation
- Real Gemini generation
- Generated cover letter rendering
- Copy functionality
- Regeneration functionality
- Protected candidate route
- Invalid generation states
- Backend regression testing
- Frontend production build

The normal backend regression suite passed:

    182 passed
    8 deselected

The frontend production build completed successfully.

The generated cover letter was also verified through browser-based testing using the actual Hirely application and Gemini service.

---

## Architecture Decision

Hirely will implement AI-assisted candidate features as independent domain-specific AI services.

The Cover Letter Generator follows:

    Candidate Data
          +
    Job Data
          |
          v
    Structured Context
          |
          v
    Controlled Prompt
          |
          v
        Gemini
          |
          v
    Pydantic Validation
          |
          v
    Structured Application Result
          |
          v
    Candidate UI

This design provides:

- Clear separation of concerns
- Controlled AI context
- Reduced hallucination risk
- Structured output validation
- Backend-only provider access
- Provider abstraction
- Independent testing
- Simple frontend integration
- Low architectural complexity
- Future extensibility

---

## Current AI Capability Model

The implemented AI capabilities can be understood as:

    Candidate
        |
        +---- Career Coach
        |        |
        |        +---- Contextual Guidance
        |
        +---- Cover Letter Generator
                 |
                 +---- Job-specific Application Draft

These capabilities operate alongside the larger recruitment intelligence architecture.

The future matching system remains responsible for:

- Candidate representation
- Job representation
- Semantic matching
- Candidate ranking
- Match explanations
- AI-powered recommendations

The candidate assistance features complement this system rather than replacing it.

---

## AI Feature Design Principles

The implemented candidate AI features follow the same core Hirely principles:

### Structured First

Application data is collected and organized before being sent to the AI model.

### Grounded Generation

The model is instructed to use only the information supplied in its context.

### Deterministic Security

Authentication and authorization remain traditional backend responsibilities.

### Provider Abstraction

AI provider communication is isolated inside shared AI services.

### Structured Output

AI responses are validated using Pydantic schemas.

### Minimum Necessary Context

Only information required for the specific AI task should be supplied.

### No Premature Complexity

RAG, vector databases, agents, and other advanced infrastructure are introduced only when the application's requirements justify them.

### Human Review

AI-generated candidate-facing content is treated as an assistive draft rather than an unquestionable source of truth.

---

## Key Takeaways

- Hirely now contains dedicated candidate-facing AI services.
- The AI Career Coach provides contextual career guidance.
- The AI Cover Letter Generator creates job-specific application drafts.
- AI features are implemented as independent domain modules.
- Context construction is separated from prompt construction.
- Prompt construction is separated from the Gemini provider implementation.
- Candidate and job information are assembled into structured context.
- Required and preferred job skills are represented separately.
- Cover letter generation is grounded in available candidate and job evidence.
- The system explicitly prevents unsupported candidate claims.
- AI output is returned through structured Pydantic schemas.
- Gemini credentials remain on the backend.
- Candidate authorization remains outside the AI logic.
- The frontend communicates with AI capabilities through FastAPI APIs.
- The Cover Letter Generator currently does not require RAG or vector storage.
- AI-generated cover letters are presented as drafts that candidates should review and personalize.
- The architecture remains modular and ready for future AI capabilities.