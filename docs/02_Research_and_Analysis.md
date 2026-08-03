# Research and Analysis

> **Version:** 0.1.0 (Planning Phase)  
> **Project:** Hirely  
> **Status:** In Progress

---

# Purpose

The purpose of this document is to record the research conducted during the planning and development of Hirely. Each research topic contributes to technical decisions, architectural planning, feature design, and implementation strategies.

Rather than collecting information without direction, this document focuses on answering practical engineering questions that directly influence the design and development of the project.

---

# Research Methodology

Each research topic in this document follows the same structure:

1. Background
2. Research Findings
3. Analysis
4. Decision for Hirely

This methodology ensures that every design decision is supported by research rather than assumptions.

---

# Research Roadmap

The following topics will be researched throughout the development of Hirely.

## 1. Career Domain Research

- Modern recruitment process
- Job application workflow
- Resume best practices
- Cover letter standards
- Career coaching fundamentals

---

## 2. Applicant Tracking Systems (ATS)

- What is ATS?
- How ATS works
- Resume parsing
- ATS optimization
- Keyword matching
- ATS limitations

---

## 3. Resume Analysis

- Resume structure
- Resume scoring techniques
- Skill extraction
- Experience evaluation
- Education analysis

---

## 4. Large Language Models (LLMs)

- LLM fundamentals
- Prompt engineering
- Context windows
- Structured outputs
- Hallucination
- Limitations

---

## 5. AI Frameworks

- LangChain
- LangGraph (Future)
- LlamaIndex (Research)
- Framework comparison

---

## 6. Backend Technologies

- FastAPI
- REST APIs
- Pydantic
- SQLAlchemy
- Async programming

---

## 7. Frontend Technologies

- Streamlit
- Alternative frontend frameworks
- UI/UX considerations

---

## 8. Document Processing

- PDF extraction
- Resume parsing
- OCR (Future)
- Text preprocessing

---

## 9. AI Model Selection

- OpenAI
- Ollama
- Local models
- Cloud models
- Cost comparison

---

## 10. Database Design

- SQLite
- PostgreSQL
- Data models
- Scalability

---

## 11. Deployment

- Docker
- Docker Compose
- AWS EC2
- Environment variables
- Production deployment

---

## 12. Security

- API security
- Secret management
- Authentication
- Data privacy
- Secure deployment

---

# Research Status

| Topic | Status |
|--------|--------|
| Career Domain | ⏳ Pending |
| ATS | ⏳ Pending |
| Resume Analysis | ⏳ Pending |
| LLMs | ⏳ Pending |
| AI Frameworks | ⏳ Pending |
| Backend | ⏳ Pending |
| Frontend | ⏳ Pending |
| Document Processing | ⏳ Pending |
| AI Models | ⏳ Pending |
| Database | ⏳ Pending |
| Deployment | ⏳ Pending |
| Security | ⏳ Pending |

---

# 1. Career Domain Research

## 1.1 Job Application Lifecycle

### Background

To build an effective AI-powered career platform, it is essential to understand the complete job application lifecycle. Rather than focusing on isolated tasks such as resume writing or interview preparation, Hirely aims to support users throughout their entire career preparation journey.

Understanding this lifecycle helps identify the challenges faced by job seekers, the decisions they make at each stage, and the opportunities where Artificial Intelligence can provide meaningful assistance.

---

### Research Findings

A typical job application lifecycle consists of the following stages:

1. Career Goal Definition
2. Skill Assessment
3. Resume Creation
4. Resume Optimization
5. Job Search
6. Job Description Analysis
7. Resume Customization
8. Cover Letter Preparation
9. Job Application Submission
10. ATS Screening
11. Recruiter Review
12. Interview Preparation
13. Interview Process
14. Job Offer
15. Career Growth and Continuous Learning

Each stage introduces unique challenges that can impact a candidate's chances of securing employment.

---

### Analysis

The research demonstrates that the hiring process extends far beyond simply creating a resume. Job seekers require continuous guidance throughout multiple stages of their career journey.

Many existing platforms solve only individual problems, such as resume building or interview preparation, requiring users to switch between multiple tools. This fragmented experience reduces efficiency and limits personalized guidance.

A unified platform that supports multiple stages of the hiring process can provide a more consistent and effective user experience.

---

### Decision for Hirely

Hirely will be designed as an end-to-end AI-powered career platform rather than a single-purpose resume application.

The initial release (Version 1.0) will focus on the most impactful stages of the job application lifecycle:

- Resume Checker
- Resume Scorer
- Cover Letter Generator
- AI Career Coach

The software architecture will remain modular so that future versions can expand to support additional stages such as interview simulation, LinkedIn profile optimization, job matching, recruiter tools, and career development services.

---

### Key Takeaways

- The hiring process is a multi-stage journey rather than a single task.
- Users require personalized assistance throughout different stages.
- Existing solutions are often fragmented across multiple platforms.
- Hirely will provide an integrated AI-powered experience.
- Future development should continue to align with the complete job application lifecycle.