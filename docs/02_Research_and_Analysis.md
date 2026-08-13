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

---

# 2. Applicant Tracking Systems (ATS)

## 2.1 What is an Applicant Tracking System?

### Background

As organizations receive hundreds or even thousands of job applications for a single position, manually reviewing every resume becomes inefficient and time-consuming. To streamline the recruitment process, companies use Applicant Tracking Systems (ATS), which automate many stages of candidate management and resume evaluation.

Understanding how ATS platforms operate is essential for designing AI-powered career tools that help users create resumes optimized for modern recruitment systems.

---

### Research Findings

An Applicant Tracking System (ATS) is recruitment software used by organizations to collect, organize, process, and manage job applications throughout the hiring process.

An ATS serves as the first stage of candidate evaluation before resumes reach recruiters or hiring managers. Rather than replacing human decision-making, it assists recruiters by organizing applicant information, extracting relevant resume data, filtering candidates based on predefined criteria, and simplifying recruitment workflows.

Modern ATS platforms commonly perform the following tasks:

- Collect job applications
- Parse resume content
- Extract candidate information
- Identify skills and qualifications
- Organize applicant records
- Rank or filter candidates
- Support recruiter workflows
- Track candidate progress throughout recruitment

The level of automation varies between ATS platforms, but nearly all systems aim to reduce manual effort while improving recruitment efficiency.

---

### Analysis

The research indicates that an ATS is significantly more than a keyword-matching tool. It functions as a recruitment management system responsible for processing candidate information before recruiters begin manual evaluation.

This understanding changes how resume optimization should be approached. Instead of focusing solely on visual formatting or keyword density, resumes should be designed to maximize readability, accurate information extraction, and compatibility with automated recruitment systems.

---

### Decision for Hirely

Hirely will treat ATS compatibility as an essential aspect of resume quality rather than as an independent feature.

The Resume Checker and Resume Scorer modules will evaluate resumes with ATS compatibility in mind, helping users improve not only resume content but also the likelihood that their resumes are successfully processed by recruitment systems.

Future versions of Hirely may include a dedicated ATS Optimization module that provides deeper analysis and recommendations based on ATS best practices.

---

### Key Takeaways

- ATS is recruitment management software.
- ATS assists recruiters rather than replacing them.
- Resume processing involves more than keyword matching.
- ATS compatibility should be considered during resume evaluation.
- Hirely should incorporate ATS awareness into its core resume analysis features.

---

## 2.2 Why Do Companies Use Applicant Tracking Systems?

### Background

As organizations receive a growing number of job applications, managing the recruitment process manually becomes inefficient, time-consuming, and difficult to scale. Companies require a centralized system that streamlines recruitment activities, improves collaboration, and reduces administrative effort.

Applicant Tracking Systems (ATS) were developed to address these challenges by automating repetitive recruitment tasks and providing recruiters with a structured hiring workflow.

---

### Research Findings

Organizations use Applicant Tracking Systems for several important reasons:

- Manage large volumes of job applications efficiently.
- Organize candidate information in a centralized database.
- Reduce the time required to review and process resumes.
- Standardize recruitment workflows across hiring teams.
- Enable collaboration between recruiters, HR professionals, and hiring managers.
- Track candidate progress throughout different hiring stages.
- Maintain recruitment records for reporting, compliance, and auditing purposes.

Although resume filtering is one function of an ATS, its broader purpose is to improve the overall efficiency and consistency of the recruitment process.

---

### Analysis

The research demonstrates that ATS platforms are designed primarily as recruitment management systems rather than simple resume filtering tools.

Understanding this distinction is important because optimizing a resume is not solely about passing automated filters. A high-quality resume should also communicate skills, experience, and qualifications clearly to human recruiters after it has been processed by the ATS.

---

### Decision for Hirely

Hirely will focus on helping users create resumes that are understandable by both Applicant Tracking Systems and human recruiters.

The platform will prioritize resume clarity, structured formatting, relevant content, and ATS compatibility rather than attempting to exploit or bypass recruitment systems.

This approach aligns Hirely with modern recruitment best practices while providing users with practical and ethical career guidance.

---

### Key Takeaways

- ATS improves recruitment efficiency.
- ATS supports the entire hiring workflow.
- Resume filtering is only one component of an ATS.
- Hirely should optimize resumes for both ATS systems and recruiters.

---

## 2.3 How Does an Applicant Tracking System Work?

### Background

Understanding the workflow of an Applicant Tracking System (ATS) is essential for developing career tools that generate resumes compatible with modern recruitment systems. Before a recruiter reviews a resume, the ATS typically processes, organizes, and evaluates candidate information.

Studying this workflow helps identify where resumes may succeed or fail during the recruitment process.

---

### Research Findings

A typical Applicant Tracking System processes resumes through the following stages:

1. Candidate submits a job application.
2. The resume is uploaded to the ATS.
3. The ATS parses the resume and extracts structured information.
4. Candidate details such as name, education, work experience, and skills are organized into a searchable profile.
5. The ATS compares candidate information against job requirements and recruiter-defined criteria.
6. Candidates are organized, filtered, or ranked for recruiter review.
7. Recruiters evaluate shortlisted candidates and continue the hiring process.

Although the exact implementation varies across ATS platforms, the overall workflow remains similar in most recruitment systems.

---

### Analysis

The research indicates that ATS platforms do not evaluate resumes in the same way humans do. Instead, they first convert resume content into structured information that can be searched, filtered, and analyzed efficiently.

This means that resumes should be written in a format that allows important information to be extracted accurately while remaining clear and readable for human recruiters.

---

### Decision for Hirely

Hirely will evaluate resumes from two perspectives:

- Human readability
- ATS readability

The Resume Checker will assess not only writing quality but also whether important resume information can be effectively processed by Applicant Tracking Systems.

This approach improves both recruiter experience and ATS compatibility.

---

### Key Takeaways

- ATS follows a structured recruitment workflow.
- Resume parsing is a critical step before recruiter review.
- ATS converts resumes into structured candidate information.
- Effective resumes should be understandable by both ATS software and human recruiters.

---

## 2.4 Resume Parsing

### Background

Resumes are typically submitted as PDF or Word documents containing unstructured text. Before a recruitment system or AI model can evaluate a resume, the document must be converted into structured information that represents the candidate's profile.

This process is known as **resume parsing** and forms a critical step in modern recruitment systems.

---

### Research Findings

Resume parsing is the process of extracting meaningful information from a resume and organizing it into structured data.

A resume parser typically identifies and extracts information such as:

- Personal information (Name, Email, Phone Number)
- Professional Summary
- Education
- Work Experience
- Technical Skills
- Certifications
- Projects
- Languages
- Achievements

Once extracted, this information can be stored, searched, compared, and analyzed by recruitment systems or AI applications.

---

### Analysis

Resume parsing transforms an unstructured document into structured candidate information that can be processed efficiently.

Accurate parsing improves the quality of resume evaluation because downstream systems, including AI models, receive organized and meaningful data instead of raw document text.

This separation also makes the overall system more modular and maintainable.

---

### Decision for Hirely

Hirely will include a dedicated resume parsing stage before AI analysis.

The processing pipeline will follow this sequence:

1. Upload Resume
2. Extract Text
3. Parse Resume Sections
4. Generate Structured Candidate Data
5. AI-Based Resume Analysis
6. Generate Personalized Feedback

This modular pipeline will improve accuracy, maintainability, and future scalability.

---

### Key Takeaways

- Resume parsing converts unstructured resumes into structured data.
- Structured information improves AI analysis.
- Resume parsing should occur before AI evaluation.
- A modular processing pipeline improves system quality and scalability.

---

## 2.5 Keyword Matching

### Background

One of the primary functions of an Applicant Tracking System (ATS) is to compare the information contained in a candidate's resume with the requirements specified in a job description. This comparison helps recruiters quickly identify applicants whose qualifications align with the role.

Keyword matching is a common technique used during this process.

---

### Research Findings

Keyword matching involves identifying important words and phrases within both the job description and the candidate's resume.

Common elements used for comparison include:

- Technical skills
- Programming languages
- Tools and technologies
- Job titles
- Certifications
- Educational qualifications
- Years of experience

The purpose of keyword matching is not to replace recruiter judgment but to assist in identifying candidates whose qualifications closely align with the job requirements.

Modern recruitment systems may combine keyword matching with additional evaluation techniques such as semantic analysis and AI-assisted ranking.

---

### Analysis

Effective keyword matching requires resumes to clearly describe relevant skills and experiences using professional and industry-recognized terminology.

Simply inserting keywords without supporting experience or context does not improve resume quality and may reduce credibility during recruiter review.

Keyword optimization should therefore focus on accurately representing a candidate's genuine qualifications while maintaining readability and professionalism.

---

### Decision for Hirely

Hirely will compare resumes with job descriptions to identify relevant and missing keywords.

Rather than encouraging keyword stuffing, the platform will recommend meaningful improvements that naturally align the resume with the target job description while preserving clarity and authenticity.

Keyword analysis will become one component of the overall Resume Score instead of being treated as the only evaluation criterion.

---

### Key Takeaways

- Keyword matching compares resume content with job requirements.
- Skills, technologies, education, and experience are commonly evaluated.
- Keyword optimization should improve clarity, not manipulate ATS systems.
- Hirely will provide balanced keyword recommendations supported by AI analysis.

---

## 2.6 Limitations of Applicant Tracking Systems

### Background

Although Applicant Tracking Systems improve recruitment efficiency, they are not perfect. Their effectiveness depends on the quality of resume parsing, matching algorithms, and the information provided by candidates.

Understanding these limitations helps developers design career tools that support both automated systems and human recruiters.

---

### Research Findings

Common limitations of Applicant Tracking Systems include:

- Difficulty interpreting complex resume layouts.
- Inconsistent extraction of information from tables, graphics, and multi-column designs.
- Limited understanding of context and real-world experience.
- Dependence on clearly written and structured resume content.
- Possible mismatches caused by different terminology or abbreviations.
- Challenges processing scanned documents without OCR support.

Modern ATS platforms continue to improve through Artificial Intelligence, but no system can fully replace human judgment during recruitment.

---

### Analysis

ATS platforms provide valuable assistance during recruitment, but they should not be viewed as perfect evaluation systems.

Candidates should focus on creating resumes that communicate their qualifications clearly instead of attempting to manipulate automated screening systems.

Effective resume evaluation should combine ATS compatibility with human readability and professional presentation.

---

### Decision for Hirely

Hirely will educate users about ATS limitations while encouraging best practices for professional resume writing.

The platform will recommend improvements that enhance resume clarity, structured formatting, and content quality rather than promoting techniques intended to bypass recruitment systems.

Hirely's recommendations will balance ATS compatibility with recruiter expectations.

---

### Key Takeaways

- ATS has technical limitations.
- Human recruiters remain an essential part of hiring.
- Resume clarity is more important than attempting to manipulate ATS.
- Hirely will promote ethical and practical resume optimization.

---

## 2.7 Final Decision for Hirely

### Summary

The research conducted on Applicant Tracking Systems demonstrates that modern recruitment is a combination of automated processing and human decision-making. ATS platforms improve recruitment efficiency by organizing candidate information, parsing resumes, supporting recruiter workflows, and assisting in candidate selection.

However, ATS platforms also have technical limitations and should not be considered complete replacements for human recruiters.

---

### Final Decision for Hirely

Based on the research findings, Hirely will adopt the following principles for resume evaluation:

- Focus on both ATS compatibility and recruiter readability.
- Encourage professional resume writing instead of keyword stuffing.
- Use resume parsing before AI analysis.
- Compare resumes against job descriptions to provide meaningful recommendations.
- Generate AI-powered feedback using structured resume information.
- Promote ethical resume optimization aligned with modern recruitment practices.

The Resume Checker and Resume Scorer will therefore combine traditional ATS best practices with Artificial Intelligence to provide balanced, practical, and personalized recommendations.

---

### Impact on System Design

The research establishes the following high-level processing pipeline for Hirely:

1. Resume Upload
2. Text Extraction
3. Resume Parsing
4. ATS Compatibility Analysis
5. Job Description Comparison
6. AI Resume Evaluation
7. Resume Score Generation
8. Personalized Improvement Suggestions

This modular pipeline will serve as the foundation for future software architecture and implementation.

---

# 3. Resume Analysis

## 3.1 What is a Resume?

### Background

A resume is one of the most important documents in the job application process. It provides a structured summary of a candidate's education, skills, work experience, projects, certifications, and achievements.

Recruiters use resumes to quickly evaluate whether a candidate is suitable for a particular role before deciding whether to proceed with interviews.

Understanding the purpose of a resume is essential for designing AI systems that provide meaningful resume analysis and improvement suggestions.

---

### Research Findings

A resume is a professional document that presents a candidate's qualifications in a clear, concise, and organized format.

Its primary purpose is to communicate relevant information that demonstrates a candidate's suitability for a specific job opportunity.

A well-written resume typically helps recruiters:

- Understand the candidate's background.
- Evaluate relevant skills and experience.
- Compare applicants consistently.
- Decide whether to invite the candidate for an interview.

Rather than serving as a complete professional biography, a resume is designed to highlight the information most relevant to the target position.

---

### Analysis

The research indicates that the objective of a resume is not simply to list qualifications but to communicate professional value effectively.

A successful resume balances completeness with clarity, allowing both Applicant Tracking Systems and human recruiters to understand the candidate's qualifications efficiently.

This highlights the importance of content quality, organization, and relevance rather than visual design alone.

---

### Decision for Hirely

Hirely will evaluate resumes based on how effectively they communicate a candidate's qualifications to both Applicant Tracking Systems and human recruiters.

The Resume Checker will prioritize clarity, relevance, structure, and professional presentation while generating personalized recommendations for improvement.

---

### Key Takeaways

- A resume is a professional summary of a candidate's qualifications.
- The primary goal of a resume is to secure an interview.
- A resume should communicate value clearly and efficiently.
- Effective resumes balance ATS compatibility with recruiter readability.

---

## 3.2 Essential Sections of a Resume

### Background

A professional resume is organized into clearly defined sections that allow recruiters and Applicant Tracking Systems (ATS) to quickly locate important information. A consistent structure improves readability, simplifies resume evaluation, and increases the likelihood that key qualifications are identified correctly.

Understanding the standard sections of a resume is essential for developing automated resume analysis tools.

---

### Research Findings

Although resume formats vary across industries and experience levels, a professional resume commonly includes the following sections:

- Contact Information
- Professional Summary or Career Objective
- Technical and Professional Skills
- Work Experience
- Projects
- Education
- Certifications
- Achievements (Optional)
- Languages (Optional)
- Volunteer Experience (Optional)

Each section provides specific information that helps recruiters evaluate a candidate's qualifications efficiently.

---

### Analysis

A well-structured resume presents information in a logical sequence, allowing both ATS platforms and recruiters to locate relevant details quickly.

Missing important sections may reduce the effectiveness of a resume by limiting the information available for evaluation. At the same time, unnecessary sections may distract from the candidate's most relevant qualifications.

The appropriate resume structure should therefore balance completeness with relevance.

---

### Decision for Hirely

Hirely will detect the presence and completeness of standard resume sections.

The Resume Checker will identify missing sections, evaluate the organization of the resume, and provide personalized recommendations to improve overall structure based on industry best practices.

---

### Key Takeaways

- Professional resumes follow a structured format.
- Each section serves a specific purpose.
- Missing sections may reduce resume effectiveness.
- Hirely will automatically detect and evaluate resume sections.

---

## 3.3 Characteristics of a Good Resume

### Background

A resume should do more than present information—it should communicate a candidate's qualifications clearly, professionally, and efficiently. Recruiters often review many resumes within a limited time, making clarity and organization essential.

Understanding the characteristics of an effective resume helps define meaningful evaluation criteria for AI-powered resume analysis systems.

---

### Research Findings

A high-quality resume generally demonstrates the following characteristics:

- Clear and easy-to-read structure
- Concise and relevant content
- Professional language and tone
- Accurate and truthful information
- Well-organized sections
- Relevant skills and experience for the target role
- Consistent formatting
- Compatibility with Applicant Tracking Systems (ATS)

Together, these characteristics improve both recruiter readability and automated resume processing.

---

### Analysis

An effective resume balances completeness with simplicity. It highlights the candidate's most relevant qualifications while avoiding unnecessary information.

A resume should not only be visually organized but also communicate professional value in a way that is understandable to both ATS platforms and human recruiters.

---

### Decision for Hirely

Hirely will evaluate resumes across multiple quality dimensions instead of assigning a score based on a single factor.

The Resume Checker will assess clarity, structure, relevance, professionalism, ATS compatibility, and overall presentation to generate detailed and personalized feedback.

---

### Key Takeaways

- A good resume communicates value clearly.
- Clarity and relevance are more important than excessive detail.
- ATS compatibility and recruiter readability should both be considered.
- Hirely will evaluate multiple aspects of resume quality.

---

## 3.4 Common Resume Mistakes

### Background

Many resumes fail to achieve their purpose not because candidates lack qualifications, but because important information is presented poorly or omitted entirely. Understanding common resume mistakes helps define the validation rules and recommendations that an AI-powered resume analysis system should provide.

---

### Research Findings

Common resume mistakes include:

- Spelling and grammatical errors.
- Generic resumes that are not tailored to the target role.
- Poor organization and inconsistent formatting.
- Missing or weak professional summaries.
- Lack of measurable achievements.
- Inclusion of irrelevant or outdated information.
- ATS-unfriendly formatting such as tables, graphics, or complex layouts.
- Missing important keywords related to the target job description.

These issues can reduce both recruiter readability and ATS compatibility.

---

### Analysis

Most resume mistakes are related to communication rather than technical ability. Even highly qualified candidates may reduce their chances of securing interviews if their resumes fail to present their experience clearly and professionally.

An effective resume analysis system should identify these issues and provide actionable recommendations for improvement.

---

### Decision for Hirely

Hirely will automatically detect common resume mistakes and categorize feedback into areas such as writing quality, structure, ATS compatibility, keyword relevance, and content effectiveness.

The platform will prioritize actionable recommendations that help users improve their resumes rather than simply identifying problems.

---

### Key Takeaways

- Common resume mistakes reduce interview opportunities.
- Resume quality depends on communication as much as qualifications.
- AI should provide clear and actionable recommendations.
- Hirely will detect and explain common resume issues.

---

## 3.5 Resume Evaluation Criteria

### Background

An AI-powered resume analysis system requires clear and consistent evaluation criteria to generate reliable feedback. Rather than relying on subjective judgment, resumes should be assessed using predefined quality dimensions that reflect modern recruitment practices.

Establishing these evaluation criteria provides a foundation for objective resume scoring and personalized recommendations.

---

### Research Findings

The following evaluation criteria were identified as the most important for assessing resume quality:

- Resume Structure
- Content Quality
- ATS Compatibility
- Relevance to the Target Job
- Skills Presentation
- Work Experience
- Project Descriptions
- Writing Quality
- Overall Professional Presentation

Each criterion represents a different aspect of resume quality and contributes to the overall effectiveness of the document.

---

### Analysis

Resume quality cannot be measured using a single factor. A well-designed evaluation system should assess multiple dimensions independently before combining them into an overall assessment.

This multi-dimensional approach produces more meaningful feedback and helps candidates understand both their strengths and areas for improvement.

---

### Decision for Hirely

Hirely will evaluate resumes using multiple independent evaluation criteria rather than relying on a single overall assessment.

Each criterion will generate its own score and feedback before contributing to the final Resume Score. This approach will improve transparency and provide users with actionable recommendations.

---

### Key Takeaways

- Resume evaluation should be multi-dimensional.
- Independent criteria improve scoring accuracy.
- Users benefit from detailed category-based feedback.
- Hirely will combine multiple evaluation criteria into one comprehensive assessment.

---

## 3.6 Resume Scoring Metrics

### Background

To generate meaningful feedback, an AI-powered resume analysis system requires a structured scoring methodology. Rather than assigning arbitrary scores, each important aspect of a resume should contribute to the final evaluation according to its significance.

A weighted scoring model improves consistency, transparency, and explainability.

---

### Research Findings

The proposed evaluation metrics for Hirely Version 1.0 are:

| Evaluation Criterion | Proposed Weight |
|----------------------|----------------:|
| Resume Structure | 10% |
| Content Quality | 20% |
| ATS Compatibility | 15% |
| Job Relevance | 20% |
| Skills Presentation | 10% |
| Work Experience | 10% |
| Projects | 10% |
| Writing Quality | 5% |

The combined score from these categories produces the overall Resume Score.

These weights are based on the current research conducted during the planning phase and may be refined as the project evolves.

---

### Analysis

A weighted scoring model provides greater transparency than a single subjective score.

Category-based scoring enables users to understand why they received a particular score while allowing the system to generate targeted recommendations for improvement.

This approach also simplifies future enhancements because individual evaluation modules can evolve independently without redesigning the entire scoring system.

---

### Decision for Hirely

Hirely Version 1.0 will implement a weighted resume scoring engine based on multiple evaluation criteria.

Each category will be evaluated independently before calculating the overall Resume Score.

The scoring engine will remain configurable so that category weights can be adjusted as future research and user feedback become available.

---

### Key Takeaways

- Resume scoring should use multiple weighted criteria.
- Category-based scoring improves explainability.
- Weighted evaluation supports future scalability.
- Hirely will implement a configurable scoring engine.

---

## 3.7 Final Decision for Hirely

### Summary

The research conducted on resume analysis demonstrates that an effective resume is more than a well-formatted document. It must clearly communicate a candidate's qualifications, align with the target job, remain compatible with Applicant Tracking Systems (ATS), and provide recruiters with relevant information quickly and professionally.

High-quality resume evaluation requires multiple assessment criteria rather than a single subjective score.

---

### Final Decision for Hirely

Based on the research findings, Hirely will implement a comprehensive resume evaluation system that:

- Analyzes resume structure and completeness.
- Evaluates content quality and relevance.
- Measures ATS compatibility.
- Compares resumes with job descriptions.
- Generates category-based scores.
- Provides personalized AI-powered recommendations.
- Explains the reasoning behind every recommendation.

The goal of Hirely is not only to evaluate resumes but also to help users continuously improve them through clear, practical, and explainable feedback.

---

### Impact on System Design

The Resume Checker module will follow the following processing pipeline:

1. Resume Upload
2. Text Extraction
3. Resume Parsing
4. Structure Analysis
5. ATS Compatibility Analysis
6. Job Description Matching
7. Resume Quality Evaluation
8. Weighted Resume Scoring
9. AI Feedback Generation
10. Personalized Improvement Suggestions

This modular workflow establishes the foundation for the Resume Checker and Resume Scorer components that will be implemented during the development phase.

---

# 4. Large Language Models (LLMs)

## 4.1 What is a Large Language Model (LLM)?

### Background

Large Language Models (LLMs) are advanced Artificial Intelligence models designed to understand, generate, summarize, and analyze human language. They have become a fundamental technology behind modern AI assistants, document analysis systems, and intelligent software applications.

Understanding how LLMs work at a high level is essential before integrating them into Hirely.

---

### Research Findings

A Large Language Model (LLM) is an AI model trained on massive collections of text to learn language patterns, relationships, and context.

Rather than storing predefined answers, LLMs predict the most appropriate sequence of words based on the information they receive.

Modern LLMs are capable of performing tasks such as:

- Question Answering
- Text Summarization
- Content Generation
- Language Translation
- Code Generation
- Document Analysis
- Information Extraction
- Text Classification

These capabilities make LLMs valuable components in AI-powered software systems.

---

### Analysis

LLMs excel at understanding and generating natural language but should not replace deterministic software components responsible for business logic, data validation, or structured processing.

The most effective AI systems combine traditional software engineering with LLM capabilities, allowing each component to perform tasks suited to its strengths.

---

### Decision for Hirely

Hirely will use Large Language Models as intelligent assistants rather than as complete decision-making systems.

Traditional software components will perform tasks such as resume parsing, ATS analysis, and score calculation, while the LLM will generate explanations, personalized recommendations, and natural language feedback.

This separation improves reliability, transparency, and maintainability.

---

### Key Takeaways

- LLMs understand and generate natural language.
- LLMs are powerful but should not replace traditional software logic.
- AI systems are strongest when combining software engineering with LLM capabilities.
- Hirely will use LLMs for explanation and guidance rather than core business logic.

---

## 4.2 Why Does Hirely Need a Large Language Model?

### Background

Many resume analysis tasks can be performed using traditional software techniques such as text extraction, resume parsing, keyword matching, and rule-based scoring. However, these techniques alone cannot provide personalized explanations, contextual recommendations, or natural language guidance.

Large Language Models (LLMs) complement traditional software by transforming structured analysis into meaningful and user-friendly feedback.

---

### Research Findings

Hirely requires an LLM to perform tasks that involve understanding and generating natural language.

These tasks include:

- Explaining resume scores.
- Providing personalized improvement suggestions.
- Rewriting resume content professionally.
- Generating cover letters.
- Assisting with interview preparation.
- Offering AI-powered career guidance.

Traditional software components remain responsible for structured processing tasks such as parsing resumes, calculating scores, and performing ATS analysis.

---

### Analysis

The research indicates that LLMs provide the greatest value when combined with deterministic software systems.

Rule-based components ensure consistency and reliability, while LLMs improve the quality of user interaction by generating personalized, contextual, and professional responses.

This hybrid architecture balances software engineering principles with modern AI capabilities.

---

### Decision for Hirely

Hirely will adopt a hybrid AI architecture.

Traditional software modules will perform deterministic tasks such as parsing, scoring, and ATS analysis.

The LLM will consume the structured outputs generated by these modules and produce explanations, coaching, recommendations, and other natural language responses.

This architecture improves reliability, transparency, scalability, and maintainability.

---

### Key Takeaways

- LLMs complement traditional software rather than replacing it.
- Structured processing should occur before AI analysis.
- AI adds value through explanation, personalization, and content generation.
- Hirely will use a hybrid architecture that combines deterministic software with Large Language Models.

---

## 4.3 Where Should Hirely Use a Large Language Model?

### Background

Large Language Models provide the greatest value in tasks that require natural language understanding, reasoning, personalization, and content generation. Identifying appropriate use cases helps ensure that AI is applied where it delivers meaningful improvements while traditional software handles deterministic operations.

---

### Research Findings

The following Hirely features are appropriate use cases for Large Language Models:

- Resume score explanations.
- Personalized resume improvement suggestions.
- Professional summary generation.
- Cover letter generation.
- Resume content rewriting.
- Interview preparation assistance.
- Career guidance and coaching.
- Personalized learning recommendations.
- Conversational AI support.

These features require contextual understanding and natural language generation, making them well suited for LLMs.

---

### Analysis

LLMs are most effective when generating human-readable responses based on structured information produced by other software components.

Using LLMs for these tasks improves user experience while allowing deterministic modules to remain responsible for data extraction, validation, and scoring.

---

### Decision for Hirely

Hirely will use Large Language Models exclusively for language-intensive tasks that require explanation, personalization, or content generation.

Every AI response will be based on structured data generated by the platform's deterministic analysis modules rather than raw resume documents whenever possible.

---

### Key Takeaways

- LLMs should be used for natural language tasks.
- Personalized feedback is a primary AI capability.
- Structured analysis should occur before AI generation.
- Hirely will use AI to improve user interaction rather than replace software logic.

---

## 4.4 Where Should Hirely NOT Use a Large Language Model?

### Background

Although Large Language Models provide significant value for natural language understanding and generation, they are not suitable for every task within an application.

Using an LLM for deterministic or security-sensitive operations can introduce unnecessary cost, latency, unpredictability, and complexity.

Therefore, Hirely must clearly define which responsibilities should remain within traditional software components.

---

### Research Findings

Hirely should avoid using an LLM for tasks that can be performed reliably using deterministic software.

Examples include:

- PDF file validation.
- File size and file type validation.
- Basic text extraction from documents.
- Database operations.
- Authentication and authorization.
- Input validation.
- Basic resume section detection.
- ATS rule evaluation.
- Deterministic score calculation.
- Application business logic.
- Security-related operations.

These tasks can be implemented using conventional software components that provide predictable and testable behavior.

---

### Analysis

LLMs should not be treated as replacements for traditional application logic.

If a task has a clearly defined input, deterministic rules, and an expected output, traditional software is generally more appropriate.

Using an LLM for such tasks may increase cost and latency while making the system more difficult to test and debug.

LLMs should instead be reserved for tasks where language understanding, contextual reasoning, personalization, or content generation provides meaningful value.

---

### Decision for Hirely

Hirely will follow a clear separation between deterministic application logic and AI-powered functionality.

Traditional software components will remain responsible for validation, parsing, scoring, database operations, authentication, security, and core business logic.

Large Language Models will be used only when their natural language capabilities provide a significant advantage.

This separation will improve reliability, maintainability, testability, performance, and cost efficiency.

---

### Key Takeaways

- Not every application task requires AI.
- Deterministic tasks should generally use traditional software.
- Security-critical operations should not depend on an LLM.
- LLM usage should be limited to tasks where language intelligence provides meaningful value.
- Hirely will maintain a clear boundary between deterministic software and AI functionality.

---

## 4.5 Prompt Engineering Basics

### Background

Prompt engineering is the process of designing instructions and input context that guide a Large Language Model toward producing useful and consistent results.

Because Hirely will use LLMs for tasks such as resume feedback, content generation, and career guidance, carefully designed prompts will be necessary to control the behavior and quality of AI responses.

---

### Research Findings

A well-designed prompt can define several important components:

- Role or system behavior.
- Task or objective.
- Relevant context and input data.
- Rules and constraints.
- Expected output format.

For example, a resume analysis prompt may define the role of the AI reviewer, provide structured resume and job description data, specify evaluation criteria, and define the expected response format.

Clear instructions generally make AI responses easier to understand, evaluate, and integrate into software applications.

---

### Analysis

Prompt engineering should be treated as part of the software design rather than as an isolated experimentation process.

Hirely will require prompts that are:

- Clear
- Specific
- Consistent
- Context-aware
- Testable
- Appropriate for the intended task

Prompts should also include appropriate constraints to reduce unsupported or fabricated information.

---

### Decision for Hirely

Hirely will maintain dedicated prompts for different AI-powered features rather than relying on one general-purpose prompt.

Prompts will clearly define the task, provide relevant structured context, establish appropriate constraints, and specify the expected response format.

Prompt versions will be maintained as part of the project's development process so that changes can be tested and evaluated systematically.

---

### Key Takeaways

- Prompt engineering helps guide LLM behavior.
- Good prompts provide clear instructions and relevant context.
- Constraints help reduce undesirable or unsupported responses.
- Different Hirely features will use task-specific prompts.
- Prompts will be treated as maintainable project components.

---

## 4.6 LLM Limitations

### Background

Large Language Models provide powerful natural language capabilities, but they also have limitations that must be considered when designing production AI systems.

Understanding these limitations is important for Hirely because the platform will use LLMs to generate resume feedback, recommendations, and other career-related content.

---

### Research Findings

Important limitations of Large Language Models include:

- Potential generation of incorrect or unsupported information.
- Probabilistic and non-deterministic behavior.
- Difficulty interpreting ambiguous or poorly structured context.
- Context size limitations.
- Sensitivity to prompt quality.
- Potentially inconsistent output formatting.
- API cost and response latency.
- Dependence on the quality and relevance of the provided context.

These limitations mean that LLM outputs should not automatically be treated as authoritative or completely reliable.

---

### Analysis

LLMs should be treated as probabilistic components rather than deterministic sources of truth.

The reliability of an AI-powered system depends not only on the model but also on input validation, prompt design, context construction, output validation, and the surrounding application architecture.

For Hirely, deterministic components should continue to control important application logic, while LLM-generated content should be validated before being presented to users when appropriate.

---

### Decision for Hirely

Hirely will design its AI layer with the limitations of LLMs in mind.

The system will:

- Validate inputs before sending them to an LLM.
- Provide structured and relevant context.
- Use task-specific prompts.
- Validate structured AI outputs where applicable.
- Avoid depending on LLMs for deterministic business logic.
- Minimize unnecessary LLM requests to control cost and latency.
- Clearly separate AI-generated recommendations from verified user information.

---

### Key Takeaways

- LLMs are powerful but not perfectly reliable.
- AI-generated information may require validation.
- Prompt quality and context strongly influence output quality.
- LLMs should not control critical deterministic business logic.
- Hirely will use architectural safeguards around its AI components.

---

## 4.7 LLM Hallucinations

### Background

LLM hallucination refers to situations where a Large Language Model generates information that is incorrect, unsupported by the provided context, or fabricated while presenting it as a valid response.

Hallucinations are an important concern for Hirely because the platform will analyze personal career information and generate recommendations based on user-provided resumes.

---

### Research Findings

Hallucinations may occur when an LLM:

- Generates skills that are not present in a resume.
- Invents work experience.
- Creates unsupported achievements.
- Assumes certifications that were not provided.
- Misinterprets incomplete or ambiguous information.
- Produces information that is not supported by the provided context.

For a career platform, fabricated candidate information can lead to misleading recommendations and reduce user trust.

---

### Analysis

LLMs should not be treated as the source of truth for candidate information.

Hirely should provide the LLM with structured and verified information whenever possible. Deterministic analysis should identify facts such as detected skills, resume sections, job-description keywords, and calculated scores before the LLM is asked to explain or transform that information.

The system should clearly distinguish between verified candidate information and AI-generated suggestions.

---

### Mitigation Strategies

Hirely will reduce hallucination risk through multiple safeguards:

- Provide relevant and structured context to the LLM.
- Explicitly instruct the model not to invent candidate information.
- Perform deterministic analysis wherever possible.
- Separate verified facts from AI-generated recommendations.
- Validate structured LLM outputs where applicable.
- Avoid using LLM-generated information as the authoritative source for candidate data.

---

### Decision for Hirely

Hirely will treat hallucination prevention as an important AI engineering requirement.

The LLM will be used primarily to explain verified analysis results, generate recommendations, and transform existing information into useful content.

The system will not allow the LLM to independently create or modify authoritative candidate facts.

---

### Key Takeaways

- LLMs can generate unsupported or fabricated information.
- Hallucinations can damage trust in career-related applications.
- Verified application data should remain the source of truth.
- Deterministic analysis should be preferred when possible.
- Hirely will implement multiple safeguards to reduce hallucination risk.

---

## 4.8 Context Window

### Background

A context window represents the amount of information that a Large Language Model can process as part of a single interaction. The context may include system instructions, user input, documents, previous messages, and other information provided to the model.

Understanding context windows is important for Hirely because resume analysis may involve multiple sources of information, including resumes, job descriptions, analysis results, and user instructions.

---

### Research Findings

The context provided to an LLM may include:

- System instructions.
- User instructions.
- Resume content.
- Job description content.
- Structured analysis results.
- Relevant conversation context.

The available context is finite and should therefore be managed carefully.

Large or unnecessary inputs can increase token usage, cost, and latency while making it more difficult to focus the model on the information relevant to the current task.

---

### Analysis

Hirely should avoid sending unnecessary information to the LLM.

Instead, the system should first process and structure the available information and then provide the LLM with the relevant context required for the specific task.

For example, when generating resume improvement feedback, the system may provide detected weaknesses, matched skills, missing job-description keywords, and relevant resume content instead of repeatedly sending unrelated application data.

---

### Decision for Hirely

Hirely will use a context management strategy in which relevant information is selected and structured before being sent to the LLM.

The system will minimize unnecessary context while ensuring that the model receives sufficient information to perform the requested task accurately.

This approach will help control token usage, reduce unnecessary costs and latency, and improve the relevance of AI-generated responses.

---

### Key Takeaways

- LLM context is finite.
- More context does not automatically produce better results.
- Relevant information should be prioritized.
- Hirely will prepare and structure context before sending it to an LLM.
- Context management will help improve efficiency, cost, and response quality.

---

## 4.9 Structured Output

### Background

LLMs normally generate natural language responses, but production applications often require predictable and machine-readable data.

Structured output allows an LLM response to follow a predefined format, such as JSON with specific fields. This makes AI responses easier for application code to consume, validate, and process.

For Hirely, structured output is important because AI-generated results will eventually be consumed by the FastAPI backend and frontend components.

---

### Research Findings

An unstructured LLM response may contain useful information but can be difficult for software to process reliably.

For example, an LLM may return a natural language response containing:

- Resume score
- Strengths
- Weaknesses
- Missing skills
- Recommendations

A structured response can represent the same information using predefined fields.

Example:

```json
{
  "score": 78,
  "strengths": [
    "Strong Python experience"
  ],
  "weaknesses": [
    "Project descriptions lack measurable achievements"
  ],
  "recommendations": [
    "Add measurable outcomes to project descriptions"
  ]
}
```

Structured responses make the boundary between the AI layer and application layer more predictable.

---

### Analysis

Structured output improves the reliability and maintainability of AI-powered applications because application code can work with defined fields rather than attempting to interpret arbitrary natural language.

However, structured output does not guarantee that the information itself is correct. A response can follow the required format while still containing incorrect or unsupported information.

Therefore, structured output should be combined with validation and appropriate application-level rules.

---

### Decision for Hirely

Hirely will prefer structured outputs for LLM tasks where the response needs to be consumed by application code.

AI responses will use predefined schemas whenever appropriate, allowing the FastAPI backend to validate and process the results consistently.

Natural language responses will still be used when a task is intended primarily for direct user interaction and does not require machine-readable data.

---

### Key Takeaways

- LLM responses should be structured when application code needs to consume them.
- Structured output improves predictability and maintainability.
- JSON can provide a machine-readable representation of AI results.
- Structured output does not eliminate hallucinations or incorrect information.
- Hirely will combine structured output with validation.

---

## 4.10 Final Decision for Hirely

### Summary

The research conducted on Large Language Models establishes that LLMs are powerful components for natural language understanding, generation, explanation, and personalization. However, they should not replace deterministic software or become the source of truth for application data.

Hirely will therefore use a hybrid architecture that combines traditional software engineering with Large Language Models.

---

### Final Architecture Decision

Hirely will separate responsibilities between deterministic application components and AI-powered components.

#### Traditional Software Components

Traditional software will remain responsible for:

- File validation.
- Text extraction.
- Resume parsing.
- Data validation.
- ATS analysis.
- Deterministic scoring.
- Database operations.
- Authentication and authorization.
- Security.
- Core application business logic.

#### AI Components

Large Language Models will be responsible for tasks such as:

- Explaining resume analysis results.
- Generating personalized recommendations.
- Rewriting resume content.
- Generating professional summaries.
- Creating cover letters.
- Supporting interview preparation.
- Providing career guidance.
- Generating natural language responses.

---

### AI Reliability Principles

Hirely will follow the following principles when integrating LLMs:

1. **Use AI where it provides meaningful value.**
2. **Prefer deterministic software for deterministic problems.**
3. **Do not treat LLM output as the source of truth for candidate information.**
4. **Provide relevant and structured context to the LLM.**
5. **Use task-specific prompts.**
6. **Prevent the model from inventing candidate facts.**
7. **Prefer structured output when application code needs to consume AI responses.**
8. **Validate AI-generated output where appropriate.**
9. **Minimize unnecessary LLM calls to control cost and latency.**
10. **Keep AI functionality modular and replaceable.**

---

### Final Processing Model

The overall AI processing approach for Hirely will follow this general pattern:

```text
User Input
    ↓
Input Validation
    ↓
Document / Data Processing
    ↓
Structured Information
    ↓
Deterministic Analysis
    ↓
Verified Analysis Results
    ↓
Relevant Context Preparation
    ↓
Task-Specific LLM Prompt
    ↓
LLM
    ↓
Structured / Natural Language Output
    ↓
Output Validation
    ↓
User-Facing Response
```

---

### Decision for Hirely

Large Language Models will be treated as one modular component within the Hirely platform rather than as the entire application intelligence.

The system architecture will combine deterministic software with LLM capabilities to achieve a balance between reliability, explainability, personalization, maintainability, performance, and cost efficiency.

The AI layer should remain modular so that the underlying LLM provider or model can be changed in the future without requiring major changes to the rest of the application.

---

### Key Takeaways

- Hirely will use a hybrid AI architecture.
- Traditional software will handle deterministic and security-sensitive operations.
- LLMs will handle language-intensive and personalized tasks.
- Verified application data will remain the source of truth.
- AI outputs will be controlled through context, prompts, structured output, and validation.
- The LLM layer will remain modular and replaceable.

# 5. Document Processing

## 5.1 Why Does Hirely Need Document Processing?

### Background

Hirely will receive resumes as user-uploaded documents rather than as pre-structured application data.

Before resume analysis, ATS evaluation, scoring, or AI-powered feedback can be performed, the system must first extract usable information from the uploaded document.

Document processing therefore forms an important part of the pipeline between the user's uploaded resume and Hirely's analysis components.

---

### Research Findings

A typical Hirely resume-processing flow will require the following stages:

```text
Uploaded Resume
       ↓
Document Processing
       ↓
Extracted Text
       ↓
Resume Parsing
       ↓
Structured Resume Data
       ↓
Analysis
```

Document processing is responsible for converting supported document formats into usable content that can be processed by subsequent application components.

---

### Document Processing vs Resume Parsing

Document processing and resume parsing are related but different responsibilities.

**Document Processing** focuses on extracting usable content from a document.

**Resume Parsing** focuses on understanding that content and identifying resume-specific information such as:

- Name
- Contact information
- Skills
- Education
- Work experience
- Projects
- Certifications
- Achievements

Therefore, document processing should occur before resume parsing.

---

### Analysis

Hirely should separate document processing from resume parsing so that each component has a clear responsibility.

This separation will make the system easier to develop, test, maintain, and extend to additional document formats in the future.

---

### Decision for Hirely

Hirely will introduce a dedicated document processing layer responsible for accepting supported resume files and extracting usable content.

The extracted content will then be passed to a separate resume parsing component responsible for converting the content into structured resume information.

This separation will establish a modular processing pipeline and prevent document-specific logic from being tightly coupled with resume analysis and scoring.

---

### Key Takeaways

- Hirely will receive resumes as uploaded documents.
- Documents must be processed before resume analysis.
- Document processing extracts usable content.
- Resume parsing converts extracted content into structured resume information.
- These responsibilities will remain separate and modular.

---

### Hirely Principle

> **Document processing extracts content; resume parsing understands the content.**

## 5.2 Supported Resume Formats

### Background

Hirely needs to define which document formats will be accepted during resume upload.

Supporting a controlled set of formats in the initial version will reduce implementation complexity and allow the document-processing pipeline to be developed and tested systematically.

---

### Initial Supported Formats

For the initial version of Hirely, the following resume formats will be supported:

- PDF
- DOCX

These formats provide a practical starting point for the first version of the resume-processing system.

---

### Future Format Support

Additional formats may be considered in future versions, including:

- TXT
- RTF
- ODT
- Image-based documents

These formats will not be part of the initial document-processing scope unless later requirements justify their inclusion.

---

### Important Consideration

A file extension alone does not determine how easily a document can be processed.

For example, a PDF may contain:

1. Machine-readable text.
2. Scanned images containing text.

A text-based PDF can generally be processed using text-extraction techniques, while an image-based or scanned PDF may require Optical Character Recognition (OCR).

Therefore, Hirely must distinguish between document format and document content when designing the processing pipeline.

---

### Analysis

Limiting the initial supported formats allows Hirely to focus on building a reliable processing pipeline before expanding format support.

The architecture should remain modular so that additional document processors can be introduced later without significantly changing the rest of the application.

---

### Decision for Hirely

Hirely Version 1 will support:

```text
PDF
DOCX
```

The document-processing architecture will use separate processing logic for different formats where necessary.

Support for additional formats will be considered in future versions based on user requirements and system needs.

---

### Key Takeaways

- Hirely V1 will support PDF and DOCX resumes.
- Additional formats will be considered later.
- File extension and document content are different concerns.
- Scanned PDFs may require OCR.
- Document processors should remain modular and extensible.

---

### Hirely Principle

> **Start with a controlled set of formats, build a reliable processing pipeline, and expand format support when the architecture and requirements justify it.**

## 5.3 Text Extraction

### Background

Text extraction is the process of retrieving usable textual content from an uploaded document.

For Hirely, text extraction is an important step because downstream components such as resume parsing, ATS analysis, scoring, and AI processing require accessible text rather than the original document file alone.

---

### Research Findings

The general document-processing flow can be represented as:

```text
Resume File
     ↓
Document Processor
     ↓
Text Extraction
     ↓
Extracted Text
     ↓
Resume Parser
     ↓
Structured Resume Data
```

The text extraction layer converts the contents of a supported document into text that can be processed by subsequent components.

---

### Text Extraction vs Resume Parsing

Text extraction and resume parsing have different responsibilities.

**Text Extraction**

The purpose is to retrieve textual content from the document.

Example:

```text
Python
FastAPI
SQL
Bachelor of Computer Science
Software Developer
```

**Resume Parsing**

The purpose is to interpret the extracted content and identify structured resume information.

For example:

```text
Skills:
- Python
- FastAPI
- SQL

Education:
- Bachelor of Computer Science

Experience:
- Software Developer
```

Therefore:

```text
Text Extraction = Get the content
Resume Parsing = Understand the content
```

---

### Analysis

Text extraction should remain a separate component from resume parsing.

This separation allows Hirely to support different document formats while keeping the resume-understanding logic independent from format-specific processing.

It also makes the system easier to test because extraction accuracy and parsing accuracy can be evaluated separately.

---

### Important Consideration

Not every document contains directly accessible text.

A document may contain:

- Machine-readable text.
- Images containing text.
- A mixture of text and images.

When text is not directly available, additional processing such as OCR may be required.

OCR and scanned-document handling will be studied separately in later sections.

---

### Decision for Hirely

Hirely will include a dedicated text-extraction stage between document processing and resume parsing.

The extraction layer will convert supported documents into usable text while remaining independent from the resume parsing and analysis components.

The architecture will also allow additional processing techniques to be introduced for documents where normal text extraction is insufficient.

---

### Key Takeaways

- Text extraction converts document content into usable text.
- Text extraction does not determine the meaning of the extracted information.
- Resume parsing is responsible for understanding the extracted content.
- Extraction and parsing will remain separate modules in Hirely.
- Documents without directly accessible text may require additional processing such as OCR.

---

### Hirely Principle

> **Extract first, understand second.**

## 5.4 PDF Processing

### Background

PDF is one of the primary document formats supported by Hirely Version 1.

PDF processing is responsible for handling uploaded PDF resumes and making their contents available to the text-extraction stage.

However, PDF documents can contain different types of content and layouts, so the processing strategy must account for both text-based and image-based PDFs.

---

### Types of PDF Documents

PDF resumes can generally be divided into two important categories.

#### 1. Text-Based PDF

A text-based PDF contains an accessible text layer.

The processing flow can be:

```text
PDF
 ↓
PDF Processing
 ↓
Text Extraction
 ↓
Extracted Text
 ↓
Resume Parsing
```

This type of PDF can usually be processed using text-extraction techniques.

#### 2. Image-Based / Scanned PDF

A scanned PDF may contain pages represented primarily as images rather than accessible text.

The processing flow may therefore become:

```text
PDF
 ↓
PDF Processing
 ↓
Image Content
 ↓
OCR
 ↓
Extracted Text
 ↓
Resume Parsing
```

OCR and scanned-document handling will be studied in later sections.

---

### PDF Layout Challenges

Resume PDFs may contain complex layouts, including:

- Multiple columns.
- Tables.
- Headers and footers.
- Bullet points.
- Different font sizes.
- Links.
- Images.
- Text positioned in different areas of a page.

Extracting text from such documents does not always guarantee that the original visual reading order will be preserved.

This can affect downstream resume parsing.

For example, content displayed in two columns may be extracted in an order that differs from the way a human reads the resume.

---

### Analysis

Hirely should treat PDF processing as more than simply extracting raw text.

The processing layer should attempt to produce usable and logically ordered content while preserving relevant information from the original document.

The PDF-processing component should remain separate from resume parsing so that document-format-specific logic does not become tightly coupled with resume-understanding logic.

---

### Decision for Hirely

Hirely will support PDF resumes in Version 1.

The PDF-processing layer will:

- Accept supported PDF files.
- Determine whether usable text is available.
- Extract text from text-based PDFs.
- Identify cases where normal text extraction is insufficient.
- Allow image-based or scanned PDFs to be processed through an OCR pipeline when supported.
- Pass extracted content to the resume-parsing layer.

PDF processing will remain modular so that extraction techniques can be improved or replaced without changing the rest of the resume-analysis pipeline.

---

### Processing Model

The general PDF processing flow will be:

```text
                PDF Resume
                    ↓
              PDF Processing
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
    Text Available       No Usable Text
          ↓                   ↓
   Text Extraction          OCR
          ↓                   ↓
          └─────────┬─────────┘
                    ↓
             Extracted Text
                    ↓
             Resume Parser
                    ↓
          Structured Resume Data
```

---

### Key Takeaways

- PDF is a primary supported format for Hirely V1.
- PDFs may contain machine-readable text or image-based content.
- Text-based PDFs can use normal text extraction.
- Scanned or image-based PDFs may require OCR.
- PDF layout can affect extraction order and downstream parsing.
- PDF processing will remain separate from resume parsing.

---

### Hirely Principle

> **PDF processing must focus on extracting usable and logically ordered content, not simply extracting any available text.**

## 5.5 DOCX Processing

### Background

DOCX is one of the primary resume formats supported by Hirely Version 1.

DOCX processing is responsible for accepting an uploaded DOCX resume and extracting usable document content for subsequent resume parsing and analysis.

DOCX documents contain structured document elements such as paragraphs, headings, lists, tables, and other content that may be relevant to a resume.

---

### DOCX Processing Flow

The general processing flow will be:

```text
DOCX Resume
     ↓
DOCX Processing
     ↓
Extracted Document Content
     ↓
Resume Parser
     ↓
Structured Resume Data
     ↓
Analysis
```

The DOCX processing layer should focus on retrieving the content of the document rather than determining what each piece of content means.

---

### Important DOCX Elements

A resume stored as a DOCX document may contain:

- Paragraphs.
- Headings.
- Bullet lists.
- Numbered lists.
- Tables.
- Headers and footers.
- Hyperlinks.
- Text formatting.
- Other document metadata.

Some of these elements may contain information that is important for resume processing.

For example, skills may appear inside a bullet list or table rather than a normal paragraph.

---

### DOCX Processing vs Resume Parsing

DOCX processing and resume parsing will have separate responsibilities.

**DOCX Processing**

The purpose is to extract usable content and relevant document elements from the DOCX file.

**Resume Parsing**

The purpose is to interpret that extracted content and identify resume-specific information such as:

- Personal information.
- Skills.
- Education.
- Work experience.
- Projects.
- Certifications.
- Achievements.

Therefore:

```text
DOCX Processing = Extract document content
Resume Parsing  = Understand resume content
```

---

### Analysis

Hirely should keep DOCX-specific processing separate from the resume parser.

This allows the resume parser to work with normalized extracted content instead of being tightly coupled to the internal structure of a particular document format.

The approach also makes the architecture easier to extend if additional document formats are supported in the future.

---

### Important Considerations

DOCX resumes may use different layouts and formatting styles.

For example:

- Important information may appear inside tables.
- Skills may be represented using bullet lists.
- Contact information may appear in a header.
- Sections may be identified using headings.
- Hyperlinks may contain useful information such as portfolio or LinkedIn URLs.

Therefore, DOCX processing should extract relevant document elements rather than relying only on plain paragraph text.

---

### Decision for Hirely

Hirely will support DOCX resumes in Version 1.

The DOCX-processing component will:

- Accept supported DOCX files.
- Extract relevant textual content.
- Process important document elements such as paragraphs, headings, lists, and tables where required.
- Preserve useful structural information where possible.
- Pass normalized content to the resume-parsing layer.
- Remain independent from resume interpretation and analysis.

---

### Processing Model

The DOCX processing pipeline will follow this general model:

```text
                 DOCX Resume
                      ↓
                DOCX Processor
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
    Text Elements          Structural Elements
          ↓                       ↓
          └───────────┬───────────┘
                      ↓
             Normalized Content
                      ↓
               Resume Parser
                      ↓
          Structured Resume Data
```

---

### Key Takeaways

- DOCX is a primary supported format for Hirely V1.
- DOCX processing extracts document content.
- Paragraphs, headings, lists, and tables may contain important resume information.
- DOCX processing should preserve useful structure where possible.
- Resume parsing remains responsible for understanding the extracted content.
- DOCX processing and resume parsing will remain separate modules.

---

### Hirely Principle

> **Extract and normalize document content first; interpret the resume structure separately.**

## 5.6 Handling Scanned / Image-Based Resumes

### Background

Not every resume contains machine-readable text.

A supported PDF may contain scanned images of resume pages rather than an accessible text layer. In this situation, normal text extraction may return little or no usable text even though the resume is visually readable to a human.

Hirely therefore needs to distinguish between a document that contains no meaningful content and a document whose content is present as images.

---

### Problem

A scanned resume may follow this structure:

```text
Scanned Resume
      ↓
PDF
      ↓
Image-Based Pages
      ↓
No Accessible Text Layer
      ↓
Normal Text Extraction
      ↓
Little or No Text
```

If Hirely only relies on normal text extraction, such resumes may incorrectly appear to contain no usable content.

---

### Required Processing Flow

When normal text extraction is insufficient, Hirely should be able to route the document through an OCR-based processing path.

The general flow will be:

```text
Uploaded Resume
      ↓
Document Processing
      ↓
Text Extraction
      ↓
Usable Text Available?
      │
      ├── Yes
      │    ↓
      │  Resume Parser
      │
      └── No / Insufficient
           ↓
          OCR
           ↓
     Extracted Text
           ↓
      Resume Parser
```

This allows Hirely to handle both text-based and image-based resumes.

---

### Important Considerations

OCR-based processing may be affected by:

- Image quality.
- Resolution.
- Font style.
- Document layout.
- Multiple columns.
- Tables.
- Background elements.
- Rotated text.
- Poorly scanned pages.
- Handwritten content.

Therefore, OCR output should not automatically be treated as perfectly accurate.

The extracted content may require validation or additional processing before being passed to the resume parser.

---

### Analysis

A scanned resume should not automatically be classified as an unsupported resume simply because normal text extraction fails.

Instead, Hirely should attempt to determine whether the document contains image-based content and, when appropriate, route it through an OCR pipeline.

This approach improves compatibility with real-world resumes while keeping OCR processing separate from normal text extraction.

---

### Decision for Hirely

Hirely will support a processing path for scanned and image-based resumes.

When a supported document does not provide sufficient machine-readable text, the document-processing pipeline may route its visual content to an OCR component.

The OCR component will produce extracted text that can then be passed to the resume-parsing layer.

OCR accuracy and failure cases will be evaluated separately before final implementation.

---

### Key Takeaways

- Supported resumes may contain image-based content.
- A scanned PDF may not have an accessible text layer.
- Failure of normal text extraction does not necessarily mean the resume is empty.
- Hirely will provide an OCR-based path for image-based documents.
- OCR output may contain errors and should be validated where appropriate.
- OCR will remain separate from normal text extraction and resume parsing.

---

### Hirely Principle

> **If text is unavailable but visual content exists, attempt appropriate OCR processing before declaring the document unreadable.**

## 5.7 Optical Character Recognition (OCR)

### Background

Optical Character Recognition (OCR) is a technology used to recognize text contained within images and convert that visual text into machine-readable text.

OCR is important for Hirely because some resumes may be scanned documents or image-based PDFs that do not contain an accessible text layer.

---

### OCR Processing Flow

The general OCR process can be represented as:

```text
Image / Scanned Document
          ↓
         OCR
          ↓
Recognized Machine-Readable Text
          ↓
    Resume Parser
          ↓
Structured Resume Data
```

For a scanned PDF, the complete processing flow may be:

```text
Scanned PDF
     ↓
PDF Processing
     ↓
Page Images
     ↓
OCR
     ↓
Extracted Text
     ↓
Resume Parser
     ↓
Structured Resume Data
```

---

### What OCR Does

OCR primarily performs text recognition.

For example, an image containing:

```text
John Doe

Skills:
Python
SQL
FastAPI
```

may produce machine-readable text such as:

```text
John Doe

Skills:
Python
SQL
FastAPI
```

The extracted text can then be passed to the resume parser.

---

### OCR vs Resume Parsing

OCR and resume parsing have different responsibilities.

**OCR**

The purpose is to recognize text from visual content.

**Resume Parsing**

The purpose is to understand the extracted text and identify resume-specific information.

For example:

```text
OCR:
"Skills: Python, SQL, FastAPI"

        ↓

Resume Parser:

Skills:
- Python
- SQL
- FastAPI
```

Therefore:

```text
OCR = Recognize text
Resume Parsing = Understand resume information
```

---

### OCR Limitations

OCR is not guaranteed to produce perfectly accurate text.

Accuracy can be affected by:

- Image resolution.
- Image quality.
- Font style.
- Text size.
- Document layout.
- Multiple columns.
- Tables.
- Background elements.
- Rotated text.
- Blurred or distorted content.
- Poor scanning quality.

OCR may therefore introduce errors such as incorrect characters, missing text, or incorrect spacing.

---

### Analysis

OCR should be treated as an additional extraction layer rather than as a complete resume-understanding solution.

Hirely should use OCR only when normal text extraction is insufficient or when the document contains image-based text.

The resulting OCR text should then enter the same downstream resume-parsing pipeline used for other extracted text.

This keeps the architecture consistent:

```text
Text-Based Document
        ↓
Normal Text Extraction
        ↓
        ┐
        │
        ↓
Extracted Text
        ↑
        │
OCR ────┘
        ↓
Resume Parser
        ↓
Structured Resume Data
```

---

### Validation Consideration

Because OCR can introduce recognition errors, Hirely should consider validating extracted content before relying on it for downstream analysis.

For example, the system may check whether:

- Meaningful text was extracted.
- The extracted content is sufficiently large.
- Common resume sections can be detected.
- The document contains mostly readable characters.
- The extraction result is not empty or corrupted.

These checks can help determine whether the OCR result is usable.

---

### Decision for Hirely

Hirely will use OCR as a fallback processing mechanism for scanned and image-based resumes when normal text extraction cannot provide sufficient content.

OCR will remain separate from:

- Document processing.
- Normal text extraction.
- Resume parsing.
- Resume analysis.

The OCR output will be passed into the common resume-processing pipeline and may be validated before further analysis.

---

### Processing Model

The overall document-processing strategy will be:

```text
                    Resume
                       ↓
              Document Processing
                       ↓
              Is usable text available?
                 /             \
               Yes              No
                ↓                ↓
        Normal Extraction       OCR
                ↓                ↓
                └───────┬────────┘
                        ↓
                 Extracted Text
                        ↓
                  Resume Parser
                        ↓
              Structured Resume Data
                        ↓
                    Analysis
```

---

### Key Takeaways

- OCR converts text inside images into machine-readable text.
- OCR is useful for scanned and image-based resumes.
- OCR does not understand resume semantics.
- Resume parsing remains responsible for understanding extracted content.
- OCR output may contain recognition errors.
- Hirely will use OCR as a fallback when normal text extraction is insufficient.
- OCR output should be validated where appropriate.

---

### Hirely Principle

> **OCR recognizes visual text; the resume parser understands what that text means.**

## 5.8 Document Processing Challenges

### Background

Real-world resumes are created using many different tools, layouts, templates, and document-generation methods.

As a result, extracting reliable content from resumes is not always straightforward.

Hirely's document-processing pipeline must be designed to handle common document-processing problems while keeping the system modular and maintainable.

---

### 1. Complex Resume Layouts

Resumes may contain complex visual layouts such as:

- Multiple columns.
- Sidebars.
- Tables.
- Text boxes.
- Headers and footers.
- Icons.
- Different font sizes.
- Images.
- Sections positioned in different areas of a page.

These layouts can affect the order and quality of extracted text.

---

### 2. Multi-Column Resumes

A resume may visually present information in multiple columns.

For example:

```text
Experience              Skills
-----------             ------
Company A               Python
Company B               SQL
Company C               Docker
```

A text-extraction system may not always return the content in the same order that a human visually reads it.

Incorrect reading order can negatively affect downstream resume parsing.

---

### 3. Tables

Tables may be used for:

- Skills.
- Education.
- Work experience.
- Contact information.
- Project information.

Text extraction may preserve the text but lose the original relationships between rows and columns.

Therefore, table-based content may require additional processing.

---

### 4. Scanned and Image-Based Documents

Some resumes may contain scanned pages or images instead of machine-readable text.

In these cases:

```text
Document
   ↓
No Usable Text
   ↓
OCR
   ↓
Extracted Text
```

OCR can introduce recognition errors and therefore should not automatically be treated as perfectly accurate.

---

### 5. OCR Errors

OCR may produce:

- Incorrect characters.
- Missing characters.
- Incorrect spacing.
- Incorrect words.
- Broken lines.
- Incorrect recognition of symbols.

These errors can affect resume parsing and later analysis.

---

### 6. Poor Document Quality

Low-quality documents can make extraction more difficult.

Examples include:

- Low-resolution scans.
- Blurred pages.
- Skewed pages.
- Rotated pages.
- Very small text.
- Poor contrast.
- Damaged documents.

Hirely should detect cases where extracted content is insufficient for reliable processing.

---

### 7. Missing or Insufficient Text

A document may technically be valid but still provide little usable text.

For example:

```text
Uploaded PDF
     ↓
Text Extraction
     ↓
Almost no text
     ↓
Possible scanned/image-based document
```

The system should distinguish between:

- Empty or invalid documents.
- Documents containing insufficient extractable text.
- Image-based documents requiring OCR.

---

### 8. Corrupted or Invalid Files

Uploaded files may be:

- Corrupted.
- Incomplete.
- Invalid despite having a valid file extension.
- Password-protected.
- Unsupported internally.

Hirely should validate files before attempting document processing.

---

### 9. Large Documents

Although resumes are normally relatively small, the system should still protect itself against unusually large files.

Large documents can increase:

- Processing time.
- Memory usage.
- Storage requirements.
- OCR processing cost.
- API or downstream processing cost.

File-size limits should therefore be considered during implementation.

---

### 10. Privacy and Sensitive Information

Resumes may contain personal and professional information such as:

- Names.
- Email addresses.
- Phone numbers.
- Addresses.
- Employment history.
- Education history.
- Professional profiles.

Document processing therefore needs to be designed with privacy and secure data handling in mind.

Sensitive resume information should not be unnecessarily exposed to external services.

---

### 11. Format-Specific Differences

PDF and DOCX are different document formats and may require different extraction techniques.

The architecture should therefore avoid assuming that one processing method will work equally well for every format.

Instead:

```text
             Uploaded Resume
                    ↓
            Document Detection
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
         PDF                 DOCX
          ↓                   ↓
    PDF Processor       DOCX Processor
          ↓                   ↓
          └─────────┬─────────┘
                    ↓
             Normalized Content
```

This allows format-specific processing while maintaining a common downstream pipeline.

---

### Analysis

Document processing should be treated as a potentially unreliable input stage.

The system cannot assume that every uploaded resume will produce perfect extracted text.

Hirely should therefore introduce validation and error-handling mechanisms before passing extracted content to the resume parser.

The document-processing layer should also remain modular so that individual extraction strategies can be improved without changing the rest of the system.

---

### Challenges Hirely Must Address

The initial implementation should consider the following challenges:

- Complex document layouts.
- Multi-column reading order.
- Tables and structured content.
- Scanned documents.
- OCR accuracy.
- Poor-quality documents.
- Insufficient extracted text.
- Corrupted or invalid files.
- Large file sizes.
- Sensitive resume information.
- Differences between document formats.

---

### Decision for Hirely

Hirely will treat document processing as a validation and extraction layer rather than assuming that uploaded documents are always clean and machine-readable.

The system will:

- Validate uploaded files.
- Use format-specific processing where required.
- Detect insufficient extraction results.
- Support an OCR fallback for appropriate image-based documents.
- Validate extracted content before resume parsing.
- Handle processing failures gracefully.
- Keep document-processing components modular.
- Consider privacy and secure handling of resume data.

---

### Key Takeaways

- Real-world resumes can have complex layouts.
- Text extraction does not always preserve visual structure.
- Tables and multi-column layouts can create parsing challenges.
- Scanned documents may require OCR.
- OCR output may contain errors.
- Invalid, corrupted, or unusually large files must be handled safely.
- Resume data can contain sensitive personal information.
- Document processing should validate and normalize content before resume parsing.
- Format-specific processors should remain modular.

---

### Hirely Principle

> **Never assume that an uploaded document is clean, simple, or perfectly machine-readable; validate, process, and normalize it before analysis.**

## 5.9 Final Decision for Hirely

### Summary

The research conducted on document processing establishes that Hirely needs a dedicated document-processing layer between uploaded resumes and the resume-parsing system.

The document-processing layer will be responsible for accepting supported files, validating them, extracting usable content, handling image-based documents when appropriate, and providing normalized content to the resume parser.

---

### Supported Formats

Hirely Version 1 will initially support:

- PDF
- DOCX

Additional formats may be considered in future versions based on user requirements.

---

### Final Processing Architecture

The document-processing pipeline will follow this general model:

```text
                    Uploaded Resume
                           ↓
                   File Validation
                           ↓
                 Document Detection
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
             PDF                       DOCX
              ↓                         ↓
       PDF Processing             DOCX Processing
              ↓                         ↓
              └────────────┬────────────┘
                           ↓
                  Text Extraction
                           ↓
                Is sufficient text?
                     /          \
                   Yes           No
                    ↓             ↓
                    │            OCR
                    │             ↓
                    └──────┬──────┘
                           ↓
                  Extracted Content
                           ↓
                  Content Validation
                           ↓
                    Resume Parser
                           ↓
              Structured Resume Data
                           ↓
                     Analysis
```

---

### Responsibilities of the Document Processing Layer

The document-processing layer will be responsible for:

- Validating uploaded files.
- Identifying supported document formats.
- Processing PDF documents.
- Processing DOCX documents.
- Extracting machine-readable text.
- Detecting insufficient text extraction.
- Routing appropriate image-based documents to OCR.
- Validating extracted content.
- Normalizing extracted content.
- Handling processing failures safely.

---

### Responsibilities Outside the Document Processing Layer

The document-processing layer will not be responsible for understanding the meaning of resume information.

The following responsibilities belong to later components:

- Resume section identification.
- Skill extraction.
- Experience extraction.
- Education extraction.
- Resume classification.
- ATS analysis.
- Resume scoring.
- AI-generated feedback.

This separation keeps document extraction independent from resume understanding and analysis.

---

### Reliability Strategy

Hirely will not assume that every uploaded resume will produce perfect extracted text.

The system will use validation and fallback mechanisms to identify situations such as:

- Empty documents.
- Insufficient extracted text.
- Image-based documents.
- OCR failures.
- Corrupted files.
- Unsupported files.
- Poor-quality document content.

Processing failures should be handled gracefully and should not cause the entire application to fail unexpectedly.

---

### Privacy Consideration

Resume documents may contain sensitive personal and professional information.

Hirely will therefore consider secure handling of uploaded documents and extracted content throughout the processing pipeline.

Document data should only be exposed to components and external services when required for the intended processing task.

---

### Modularity Decision

Document processing will be designed as a modular layer.

Format-specific processing components should remain separated so that extraction techniques can be improved or additional formats can be added later without requiring major changes to the resume parser or analysis components.

The general architecture will therefore follow:

```text
Document Format
      ↓
Format-Specific Processor
      ↓
Normalized Content
      ↓
Resume Parser
      ↓
Structured Resume
```

---

### Final Decision for Hirely

Hirely will implement a modular document-processing layer that supports PDF and DOCX resumes in Version 1.

The layer will validate uploaded documents, perform format-specific processing, extract usable text, use OCR when appropriate, validate extracted content, and provide normalized content to the resume parser.

Document processing will remain separate from resume parsing, ATS analysis, scoring, and AI functionality.

This architecture will provide a reliable foundation for the later resume-analysis pipeline while allowing Hirely to expand document support and processing capabilities in future versions.

---

### Key Takeaways

- Hirely V1 will support PDF and DOCX.
- Document processing will be a dedicated application layer.
- File validation will happen before extraction.
- PDF and DOCX may require different processing strategies.
- OCR will be used when appropriate for image-based documents.
- Extracted content will be validated before resume parsing.
- Document processing and resume parsing will remain separate.
- The architecture will be modular and extensible.
- Resume data will be handled with privacy and security considerations.

---

### Hirely Principle

> **Validate → Extract → Normalize → Parse.**

The document-processing layer prepares reliable input for the resume parser; it does not attempt to understand the resume itself.

# 6. AI Frameworks

## 6.1 What is LangChain?

### Background

Large Language Models can be accessed directly through provider-specific APIs, but building a complete AI-powered application often requires additional components such as model integrations, tools, structured interactions, and agent workflows.

LangChain is an open-source framework designed to simplify the development of applications and agents powered by Large Language Models.

It provides abstractions and integrations for working with models, tools, and agent workflows.

---

### LangChain in Simple Terms

A basic application without an AI framework may communicate directly with an LLM provider:

```text
Application
     ↓
Provider API
     ↓
LLM
     ↓
Response
```

With LangChain, an additional application framework layer can be introduced:

```text
Application
     ↓
LangChain
     ↓
Model / Tools / Agent
     ↓
LLM Provider
     ↓
Response
```

LangChain therefore acts as an abstraction and integration layer between an application and many components of an LLM-powered system.

---

### LangChain vs LLM

LangChain is not an LLM.

An LLM is the actual model responsible for generating or interpreting information.

Examples of LLM providers and models include:

- OpenAI models.
- Anthropic models.
- Google models.
- Open-weight models.

LangChain provides a framework for interacting with models and building higher-level AI applications.

Therefore:

```text
LLM
=
AI Model

LangChain
=
Framework for building applications around AI Models
```

---

### Standard Model Interface

One of LangChain's important capabilities is providing a standardized interface for interacting with different model providers.

Different providers may expose different APIs and response formats.

LangChain provides common model interfaces so that application logic can be less tightly coupled to a specific provider.

Conceptually:

```text
             Application
                  ↓
              LangChain
                  ↓
        ┌─────────┼─────────┐
        ↓         ↓         ↓
     OpenAI    Anthropic   Google
        ↓         ↓         ↓
      Model     Model      Model
```

This can make it easier to experiment with different models and providers.

---

### LangChain and Agents

LangChain also provides agent abstractions.

An agent can combine:

```text
Language Model
      +
Tools
      +
Decision / Agent Loop
```

The model can determine when tools should be used and can work through multiple steps before producing a final result.

For simple LLM applications, an agent may not be necessary.

For applications requiring tool usage or more dynamic workflows, agent abstractions can become useful.

---

### LangChain and Tools

Tools allow an AI system to perform actions beyond generating text.

Examples include:

- Searching information.
- Querying a database.
- Calling an external API.
- Performing calculations.
- Executing application-specific functions.

Conceptually:

```text
                 LLM
                  ↓
            Decide whether
             a tool is needed
                  ↓
              Tool Call
                  ↓
          Tool Execution
                  ↓
             Tool Result
                  ↓
                 LLM
                  ↓
             Final Output
```

LangChain provides abstractions for defining and integrating such tools.

---

### LangChain and LangGraph

LangChain and LangGraph serve different purposes.

At a high level:

```text
LangChain
    ↓
Higher-level agent framework
    ↓
Models + Tools + Agent abstractions
```

```text
LangGraph
    ↓
Lower-level orchestration framework/runtime
    ↓
Stateful and complex workflows
```

LangChain agents are built on top of LangGraph.

LangGraph will be researched separately later in this module.

---

### LangChain and Hirely

Hirely will eventually contain an AI layer responsible for capabilities such as:

- Resume feedback.
- Personalized recommendations.
- Career guidance.
- Content generation.
- Cover-letter generation.
- Interview preparation.

LangChain could provide useful abstractions for connecting these AI capabilities with models and application tools.

However, using LangChain should be based on actual project requirements rather than assuming that every AI operation requires a framework.

---

### Analysis

LangChain can reduce the amount of provider-specific integration code required in an LLM-powered application.

Its standardized interfaces can also make experimentation with different models easier.

However, adding a framework introduces another dependency and abstraction layer.

Therefore, Hirely should use LangChain only where its abstractions provide meaningful value.

Simple tasks that can be implemented cleanly using a direct model API should not automatically be forced through unnecessary framework abstractions.

---

### Decision for Hirely

LangChain will be researched as a potential AI framework for Hirely.

At this stage, Hirely will not make the final decision to use LangChain throughout the entire application.

The framework will be evaluated based on:

- Model integration.
- Tool integration.
- Agent requirements.
- Structured output support.
- Maintainability.
- Complexity.
- Performance.
- Project requirements.

The final framework decision will be made after completing the remaining AI-framework research.

---

### Key Takeaways

- LangChain is an open-source framework for building LLM-powered applications and agents.
- LangChain is not an LLM.
- It provides abstractions for models, tools, and agent workflows.
- It provides standardized interfaces across model providers.
- Tools allow AI applications to perform external actions.
- LangChain provides higher-level abstractions than LangGraph.
- LangChain may be useful for Hirely's AI layer.
- Hirely will evaluate LangChain before making a final adoption decision.

---

### Hirely Principle

> **Use an AI framework when its abstractions simplify the application; do not add a framework merely because the application uses an LLM.**

## 6.2 Why Does Hirely Need LangChain?

### Background

Hirely will contain an AI layer responsible for features such as resume feedback, personalized recommendations, career guidance, content generation, and potentially tool-assisted workflows.

The use of LangChain should therefore be evaluated based on whether it simplifies these requirements.

The goal is not to introduce LangChain simply because Hirely uses Large Language Models.

---

### Potential Role of LangChain in Hirely

A possible AI architecture could be:

```text
Hirely Application
        ↓
     AI Service
        ↓
     LangChain
        ↓
 Model / Tools / Workflow
        ↓
       LLM
```

LangChain can provide abstractions for connecting application logic with models, tools, and agent-based workflows.

---

### Potential Hirely Use Case 1: Resume Feedback

Hirely may eventually generate personalized resume feedback.

A simplified flow could be:

```text
Resume
   ↓
Structured Resume Data
   ↓
AI Service
   ↓
LLM
   ↓
Personalized Feedback
```

LangChain could provide useful model and structured-output integrations around this workflow.

However, if the implementation only requires a simple model request, using LangChain may not provide enough additional value to justify the extra abstraction.

---

### Potential Hirely Use Case 2: Career Recommendations

Hirely may provide personalized career recommendations based on information such as:

- Skills.
- Experience.
- Education.
- Projects.
- Career goals.

A future workflow could involve:

```text
User Profile
      ↓
Relevant Information
      ↓
AI Processing
      ↓
LLM
      ↓
Career Recommendations
```

If this workflow later requires retrieval, tools, or multiple AI steps, a framework such as LangChain may become more useful.

---

### Potential Hirely Use Case 3: Tool Integration

Some future Hirely features may need AI to interact with application tools.

For example:

```text
LLM
 ↓
Tool Selection
 ↓
Hirely Tool
 ↓
Result
 ↓
LLM
 ↓
Final Response
```

Potential tools could include:

- Resume analysis functions.
- Database queries.
- Job-search services.
- Skill-matching functions.
- External APIs.

LangChain provides abstractions for tool integration and agent workflows.

---

### Potential Hirely Use Case 4: Structured AI Output

Hirely should not rely on free-form AI responses for every feature.

For example, instead of receiving:

```text
"The candidate has strong Python skills..."
```

the application may eventually require structured information such as:

```text
{
    "score": 82,
    "strengths": [...],
    "weaknesses": [...],
    "recommendations": [...]
}
```

Structured outputs can make AI responses easier for the application to validate and use.

LangChain provides model interfaces that support structured output capabilities.

---

### Potential Hirely Use Case 5: Multiple Model Providers

Hirely may need to experiment with different LLM providers during development.

Conceptually:

```text
                 Hirely AI Service
                        ↓
                    LangChain
                        ↓
             ┌──────────┼──────────┐
             ↓          ↓          ↓
          Provider A Provider B Provider C
             ↓          ↓          ↓
           Model      Model      Model
```

A common abstraction can reduce the amount of provider-specific application code.

This may be useful when evaluating models based on:

- Quality.
- Cost.
- Latency.
- Availability.
- Feature support.

---

### When LangChain May NOT Be Necessary

LangChain should not automatically be used for every AI operation.

For a simple workflow:

```text
User Input
    ↓
Prompt
    ↓
LLM API
    ↓
Response
```

a direct model API may be simpler and easier to maintain.

Introducing a framework for a very small operation could create unnecessary complexity.

---

### Analysis

The value of LangChain for Hirely depends on the complexity of the AI workflows we eventually implement.

Potential benefits include:

- Model abstraction.
- Model-provider integrations.
- Tool integration.
- Agent capabilities.
- Structured output support.
- Reusable AI application components.

Potential costs include:

- Additional dependency.
- Additional abstraction.
- Framework-specific concepts.
- Potentially more complex debugging.
- Dependency on framework APIs and ecosystem changes.

Therefore, LangChain should be evaluated based on actual Hirely requirements rather than being treated as a mandatory technology.

---

### Decision for Hirely

At this stage, LangChain will be treated as a **candidate framework for the Hirely AI layer**, not as a mandatory dependency for the entire application.

We will continue researching its:

- Core concepts.
- Components.
- Model integrations.
- Tool and agent capabilities.
- Limitations.

The final decision will be made after comparing LangChain with alternatives such as LangGraph and LlamaIndex.

---

### Key Takeaways

- Hirely may benefit from LangChain for complex AI workflows.
- LangChain can provide model and tool abstractions.
- Structured AI output may be useful for Hirely.
- Multiple model-provider integrations may become valuable.
- Simple LLM calls may not require LangChain.
- LangChain should be used only where it provides meaningful architectural value.
- The final adoption decision will be made after completing the framework comparison.

---

### Hirely Principle

> **Choose the simplest architecture that satisfies the requirement; introduce LangChain when its abstractions provide measurable value.**

## 6.3 LangChain Core Concepts

### Background

Understanding LangChain requires understanding its fundamental building blocks before studying individual integrations or advanced agent architectures.

The main concepts relevant to Hirely include:

- Messages.
- Models.
- Tools.
- Structured output.
- Runnables and composition.
- Agents.

These concepts form the foundation for building LLM-powered applications with LangChain.

---

### 1. Messages

Messages represent the context exchanged with a model.

A message generally contains:

- A role.
- Content.
- Optional metadata.

Common message roles include:

- System.
- Human / User.
- AI.
- Tool.

Conceptually:

```text
System Message
      ↓
Instructions / Behavior

Human Message
      ↓
User Input

AI Message
      ↓
Model Response

Tool Message
      ↓
Tool Result
```

Messages provide a standardized representation of model interactions.

---

### 2. Models

Models are the actual AI components that process input and generate or reason over output.

Conceptually:

```text
Application
     ↓
LangChain Model Interface
     ↓
LLM / Chat Model
     ↓
Response
```

The model is responsible for capabilities such as:

- Understanding language.
- Generating text.
- Following instructions.
- Calling tools when supported.
- Producing structured output when supported.

LangChain provides standardized interfaces that allow application code to interact with different model providers.

---

### 3. Tools

Tools are callable functions that allow an AI system to interact with external functionality.

Examples include:

- Database queries.
- API calls.
- Search operations.
- Calculations.
- Application-specific functions.

Conceptually:

```text
User Request
     ↓
     LLM
     ↓
Need external information?
     ↓
    Tool
     ↓
Tool Result
     ↓
    LLM
     ↓
Final Response
```

A tool has defined inputs and outputs so that the model can understand how to use it.

---

### 4. Structured Output

Normally, an LLM may return free-form text.

For example:

```text
"The resume has strong Python experience but should improve
the project descriptions."
```

For software applications, structured data is often more useful.

For example:

```json
{
  "score": 82,
  "strengths": [
    "Python experience"
  ],
  "weaknesses": [
    "Project descriptions"
  ],
  "recommendations": [
    "Add measurable project outcomes"
  ]
}
```

Structured output allows the application to work with predictable data instead of parsing arbitrary natural-language responses.

Hirely can potentially use structured outputs for:

- Resume analysis results.
- Skill extraction.
- ATS analysis.
- Recommendations.
- Resume scoring.
- AI-generated reports.

---

### 5. Runnables

A Runnable represents a unit of work that can be invoked and composed with other operations.

Common operations include:

```text
invoke
batch
stream
```

Conceptually:

```text
Input
  ↓
Runnable A
  ↓
Runnable B
  ↓
Runnable C
  ↓
Output
```

This allows different processing steps to be combined into reusable workflows.

For example:

```text
Resume Text
     ↓
Prompt
     ↓
Model
     ↓
Structured Output
```

Each stage can be treated as part of a larger processing pipeline.

---

### 6. Composition

LangChain components can be combined to construct larger workflows.

A conceptual Hirely workflow could be:

```text
Resume Data
     ↓
Prompt Construction
     ↓
Model
     ↓
Structured Output
     ↓
Validation
     ↓
Final Analysis
```

The benefit of composition is that individual components can remain focused on a specific responsibility while the overall application combines them into a larger workflow.

---

### 7. Agents

Agents combine models with tools.

An agent can:

1. Receive a task.
2. Use the model to determine what needs to be done.
3. Select an appropriate tool.
4. Execute the tool.
5. Observe the result.
6. Continue processing.
7. Return a final response.

Conceptually:

```text
              User Task
                  ↓
                Agent
                  ↓
                Model
                  ↓
          ┌───────┴───────┐
          ↓               ↓
      No Tool          Tool Needed
          ↓               ↓
     Final Answer       Tool Call
                          ↓
                     Tool Result
                          ↓
                        Model
                          ↓
                     Final Answer
```

Agents are more appropriate for dynamic tasks where the system needs to decide what actions to take.

Not every Hirely AI feature will require an agent.

---

### 8. Relationship Between the Concepts

The concepts can be connected as follows:

```text
                    Hirely Application
                           ↓
                        Messages
                           ↓
                         Model
                           ↓
                 ┌─────────┴─────────┐
                 ↓                   ↓
             Direct Task        Agent Workflow
                 ↓                   ↓
          Structured Output        Tools
                 ↓                   ↓
             Application        Tool Results
                 ↓                   ↓
                 └─────────┬─────────┘
                           ↓
                     Final Result
```

Runnables and composition can be used to connect processing steps into reusable workflows.

---

### LangChain Mental Model

A simplified mental model for LangChain is:

```text
Messages
   ↓
Models
   ↓
Tools
   ↓
Agents / Workflows
   ↓
Structured Output
   ↓
Application
```

This is a conceptual model rather than a strict execution order.

Different applications may use only a subset of these components.

---

### Application to Hirely

Potential mappings for Hirely include:

```text
Resume
  ↓
Document Processing
  ↓
Structured Resume Data
  ↓
Prompt / Context
  ↓
LangChain Model
  ↓
Structured Analysis
  ↓
Hirely Application
```

For more advanced features:

```text
User Request
     ↓
Hirely AI Service
     ↓
LangChain Agent
     ↓
Model
     ↓
Tool Calls
     ↓
Tool Results
     ↓
Structured Output
     ↓
Hirely Application
```

However, these are potential architectures rather than final implementation decisions.

---

### Analysis

The main value of understanding these concepts is architectural clarity.

Hirely should not treat LangChain as a single feature or library that automatically solves the AI problem.

Instead, LangChain provides different building blocks that can be selected according to application requirements.

For example:

- A simple AI response may only require a model.
- A predictable application result may benefit from structured output.
- An external action may require a tool.
- A dynamic multi-step task may benefit from an agent.
- A reusable processing pipeline may benefit from composition.

---

### Decision for Hirely

Hirely will evaluate LangChain components individually rather than adopting every component by default.

The project will prioritize:

- Clear separation of responsibilities.
- Structured AI outputs where application integration requires them.
- Tools only where external actions or information access are necessary.
- Agents only where dynamic decision-making provides meaningful value.
- Composable workflows where they improve maintainability.

Simple AI operations will remain as simple as possible.

---

### Key Takeaways

- Messages represent model interaction context.
- Models provide the core AI capabilities.
- Tools allow AI systems to interact with external functionality.
- Structured output provides predictable machine-readable results.
- Runnables represent composable units of work.
- Agents combine models and tools for dynamic tasks.
- Not every Hirely feature requires every LangChain component.
- LangChain should be used selectively according to actual requirements.

---

### Hirely Principle

> **Treat LangChain as a collection of composable building blocks, not as a requirement to use every abstraction.**

## 6.4 LangChain Components

### Background

LangChain provides multiple building blocks for developing LLM-powered applications.

The major components relevant to Hirely include:

- Models.
- Messages.
- Prompts.
- Tools.
- Agents.
- Structured Output.
- Runnables and Composition.
- Middleware.
- Provider Integrations.

These components can be combined depending on the requirements of the application.

Hirely will not necessarily use every component.

---

### 1. Models

Models are the core AI engines used by LangChain applications.

They can be used directly or as part of an agent.

Conceptually:

```text
Application
     ↓
LangChain Model Interface
     ↓
LLM / Chat Model
     ↓
Response
```

Models may support capabilities such as:

- Text generation.
- Reasoning.
- Tool calling.
- Structured output.
- Multimodal input/output.

The exact capabilities depend on the selected model and provider.

---

### 2. Messages

Messages represent information exchanged between an application and a model.

Common message types include:

```text
System
Human
AI
Tool
```

Conceptually:

```text
System Message
      ↓
Instructions

Human Message
      ↓
User Request

AI Message
      ↓
Model Response

Tool Message
      ↓
Tool Result
```

Messages provide a consistent representation of model interaction.

---

### 3. Prompts

Prompts define the instructions and context provided to a model.

A simple prompt may contain:

```text
System Instructions
        +
User Input
        +
Relevant Context
```

For Hirely, prompts may be used to guide tasks such as:

- Resume analysis.
- Career recommendations.
- Skill-gap analysis.
- Cover-letter generation.
- Interview preparation.

Prompt design should remain separate from business logic where practical so that prompts can be changed without rewriting the entire application.

---

### 4. Tools

Tools allow an AI application to perform actions outside the model itself.

Examples include:

- Database queries.
- Search.
- API calls.
- Calculations.
- Resume-processing functions.
- Job-matching functions.

Conceptually:

```text
Model
  ↓
Tool Selection
  ↓
Tool
  ↓
Result
  ↓
Model
```

Tools should have clearly defined inputs and outputs.

For example:

```text
Tool:
search_jobs

Input:
{
    "skill": "Python",
    "location": "Remote"
}

Output:
Job results
```

---

### 5. Agents

Agents combine models and tools to perform dynamic tasks.

A simplified agent loop is:

```text
User Request
     ↓
    Model
     ↓
Need Tool?
   /     \
 No       Yes
 ↓         ↓
Final     Tool
Answer     ↓
          Result
            ↓
          Model
            ↓
       Final Answer
```

Agents are useful when the system needs to dynamically determine which actions to take.

They are not required for every LLM operation.

---

### 6. Structured Output

Structured output allows the application to receive predictable data instead of relying only on free-form natural language.

For example:

```text
Free-form:

"The resume is strong but needs better project descriptions."
```

versus:

```json
{
  "score": 82,
  "strengths": [
    "Strong technical skills"
  ],
  "weaknesses": [
    "Project descriptions need improvement"
  ],
  "recommendations": [
    "Add measurable project outcomes"
  ]
}
```

Structured output can be useful for Hirely features that need to pass AI results into backend logic or frontend components.

Potential use cases include:

- Resume scoring.
- Skill extraction.
- Resume analysis.
- Recommendation generation.
- ATS analysis.

LangChain supports structured responses using schemas such as Pydantic models, dataclasses, TypedDict, and JSON Schema. :contentReference[oaicite:3]{index=3}

---

### 7. Runnables and Composition

LangChain supports composable processing units that can be combined into larger workflows.

A conceptual pipeline may look like:

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Structured Output
  ↓
Validation
  ↓
Final Result
```

Composition allows individual steps to remain focused while being connected into a larger workflow.

This is useful when Hirely needs predictable multi-step processing without necessarily requiring an agent.

---

### 8. Middleware

Middleware provides a mechanism for controlling or customizing agent execution.

Potential uses include:

- Logging.
- Analytics.
- Retries.
- Fallbacks.
- Rate limiting.
- Guardrails.
- PII detection.
- Prompt transformation.
- Output transformation.
- Early termination.

Conceptually:

```text
Request
   ↓
Middleware
   ↓
Agent
   ↓
Middleware
   ↓
Response
```

Middleware may become useful in Hirely when the AI system moves toward production.

For example:

```text
User Request
     ↓
PII / Security Check
     ↓
AI Agent
     ↓
Output Validation
     ↓
Response
```

---

### 9. Provider Integrations

LangChain supports integrations with multiple model providers.

Conceptually:

```text
                  LangChain
                      ↓
               Model Interface
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
     OpenAI       Anthropic       Google
        ↓             ↓             ↓
      Model          Model         Model
```

A common interface can reduce provider-specific coupling in application code.

This can make it easier to compare or switch models during development.

---

### 10. How Components Work Together

A simple LangChain application may look like:

```text
User Input
    ↓
Messages / Prompt
    ↓
Model
    ↓
Structured Output
    ↓
Application
```

A more advanced application may look like:

```text
User Input
    ↓
Messages / Prompt
    ↓
Agent
    ↓
Model
    ↓
Tool
    ↓
Tool Result
    ↓
Model
    ↓
Structured Output
    ↓
Application
```

Middleware can be placed around the agent execution where additional control is required.

---

### 11. Potential Hirely Architecture

A future Hirely AI service could potentially use:

```text
                  Hirely AI Service
                         ↓
                     LangChain
                         ↓
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
      Model             Tools           Output
        ↓                ↓                ↓
       LLM         Hirely Functions    Structured
                                          Data
        └────────────────┼────────────────┘
                         ↓
                   Hirely Backend
```

However, this is a potential architecture rather than the final implementation.

---

### Component Selection Strategy

Hirely should select components according to the problem.

```text
Simple AI Request
       ↓
     Model

Predictable AI Result
       ↓
Structured Output

External Action
       ↓
     Tool

Dynamic Multi-Step Task
       ↓
     Agent

Complex Agent Control
       ↓
   Middleware / LangGraph
```

Not every feature needs all components.

---

### Analysis

LangChain is better understood as a collection of composable building blocks rather than a single monolithic system.

This allows an application to start with simple model calls and introduce additional components only when requirements become more complex.

For Hirely, this supports an incremental architecture:

```text
Simple
  ↓
Model
  ↓
Structured Output
  ↓
Tools
  ↓
Agents
  ↓
Advanced Orchestration
```

This avoids unnecessary complexity during the early stages of development.

---

### Decision for Hirely

Hirely will evaluate LangChain components independently.

The initial architecture should prefer the simplest component capable of solving each requirement.

Potential component usage:

| Requirement | Potential Component |
|---|---|
| Direct AI generation | Model |
| Conversation/context | Messages |
| Instructions | Prompts |
| External functionality | Tools |
| Dynamic decision-making | Agents |
| Predictable machine-readable result | Structured Output |
| Multi-step composition | Runnables / Composition |
| Production execution controls | Middleware |
| Complex stateful orchestration | LangGraph |

These are evaluation decisions rather than final implementation commitments.

---

### Key Takeaways

- LangChain consists of multiple reusable components.
- Models provide the core AI capability.
- Messages represent model interaction.
- Prompts provide instructions and context.
- Tools connect AI systems with external functionality.
- Agents combine models and tools for dynamic tasks.
- Structured output provides predictable application-ready data.
- Runnables enable composition of processing steps.
- Middleware can add control, guardrails, retries, and monitoring.
- Provider integrations reduce model-provider coupling.
- Hirely should use only the components required by each feature.

---

### Hirely Principle

> **Choose the smallest LangChain component set that solves the actual problem, and add complexity only when the requirements justify it.**

## 6.5 LangChain and LLM Providers

### Background

Hirely will need access to one or more Large Language Models for its AI features.

Different LLM providers expose different APIs, SDKs, model identifiers, capabilities, and configuration options.

LangChain provides model interfaces and provider integrations that can reduce direct coupling between application code and individual model providers.

---

### Direct Provider Integration

Without a framework abstraction, an application may communicate directly with a provider:

```text
Hirely
   ↓
Provider SDK / API
   ↓
Specific Model
   ↓
Response
```

If the application later changes providers, provider-specific code may need to be changed.

---

### LangChain Model Abstraction

With LangChain:

```text
Hirely
   ↓
AI Service
   ↓
LangChain Model Interface
   ↓
Provider Integration
   ↓
Specific Model
```

The application can interact with a common model interface while the provider integration handles provider-specific details.

---

### Multiple Providers

Conceptually:

```text
                    Hirely AI Service
                           ↓
                        LangChain
                           ↓
                  Common Model Interface
                           ↓
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       OpenAI          Anthropic          Google
          ↓                ↓                ↓
        Models            Models            Models
```

This architecture can make model experimentation easier.

---

### Provider and Model

A provider identifies the service responsible for supplying the model.

The model identifies the specific model being used.

Conceptually:

```text
Provider
   +
Model
   ↓
Specific AI Model
```

For example:

```text
openai : model-name
anthropic : model-name
google_genai : model-name
```

The exact model identifiers depend on the provider and current model catalog.

---

### Why Provider Abstraction Can Help Hirely

Hirely may need to evaluate different models during development.

Possible evaluation criteria include:

- Response quality.
- Resume-analysis quality.
- Structured-output reliability.
- Tool-calling capability.
- Latency.
- Cost.
- Context capacity.
- Reliability.
- Availability.

A model abstraction can make this experimentation easier because application-level code does not need to be completely rewritten for every provider.

---

### Example Hirely Scenario

Suppose Hirely initially evaluates one model:

```text
Hirely
   ↓
LangChain
   ↓
Provider A
   ↓
Model A
```

Later, the team wants to evaluate another model:

```text
Hirely
   ↓
LangChain
   ↓
Provider B
   ↓
Model B
```

The AI service can potentially keep much of its application-level structure while changing the model configuration.

However, provider and model capabilities are not always identical.

---

### Important: Abstraction Does Not Remove Provider Differences

Using LangChain does not mean every model behaves identically.

Different providers and models may differ in:

- Context limits.
- Tool-calling behavior.
- Structured-output support.
- Multimodal capabilities.
- Reasoning capabilities.
- Latency.
- Pricing.
- Rate limits.
- Model quality.

Therefore, Hirely must still evaluate the actual model being used.

```text
Common Interface
      ≠
Identical Model Behavior
```

---

### Model Capabilities

Before selecting a model for Hirely, the project should evaluate whether the model supports the required capabilities.

Potential requirements include:

```text
Text Generation
      +
Structured Output
      +
Tool Calling
      +
Required Context
      +
Required Performance
```

The exact requirements will depend on the AI features implemented later.

---

### Configuration Strategy

Model configuration should remain separate from core business logic where practical.

Conceptually:

```text
Application Logic
       ↓
AI Service
       ↓
Model Configuration
       ↓
Provider / Model
```

This makes experimentation and configuration changes easier.

---

### Development Strategy for Hirely

During development, Hirely may evaluate multiple model providers instead of immediately locking the entire application to one provider.

The evaluation should use representative Hirely tasks such as:

- Resume analysis.
- Skill extraction.
- Resume feedback.
- Career recommendations.
- Structured analysis.
- Content generation.

The selected model should be based on actual project requirements rather than popularity alone.

---

### Cost Consideration

LLM usage can generate significant costs as application usage increases.

Therefore, model selection should consider:

```text
Quality
   +
Cost
   +
Latency
   +
Reliability
```

A more capable model is not automatically the best choice for every Hirely operation.

Different features may eventually use different models if the architecture and requirements justify it.

---

### Fallback Consideration

For production systems, model availability should also be considered.

A future architecture could potentially support:

```text
Primary Model
      ↓
Failure / Unavailable
      ↓
Fallback Model
```

However, fallback behavior should only be introduced when it provides meaningful reliability benefits and after compatibility between the models has been evaluated.

---

### Analysis

LangChain's model abstraction can reduce provider-specific coupling and make model experimentation easier.

However, it does not eliminate the need to understand provider-specific behavior.

Hirely should therefore use LangChain as an abstraction layer while still treating model selection as an engineering decision.

---

### Decision for Hirely

Hirely will keep the AI model integration behind an application-level AI service.

LangChain may be used inside this service to provide model abstractions and provider integrations.

The application should avoid spreading provider-specific code throughout the rest of the Hirely codebase.

Conceptually:

```text
Hirely Application
        ↓
     AI Service
        ↓
    LangChain
        ↓
Provider Integration
        ↓
      Model
```

The final model/provider selection will be made after evaluating Hirely's actual AI requirements.

---

### Key Takeaways

- LLM providers expose different models and APIs.
- LangChain provides common model abstractions and provider integrations.
- Provider abstraction can reduce application-level coupling.
- Different models can still behave differently despite a common interface.
- Hirely should evaluate models using real project requirements.
- Cost, quality, latency, reliability, and capabilities should all be considered.
- Provider-specific code should remain isolated from core business logic.
- LangChain is a possible abstraction layer, not a replacement for model evaluation.

---

### Hirely Principle

> **Keep provider-specific details behind the AI service boundary so Hirely can evaluate and change models without unnecessarily rewriting the application.**

## 6.6 LangChain Tools and Agents

### Background

AI models are powerful at understanding and generating information, but a model by itself cannot automatically perform arbitrary actions in an external application.

Tools provide a mechanism for connecting a model or agent to external functionality.

Agents can then use models and tools together to perform dynamic, multi-step tasks.

---

### Tools

A tool is a callable function that an AI system can use to perform a specific operation.

Examples include:

- Searching information.
- Querying a database.
- Calling an API.
- Performing calculations.
- Accessing application functionality.
- Retrieving resume information.

Conceptually:

```text
AI Model
   ↓
Tool Selection
   ↓
Tool
   ↓
Tool Execution
   ↓
Tool Result
```

A tool should have clearly defined inputs and outputs.

---

### Example Tool

Consider a Hirely job-search tool:

```text
Tool Name:
search_jobs

Input:
{
    "skills": ["Python", "SQL"],
    "location": "Remote"
}

Output:
Job Results
```

The tool performs the actual operation.

The model determines when the tool may be useful.

---

### Tool Calling

A simplified tool-calling workflow is:

```text
User Request
     ↓
    Model
     ↓
Does the task require a tool?
     ↓
    Yes
     ↓
Tool Call
     ↓
Tool Execution
     ↓
Tool Result
     ↓
    Model
     ↓
Final Response
```

The model does not directly execute the tool.

Instead, it produces a tool call containing the required arguments, and the application/framework executes the tool.

---

### Types of Hirely Tools

Potential Hirely tools could include:

```text
Resume Tools
├── get_resume
├── analyze_resume
└── extract_skills

Job Tools
├── search_jobs
├── get_job_details
└── match_jobs

User Tools
├── get_user_profile
└── get_career_preferences
```

These are examples for architectural analysis and are not final implementation decisions.

---

### Agents

An agent combines a model with tools and an execution loop.

The agent can determine:

- What the user is asking.
- Whether a tool is required.
- Which tool should be used.
- What arguments should be supplied.
- Whether another step is necessary.
- When the task is complete.

Conceptually:

```text
                  User Request
                       ↓
                     Agent
                       ↓
                     Model
                       ↓
                Decide Next Step
                  /          \
                 /            \
             Tool Needed     No Tool
                ↓               ↓
              Tool          Final Answer
                ↓
           Tool Result
                ↓
              Model
                ↓
        Decide Next Step
                ↓
          Final Answer
```

---

### Agent Loop

A simplified agent loop is:

```text
1. Receive task
       ↓
2. Send context to model
       ↓
3. Model decides next action
       ↓
4. Execute selected tool if required
       ↓
5. Return tool result to model
       ↓
6. Model evaluates result
       ↓
7. Repeat if necessary
       ↓
8. Produce final answer
```

This makes agents different from simple one-shot model calls.

---

### Simple Model vs Agent

A simple model workflow:

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Output
```

An agent workflow:

```text
Input
  ↓
Agent
  ↓
Model
  ↓
Tool?
 ├── No → Final Output
 └── Yes
       ↓
     Tool
       ↓
     Result
       ↓
     Model
       ↓
     Tool?
       ↓
    ...
       ↓
 Final Output
```

Agents introduce additional decision-making and execution steps.

---

### Potential Hirely Example

Suppose a user asks:

> "Based on my resume, find jobs that match my skills and explain why they are suitable."

A potential agent workflow could be:

```text
User Request
      ↓
     Agent
      ↓
 Get Resume
      ↓
   Resume Data
      ↓
Extract Skills
      ↓
    Skills
      ↓
 Search Jobs
      ↓
 Job Results
      ↓
 Compare Resume + Jobs
      ↓
Generate Explanation
      ↓
 Final Response
```

The agent could coordinate multiple tools to complete the task.

---

### Another Hirely Example

Consider:

> "What skills am I missing for a Machine Learning Engineer role?"

Potential workflow:

```text
User Request
      ↓
     Agent
      ↓
Get Resume
      ↓
Extract Current Skills
      ↓
Get Target Role Requirements
      ↓
Compare Skills
      ↓
Identify Gaps
      ↓
Generate Recommendations
      ↓
Final Response
```

This is a more dynamic workflow than simply asking an LLM to generate text.

---

### When Hirely Should Use Tools

Tools are useful when the AI needs access to information or functionality that is not contained in the model's existing context.

Potential examples:

```text
Need current job data
        ↓
    Job Search Tool

Need user resume
        ↓
    Resume Tool

Need application data
        ↓
    Database Tool

Need calculation
        ↓
    Calculation Tool
```

---

### When Hirely Should Use Agents

Agents may be appropriate when:

- The task requires multiple steps.
- The next step depends on previous results.
- Different tools may be required.
- The system needs dynamic decision-making.
- The workflow cannot easily be represented as a fixed sequence.

For simple deterministic workflows, a normal pipeline may be preferable.

---

### Agent vs Fixed Workflow

A fixed workflow might be:

```text
Resume
  ↓
Extract Skills
  ↓
Match Jobs
  ↓
Generate Report
```

The steps are predetermined.

An agent workflow may be:

```text
User Request
      ↓
    Agent
      ↓
Determine Required Actions
      ↓
Tool A / Tool B / Tool C
      ↓
Evaluate Results
      ↓
Determine Next Action
      ↓
Final Response
```

Agents provide more flexibility but also introduce more complexity.

---

### Risks of Agents

Agents should not be added without considering their risks.

Potential problems include:

- Unexpected tool calls.
- Incorrect tool arguments.
- Unnecessary tool usage.
- Longer execution time.
- Higher model usage and cost.
- More difficult debugging.
- Non-deterministic execution.
- Incorrect reasoning leading to incorrect actions.

Therefore, agent workflows require appropriate validation and controls.

---

### Security Considerations

Tools can provide access to sensitive functionality.

For Hirely, tools may eventually access:

- Resume data.
- User profiles.
- Database records.
- External services.

Therefore, tools should have:

- Clearly defined permissions.
- Input validation.
- Output validation.
- Appropriate authentication.
- Minimal required access.
- Error handling.

An AI agent should not automatically receive unrestricted access to the application's systems.

---

### Analysis

Tools and agents can significantly extend the capabilities of an LLM-powered application.

However:

```text
More capability
      ↓
More complexity
      ↓
More control required
```

Hirely should therefore use tools where external functionality is genuinely required and agents only where dynamic decision-making provides meaningful value.

---

### Decision for Hirely

Hirely will support the possibility of application-specific tools in the AI layer.

Potential tools may eventually expose safe operations such as:

- Resume retrieval.
- Resume analysis.
- Job search.
- Skill matching.
- Career information retrieval.

Agents will be considered for complex multi-step AI workflows.

Simple deterministic workflows will remain ordinary application pipelines unless an agent provides a clear advantage.

All agent tools should be explicitly defined, validated, permission-controlled, and limited to the minimum functionality required.

---

### Key Takeaways

- Tools are callable functions available to an AI system.
- Tools provide access to external functionality.
- Agents combine models and tools with a decision-making loop.
- Tool calling allows models to request external actions.
- Agents are useful for dynamic multi-step tasks.
- Fixed workflows are often preferable for deterministic processes.
- Agents introduce additional complexity and cost.
- Tool permissions and input validation are important security requirements.
- Hirely will evaluate agents only where they provide meaningful value.

---

### Hirely Principle

> **Give AI the tools it needs, but never give an agent more access or autonomy than the task requires.**

## 6.7 LangChain Limitations

### Background

LangChain provides useful abstractions for building LLM-powered applications, but introducing a framework also introduces additional complexity and dependencies.

Hirely should therefore evaluate both the benefits and limitations of using LangChain.

The goal is not to use LangChain everywhere, but to determine where its abstractions provide meaningful value.

---

### 1. Added Complexity

For a simple AI operation:

```text
Input
  ↓
Prompt
  ↓
LLM
  ↓
Response
```

a direct model API may be sufficient.

Introducing LangChain for a very simple operation may add unnecessary abstractions.

Therefore:

```text
Simple Requirement
      ↓
Prefer Simple Implementation
```

---

### 2. Additional Abstraction Layer

With LangChain, the application may contain additional layers:

```text
Hirely
   ↓
AI Service
   ↓
LangChain
   ↓
Provider Integration
   ↓
Model API
```

This abstraction can provide portability and reusable components, but it can also make debugging and understanding the complete execution path more difficult.

---

### 3. Framework Dependency

If Hirely becomes heavily dependent on LangChain-specific APIs throughout the application, changing the AI framework later may become more difficult.

A better architecture is:

```text
Hirely Application
        ↓
     AI Service
        ↓
    LangChain
        ↓
      Model
```

The AI service boundary keeps framework-specific implementation details isolated.

---

### 4. Framework Evolution

AI frameworks evolve rapidly.

APIs, abstractions, integrations, and recommended development patterns can change over time.

Hirely should therefore avoid spreading framework-specific code across unrelated parts of the application.

Keeping framework usage inside the AI layer can reduce the impact of future changes.

---

### 5. Agents Add Complexity

Agents can provide dynamic decision-making, but they are not necessary for every AI workflow.

For example:

```text
Resume
  ↓
Extract Skills
  ↓
Calculate Score
  ↓
Generate Report
```

This is a predictable workflow and can be implemented as a fixed pipeline.

Using an agent for such a workflow may introduce unnecessary complexity.

Agents are more appropriate when the next action genuinely depends on the current state or model decision.

---

### 6. Debugging Complexity

A simple AI workflow may look like:

```text
Input
  ↓
Model
  ↓
Output
```

A more complex agent workflow may look like:

```text
Input
  ↓
Agent
  ↓
Model
  ↓
Tool
  ↓
Model
  ↓
Tool
  ↓
Model
  ↓
Output
```

When something fails in the second workflow, there are more components and execution steps to investigate.

Therefore, Hirely should prefer simpler workflows when they satisfy the requirement.

---

### 7. Cost and Latency

More complex workflows may require:

- Multiple model calls.
- Multiple tool calls.
- Additional processing.
- More tokens.

This can increase:

- API cost.
- Response latency.
- Infrastructure requirements.
- Failure opportunities.

Hirely should therefore avoid unnecessary model calls and unnecessary agent loops.

---

### 8. Provider Differences Remain

LangChain can provide common interfaces across model providers, but different providers and models can still behave differently.

Differences may include:

- Model capabilities.
- Context limits.
- Tool-calling behavior.
- Structured-output support.
- Performance.
- Pricing.
- Reliability.

Therefore:

```text
Common Interface
      ≠
Identical Model Behavior
```

Hirely must still evaluate the actual models being used.

---

### 9. Abstraction vs Control

Framework abstractions can make development easier, but direct provider APIs may sometimes provide more direct control over provider-specific capabilities.

Hirely therefore needs to balance:

```text
Abstraction
    vs
Control
```

The correct choice depends on the requirements of each feature.

---

### 10. Potential Vendor / Framework Lock-In

Heavy dependence on framework-specific abstractions can create a form of framework coupling.

For example:

```text
Business Logic
      ↓
LangChain-Specific APIs
      ↓
Model
```

can make future migration more difficult.

A stronger architecture is:

```text
Business Logic
      ↓
Hirely AI Service Interface
      ↓
AI Implementation
      ↓
LangChain / Direct API
      ↓
Model
```

This allows the underlying AI implementation to change without rewriting the entire application.

---

### Analysis

LangChain can provide significant value for applications requiring model integrations, tools, agents, structured outputs, and composable AI workflows.

However, those capabilities also introduce additional concepts and complexity.

Hirely should therefore avoid treating LangChain as a mandatory layer for every AI operation.

The framework should be introduced where its abstractions solve a real engineering problem.

---

### Decision for Hirely

Hirely will not automatically use LangChain for every AI operation.

The project will follow these principles:

- Prefer direct implementations for simple AI operations when appropriate.
- Use LangChain where its abstractions provide meaningful value.
- Keep framework-specific code inside the AI service boundary.
- Avoid unnecessary agent usage.
- Minimize unnecessary model and tool calls.
- Evaluate provider-specific capabilities separately.
- Keep the architecture flexible enough to replace or modify the AI framework later.

---

### Key Takeaways

- LangChain can simplify complex AI application development.
- LangChain also introduces additional abstraction and dependency.
- Simple AI operations may not require a framework.
- Agents can add significant complexity.
- More AI calls can increase cost and latency.
- Provider differences still exist behind common interfaces.
- Framework-specific code should be isolated.
- Hirely should use LangChain selectively rather than everywhere.

---

### Hirely Principle

> **Use LangChain where it reduces complexity; do not introduce LangChain where it creates more complexity than it removes.**

## 6.8 LangGraph

### Background

LangGraph is a framework/runtime designed for building more complex, stateful, and long-running AI workflows and agents.

It provides lower-level orchestration capabilities than the higher-level abstractions commonly associated with LangChain agents.

LangGraph can also be used independently of LangChain.

---

### Why LangGraph Exists

Simple AI applications may follow a straightforward workflow:

```text
Input
  ↓
Model
  ↓
Output
```

More advanced AI applications may require:

- Multiple steps.
- Tool calls.
- Conditional decisions.
- Persistent state.
- Human approval.
- Long-running execution.
- Multiple iterations.
- Recovery after interruptions.

A workflow may therefore look like:

```text
User Request
     ↓
Analyze Input
     ↓
Decision
  /      \
 ↓        ↓
Tool A   Tool B
  \      /
   ↓    ↓
 Combine Results
       ↓
 Generate Response
```

Managing such workflows becomes more complex than a simple model call.

LangGraph provides an orchestration model for these kinds of applications.

---

### Core Mental Model

A useful simplified mental model for LangGraph is:

```text
State
  +
Nodes
  +
Edges
  ↓
Graph-based Workflow
```

Where:

```text
State
=
Information maintained throughout execution

Node
=
A unit of work

Edge
=
Defines how execution moves between nodes
```

---

### State

State represents information that needs to be maintained during the workflow.

For example, a Hirely AI workflow might maintain:

```text
State
├── User Request
├── Resume Data
├── Extracted Skills
├── Job Results
├── Recommendations
└── Current Workflow Status
```

As the workflow executes, different nodes can read or update the state.

Conceptually:

```text
Initial State
      ↓
Node A
      ↓
Updated State
      ↓
Node B
      ↓
Updated State
      ↓
Node C
```

This makes state an important part of complex workflows.

---

### Nodes

A node represents a unit of work within the graph.

Examples could include:

```text
Resume Analysis Node
Job Search Node
Skill Matching Node
Recommendation Node
Validation Node
```

Conceptually:

```text
        ┌──────────────┐
        │ Resume Node  │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Skill Node   │
        └──────┬───────┘
               ↓
        ┌──────────────┐
        │ Job Node     │
        └──────────────┘
```

A node can perform application logic, call a model, or interact with tools.

---

### Edges

Edges define how execution moves between nodes.

A simple workflow:

```text
Node A
  ↓
Node B
  ↓
Node C
```

A conditional workflow:

```text
             Node A
                ↓
            Decision
           /        \
          ↓          ↓
       Node B      Node C
          \          /
           \        /
             Node D
```

This allows workflows to branch based on the current state or result.

---

### Conditional Routing

One important capability of graph-based workflows is conditional execution.

For example:

```text
Analyze Resume
      ↓
Is resume valid?
   /        \
 No          Yes
 ↓            ↓
Request       Analyze
Correction    Skills
                ↓
             Continue
```

This provides more explicit control over workflow execution than simply allowing an agent to decide everything dynamically.

---

### LangGraph and Agents

LangGraph is particularly relevant to agentic applications.

A simplified architecture is:

```text
User
 ↓
Agent Workflow
 ↓
Model
 ↓
Tool
 ↓
Result
 ↓
State Update
 ↓
Model
 ↓
Decision
 ↓
Next Step
```

The graph controls how the workflow progresses.

This can make complex agent behavior more explicit and controllable.

---

### Persistence

Long-running workflows may need to preserve their state.

For example:

```text
Workflow
   ↓
Step 1
   ↓
State Saved
   ↓
Execution Interrupted
   ↓
Resume Later
   ↓
Continue Workflow
```

Persistence can be important for workflows that should survive interruptions or continue over longer periods.

---

### Human-in-the-Loop

Some AI operations should not be completely autonomous.

For example, Hirely might eventually generate an important recommendation and require user confirmation:

```text
AI Recommendation
       ↓
Human Review
       ↓
User Approves?
    /       \
  No         Yes
  ↓           ↓
Modify      Continue
             ↓
          Execute
```

A stateful workflow framework can help model this type of interaction.

---

### Durable Execution

A complex workflow may contain many steps.

If execution fails halfway through, restarting everything may be inefficient.

A durable workflow can potentially resume from a previously persisted state rather than starting from the beginning.

Conceptually:

```text
Step 1
  ↓
Step 2
  ↓
State Saved
  ↓
Step 3
  X
Failure
  ↓
Resume
  ↓
Step 3
  ↓
Step 4
```

This becomes particularly relevant for long-running workflows.

---

### LangChain vs LangGraph

A simplified comparison:

```text
LangChain
    ↓
Higher-level AI application framework
    ↓
Models + Tools + Agents
```

```text
LangGraph
    ↓
Lower-level orchestration framework/runtime
    ↓
Stateful Graph-Based Workflows
```

LangChain agents can use LangGraph internally, while LangGraph can also be used independently.

Therefore:

```text
LangChain
   +
LangGraph
```

can be used together, but they are not identical technologies.

---

### When LangGraph May Be Useful for Hirely

Potential Hirely workflows could eventually become complex enough to benefit from explicit orchestration.

Examples:

#### Resume Analysis Workflow

```text
Upload Resume
      ↓
Extract Content
      ↓
Validate Data
      ↓
Extract Skills
      ↓
Analyze Experience
      ↓
Generate Feedback
      ↓
Validate Output
      ↓
Save Results
```

#### Career Recommendation Workflow

```text
User Profile
      ↓
Resume Data
      ↓
Skill Analysis
      ↓
Career Goals
      ↓
Job / Role Information
      ↓
Compare Options
      ↓
Generate Recommendations
      ↓
User Review
```

These workflows contain multiple stages and potentially multiple decisions.

---

### When LangGraph Is NOT Necessary

A simple feature such as:

```text
User
 ↓
Prompt
 ↓
Model
 ↓
Response
```

does not need a graph orchestration framework.

Likewise, a simple deterministic function may not require LangGraph.

Therefore:

```text
Simple Workflow
      ↓
Keep It Simple

Complex Stateful Workflow
      ↓
Consider LangGraph
```

---

### Analysis

LangGraph provides more explicit control over complex AI execution.

Its state, node, and edge model can make multi-step workflows easier to reason about and control.

However, this additional control also introduces additional concepts and complexity.

Hirely should therefore not introduce LangGraph simply because it is part of the modern AI ecosystem.

It should be introduced only when the application's workflows actually require:

- Stateful execution.
- Complex branching.
- Multiple iterations.
- Long-running workflows.
- Human-in-the-loop interaction.
- Durable execution.
- Explicit orchestration.

---

### Decision for Hirely

LangGraph will be treated as a potential orchestration layer for complex Hirely AI workflows.

The initial Hirely architecture should not require LangGraph for simple model calls or straightforward deterministic pipelines.

If Hirely develops complex agent workflows that require persistent state, branching, human interaction, or durable execution, LangGraph will be evaluated for those workflows.

Conceptually:

```text
Simple AI Feature
      ↓
Model / LangChain
```

```text
Complex Stateful AI Workflow
      ↓
LangGraph
      ↓
Models + Tools + State
```

The final decision will depend on the complexity of the actual Hirely implementation.

---

### Key Takeaways

- LangGraph is a lower-level orchestration framework/runtime.
- It is designed for complex and stateful AI workflows.
- Its core mental model involves state, nodes, and edges.
- Nodes represent units of work.
- Edges control workflow transitions.
- Conditional routing allows branching workflows.
- Persistence can support long-running workflows.
- Human-in-the-loop workflows can be modeled explicitly.
- LangGraph can be used with or without LangChain.
- Simple AI features do not require LangGraph.
- Hirely should consider LangGraph only when workflow complexity justifies it.

---

### Hirely Principle

> **Use explicit orchestration when AI workflows become complex enough to require state, control, and reliable execution—not simply because a workflow uses AI.**

## 6.9 LlamaIndex

### Background

LlamaIndex is an open-source framework for building LLM-powered applications that work with external and private data.

Its main focus is connecting Large Language Models with data sources and building data-aware AI applications.

A simplified mental model is:

```text
Your Data
    +
LLM
    ↓
LlamaIndex
    ↓
Data-Aware AI Application
```

---

### Why LlamaIndex Exists

A general-purpose LLM does not automatically have access to private application data.

For example, Hirely may contain:

- User resumes.
- User profiles.
- Job descriptions.
- Skill information.
- Career information.
- Other application-specific documents.

Hirely may want the AI system to answer questions using this information.

Therefore, the application needs a mechanism for:

```text
Application Data
      ↓
Process
      ↓
Index
      ↓
Retrieve Relevant Information
      ↓
Provide Context to LLM
      ↓
Generate Answer
```

LlamaIndex provides components for building these types of data-connected workflows.

---

### LlamaIndex and RAG

One of the important use cases associated with LlamaIndex is Retrieval-Augmented Generation (RAG).

A simplified RAG workflow is:

```text
Documents
    ↓
Load
    ↓
Process
    ↓
Index
    ↓
Store
    ↓
User Question
    ↓
Retrieve Relevant Information
    ↓
LLM
    ↓
Answer
```

The goal is to provide the model with relevant information from external data rather than relying only on information already contained in the model.

---

### Hirely RAG Example

Suppose a user uploads a resume.

The resume contains:

```text
Python
SQL
Machine Learning
TensorFlow
Pandas
```

The user asks:

> "What skills should I improve to become an ML Engineer?"

A possible workflow is:

```text
User Question
      ↓
Retrieve Relevant Resume Information
      ↓
Resume Knowledge
      ↓
Relevant Context
      ↓
LLM
      ↓
Personalized Recommendation
```

This allows the response to be based on the user's actual information.

---

### Data Sources

An AI application may need to work with different types of data.

Potential sources include:

```text
Documents
PDFs
Web Pages
Databases
APIs
Structured Data
Unstructured Data
Knowledge Bases
```

For Hirely, potential sources include:

```text
              Hirely Data
                   ↓
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    Resumes       Jobs       Skills
       ↓           ↓           ↓
       └───────────┼───────────┘
                   ↓
              Data Layer
                   ↓
                 LLM
```

The exact data architecture will be determined later.

---

### Indexing

Indexing is the process of preparing data so that relevant information can be retrieved efficiently.

Conceptually:

```text
Raw Data
   ↓
Processing
   ↓
Index
   ↓
Retrieval
```

For example:

```text
Resume
   ↓
Process Resume
   ↓
Create Index
   ↓
User Question
   ↓
Retrieve Relevant Resume Information
```

The exact indexing strategy depends on the type and structure of the data.

---

### Retrieval

Retrieval is the process of finding information relevant to a user's question.

For example:

```text
Question:

"What Python projects have I worked on?"
```

The system should retrieve the relevant portions of the user's stored information.

Conceptually:

```text
User Question
      ↓
Retriever
      ↓
Relevant Data
      ↓
LLM
      ↓
Answer
```

Good retrieval is important because the model's answer depends heavily on the quality and relevance of the context provided to it.

---

### LlamaIndex vs LLM

LlamaIndex is not an LLM.

```text
LlamaIndex
=
Framework for connecting AI applications with data

LLM
=
AI model responsible for language generation/reasoning
```

Conceptually:

```text
Data
 ↓
LlamaIndex
 ↓
LLM
 ↓
Response
```

---

### LlamaIndex vs LangChain

The two ecosystems overlap, but their primary areas of focus can be viewed differently.

A simplified mental model is:

```text
LangChain
    ↓
Models + Tools + Agents + AI Application Workflows
```

while:

```text
LlamaIndex
    ↓
Data + Indexing + Retrieval + RAG + Data-Aware AI
```

This is a conceptual distinction rather than a strict separation.

LangChain can also be used for retrieval and RAG.

LlamaIndex can also support agentic applications.

The important difference is the emphasis of their abstractions and ecosystems.

---

### Hirely Example: Data-Centric AI

Consider:

> "Analyze my resume and tell me which skills I am missing."

This can be viewed primarily as a data and retrieval problem:

```text
Resume
   ↓
Process
   ↓
Index / Store
   ↓
Retrieve Relevant Information
   ↓
LLM
   ↓
Skill Gap Analysis
```

LlamaIndex could be evaluated for this type of architecture.

---

### Hirely Example: Agent-Centric AI

Now consider:

> "Find suitable jobs, compare them with my resume, and recommend the best opportunities."

This may involve:

```text
User Request
      ↓
Agent
      ↓
Get Resume
      ↓
Search Jobs
      ↓
Compare Skills
      ↓
Evaluate Results
      ↓
Generate Recommendations
```

This is more strongly related to tools, agents, and orchestration.

LangChain and LangGraph may therefore be particularly relevant for this type of workflow.

---

### Important Overlap

The comparison should not be interpreted as:

```text
LangChain → Agents only
LlamaIndex → RAG only
```

Both ecosystems provide capabilities that overlap.

A better interpretation is:

```text
LangChain
→ Broad LLM application and agent ecosystem

LlamaIndex
→ Strong emphasis on data-connected LLM applications
```

The actual choice should depend on the requirements of the application.

---

### Potential Hirely Use Cases

LlamaIndex could potentially be useful for:

- Resume knowledge bases.
- Document question answering.
- Retrieval-Augmented Generation.
- Skill information retrieval.
- Job-description retrieval.
- Career knowledge bases.
- Personalized AI responses based on user data.

These are potential use cases and do not represent final implementation decisions.

---

### Limitations and Trade-offs

Using a framework also introduces additional abstraction and dependency.

Potential concerns include:

- Additional complexity.
- Framework dependency.
- Need to understand indexing and retrieval concepts.
- Retrieval quality becoming an important engineering concern.
- Additional infrastructure for data storage and retrieval.
- Potential overlap with capabilities already provided by other frameworks.

Therefore, Hirely should evaluate whether LlamaIndex provides enough value for the project's actual data requirements.

---

### Analysis

LlamaIndex is particularly relevant when an AI application needs to work with external, private, or application-specific data.

Hirely has several potential data-heavy AI use cases, especially around resumes, jobs, skills, and career information.

Therefore, LlamaIndex is worth evaluating as part of the Hirely AI architecture.

However, the project should not automatically introduce LlamaIndex if the required retrieval functionality can be implemented more simply using existing application infrastructure or another suitable approach.

---

### Decision for Hirely

LlamaIndex will be evaluated as a potential framework for Hirely's data-connected AI capabilities.

Potential areas for evaluation include:

- Resume retrieval.
- RAG.
- Document processing.
- Knowledge bases.
- Data indexing.
- Retrieval quality.
- Integration with the existing Hirely architecture.

The final decision will be made after comparing LlamaIndex with LangChain and LangGraph.

---

### Key Takeaways

- LlamaIndex is a framework for building LLM-powered applications connected to external data.
- It is strongly associated with data ingestion, indexing, retrieval, and RAG workflows.
- LlamaIndex is not an LLM.
- Retrieval allows relevant application data to be provided to an LLM.
- Hirely's resumes, jobs, skills, and career information may benefit from data-connected AI.
- LlamaIndex and LangChain overlap in several areas.
- LlamaIndex should be evaluated based on Hirely's actual data and retrieval requirements.
- The framework should not be introduced unless it provides meaningful value.

---

### Hirely Principle

> **For AI features that depend heavily on Hirely's own data, prioritize reliable data access and retrieval before adding unnecessary agent complexity.**

## 6.10 Framework Comparison

### Purpose

The purpose of this comparison is to evaluate LangChain, LangGraph, and LlamaIndex based on Hirely's actual requirements.

The project should not select a framework based on popularity or the number of available features.

The framework should be selected based on the problem it needs to solve.

---

### Simplified Mental Model

A useful high-level mental model is:

```text
                 AI Application
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    LangChain      LangGraph     LlamaIndex
        │             │             │
        ↓             ↓             ↓
   AI Building     Workflow       Data &
     Blocks        Control       Retrieval
```

This is a conceptual model rather than a strict separation.

The three ecosystems have overlapping capabilities.

---

### LangChain

LangChain is primarily useful as a higher-level framework for building LLM-powered applications.

Important areas include:

- Models.
- Tools.
- Agents.
- Structured output.
- Model-provider integrations.
- AI application workflows.

Mental model:

```text
LangChain
    ↓
Models + Tools + Agents + AI Application Building Blocks
```

---

### LangGraph

LangGraph focuses on lower-level orchestration of complex and stateful AI workflows.

Important areas include:

- State.
- Nodes.
- Edges.
- Conditional routing.
- Persistence.
- Human-in-the-loop workflows.
- Long-running execution.
- Agent orchestration.

Mental model:

```text
LangGraph
    ↓
State + Nodes + Edges
    ↓
Complex AI Workflow
```

---

### LlamaIndex

LlamaIndex focuses strongly on connecting LLM applications with external and private data.

Important areas include:

- Data ingestion.
- Indexing.
- Retrieval.
- RAG.
- Knowledge bases.
- Data-connected AI applications.

Mental model:

```text
LlamaIndex
    ↓
Data + Indexing + Retrieval
    ↓
Data-Aware AI Application
```

---

### Comparison by Primary Focus

| Framework | Primary Focus |
|---|---|
| LangChain | LLM application building and agent capabilities |
| LangGraph | Stateful AI workflow orchestration |
| LlamaIndex | Data-connected AI and retrieval |

These descriptions represent the primary architectural emphasis and do not imply that each framework is limited to only one capability.

---

### Comparison of Major Capabilities

| Capability | LangChain | LangGraph | LlamaIndex |
|---|---|---|---|
| General LLM applications | Strong | Moderate | Moderate |
| Model integrations | Strong | Strong through integrations | Strong |
| Tools | Strong | Strong | Supported |
| Agents | Strong | Strong | Supported |
| Complex workflows | Moderate | Strong | Moderate |
| Stateful execution | Limited compared with LangGraph | Strong | Not primary focus |
| RAG | Strong | Possible | Strong |
| Data indexing | Supported | Not primary focus | Strong |
| Retrieval | Supported | Not primary focus | Strong |
| Document-focused AI | Supported | Not primary focus | Strong |
| Simple AI applications | Strong | Usually unnecessary | Possible |

The table is an architectural comparison, not an official framework ranking.

---

### Hirely Feature Mapping

#### Feature 1: Simple Resume Feedback

Potential workflow:

```text
Resume
  ↓
Prompt
  ↓
Model
  ↓
Structured Feedback
```

This feature may not require a complex framework.

A direct model API or a simple LangChain integration could be sufficient.

---

#### Feature 2: AI Job Assistant

Potential workflow:

```text
User Request
      ↓
Agent
      ↓
Get Resume
      ↓
Search Jobs
      ↓
Compare Skills
      ↓
Evaluate Results
      ↓
Recommendation
```

Potential technologies:

```text
LangChain
   ↓
Tools + Agent

LangGraph
   ↓
Complex workflow orchestration if required
```

---

#### Feature 3: Ask Questions About Resume

Potential workflow:

```text
User Question
      ↓
Retrieve Relevant Resume Information
      ↓
Relevant Context
      ↓
LLM
      ↓
Answer
```

Potential technology:

```text
LlamaIndex
   ↓
Data + Retrieval + RAG
```

However, other retrieval architectures may also satisfy this requirement.

---

### Framework Combination

The frameworks do not necessarily have to be mutually exclusive.

A future architecture could potentially contain:

```text
                    Hirely AI
                        │
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
     Simple AI       Agentic AI       RAG
        ↓               ↓               ↓
   Model /           LangGraph      LlamaIndex
   LangChain            ↓               ↓
                      Models           LLM
```

However, introducing multiple frameworks also increases:

- Dependencies.
- Operational complexity.
- Maintenance requirements.
- Learning requirements.
- Potential integration problems.

Therefore, multiple frameworks should only be introduced when they provide clearly different and valuable capabilities.

---

### Complexity Consideration

A major architectural principle for Hirely is:

```text
Start Simple
    ↓
Identify Actual Requirements
    ↓
Add Complexity Only When Needed
```

The project should avoid:

```text
Use Everything
     ↓
More Dependencies
     ↓
More Complexity
```

---

### Decision Criteria for Hirely

The final framework decision should consider:

1. Feature requirements.
2. Data requirements.
3. Retrieval requirements.
4. Agent requirements.
5. Workflow complexity.
6. State management.
7. Maintainability.
8. Performance.
9. Cost.
10. Framework complexity.
11. Provider flexibility.
12. Long-term architecture.

---

### Preliminary Hirely Assessment

At the current research stage:

```text
LangChain
→ Strong candidate for general LLM application capabilities.

LangGraph
→ Strong candidate for complex stateful AI workflows.

LlamaIndex
→ Strong candidate for data-heavy AI and retrieval workflows.
```

This is a preliminary assessment.

It is not the final architecture decision.

---

### Potential Evolution of Hirely

A possible incremental approach is:

```text
Phase 1
Simple AI
    ↓
Direct Model API / LangChain
```

```text
Phase 2
Need Tools
    ↓
LangChain Tools
```

```text
Phase 3
Need Complex Stateful Workflows
    ↓
Evaluate LangGraph
```

```text
Phase 4
Need Advanced Data Retrieval / RAG
    ↓
Evaluate LlamaIndex
```

The actual order may change based on the features implemented.

---

### Analysis

The comparison shows that the frameworks solve related but different architectural problems.

LangChain provides broad LLM application and agent-building capabilities.

LangGraph provides more explicit control over complex and stateful workflows.

LlamaIndex provides strong abstractions for data-connected AI, indexing, and retrieval.

Therefore, the correct question is not:

> "Which framework is the best?"

The correct question is:

> "Which framework, if any, best solves the specific problem Hirely currently has?"

---

### Preliminary Decision

Hirely will not adopt all three frameworks by default.

The project will initially favor the simplest architecture capable of satisfying its requirements.

Potential direction:

```text
General AI
    ↓
LangChain / Direct Model API

Complex Stateful Agent Workflows
    ↓
LangGraph

Data-Heavy RAG / Retrieval
    ↓
Evaluate LlamaIndex
```

The final technology decision will be made after completing the research and understanding the actual implementation requirements.

---

### Key Takeaways

- LangChain focuses broadly on LLM application and agent development.
- LangGraph focuses on complex and stateful AI workflow orchestration.
- LlamaIndex focuses strongly on data-connected AI, indexing, and retrieval.
- Their capabilities overlap.
- Hirely does not need to use all three.
- Simple features should remain simple.
- Complex workflows may justify LangGraph.
- Data-heavy RAG workflows may justify LlamaIndex.
- LangChain is a candidate for general AI application capabilities.
- Framework selection should be requirement-driven.

---

### Hirely Principle

> **Do not ask which AI framework is best in general; ask which architecture best solves the specific Hirely problem with the least unnecessary complexity.**

## 6.11 Final Framework Decision for Hirely

### Purpose

The purpose of this section is to make a preliminary technology decision for Hirely based on the research completed in the previous sections.

The decision should be requirement-driven rather than framework-driven.

The project should not introduce a framework simply because it is popular or provides many features.

The preferred approach is:

```text
Hirely Requirement
       ↓
Identify Architecture Problem
       ↓
Choose Appropriate Technology
```

---

### Research Summary

The research covered:

```text
LangChain
   ↓
LLM Application Building
   ↓
Tools and Agents
   ↓
Limitations

LangGraph
   ↓
Stateful and Complex AI Workflow Orchestration

LlamaIndex
   ↓
Data, Indexing, Retrieval and RAG
```

These technologies have overlapping capabilities, but their primary architectural emphasis differs.

---

### Framework Roles

#### LangChain

Primary role:

```text
LLM Application Development
```

Potential Hirely uses:

- Model integrations.
- Tools.
- Agents.
- Structured output.
- AI application components.

LangChain is a candidate for general AI application functionality where its abstractions provide meaningful value.

---

#### LangGraph

Primary role:

```text
Complex Stateful AI Workflow Orchestration
```

Potential Hirely uses:

- Multi-step agent workflows.
- State management.
- Conditional routing.
- Human-in-the-loop workflows.
- Long-running workflows.
- Durable execution.

LangGraph should only be introduced when workflow complexity justifies an explicit orchestration layer.

---

#### LlamaIndex

Primary role:

```text
Data-Connected AI and Retrieval
```

Potential Hirely uses:

- Resume knowledge bases.
- Document retrieval.
- RAG.
- Data indexing.
- Knowledge retrieval.
- Data-aware AI applications.

LlamaIndex should be evaluated when Hirely's AI features depend heavily on external or private data.

---

### Preliminary Hirely Architecture

The AI layer can be conceptually divided into three categories:

```text
                         Hirely AI
                             │
             ┌───────────────┼───────────────┐
             ↓               ↓               ↓
         Simple AI       Agentic AI       Data/RAG
             │               │               │
             ↓               ↓               ↓
       Model API /        LangChain       Retrieval
       LangChain             │            System
                             ↓               │
                         LangGraph       LlamaIndex
```

This represents possible technology roles rather than a requirement to install and use all frameworks simultaneously.

---

### Decision Rule

Hirely will use the following decision process:

```text
Feature Requirement
       ↓
Is it a simple AI operation?
       ↓
      Yes
       ↓
Direct Model API / Simple AI Layer
```

If tools or agent capabilities are required:

```text
Feature
  ↓
Tools / Agent
  ↓
LangChain
```

If the workflow becomes complex and stateful:

```text
Feature
  ↓
Complex Workflow
  ↓
LangGraph
```

If the feature depends heavily on external/private data and retrieval:

```text
Feature
  ↓
Data / Retrieval / RAG
  ↓
Evaluate LlamaIndex
```

These are decision guidelines rather than rigid rules.

---

### Initial Technology Strategy

Hirely should begin with the simplest architecture capable of satisfying the current requirements.

The initial strategy is:

```text
Core AI
   ↓
Direct Model API
   +
LangChain where useful
```

Additional technologies will be introduced only when their specific capabilities become necessary.

Potential future additions:

```text
Complex Agent Workflow
        ↓
     LangGraph
```

```text
Advanced Data Retrieval / RAG
        ↓
   Evaluate LlamaIndex
```

---

### Why Not Use Everything Immediately?

Using all three frameworks from the beginning would introduce unnecessary complexity.

Potential consequences include:

- More dependencies.
- More abstractions.
- More maintenance.
- More learning overhead.
- More integration complexity.
- More difficult debugging.
- Potential duplication of functionality.

Therefore:

```text
More Frameworks
      ≠
Better Architecture
```

A better principle is:

```text
Required Capability
      ↓
Minimum Necessary Technology
```

---

### Hirely Architecture Principle

The project should follow:

```text
Start Simple
     ↓
Build Features
     ↓
Identify Real Problems
     ↓
Introduce Appropriate Abstractions
     ↓
Scale the Architecture
```

This prevents premature architectural complexity.

---

### Long-Term Possibility

As Hirely evolves, its AI architecture may become:

```text
                    Hirely AI Layer
                          │
          ┌───────────────┼────────────────┐
          ↓               ↓                ↓
       Models           Agents            Data
          │               │                │
          ↓               ↓                ↓
     Model API /      LangChain +      Retrieval /
      LangChain       LangGraph         RAG Layer
                                             │
                                         LlamaIndex
                                        if justified
```

The exact implementation will depend on the actual requirements discovered during development.

---

### Final Preliminary Decision

At the current research stage:

```text
LangChain
→ Candidate for general LLM application capabilities,
  tools, and agents.

LangGraph
→ Candidate for complex, stateful, and long-running
  AI workflows.

LlamaIndex
→ Candidate for data-heavy AI, indexing, retrieval,
  and RAG workflows.
```

Hirely will not automatically adopt all three.

The project will begin with the simplest suitable AI architecture and introduce additional frameworks only when their capabilities solve a real requirement.

---

### Key Takeaways

- Technology decisions should be requirement-driven.
- LangChain is a candidate for general LLM application capabilities.
- LangGraph is a candidate for complex stateful workflows.
- LlamaIndex is a candidate for data-heavy retrieval and RAG.
- The three frameworks have overlapping capabilities.
- Hirely should not use all three by default.
- Simple features should remain simple.
- Additional frameworks should be introduced only when justified.
- Architecture should evolve as real requirements emerge.
- The goal is maintainability and appropriate complexity, not maximum framework usage.

---

### Hirely Principle

> **Choose the simplest architecture that solves the current problem, and introduce additional AI frameworks only when their capabilities provide clear engineering value.**
# 7 Backend Technologies
## 7.1 FastAPI

### Background

Hirely is an AI-powered application that will need a backend layer to connect the frontend with AI services, document processing, databases, and other application functionality.

The backend will provide APIs through which the frontend can communicate with Hirely's application logic.

A simplified architecture is:

```text
User
  ↓
Frontend
  ↓
HTTP Request
  ↓
Backend API
  ↓
Application Logic
  ↓
AI / Document Processing / Database
  ↓
HTTP Response
  ↓
Frontend
  ↓
User
```

FastAPI is a Python web framework designed for building APIs.

For Hirely, FastAPI is being researched as a potential backend framework because the project is heavily based on Python technologies, including AI, machine learning, document processing, and LLM-related functionality.

---

### What is FastAPI?

FastAPI is a modern Python web framework for building APIs.

Its purpose is to provide a structured way to expose backend functionality through HTTP endpoints.

Conceptually:

```text
Python
   ↓
FastAPI
   ↓
Backend APIs
   ↓
Application Services
```

FastAPI itself is not:

```text
❌ An LLM
❌ A machine learning model
❌ A database
❌ A document processor
❌ An AI framework
```

Instead, it provides the API layer through which these different components can communicate.

---

### Why Does Hirely Need a Backend?

Hirely will contain multiple application components.

Potential components include:

```text
Frontend
    ↓
Backend API
    ├── User Management
    ├── Resume Upload
    ├── Resume Processing
    ├── Resume Analysis
    ├── AI Services
    ├── Job-related Features
    └── Database Operations
```

The frontend should not be responsible for directly managing all of these backend operations.

Instead, the frontend communicates with the backend through APIs.

---

### Frontend-to-Backend Communication

A simplified Hirely workflow can be represented as:

```text
User
 ↓
Upload Resume
 ↓
Frontend
 ↓
HTTP Request
 ↓
FastAPI Backend
 ↓
Validate Request
 ↓
Process Resume
 ↓
AI Analysis
 ↓
Generate Result
 ↓
HTTP Response
 ↓
Frontend
 ↓
Display Result
```

This separation allows the frontend and backend to have clearly defined responsibilities.

---

### API Concept

API stands for:

**Application Programming Interface**

In the context of Hirely, an API provides a defined interface through which another application can communicate with the backend.

For example:

```text
Frontend
    ↓
POST /api/resume/analyze
    ↓
FastAPI
    ↓
Resume Analysis Service
    ↓
Result
    ↓
Frontend
```

The API defines how the frontend can request a particular backend operation.

---

### Hirely API Examples

Potential Hirely endpoints could include:

```text
POST /api/resume/upload
POST /api/resume/analyze
GET  /api/resume/{id}

POST /api/jobs/search
GET  /api/jobs/{id}

GET  /api/users/{id}
```

These are conceptual examples for architecture planning.

The final API structure will be defined later during API design and implementation.

---

### FastAPI and Python

FastAPI is built for Python.

This is relevant to Hirely because Python is expected to play an important role in:

```text
AI
Machine Learning
LLMs
Resume Processing
Document Processing
Data Processing
```

Therefore, a Python-based backend can allow the application to work within a consistent Python ecosystem.

Conceptually:

```text
                    Hirely Backend
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
       API Layer       AI Services     Data Layer
          ↓               ↓               ↓
       FastAPI          Python        Database
```

---

### FastAPI Routes

An API endpoint is commonly represented through a route.

For example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Hirely"}
```

The route:

```text
GET /
```

can return:

```json
{
  "message": "Welcome to Hirely"
}
```

This simple example demonstrates the basic relationship between:

```text
HTTP Method
     ↓
Route
     ↓
Python Function
     ↓
Response
```

The syntax will be studied further during implementation.

---

### HTTP Methods

APIs commonly use HTTP methods to describe the type of operation being requested.

Important methods include:

```text
GET
POST
PUT
PATCH
DELETE
```

A simplified interpretation is:

```text
GET
→ Retrieve information

POST
→ Create or submit information

PUT
→ Replace/update information

PATCH
→ Partially update information

DELETE
→ Remove information
```

For example:

```text
GET /api/resume/123
```

could retrieve a resume.

While:

```text
POST /api/resume/upload
```

could submit a new resume for processing.

The complete API design will be researched separately under REST APIs.

---

### FastAPI and Type Hints

FastAPI makes extensive use of Python type hints.

For example:

```python
def analyze_resume(resume_id: int):
    ...
```

Here:

```text
resume_id: int
```

indicates that the function expects an integer value.

Type information can help FastAPI understand the expected structure and types of API data.

This becomes particularly important when combined with request validation and Pydantic models.

---

### FastAPI and Pydantic

FastAPI works closely with Pydantic for data validation and data modeling.

Conceptually:

```text
Client Request
      ↓
FastAPI
      ↓
Pydantic Validation
      ↓
Application Logic
      ↓
Response
```

For example, a resume-analysis request might eventually contain:

```text
resume_id
user_id
analysis_type
```

A Pydantic model can define the expected structure of this request.

Pydantic will be studied separately as part of the Backend Technologies research.

---

### FastAPI and AI Services

FastAPI can act as the API layer connecting users to Hirely's AI functionality.

For example:

```text
User
 ↓
Frontend
 ↓
POST /api/resume/analyze
 ↓
FastAPI
 ↓
Resume Processing
 ↓
Resume Parser
 ↓
AI / LLM
 ↓
Analysis Result
 ↓
FastAPI
 ↓
Frontend
```

This allows AI functionality to be exposed through normal backend APIs.

---

### FastAPI and Database

FastAPI can also communicate with database-related services.

A simplified architecture is:

```text
Frontend
   ↓
FastAPI
   ↓
Application Logic
   ↓
Database Layer
   ↓
Database
```

For Hirely, the database may eventually contain information such as:

```text
Users
Resumes
Skills
Experience
Education
Jobs
Analysis Results
```

The exact database technology will be researched separately under Database Design.

SQLAlchemy will also be evaluated separately as part of Backend Technologies.

---

### FastAPI and Document Processing

Hirely's resume workflow may require document processing.

A possible architecture is:

```text
Resume Upload
      ↓
FastAPI
      ↓
File Validation
      ↓
Document Processing
      ↓
Text Extraction
      ↓
Resume Parsing
      ↓
AI Analysis
      ↓
Result
```

FastAPI is responsible for receiving and exposing the operation through an API.

The actual document processing is handled by separate services or libraries.

Therefore:

```text
FastAPI
≠
Document Processing
```

Instead:

```text
FastAPI
   ↓
Document Processing Service
```

This separation helps keep the architecture modular.

---

### FastAPI and Async Programming

FastAPI supports asynchronous programming.

This can be useful for backend operations involving tasks where the application spends time waiting for external operations, such as:

```text
External APIs
Database operations
Network requests
AI service requests
Other I/O operations
```

Conceptually:

```text
Request
   ↓
FastAPI
   ↓
Async Operation
   ↓
Wait without unnecessarily blocking other work
   ↓
Result
```

Async programming will be studied separately under:

```text
6.5 Async Programming
```

Therefore, async behavior should not be treated as the main purpose of FastAPI.

---

### Automatic API Documentation

One useful characteristic of FastAPI is its ability to generate API documentation from the API definitions.

Conceptually:

```text
FastAPI Routes
      ↓
API Schema
      ↓
Automatic Documentation
```

This can help developers understand and test available endpoints during development.

For a project such as Hirely, this can become useful as the number of API endpoints increases.

---

### FastAPI Architecture in Hirely

A possible backend architecture is:

```text
                         Hirely
                            │
                        Frontend
                            │
                         HTTP/API
                            │
                            ↓
                         FastAPI
                            │
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
       User Services    AI Services    Data Services
             │              │              │
             ↓              ↓              ↓
       Authentication      LLM          Database
             │              │              │
             ↓              ↓              ↓
       Resume Services   AI Analysis   SQLAlchemy
             │
             ↓
       Document Processing
```

This is a conceptual architecture.

The exact implementation will be defined during later design stages.

---

### Separation of Responsibilities

A major architectural benefit of using an API framework is the ability to separate responsibilities.

For example:

```text
Frontend
→ User interface

FastAPI
→ API layer

Application Services
→ Business logic

Document Processing
→ File and text processing

AI Services
→ LLM and AI operations

Database Layer
→ Data persistence
```

This separation can make the system easier to maintain and evolve.

---

### Advantages Relevant to Hirely

Potential advantages of FastAPI for Hirely include:

- Python-based development.
- Suitable for API development.
- Strong use of Python type hints.
- Request and response validation support.
- Integration with Pydantic.
- Support for asynchronous programming.
- Automatic API documentation.
- Suitable for separating API logic from AI and data services.
- Good fit for Python-based AI applications.

These advantages are reasons for evaluating FastAPI rather than an automatic decision to use it.

---

### Potential Limitations and Considerations

FastAPI also requires architectural discipline.

Potential considerations include:

- Developers need to understand HTTP and API design.
- Authentication and authorization still need to be designed.
- Database architecture still needs to be designed.
- Background processing may require additional components.
- Application structure must be organized as the project grows.
- Security must be explicitly designed.
- API versioning and error handling need to be considered.

FastAPI provides the API framework, but it does not automatically solve the complete backend architecture.

---

### FastAPI Does Not Replace the Entire Backend

An important distinction is:

```text
FastAPI
    ↓
API Framework
```

not:

```text
FastAPI
    ↓
Complete Backend System
```

A production backend may contain:

```text
FastAPI
   +
Business Logic
   +
Database
   +
Authentication
   +
Validation
   +
AI Services
   +
Document Processing
   +
Logging
   +
Error Handling
   +
Security
```

FastAPI provides the foundation for the API layer, while the rest of the backend architecture must be designed separately.

---

### Analysis for Hirely

Hirely is expected to use Python heavily for AI, LLM, and document-processing functionality.

The application will also require an API layer through which the frontend can communicate with these backend services.

FastAPI provides a potential Python-based API layer for this architecture.

A conceptual flow is:

```text
Frontend
    ↓
FastAPI
    ↓
Backend Services
    ├── Resume Processing
    ├── AI Analysis
    ├── User Services
    └── Database Services
```

This makes FastAPI a strong candidate for Hirely's backend technology.

---

### Decision for Hirely

FastAPI will be adopted as the **preliminary backend API framework for Hirely**, subject to validation during implementation.

The main reasons are:

1. Hirely is heavily based on Python.
2. Hirely requires an API layer.
3. FastAPI is designed for building Python APIs.
4. It supports type-hint-based development.
5. It integrates with Pydantic for validation.
6. It supports asynchronous programming.
7. It can expose AI and document-processing functionality through APIs.
8. It provides automatic API documentation.

The final backend architecture will also depend on the decisions made for:

```text
REST APIs
Pydantic
SQLAlchemy
Async Programming
Authentication
Security
Database
Deployment
```

---

### Preliminary Hirely Backend Architecture

The current direction is:

```text
                     Hirely Backend
                           │
                        FastAPI
                           │
            ┌──────────────┼──────────────┐
            ↓              ↓              ↓
       API Routes     Application      Services
                         Logic            │
                           │       ┌──────┼──────┐
                           │       ↓      ↓      ↓
                           │      AI   Documents Database
                           │
                           ↓
                       Validation
                       / Pydantic
```

This architecture will evolve as the remaining backend research is completed.

---

### Key Takeaways

- FastAPI is a Python web framework for building APIs.
- It can provide the backend API layer for Hirely.
- APIs allow the frontend to communicate with backend services.
- FastAPI is not an LLM, database, or document-processing system.
- FastAPI can expose AI functionality through HTTP endpoints.
- FastAPI works closely with Python type hints and Pydantic.
- FastAPI supports asynchronous programming.
- FastAPI can generate API documentation.
- Backend responsibilities should remain separated into appropriate services.
- FastAPI does not automatically solve authentication, database design, security, or complete backend architecture.
- FastAPI is a strong candidate for Hirely's backend API layer.

---

### Hirely Principle

> **Use the backend API as a clean communication layer between Hirely's frontend and its AI, document-processing, database, and application services.**

## 7.2 REST APIs

### Background

Hirely will need a backend API through which the frontend can communicate with backend services such as:

- Resume processing
- Resume analysis
- AI services
- User management
- Job-related functionality
- Database operations

A simplified architecture is:

    User
      ↓
    Frontend
      ↓
    HTTP Request
      ↓
    REST-style API
      ↓
    FastAPI
      ↓
    Backend Services
      ├── Resume Processing
      ├── AI Services
      ├── User Services
      └── Database Services
      ↓
    HTTP Response
      ↓
    Frontend
      ↓
    User

REST provides principles for designing this API in a consistent and predictable way.

---

### What is REST?

REST stands for:

**Representational State Transfer**

REST is an **architectural style for designing networked applications and APIs**.

The most important idea is:

> **Design APIs around resources and use standard HTTP methods to operate on those resources.**

For Hirely, possible resources include:

    Users
    Resumes
    Jobs
    Skills
    Analyses

Instead of designing APIs primarily around function names, REST encourages us to think in terms of resources.

---

### REST is Not a Framework

REST and FastAPI are different concepts.

    REST
    ↓
    Architectural style

While:

    FastAPI
    ↓
    Python web framework

Therefore:

    REST principles
           +
        FastAPI
           ↓
    REST-style API implementation

FastAPI can be used to implement APIs following REST principles.

---

### API vs REST API

An API is a general interface that allows software components to communicate.

A REST API is an API designed according to REST principles.

Conceptually:

    API
    │
    └── Can be designed in different ways

    REST API
    │
    └── API following REST architectural principles

Therefore:

> Every REST API is an API, but not every API is necessarily RESTful.

---

### Resource-Oriented Design

One of the most important REST concepts is the **resource**.

For Hirely, resources can include:

    User
    Resume
    Job
    Skill
    Analysis

These resources can be represented through URLs.

For example:

    /api/resumes

represents the resume collection.

And:

    /api/resumes/123

represents one specific resume.

The URL identifies the resource.

The HTTP method describes the operation.

---

### Resource + HTTP Method

A useful mental model is:

    RESOURCE + HTTP METHOD

For example:

    GET /api/resumes

means:

> Retrieve resumes.

While:

    POST /api/resumes

means:

> Create or submit a new resume.

And:

    GET /api/resumes/123

means:

> Retrieve resume 123.

This separation makes API behavior more predictable.

---

### HTTP Methods

REST-style APIs commonly use HTTP methods to represent operations.

Important methods include:

    GET
    POST
    PUT
    PATCH
    DELETE

---

### GET

**GET = retrieve information**

Example:

    GET /api/resumes

Meaning:

> Retrieve the resumes.

Another example:

    GET /api/resumes/123

Meaning:

> Retrieve resume 123.

Conceptually:

    Frontend
       ↓
    GET /api/resumes/123
       ↓
    FastAPI
       ↓
    Database
       ↓
    Resume
       ↓
    Frontend

GET is generally used for retrieving information rather than changing server state.

---

### POST

**POST = create or submit data**

Example:

    POST /api/resumes

could mean:

> Submit a new resume.

The request could contain:

    Resume File
    User Information
    Metadata

Another possible Hirely operation could be:

    POST /api/analyses

which could submit a request to create a new resume analysis.

Conceptually:

    Frontend
       ↓
    POST Request
       ↓
    FastAPI
       ↓
    Validate
       ↓
    Process
       ↓
    AI Analysis
       ↓
    Result

---

### PUT

**PUT = replace a resource representation**

Example:

    PUT /api/users/123

could mean:

> Replace the current representation of user 123.

Conceptually:

    Frontend
       ↓
    PUT /api/users/123
       ↓
    FastAPI
       ↓
    Replace User Data

PUT is generally associated with replacing the representation of a resource.

---

### PATCH

**PATCH = partially modify a resource**

Suppose a user only wants to change their name.

The frontend could send:

    PATCH /api/users/123

with:

    {
        "name": "New Name"
    }

The server can update only the specified field.

Think:

    PUT
    ↓
    Replace

    PATCH
    ↓
    Partial modification

---

### DELETE

**DELETE = remove a resource**

Example:

    DELETE /api/resumes/123

Meaning:

> Delete resume 123.

Conceptually:

    Frontend
       ↓
    DELETE /api/resumes/123
       ↓
    FastAPI
       ↓
    Database
       ↓
    Resume Removed

---

### HTTP Method Summary

| Method | General Meaning | Hirely Example |
|---|---|---|
| GET | Retrieve | GET /api/resumes/123 |
| POST | Create/submit | POST /api/resumes |
| PUT | Replace/update | PUT /api/users/123 |
| PATCH | Partially update | PATCH /api/users/123 |
| DELETE | Delete | DELETE /api/resumes/123 |

---

### RESTful URL Design

REST encourages URLs to represent resources rather than actions.

#### Less resource-oriented approach

    /api/getAllResumes
    /api/createResume
    /api/deleteResume
    /api/updateResume

These URLs describe actions.

#### REST-style approach

    GET    /api/resumes
    POST   /api/resumes
    GET    /api/resumes/123
    PUT    /api/resumes/123
    PATCH  /api/resumes/123
    DELETE /api/resumes/123

Here:

    URL
    ↓
    Identifies the resource

    HTTP Method
    ↓
    Describes the operation

This is an important REST design principle.

---

### Collection vs Individual Resource

REST APIs commonly distinguish between a collection and an individual resource.

Collection:

    /api/resumes

represents:

> The collection of resumes.

Individual resource:

    /api/resumes/123

represents:

> Resume with ID 123.

Therefore:

    /api/resumes
            ↑
        Collection

and:

    /api/resumes/123
                  ↑
        Individual Resource

This makes API URLs predictable.

---

### Hirely Resources

Potential Hirely resources include:

    /api/users
    /api/resumes
    /api/jobs
    /api/skills
    /api/analyses

For example:

    /api/resumes

represents resumes.

    /api/jobs

represents jobs.

    /api/analyses

represents analysis resources.

The exact API structure will be finalized during implementation.

---

### Hirely User APIs

Potential user endpoints:

    GET    /api/users
    GET    /api/users/123
    POST   /api/users
    PATCH  /api/users/123
    DELETE /api/users/123

These provide a consistent interface for user resources.

---

### Hirely Resume APIs

Potential resume endpoints:

    GET    /api/resumes
    GET    /api/resumes/123
    POST   /api/resumes
    DELETE /api/resumes/123

A resume upload could use:

    POST /api/resumes

The exact implementation may use multipart file upload because resumes can be PDF or DOCX files.

---

### Hirely Job APIs

Potential job endpoints:

    GET  /api/jobs
    GET  /api/jobs/123
    POST /api/jobs

For example:

    GET /api/jobs

could retrieve available jobs.

And:

    GET /api/jobs/123

could retrieve information about one specific job.

---

### Resource Relationships

Resources can have relationships.

For example:

    User
     └── Resumes

A user may have multiple resumes.

A possible endpoint could be:

    GET /api/users/123/resumes

meaning:

> Retrieve resumes belonging to user 123.

Another possible relationship:

    Resume
     └── Analyses

could potentially be represented as:

    GET /api/resumes/123/analyses

However, nested resources should be used carefully.

The API should remain simple and understandable.

---

### Request

A REST API communication begins with a request.

A request can contain:

    HTTP Method
    URL
    Headers
    Body

Example:

    POST /api/resumes

The request may contain resume information or a resume file.

Conceptually:

    Frontend
       ↓
    HTTP Request
       ├── Method
       ├── URL
       ├── Headers
       └── Body
       ↓
    FastAPI

---

### Response

The backend sends a response back to the client.

A response can contain:

    Status Code
    Headers
    Body

For example:

    {
        "id": 123,
        "filename": "resume.pdf",
        "status": "processed"
    }

Conceptually:

    FastAPI
       ↓
    HTTP Response
       ├── Status Code
       ├── Headers
       └── Body
       ↓
    Frontend

---

### HTTP Status Codes

REST APIs use HTTP status codes to communicate the result of an operation.

Important status codes include:

    200
    OK

    201
    Created

    204
    No Content

    400
    Bad Request

    401
    Unauthorized

    403
    Forbidden

    404
    Not Found

    500
    Internal Server Error

---

### 200 OK

    200 OK

Generally means:

> The request was successfully processed.

Example:

    GET /api/resumes/123

could return:

    200 OK

with the resume data.

---

### 201 Created

    201 Created

is commonly used when a new resource has been successfully created.

For example:

    POST /api/resumes

could return:

    201 Created

after successfully creating the resume resource.

---

### 204 No Content

    204 No Content

means the request succeeded but there is no response body to return.

This can be useful for certain successful update or delete operations.

---

### 400 Bad Request

    400 Bad Request

generally means the request is invalid or cannot be processed because of client-provided input.

For example:

    Invalid request data

---

### 401 Unauthorized

    401 Unauthorized

generally indicates that authentication is required or the provided authentication credentials are invalid.

Example:

    Frontend
       ↓
    GET /api/resumes/123
       ↓
    No valid authentication
       ↓
    401 Unauthorized

---

### 403 Forbidden

    403 Forbidden

generally means the client is authenticated but does not have permission to perform the requested operation.

Example:

    User A
       ↓
    Attempts to access User B's protected resource
       ↓
    403 Forbidden

Authentication and authorization will be studied more deeply later.

---

### 404 Not Found

    404 Not Found

means the requested resource cannot be found.

Example:

    GET /api/resumes/999

If resume 999 does not exist:

    404 Not Found

---

### 500 Internal Server Error

    500 Internal Server Error

generally indicates an unexpected problem on the server side.

For example:

    Frontend
       ↓
    API Request
       ↓
    FastAPI
       ↓
    Unexpected Backend Error
       ↓
    500 Internal Server Error

Production applications should handle errors properly rather than exposing internal implementation details.

---

### Statelessness

One important REST principle is **statelessness**.

Statelessness means that each request should contain the information necessary for the server to process that request.

Conceptually:

    Request 1
       ↓
    Server
       ↓
    Response

    Request 2
       ↓
    Server
       ↓
    Response

The server should not depend on hidden conversational state from an earlier request to understand the current request.

Authentication information can be included with requests through mechanisms such as tokens.

---

### Why Statelessness Matters for Hirely

Stateless API design can make scaling easier.

For example:

                        Load Balancer
                        /           \
                       ↓             ↓
                  FastAPI 1      FastAPI 2
                       ↑             ↑
                       └──── API ────┘

If requests contain the necessary information, different backend instances can process different requests.

This can become useful as Hirely grows.

---

### REST and Authentication

Hirely will eventually require authentication and authorization.

A simplified flow may look like:

    User
     ↓
    Login
     ↓
    Authentication
     ↓
    Token / Session
     ↓
    API Request
     ↓
    FastAPI
     ↓
    Authorization
     ↓
    Resource

For example:

    GET /api/resumes/123

may require the user to be authenticated and authorized to access that resume.

Authentication and security will be researched separately.

---

### REST and CRUD

CRUD stands for:

    Create
    Read
    Update
    Delete

REST APIs often support CRUD-style operations, but:

**REST ≠ CRUD**

CRUD describes common data operations.

REST is a broader architectural style involving concepts such as:

    Resources
    HTTP methods
    Representations
    Stateless communication
    Standard HTTP semantics

Therefore:

    CRUD
    ↓
    Operations

    REST
    ↓
    Architectural style

They are related but not identical.

---

### REST and FastAPI

The relationship can be summarized as:

    REST
    ↓
    Architectural principles

    HTTP
    ↓
    Communication protocol

    FastAPI
    ↓
    Python framework

    Pydantic
    ↓
    Data validation / modeling

    SQLAlchemy
    ↓
    Database interaction

For Hirely:

    Frontend
       ↓
    HTTP
       ↓
    REST-style API
       ↓
    FastAPI
       ↓
    Backend Services

---

### Hirely Resume Lifecycle

A simplified resume lifecycle demonstrates how REST principles can be applied.

#### 1. Create Resume

    POST /api/resumes

    Frontend
       ↓
    POST
       ↓
    FastAPI
       ↓
    Store Resume

#### 2. Retrieve Resume

    GET /api/resumes/123

    Frontend
       ↓
    GET
       ↓
    FastAPI
       ↓
    Resume

#### 3. Update Resume

    PATCH /api/resumes/123

    Frontend
       ↓
    PATCH
       ↓
    FastAPI
       ↓
    Update Resume

#### 4. Delete Resume

    DELETE /api/resumes/123

    Frontend
       ↓
    DELETE
       ↓
    FastAPI
       ↓
    Delete Resume

This creates a predictable resource lifecycle.

---

### REST and AI Operations

Not every Hirely operation will necessarily be simple CRUD.

Hirely may eventually have operations such as:

    Resume Analysis
    Document Processing
    AI Generation
    Job Matching
    Long-running AI Tasks

Some of these operations may require specialized API designs.

Therefore:

> REST principles should guide the API architecture, but every operation should still be designed according to its actual requirements.

We should not force every AI operation into an unnecessarily complicated CRUD model.

---

### REST API Architecture for Hirely

The current conceptual architecture is:

                             Hirely
                               │
                            Frontend
                               │
                              HTTP
                               │
                               ↓
                        REST-style API
                               │
                            FastAPI
                               │
                 ┌─────────────┼─────────────┐
                 ↓             ↓             ↓
              Resume          AI          Database
              Services      Services       Services

The API layer acts as the communication boundary between the frontend and backend services.

---

### Separation of Responsibilities

The architecture should keep different responsibilities separate.

    Frontend
    → User interface

    HTTP
    → Communication protocol

    REST
    → API architectural principles

    FastAPI
    → API implementation

    Pydantic
    → Request/response validation and modeling

    Application Services
    → Business logic

    AI Services
    → AI/LLM functionality

    Document Processing
    → File/text processing

    Database Layer
    → Data persistence

This separation improves maintainability and makes the system easier to evolve.

---

### Advantages of REST-style APIs for Hirely

Potential advantages include:

- Standard HTTP methods.
- Resource-oriented design.
- Predictable URL structures.
- Clear separation between frontend and backend.
- Stateless communication.
- Easy integration with different clients.
- Suitable for web and mobile applications.
- Easy to test using standard HTTP tools.
- Can work well with FastAPI.
- Provides a clear foundation for a scalable backend architecture.

---

### Potential Limitations and Considerations

REST-style APIs also require careful design.

Important considerations include:

- Correct HTTP method selection.
- Consistent URL naming.
- Proper status code usage.
- Authentication and authorization.
- Error handling.
- API versioning.
- Request validation.
- Response schema design.
- Pagination for large collections.
- Rate limiting where appropriate.
- Handling long-running AI operations.
- Avoiding unnecessarily complex nested URLs.

REST provides architectural principles, but good API design still requires engineering decisions.

---

### Analysis for Hirely

Hirely needs a standardized communication layer between its frontend and backend.

REST-style API design provides a familiar and predictable approach.

For example:

    Frontend
       ↓
    GET /api/resumes/123
       ↓
    FastAPI
       ↓
    Resume Service
       ↓
    Database
       ↓
    Response

Or:

    Frontend
       ↓
    POST /api/analyses
       ↓
    FastAPI
       ↓
    Resume Analysis Service
       ↓
    AI Service
       ↓
    Analysis Result

This allows Hirely's backend services to remain separated from the frontend.

---

### Decision for Hirely

Hirely will use **REST-style API design principles** for its backend API layer where appropriate.

The preliminary technology and architecture decision is:

    HTTP
      ↓
    REST-style API
      ↓
    FastAPI
      ↓
    Application Services
      ↓
    AI / Document Processing / Database

REST is selected because it provides a clear and widely understood approach for designing APIs around resources and HTTP operations.

However, the final API design will be refined during implementation.

---

### Preliminary Hirely API Structure

The current conceptual API structure is:

    /api
     ├── /users
     │     ├── GET
     │     ├── POST
     │     └── /{id}
     │           ├── GET
     │           ├── PATCH
     │           └── DELETE
     │
     ├── /resumes
     │     ├── GET
     │     ├── POST
     │     └── /{id}
     │           ├── GET
     │           ├── PATCH
     │           └── DELETE
     │
     ├── /jobs
     │     ├── GET
     │     └── /{id}
     │           └── GET
     │
     └── /analyses
           ├── GET
           ├── POST
           └── /{id}
                 └── GET

This is a preliminary structure and may change as the actual Hirely features are implemented.

---

### Key Takeaways

- REST stands for Representational State Transfer.
- REST is an architectural style, not a programming language or framework.
- REST APIs are commonly designed around resources.
- URLs identify resources.
- HTTP methods describe operations.
- GET is generally used for retrieving data.
- POST is generally used for creating or submitting data.
- PUT is generally associated with replacing a resource.
- PATCH is generally used for partial modification.
- DELETE is used for deleting a resource.
- REST and CRUD are related but not the same.
- REST APIs use HTTP status codes to communicate results.
- Statelessness is an important REST principle.
- FastAPI can be used to implement REST-style APIs.
- REST should guide the design without forcing every operation into a simple CRUD pattern.
- Hirely will use REST-style API principles where they provide a clean and appropriate design.

---

### Important Mental Model

Remember this:

    HTTP
    ↓
    Communication Protocol

    REST
    ↓
    Architectural Style

    FastAPI
    ↓
    Python Framework

    Pydantic
    ↓
    Validation / Data Modeling

    SQLAlchemy
    ↓
    Database Interaction

For Hirely:

    Frontend
       ↓
    HTTP Request
       ↓
    REST-style API
       ↓
    FastAPI
       ↓
    Application Logic
       ↓
    AI / Document Processing / Database
       ↓
    HTTP Response
       ↓
    Frontend

---

### Hirely Principle

> **Design APIs around meaningful resources, use standard HTTP semantics, keep communication predictable, and let FastAPI implement the API layer.**

## 7.3 Pydantic

### Background

After understanding FastAPI and REST APIs, the next important requirement for Hirely is **data validation and data modeling**.

A backend application receives data from many different sources:

- Frontend
- REST API requests
- Resume parser
- Document processing system
- OCR
- AI / LLM systems
- Database layer
- External services

We cannot assume that all incoming data will always have the correct structure.

For example, Hirely may expect:

    experience_years → integer
    skills → list of strings
    email → string

But the application may receive:

    experience_years → "five"
    skills → "Python, SQL"
    email → missing

If invalid data enters the application, it can create:

- Runtime errors
- Unexpected behavior
- Incorrect analysis
- Database problems
- API errors
- AI pipeline failures

Therefore, Hirely needs a proper mechanism to define and validate the structure of its data.

This is where **Pydantic** becomes important.


### What is Pydantic?

**Pydantic is a Python library used for data validation and data modeling using Python type annotations.**

In simple terms:

> Pydantic allows us to define what our data should look like and validate incoming data against that structure.

Conceptually:

    Incoming Data
          ↓
       Pydantic
          ↓
       Validation
          ↓
    Structured Data
          ↓
    Application Logic

Pydantic allows us to create structured models that describe the data our application expects.


### Why do we need Pydantic?

Imagine Hirely receives candidate information.

The application expects:

    name → string
    email → string
    experience_years → integer

But the incoming request contains:

    name → "John"
    email → 12345
    experience_years → "three"

The application now has inconsistent data.

Without validation:

    Request
      ↓
    Application
      ↓
    Business Logic
      ↓
    Database / AI
      ↓
    Error

With validation:

    Request
      ↓
    Pydantic
      ↓
    Validation
      ↓
    Valid Data
      ↓
    Application

Invalid data can be detected much earlier.

Therefore:

> Pydantic helps protect the application from incorrectly structured data.


### Pydantic as a Data Gatekeeper

A useful mental model for Pydantic is:

> **Pydantic acts as a gatekeeper for structured data.**

The flow is:

    External Data
          ↓
       Pydantic
          ↓
       Validate
          ↓
    ┌─────┴─────┐
    ↓           ↓
  Valid       Invalid
    ↓           ↓
Application   Error

This creates a boundary between external data and internal application logic.


### Pydantic and Python Type Hints

Pydantic makes extensive use of Python type annotations.

For example:

    name: str

means:

    name should be a string

Similarly:

    age: int

means:

    age should be an integer

And:

    skills: list[str]

means:

    skills should be a list containing strings

This makes Pydantic models easy to understand because the expected structure is visible directly in the model.


### BaseModel

One of the most important concepts in Pydantic is:

    BaseModel

Pydantic models generally inherit from `BaseModel`.

Conceptually:

    BaseModel
        ↓
    Our Model
        ↓
    Validated Data Structure

For example, a candidate model can contain:

    Candidate
    ├── name
    ├── email
    ├── experience_years
    └── skills

The model defines the expected structure of candidate data.


### Pydantic Fields

Every attribute inside a Pydantic model represents a field.

For example:

    Candidate

    name
    email
    phone
    experience_years
    skills

Each field can have a defined type.

Conceptually:

    name
    → string

    email
    → string

    phone
    → string

    experience_years
    → integer

    skills
    → list of strings

This creates a clear data contract.


### Required Fields

Some information is essential.

For example, Hirely may require:

    name
    email

These fields should be required if the application cannot work correctly without them.

Conceptually:

    Candidate
    ├── name → required
    ├── email → required
    └── phone → optional

If a required field is missing, Pydantic can identify the problem during validation.


### Optional Fields

Real-world data is not always complete.

This is especially true for resumes.

One candidate may provide:

    Name
    Email
    Phone
    LinkedIn
    GitHub

Another candidate may provide:

    Name
    Email
    Phone

Therefore, some fields need to be optional.

For example:

    phone → optional
    linkedin → optional
    github → optional

This is important because Hirely should not assume that every resume contains exactly the same information.


### Default Values

Pydantic models can also define default values.

For example, an analysis may have:

    status → pending

If no status is provided when the analysis is created, the application can use:

    pending

The analysis can later move through states such as:

    pending
       ↓
    processing
       ↓
    completed

or:

    pending
       ↓
    processing
       ↓
    failed

This can become useful in Hirely's resume analysis pipeline.


### Data Validation

Validation means checking whether incoming data satisfies the expected rules.

Suppose Hirely expects:

    pages → integer

Valid:

    pages = 3

Potentially invalid:

    pages = "three"

The validation flow becomes:

    Incoming Data
          ↓
       Pydantic
          ↓
       Validation
          ↓
    ┌─────┴─────┐
    ↓           ↓
  Valid       Invalid
    ↓           ↓
Continue     Error

The goal is to detect invalid data as early as possible.


### Type Validation

Pydantic validates data according to the declared types.

For Hirely, we may have:

    score
    → number

    skills
    → list of strings

    experience_years
    → integer

    name
    → string

    projects
    → list of structured objects

This is particularly useful because Hirely will work with complex resume information.


### Type Coercion

Pydantic can perform certain conversions when appropriate.

For example:

    Expected:
    experience_years → int

    Received:
    "3"

Depending on the validation configuration, Pydantic may convert:

    "3"
      ↓
     3

This is called:

> Type coercion

However, automatic conversion should not always be blindly trusted.

For important Hirely data, we need to decide where conversion is acceptable and where stricter validation is required.


### Strict Validation

Sometimes automatic conversion is not desirable.

For example:

    Expected:
    3

    Received:
    "3"

In some situations, we may want to reject the string rather than convert it.

Pydantic provides strict validation capabilities for stronger type enforcement.

Conceptually:

    Normal Validation
    → more flexible validation

    Strict Validation
    → stronger type enforcement


### Nested Models

Real-world application data is rarely flat.

A resume is a perfect example.

A resume can contain:

    Resume
    ├── Personal Information
    ├── Education
    ├── Experience
    ├── Skills
    └── Projects

Each section can contain its own fields.

For example:

    Personal Information
    ├── name
    ├── email
    ├── phone
    ├── linkedin
    └── github

And:

    Education
    ├── degree
    ├── institution
    ├── start_date
    └── end_date

This is called:

> Nested modeling

Pydantic allows complex structures to be represented using nested models.


### Why Nested Models Matter for Hirely

Hirely's resume data will eventually become complex.

A resume is not simply:

    name
    email
    skills

It may contain:

    Personal Information
    Education
    Work Experience
    Skills
    Projects
    Certifications
    Achievements
    Languages

Some sections can contain multiple records.

For example:

    Experience
       ↓
    Experience 1
       ↓
    Experience 2
       ↓
    Experience 3

Therefore, structured models are required instead of one large unorganized object.


### Pydantic and FastAPI

Pydantic has a very close relationship with FastAPI.

Our sequence is:

    FastAPI
       ↓
    REST APIs
       ↓
    Pydantic

FastAPI provides the API framework.

Pydantic provides data modeling and validation.

Conceptually:

    Client
       ↓
    HTTP Request
       ↓
    FastAPI
       ↓
    Pydantic
       ↓
    Validation
       ↓
    Application Logic

This combination is very useful for building structured Python APIs.


### Pydantic Request Models

When a client sends data to Hirely, the backend needs to understand what the request should contain.

For example:

    POST /api/resume/analyze

The request may contain:

    resume_id
    analysis_type

A Pydantic request model can define the expected structure.

Conceptually:

    Frontend
       ↓
    HTTP Request
       ↓
    FastAPI
       ↓
    Pydantic Request Model
       ↓
    Validation
       ↓
    Service Layer

This creates a clear contract between the frontend and backend.


### Pydantic Response Models

Pydantic can also define API response structures.

Suppose Hirely returns:

    resume_id
    score
    strengths
    weaknesses
    recommendations

We want the response to have a predictable structure.

Conceptually:

    Application
       ↓
    Pydantic Response Model
       ↓
    FastAPI
       ↓
    JSON Response
       ↓
    Frontend

This makes the API easier to consume and maintain.


### Request Model vs Response Model

Request and response structures do not always need to be identical.

For example:

    CreateUserRequest

    name
    email
    password

Response:

    UserResponse

    id
    name
    email
    created_at

The password may be required when creating the account but should not be returned in a normal response.

Therefore:

    Request Model
    → what the client sends

    Response Model
    → what the API returns

Separating these models improves API design and security.


### Pydantic and API Contracts

An API needs a predictable contract between frontend and backend.

The frontend should know:

- What fields it can send
- Which fields are required
- What types are expected
- What structure the response will have

Pydantic helps define these structures.

Conceptually:

    Frontend
       ↓
    Request Contract
       ↓
    FastAPI
       ↓
    Pydantic
       ↓
    Application

And:

    Application
       ↓
    Pydantic Response Model
       ↓
    FastAPI
       ↓
    Response Contract
       ↓
    Frontend

This makes communication between frontend and backend more reliable.


### Pydantic and Serialization

Serialization means converting structured application data into a format that can be transmitted or stored.

Conceptually:

    Pydantic Model
          ↓
      Serialization
          ↓
    Dictionary / JSON-compatible Data

Modern Pydantic provides methods such as:

    model_dump()

Conceptually:

    Pydantic Model
          ↓
      model_dump()
          ↓
    Python Dictionary

This is useful when validated data needs to move between different layers of Hirely.


### Pydantic and JSON Schema

Pydantic models can also be represented using JSON Schema.

Conceptually:

    Pydantic Model
          ↓
      JSON Schema
          ↓
    Machine-readable Structure

This can be useful for:

- API documentation
- API contracts
- Schema generation
- Developer tooling
- Client development

This also connects with FastAPI because FastAPI can use Pydantic models when generating API documentation and schemas.


### Pydantic Validation Errors

When data does not satisfy the expected model, Pydantic provides structured validation errors.

For example:

    Missing required field

or:

    Incorrect field type

or:

    Invalid value

Conceptually:

    Incoming Data
          ↓
       Pydantic
          ↓
       Validation
          ↓
    Validation Error
          ↓
      Error Details

This makes it easier to understand what went wrong.


### Pydantic and Document Processing

This connects directly with our previous Hirely research.

We established:

> Document processing and resume parsing are NOT the same thing.

Document processing answers:

> How do we extract the content?

Resume parsing answers:

> What does the extracted content mean?

Pydantic answers:

> Does the resulting structured data match the structure our application expects?

Therefore:

    Resume Upload
          ↓
    File Validation
          ↓
    Document Detection
          ↓
    PDF / DOCX Processing
          ↓
    OCR when required
          ↓
    Text Extraction
          ↓
    Resume Parser
          ↓
    Structured Resume Data
          ↓
    Pydantic Validation
          ↓
    Validated Resume
          ↓
    Resume Analysis

This keeps each component responsible for a specific task.


### Document Processing vs Pydantic

These technologies solve different problems.

Document Processing:

    PDF Processing
    DOCX Processing
    OCR
    Text Extraction
    Document Detection

Pydantic:

    Data Modeling
    Data Validation
    Structured Data
    API Schemas
    Serialization

Therefore:

    Document Processing
    → extracts content

    Resume Parser
    → structures information

    Pydantic
    → validates the structure

    Analysis
    → analyzes the validated information


### Pydantic and Resume Parser Output

Suppose our resume parser produces:

    {
        "name": "Candidate",
        "email": "candidate@example.com",
        "skills": ["Python", "SQL"],
        "experience": []
    }

The parser has produced structured information.

But we still need to verify that the structure matches what Hirely expects.

Therefore:

    Resume
       ↓
    Document Processing
       ↓
    Text
       ↓
    Resume Parser
       ↓
    Structured Resume Data
       ↓
    Pydantic
       ↓
    Validated Resume
       ↓
    Resume Analysis

This separates:

    Extraction
    Parsing
    Validation
    Analysis


### Pydantic and AI / LLMs

This will become one of the most important future uses of Pydantic in Hirely.

Later, Hirely will use AI / LLMs for:

- Resume analysis
- Skill analysis
- Job matching
- Recommendations
- Resume improvement

Suppose an AI model produces:

    {
        "score": 82,
        "skills": ["Python", "SQL"],
        "strengths": [
            "Strong programming background"
        ],
        "weaknesses": [
            "Limited cloud experience"
        ],
        "recommendations": [
            "Improve cloud knowledge"
        ]
    }

Hirely expects a defined structure.

Pydantic can validate that structure before the rest of the application uses it.

The flow becomes:

    Resume
       ↓
    AI / LLM
       ↓
    Generated Output
       ↓
    Pydantic
       ↓
    Validation
       ↓
    Validated Analysis
       ↓
    Application


### AI Output Should Not Be Automatically Trusted

An AI model can generate output that looks structured but is still incorrect.

For example, Hirely may expect:

    score → integer

but the AI may produce:

    score → "excellent"

Pydantic can identify the structural/type problem.

However, if the AI produces:

    score → 82

Pydantic can determine that 82 is structurally valid as an integer.

But Pydantic cannot determine whether 82 is actually the correct score.

Therefore:

    Pydantic
    → structural validation

    Business Logic / Evidence / Evaluation
    → semantic validation

This distinction will be extremely important when we build Hirely's AI layer.


### Pydantic Does Not Solve AI Hallucination

Pydantic is not an AI hallucination detector.

Suppose an LLM generates:

    company = Google
    position = Senior Software Engineer

Pydantic can validate:

    company
    → string

    position
    → string

But it cannot determine whether the candidate actually worked at Google.

Therefore:

    Pydantic
    → validates structure

    Other systems
    → verify meaning / truth

This means:

> Pydantic provides structural validation, not complete semantic validation.


### Pydantic and Structured AI Output

Hirely may eventually require an AI result such as:

    AnalysisResult
    ├── overall_score
    ├── strengths
    ├── weaknesses
    ├── missing_skills
    ├── recommendations
    └── job_match

Expected structures could be:

    overall_score
    → number

    strengths
    → list of strings

    weaknesses
    → list of strings

    missing_skills
    → list of strings

    recommendations
    → list of strings

This makes AI output easier for the application to consume.

The principle is:

    LLM
      ↓
    Generate
      ↓
    Pydantic
      ↓
    Validate
      ↓
    Application


### Pydantic vs Database Models

A very important distinction is:

    Pydantic Model
    ≠
    Database Model

Pydantic mainly deals with:

    Data Validation
    Data Modeling
    API Schemas
    Serialization
    Structured Application Data

The database layer deals with:

    Tables
    Relationships
    Queries
    Persistence
    Database Operations

This distinction will become important when we research SQLAlchemy.


### Pydantic vs SQLAlchemy

The roles are different.

Pydantic:

    Data Validation
    Data Modeling
    API Schemas
    Serialization

SQLAlchemy:

    Database Interaction
    ORM
    Queries
    Persistence
    Database Models

Conceptual Hirely architecture:

    Frontend
       ↓
    FastAPI
       ↓
    Pydantic
       ↓
    Application Logic
       ↓
    SQLAlchemy
       ↓
    Database

Therefore:

    Pydantic
    → validates application data

    SQLAlchemy
    → interacts with the database

They work together but solve different problems.


### Pydantic Is Not an ORM

ORM means:

> Object Relational Mapping

An ORM maps application objects to database structures.

Pydantic is not an ORM.

Pydantic focuses on:

    Validation
    Modeling
    Serialization

SQLAlchemy focuses on:

    Database
    ORM
    Queries
    Persistence

Therefore:

    Pydantic
    ≠
    SQLAlchemy


### Pydantic and Maintainability

Pydantic can improve maintainability.

Imagine Hirely has:

    Resume Service
    AI Service
    API Service
    Database Service

Without shared models, different services may interpret the same data differently.

For example:

    Resume Service
    skills → list

    AI Service
    skills → string

    API Service
    skills → dictionary

This creates inconsistency.

A shared Pydantic model can provide a common contract.

Conceptually:

                 Resume Model
                      ↓
          ┌───────────┼───────────┐
          ↓           ↓           ↓
        Parser        API         AI

This improves consistency between different components.


### Pydantic and Modularity

Pydantic should have a focused responsibility.

    FastAPI
    → API Framework

    Pydantic
    → Data Validation / Modeling

    Document Processing
    → Document Handling

    Resume Parser
    → Resume Information Extraction / Structuring

    AI Service
    → AI / LLM Interaction

    SQLAlchemy
    → Database Interaction

Each component has a clear responsibility.

This supports the modular architecture we are building for Hirely.


### Pydantic at Data Boundaries

One of the strongest architectural uses of Pydantic is at important data boundaries.

Potential Hirely boundaries include:

    Frontend
       ↓
    Pydantic

    Resume Parser
       ↓
    Pydantic

    AI / LLM
       ↓
    Pydantic

    External Service
       ↓
    Pydantic

The general principle is:

> Validate data when it enters an important application boundary.

This prevents unexpected structures from spreading throughout the system.


### Hirely Resume Data Flow

Our current conceptual resume pipeline is:

    Resume Upload
          ↓
    File Validation
          ↓
    Document Detection
          ↓
    PDF / DOCX Processing
          ↓
    OCR when required
          ↓
    Text Extraction
          ↓
    Resume Parser
          ↓
    Structured Resume Data
          ↓
    Pydantic Validation
          ↓
    Validated Resume
          ↓
    Resume Analysis

Notice the separation:

    Document Processing
    → extracts content

    Resume Parsing
    → structures content

    Pydantic
    → validates structure

    Analysis
    → analyzes validated information


### Hirely AI Data Flow

When AI is introduced:

    Validated Resume
          ↓
       AI / LLM
          ↓
    Generated Analysis
          ↓
    Pydantic Validation
          ↓
    Validated Analysis
          ↓
    Application Logic
          ↓
    API Response

This is important because LLM output is probabilistic while the rest of the application needs predictable structures.


### Pydantic and Business Logic

Another important distinction is:

    Pydantic
    → What shape should the data have?

    Business Logic
    → What should the application do with the data?

For example, Pydantic can validate:

    score → integer

Business logic can decide:

    score >= 80
    → Strong Match

    score >= 60
    → Moderate Match

    score < 60
    → Weak Match

Therefore, business decisions should remain in the application/service layer rather than being mixed into basic data modeling.


### Pydantic and Security

Pydantic is not a complete security framework.

However, carefully designed models can help control what information is accepted and exposed.

Imagine an internal user object contains:

    id
    name
    email
    password_hash
    created_at

But the API response should contain:

    id
    name
    email
    created_at

The sensitive field:

    password_hash

should not be exposed through a normal response.

However:

    Pydantic ≠ Authentication
    Pydantic ≠ Authorization
    Pydantic ≠ Complete Security

Security will be researched separately.


### Advantages of Pydantic

Pydantic provides several important advantages for Hirely:

- Clear data models
- Data validation
- Type-based structure
- FastAPI integration
- Nested models
- Serialization
- API contracts
- Structured AI output validation
- Better maintainability
- Consistent data structures
- Clear boundaries between components


### Limitations of Pydantic

Pydantic is powerful, but it does not solve every application problem.

Pydantic does not replace:

    Authentication
    Authorization
    Database Management
    Document Processing
    OCR
    AI Reasoning
    Business Logic
    Complete Security
    Semantic Truth Verification

For example:

Pydantic can validate:

    score → integer

But it cannot determine:

    Is this score actually correct?

Pydantic can validate:

    company → string

But it cannot determine:

    Did the candidate actually work at that company?

Therefore:

> Pydantic provides structural validation, not complete semantic validation.


### Hirely Pydantic Architecture

The current conceptual architecture is:

                    External Data
                         │
                         ↓
                     Pydantic
                         │
                     Validation
                         │
                         ↓
                  Structured Data
                         │
                         ↓
                Application Services
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
           Resume        AI      Database
           Services    Services     Layer
              ↓          ↓          ↓
            Parser       LLM    SQLAlchemy

The key principle is:

    Validate
       ↓
    Structure
       ↓
    Process


### Final Decision for Hirely

Based on our research, Pydantic will be used as the **data validation and data modeling layer for Hirely**.

The main reasons are:

- Hirely requires structured data models.
- Hirely receives data from multiple sources.
- API requests require predictable structures.
- API responses should follow defined schemas.
- Resume parser output needs a predictable structure.
- AI-generated structured output should be validated.
- Pydantic integrates naturally with FastAPI.
- Python type annotations fit naturally into the backend.
- Shared models improve consistency.
- Pydantic creates a clear boundary between external data and application logic.

The exact implementation details will be decided during the development phase.


### Key Takeaways

Remember Pydantic using this simple flow:

    External / Untrusted Data
              ↓
           Pydantic
              ↓
           Validate
              ↓
        Structured Data
              ↓
       Application Logic

For Hirely:

    Frontend
       ↓
    FastAPI
       ↓
    Pydantic
       ↓
    Application
       ↓
    ┌───────────────┬────────────────┬────────────────┐
    ↓               ↓                ↓
    Resume          AI           Database
    Processing    Services          Layer
    ↓               ↓                ↓
    Parser          LLM         SQLAlchemy
    ↓               ↓
    Pydantic        Pydantic
    Validation      Validation

The most important idea is:

> **Pydantic defines the structure Hirely expects and validates data before important application logic uses it.**

## 7.4 SQLAlchemy

### Background

After understanding FastAPI, REST APIs, and Pydantic, the next requirement for Hirely is the database layer.

Hirely will need to store and retrieve many types of information, such as:

- Users
- Resumes
- Resume metadata
- Education
- Work experience
- Skills
- Projects
- Jobs
- Applications
- Resume analyses
- Recommendations
- Analysis history

The backend needs a reliable way to communicate with the database.

Conceptually:

    Hirely Backend
          ↓
    Database Layer
          ↓
       Database

This is where SQLAlchemy becomes important.


### What is SQLAlchemy?

**SQLAlchemy is a Python SQL toolkit and Object Relational Mapper (ORM).**

In simple terms:

> SQLAlchemy allows a Python application to interact with a relational database in a structured way.

Conceptually:

    Python Application
          ↓
      SQLAlchemy
          ↓
       Database

SQLAlchemy provides tools for:

- Database connections
- SQL queries
- Database models
- Relationships
- CRUD operations
- Transactions
- ORM-based database interaction


### Why do we need SQLAlchemy?

A backend application needs to perform many database operations.

For Hirely, these may include:

- Creating users
- Retrieving users
- Storing resumes
- Retrieving resumes
- Updating resume information
- Storing analysis results
- Retrieving analysis history
- Managing relationships between entities

Without a proper database layer, database operations can become scattered throughout the application.

Conceptually:

    Application
          ↓
      SQL Queries
          ↓
       Database

As the project grows, this can become difficult to maintain.

SQLAlchemy provides a structured layer between the application and the database:

    Application
          ↓
      SQLAlchemy
          ↓
       Database


### What is ORM?

ORM stands for:

> **Object Relational Mapping**

An ORM connects application objects with relational database structures.

Python works with:

    Objects

Relational databases work with:

    Tables
    Rows
    Columns
    Relationships

ORM creates a mapping between them.

Conceptually:

    Python World              Database World

    User Object       ↔       users Table

    Resume Object     ↔       resumes Table

    Job Object        ↔       jobs Table

    Analysis Object   ↔       analyses Table

Therefore:

> ORM allows the application to work with database entities using programming-language objects instead of dealing with database structures everywhere.


### SQLAlchemy Models

A SQLAlchemy model represents a database entity in the Python application.

For Hirely, possible models include:

    User
    Resume
    Education
    Experience
    Skill
    Project
    Job
    Application
    Analysis

For example:

    User Model
        ↓
    users Table

    Resume Model
        ↓
    resumes Table

    Analysis Model
        ↓
    analyses Table

This creates a clear relationship between the application's data models and the database structure.


### Model vs Database Table

It is important to understand the difference.

A model exists in the Python application:

    User
    ├── id
    ├── name
    ├── email
    └── created_at

The database contains the corresponding table:

    users
    ├── id
    ├── name
    ├── email
    └── created_at

SQLAlchemy provides the mapping:

    Python Model
          ↕
      SQLAlchemy
          ↕
    Database Table


### Database Columns

A database table contains columns.

For example:

    users

    id
    name
    email
    created_at

Each column has a data type.

Conceptually:

    id
    → Integer

    name
    → String

    email
    → String

    created_at
    → DateTime

SQLAlchemy allows these database columns to be represented in Python models.


### Primary Key

A primary key uniquely identifies a database record.

For example:

    users

    id | name
    ---|------
    1  | Ali
    2  | Ahmed
    3  | John

Here:

    id

is the primary key.

For Hirely:

    User
      ↓
    id → Primary Key

Similarly:

    Resume
      ↓
    id → Primary Key

    Analysis
      ↓
    id → Primary Key

Primary keys are important because other database records may need to reference them.


### Foreign Key

A foreign key creates a connection between database tables.

For example:

    users

    id | name
    ---|------
    1  | Ali
    2  | Ahmed

And:

    resumes

    id | user_id | file_name
    ---|---------|-----------
    1  | 1       | resume.pdf
    2  | 1       | resume2.pdf
    3  | 2       | cv.pdf

Here:

    resumes.user_id

references:

    users.id

Conceptually:

    users.id
        ↑
        │
    resumes.user_id

This allows the database to represent relationships between entities.


### Why Foreign Keys Matter for Hirely

A user can have multiple resumes.

For example:

    User
      │
      ├── Resume 1
      ├── Resume 2
      └── Resume 3

The database needs to know which user owns each resume.

This can be represented through:

    resumes.user_id
          ↓
       users.id

Therefore, foreign keys are important for maintaining relationships between Hirely's entities.


### Relationships

Hirely will contain many related entities.

For example:

    User
      ↓
    Resumes
      ↓
    Analyses

And:

    Resume
      ↓
    Skills

And:

    Resume
      ↓
    Experience

SQLAlchemy allows these database relationships to be represented in the application's models.


### One-to-Many Relationship

One-to-many means:

> One record is associated with multiple records.

For Hirely:

    One User
       ↓
    Multiple Resumes

Conceptually:

    User
      │
      ├── Resume 1
      ├── Resume 2
      └── Resume 3

Another possible relationship is:

    One Resume
       ↓
    Multiple Analyses

For example:

    Resume
      │
      ├── Analysis 1
      ├── Analysis 2
      └── Analysis 3


### Many-to-One Relationship

The same relationship can be viewed from the opposite direction.

For example:

    Resume 1 ──┐
    Resume 2 ──┼──→ User
    Resume 3 ──┘

Many resumes belong to one user.

Therefore:

    User
    → One

    Resume
    → Many


### Many-to-Many Relationship

Many-to-many means:

> Multiple records on one side can be associated with multiple records on the other side.

Skills are a good example.

One candidate can have:

    Python
    SQL
    FastAPI

And one skill can belong to many candidates.

Conceptually:

    Candidate
         ↕
       Skills

A relational database normally represents this using an association table:

    candidates
         ↓
    candidate_skills
         ↓
       skills

This allows Hirely to represent candidate-skill relationships efficiently.


### CRUD Operations

CRUD is a fundamental database concept.

CRUD stands for:

    C → Create
    R → Read
    U → Update
    D → Delete

Hirely will require all four operations.


### Create

Create means inserting new data.

Examples:

    Create User
    Create Resume
    Create Job
    Create Analysis

Conceptually:

    Application
        ↓
    SQLAlchemy
        ↓
    Database


### Read

Read means retrieving existing data.

Examples:

    Get User
    Get Resume
    Get Analysis
    Get Job

Conceptually:

    Database
        ↓
    SQLAlchemy
        ↓
    Application


### Update

Update means modifying existing information.

Examples:

    Update User Profile
    Update Resume Metadata
    Update Job
    Update Analysis Status


### Delete

Delete means removing data.

Examples:

    Delete Resume
    Delete Job
    Delete User

Deletion needs to be designed carefully when related records exist.

For example:

    User
      ↓
    Resumes
      ↓
    Analyses

If a user is deleted, Hirely needs a clear policy for what happens to the related records.


### SQLAlchemy Session

The **Session** is an important SQLAlchemy concept.

It provides a workspace through which the application performs database operations.

Conceptually:

    Application
          ↓
        Session
          ↓
       Database

The Session can be involved in:

- Reading data
- Adding records
- Updating records
- Deleting records
- Committing changes
- Rolling back changes

It also plays an important role in transaction management.


### Transactions

A transaction represents a logical unit of database work.

For example, Hirely may need to:

    Create Analysis
          ↓
    Store Analysis Result
          ↓
    Update Analysis Status

These operations may need to succeed together.

Conceptually:

    Begin Transaction
          ↓
    Operation A
          ↓
    Operation B
          ↓
    Operation C
          ↓
    Commit

If something fails:

    Error
      ↓
    Rollback

This helps maintain database consistency.


### Commit

Commit confirms the changes made during a transaction.

Conceptually:

    Application
        ↓
      Session
        ↓
      Commit
        ↓
     Database

After the transaction is committed, the changes become persistent in the database.


### Rollback

Rollback reverses uncommitted changes from the current transaction.

Conceptually:

    Database Operation
          ↓
        Error
          ↓
      Rollback
          ↓
    Previous Consistent State

This is important when multiple related database operations are performed together.


### SQLAlchemy and FastAPI

SQLAlchemy fits naturally into the backend architecture we have already designed.

Our architecture becomes:

    Client
       ↓
    FastAPI
       ↓
    Pydantic
       ↓
    Service Layer
       ↓
    SQLAlchemy
       ↓
    Database

Each component has a different responsibility.

    FastAPI
    → API / HTTP handling

    Pydantic
    → Data validation and schemas

    Service Layer
    → Business logic

    SQLAlchemy
    → Database interaction

    Database
    → Persistent storage


### Pydantic vs SQLAlchemy

This distinction is extremely important.

Pydantic:

    Data Validation
    Data Modeling
    API Request Schemas
    API Response Schemas
    Serialization

SQLAlchemy:

    Database Models
    Database Queries
    Relationships
    Transactions
    Persistence
    ORM

Therefore:

    Pydantic
       ↓
    Validates application data

    SQLAlchemy
       ↓
    Stores and retrieves application data


### Pydantic Model vs SQLAlchemy Model

Pydantic models and SQLAlchemy models may represent similar information, but they have different purposes.

Pydantic model:

    API / Application Data
          ↓
    Validation
          ↓
    Structured Data

SQLAlchemy model:

    Application Data
          ↓
    Database Mapping
          ↓
    Database Table

Conceptually:

    API Request
        ↓
    Pydantic
        ↓
    Service Layer
        ↓
    SQLAlchemy
        ↓
    Database


### SQLAlchemy and Hirely Users

A user registration flow may look like:

    User Registration
          ↓
    FastAPI
          ↓
    Pydantic
          ↓
    User Service
          ↓
    SQLAlchemy
          ↓
    Users Table

When retrieving the user:

    Users Table
          ↓
    SQLAlchemy
          ↓
    User Service
          ↓
    Pydantic
          ↓
    FastAPI
          ↓
    Frontend


### SQLAlchemy and Hirely Resumes

Resume information can follow:

    Resume Upload
          ↓
    Document Processing
          ↓
    Resume Parser
          ↓
    Structured Resume Data
          ↓
    Pydantic Validation
          ↓
    Resume Service
          ↓
    SQLAlchemy
          ↓
    Database

The database can store resume-related information such as:

    resume_id
    user_id
    file_name
    file_type
    storage_reference
    created_at


### SQLAlchemy and Resume Analysis

Hirely will also need to store analysis results.

Conceptually:

    Resume
       ↓
    AI Analysis
       ↓
    Structured Analysis
       ↓
    Pydantic Validation
       ↓
    SQLAlchemy
       ↓
    Analysis Table

This allows Hirely to maintain analysis history and retrieve previous results.


### SQLAlchemy and AI

Later, Hirely will use AI / LLMs for:

- Resume analysis
- Skill analysis
- Job matching
- Recommendations
- Resume improvement

The flow can become:

    Resume
       ↓
    AI / LLM
       ↓
    Structured Output
       ↓
    Pydantic
       ↓
    Validation
       ↓
    SQLAlchemy
       ↓
    Database

This separates AI generation from database persistence.


### SQLAlchemy and Database Security

Database credentials should not be hardcoded directly into the source code.

Configuration should be managed through environment variables or another secure configuration mechanism.

Conceptually:

    Environment
          ↓
    Database Configuration
          ↓
    SQLAlchemy
          ↓
    Database

For example:

    DATABASE_URL

can contain the database connection configuration.

Sensitive credentials should be protected properly.


### SQLAlchemy and Database Performance

As Hirely grows, database performance will become important.

Important areas include:

- Efficient queries
- Indexes
- Pagination
- Connection pooling
- Relationship loading
- Transactions
- Proper database design

SQLAlchemy provides tools for these areas, but efficient database design and query design are still the developer's responsibility.


### SQLAlchemy and Database Migrations

Database schemas change as applications evolve.

For example:

Initial:

    users
    ├── id
    ├── name
    └── email

Later:

    users
    ├── id
    ├── name
    ├── email
    └── created_at

We need a controlled way to apply database schema changes.

For SQLAlchemy-based applications, **Alembic** is commonly used for database migrations.

Conceptually:

    SQLAlchemy Models
          ↓
    Schema Changes
          ↓
    Alembic Migration
          ↓
    Database


### SQLAlchemy and Hirely Architecture

Our current backend architecture is:

    Frontend
       ↓
    FastAPI
       ↓
    REST API
       ↓
    Pydantic
       ↓
    Service / Business Logic
       ↓
    SQLAlchemy
       ↓
    Relational Database

For the resume system:

    Resume Upload
          ↓
    Document Processing
          ↓
    Resume Parser
          ↓
    Pydantic
          ↓
    Resume Service
          ↓
    SQLAlchemy
          ↓
    Database

For AI analysis:

    Stored Resume
          ↓
    AI / LLM
          ↓
    Pydantic
          ↓
    Analysis Service
          ↓
    SQLAlchemy
          ↓
    Database


### SQLAlchemy Does Not Replace Other Technologies

SQLAlchemy has a specific responsibility.

It does not replace:

    FastAPI
    Pydantic
    Business Logic
    Authentication
    Authorization
    Document Processing
    OCR
    AI / LLM
    Database

Instead, it works together with them.

Conceptually:

    FastAPI
    → API

    Pydantic
    → Validation

    Business Logic
    → Application Decisions

    SQLAlchemy
    → Database Interaction

    Database
    → Persistent Storage


### Final Decision for Hirely

Based on our research, SQLAlchemy will be used as the **database interaction and ORM layer for Hirely**.

The main reasons are:

- Python integration
- ORM support
- Database model mapping
- Relationship management
- CRUD operations
- Transaction support
- Query construction
- Maintainable database architecture
- Strong integration with the Python backend ecosystem

The database layer will remain separate from the API and validation layers.

Our conceptual architecture is:

    FastAPI
       ↓
    Pydantic
       ↓
    Business Logic
       ↓
    SQLAlchemy
       ↓
    Database


### Key Takeaways

Remember SQLAlchemy using this simple idea:

> **SQLAlchemy connects our Python application with the relational database.**

The most important distinction is:

    Pydantic
    → Validates and structures data

    SQLAlchemy
    → Interacts with the database

And the Hirely backend architecture is:

    Frontend
       ↓
    FastAPI
       ↓
    Pydantic
       ↓
    Business Logic
       ↓
    SQLAlchemy
       ↓
    Database

For Hirely specifically:

    User
       ↓
    Resume
       ↓
    Analysis
       ↓
    Recommendations

SQLAlchemy will provide the database layer required to store and retrieve these entities and their relationships.

## 7.5 Async Programming

### Background

Modern backend applications frequently perform operations that involve waiting.

Examples include:

- Database operations
- API requests
- Network requests
- LLM API calls
- File operations
- External services

Hirely will perform several of these operations.

For example:

    User
      ↓
    FastAPI
      ↓
    Resume Analysis
      ↓
    LLM API
      ↓
    Wait for Response
      ↓
    Continue Processing

During the waiting period, the application may be able to handle other work.

This is where asynchronous programming becomes useful.


### What is Async Programming?

**Asynchronous programming** is a programming approach that allows an application to handle waiting operations without unnecessarily blocking the execution of other available work.

The basic idea is:

> Do not unnecessarily block the application while waiting for an I/O operation to complete.

Conceptually:

    Request A
       ↓
    Waiting for Database
       │
       ├────────→ Request B
       │             ↓
       │        Other Work
       │
       ←─────────────┘

Asynchronous programming is especially useful for applications that perform many I/O-bound operations.


### Synchronous Programming

In synchronous execution, operations generally happen sequentially.

For example:

    Request A
       ↓
    Database Operation
       ↓
    Wait
       ↓
    Response A
       ↓
    Request B
       ↓
    Database Operation
       ↓
    Response B

If the application spends significant time waiting for an external operation, other work may be delayed depending on the execution model.


### Asynchronous Programming

With asynchronous execution, an application can make progress on other available tasks while an I/O operation is waiting.

Conceptually:

    Request A
       ↓
    Start I/O Operation
       ↓
    Waiting...
    
    Request B
       ↓
    Start Other Work
       ↓
    Continue
    
    I/O Operation Completes
       ↓
    Continue Request A

This allows the application to use its execution time more efficiently for I/O-heavy workloads.


### I/O-Bound Operations

An I/O-bound operation is an operation where the application spends significant time waiting for something outside the CPU.

Common examples include:

- Database operations
- Network requests
- HTTP requests
- External APIs
- LLM API calls
- File I/O

These operations are important for Hirely because the application will communicate with databases and external AI services.


### CPU-Bound Operations

A CPU-bound operation requires significant CPU computation.

Examples include:

- Heavy mathematical calculations
- Large computational workloads
- Complex data processing
- Certain machine learning operations
- Intensive image processing

Async programming by itself does not automatically make CPU-bound work faster.

Therefore:

    I/O-Bound
       ↓
    Async can be useful

    CPU-Bound
       ↓
    Async alone is generally not the solution


### Why Async Programming is Important for Hirely

Hirely will perform several I/O-heavy operations.

For example:

    User Request
          ↓
    FastAPI
          ↓
    Resume Analysis
          ↓
    LLM API Request
          ↓
    Wait for LLM Response
          ↓
    Continue Processing

The LLM request involves network communication and waiting.

Other examples include:

    FastAPI Requests
    Database Operations
    LLM API Calls
    External APIs
    Network Requests
    File Operations

Asynchronous programming can therefore help Hirely handle I/O-bound workloads efficiently.


### Async Programming and FastAPI

FastAPI supports asynchronous endpoints.

Conceptually:

    Client
       ↓
    FastAPI
       ↓
    Async Endpoint
       ↓
    Async I/O
       ↓
    Response

An endpoint can be defined as an asynchronous function.

The important Python keyword is:

    async def

For example:

    async def analyze_resume():
        ...

This allows the function to participate in Python's asynchronous execution model.


### The `async` Keyword

The `async` keyword is used to define an asynchronous function.

Conceptually:

    async def function():
        ...

An asynchronous function can use asynchronous operations with `await`.

However:

> Simply using `async def` does not automatically make every operation inside the function asynchronous.

The operations being performed must also support asynchronous execution.


### The `await` Keyword

The `await` keyword is used to wait for an asynchronous operation.

Conceptually:

    result = await some_operation()

The idea is:

> Wait for this asynchronous operation while allowing the asynchronous execution system to make progress on other available work.

For example:

    Request A
       ↓
    await LLM request
       ↓
    Waiting...
       ↓
    Other tasks can make progress
       ↓
    LLM response arrives
       ↓
    Continue Request A


### Event Loop

The **event loop** is a central part of Python's asynchronous programming model.

A simplified representation is:

    Event Loop
        │
        ├── Task A
        ├── Task B
        └── Task C

When one task is waiting for an I/O operation, the event loop can allow another task to make progress.

Conceptually:

    Task A
       ↓
    Waiting for I/O
       ↓
    Event Loop
       ↓
    Task B
       ↓
    Other Work

When the I/O operation completes, the event loop can continue the waiting task.


### Async Programming and Concurrency

Asynchronous programming is mainly useful for achieving efficient **concurrency**.

Concurrency means multiple tasks can make progress over overlapping periods.

Conceptually:

    Task A
       ↓
    Waiting
       ↓
    Task B
       ↓
    Working
       ↓
    Task A Continues

This is different from automatically executing multiple CPU operations simultaneously.


### Async is Not the Same as Parallelism

Async programming should not be confused with parallelism.

**Concurrency:**

    Multiple tasks
          ↓
    Make progress over overlapping periods

**Parallelism:**

    Multiple computations
          ↓
    Execute simultaneously

For Hirely, the primary benefit of async programming is:

    Concurrency
        ↓
    Efficient I/O handling


### Async LLM Requests

LLM communication is an important use case for Hirely.

A resume analysis may involve:

    Resume
       ↓
    Prepare Prompt
       ↓
    LLM API Request
       ↓
    Wait
       ↓
    LLM Response
       ↓
    Validate Result

The LLM API request is a network operation.

An asynchronous implementation can use:

    await LLM Request

This allows the application to handle other available work while waiting for the external service.


### Async Database Operations

Database operations can also involve waiting.

For example:

    FastAPI
       ↓
    Service Layer
       ↓
    Database Query
       ↓
    Wait
       ↓
    Database Result

If the database access library supports asynchronous operations, the application can use asynchronous database access.

Conceptually:

    FastAPI
       ↓
    Async Service
       ↓
    Async SQLAlchemy
       ↓
    Async Database Driver
       ↓
    PostgreSQL


### Async HTTP Requests

Hirely may communicate with external services.

For example:

    Hirely
       ↓
    External API

Network communication involves waiting:

    HTTP Request
        ↓
    Network
        ↓
    Wait
        ↓
    Response

Asynchronous HTTP clients can allow the application to perform other available work while waiting for network responses.


### Async File Operations

Document processing may also involve file operations.

For example:

    Resume Upload
          ↓
    Read File
          ↓
    Process Document

Some file operations can be handled asynchronously depending on the library and implementation.

However:

> Not every file operation automatically needs to be asynchronous.

Async should be used where it provides practical value.


### Async Libraries

An important architectural principle is that an `async` function should use asynchronous-compatible operations where appropriate.

For example:

    Async Function
         ↓
    Async Database Operation
         ↓
    Async HTTP Request

Simply writing:

    async def

around blocking synchronous code does not automatically make the operation non-blocking.

Therefore:

> Async programming requires appropriate async-compatible libraries and operations.


### Async and SQLAlchemy

SQLAlchemy can be used in asynchronous applications when configured with appropriate asynchronous database support.

Conceptually:

    FastAPI
       ↓
    Async Service
       ↓
    Async SQLAlchemy
       ↓
    Async Database Driver
       ↓
    Database

This connects the two backend technologies already researched:

    FastAPI
       ↓
    Async Programming
       ↓
    SQLAlchemy
       ↓
    Database


### Async and Pydantic

Pydantic itself is primarily responsible for data validation and structured data.

Async programming handles the execution model for I/O-bound operations.

Therefore:

    FastAPI
       ↓
    Async Request Handling
       ↓
    Pydantic
       ↓
    Business Logic
       ↓
    Async Database / APIs

Pydantic and async programming have different responsibilities but work together within the backend.


### Async Hirely Resume Analysis Flow

A future Hirely resume analysis request may follow:

    User
       ↓
    FastAPI
       ↓
    Pydantic Validation
       ↓
    Resume Service
       ↓
    Async Database Request
       ↓
    Resume Data
       ↓
    Prepare AI Context
       ↓
    Async LLM Request
       ↓
    AI Response
       ↓
    Pydantic Validation
       ↓
    SQLAlchemy
       ↓
    Database
       ↓
    FastAPI Response
       ↓
    User

Important asynchronous operations may include:

- Database requests
- LLM API requests
- External API requests
- Network operations


### Where Async Should Be Used in Hirely

Good candidates for asynchronous programming include:

- LLM API calls
- External API calls
- Database operations
- Network requests
- Other I/O-bound operations

Potentially:

- File I/O

depending on the selected implementation and libraries.


### Where Async Should Not Automatically Be Used

Not every function in Hirely needs to be asynchronous.

Examples include:

- Simple calculations
- Basic validation
- Small data transformations
- Simple deterministic business logic

The goal should not be:

    Make Everything Async

Instead:

> **Use asynchronous programming where it provides practical benefits, especially for I/O-bound operations.**


### Async and Blocking Operations

A major consideration is blocking code.

For example:

    async def function():
        synchronous_blocking_operation()

Although the function is declared with `async def`, the blocking operation can still block execution.

Therefore:

    async def
        ≠
    Everything is automatically asynchronous

The underlying operations must support asynchronous execution when non-blocking behavior is required.


### Async and Hirely Backend Architecture

The backend architecture can be represented as:

    Frontend
       ↓
    FastAPI
       ↓
    Async API Handling
       ↓
    Pydantic
       ↓
    Service / Business Logic
       ↓
    Async Database / External Services
       ↓
    SQLAlchemy / HTTP Clients
       ↓
    Database / External APIs

This architecture is suitable for an application that performs multiple I/O-heavy operations.


### Async Programming and Scalability

As Hirely grows, the backend may need to handle multiple users and requests simultaneously.

For example:

    User A
       ↓
    Resume Analysis

    User B
       ↓
    Resume Analysis

    User C
       ↓
    Resume Analysis

Each request may involve waiting for:

    Database
    LLM
    External API

Async programming can help the backend efficiently manage these waiting periods.

However, async programming alone does not guarantee scalability.

Scalability also depends on:

- Database design
- Query efficiency
- Application architecture
- Infrastructure
- Caching
- External service limits
- Resource management


### Async Programming Limitations

Async programming is useful, but it is not a universal performance solution.

Important limitations include:

- It does not automatically speed up CPU-heavy operations.
- Blocking code can still block an async application.
- Async-compatible libraries may be required.
- Poorly designed async code can become difficult to understand.
- Async does not automatically mean parallel execution.
- Database and external-service limitations still apply.

Therefore, async should be introduced where it solves a real problem.


### Decision for Hirely

Based on the research, **Hirely will use asynchronous programming for appropriate I/O-bound backend operations**.

The primary candidates are:

- Database operations
- LLM API calls
- External API requests
- Network operations

FastAPI's asynchronous capabilities will be used where appropriate.

The architecture will follow the principle:

    Use Async Where I/O Waiting Matters

rather than making every function asynchronous without a practical reason.


### Hirely Backend Architecture

The current backend architecture becomes:

    Frontend
       ↓
    FastAPI
       ↓
    Async Request Handling
       ↓
    Pydantic
       ↓
    Service / Business Logic
       ↓
    SQLAlchemy
       ↓
    Database

For AI-powered operations:

    Resume
       ↓
    Async Service
       ↓
    LLM API
       ↓
    Structured Output
       ↓
    Pydantic
       ↓
    SQLAlchemy
       ↓
    Database


### Key Takeaways

The most important concepts are:

    async def
    → Defines an asynchronous function

    await
    → Waits for an asynchronous operation

    Event Loop
    → Coordinates asynchronous tasks

    I/O-Bound
    → Good candidate for async programming

    CPU-Bound
    → Async alone is generally not the solution

    Async
    → Primarily helps with concurrency and I/O efficiency

    Async ≠ Parallelism
    → They are different concepts

    async def ≠ Automatically Async
    → Underlying operations must support asynchronous execution


### Final Concept

The core idea for Hirely is:

> **Asynchronous programming allows Hirely to handle I/O-bound operations efficiently without unnecessarily blocking the application while waiting for external operations to complete.**

The main Hirely architecture is:

    FastAPI
       ↓
    Async Programming
       ↓
    Pydantic
       ↓
    Business Logic
       ↓
    SQLAlchemy
       ↓
    Database

And for AI operations:

    FastAPI
       ↓
    Async Service
       ↓
    LLM API
       ↓
    Pydantic
       ↓
    SQLAlchemy
       ↓
    Database

# 8 Frontend Technologies

## 8.1 Streamlit

### Background

Hirely needs a frontend through which users can interact with the application.

The frontend will eventually need to support interactions such as:

- Uploading a resume
- Providing job-related information
- Starting resume analysis
- Viewing resume scores
- Viewing extracted skills
- Viewing analysis results
- Viewing recommendations

Since Hirely is being developed primarily with Python-based technologies, Streamlit is one of the frontend technologies worth researching.

Streamlit is a Python framework for creating interactive web applications, particularly for data science, machine learning, and AI applications.

The basic idea is:

    Python Code
        ↓
    Streamlit
        ↓
    Interactive Web Application


### What is Streamlit?

**Streamlit is an open-source Python framework for building interactive web applications using Python.**

Instead of requiring developers to build a traditional frontend using separate HTML, CSS, and JavaScript technologies, Streamlit allows much of the interface to be created directly from Python.

Conceptually:

    Python
       ↓
    Streamlit
       ↓
    Web Interface

This makes Streamlit particularly useful for quickly creating interfaces around Python-based data and AI applications.


### Why Streamlit is Relevant to Hirely

Hirely is an AI-focused application.

The application will need a user interface for workflows such as:

    User
      ↓
    Upload Resume
      ↓
    Analyze Resume
      ↓
    AI Processing
      ↓
    Display Results

Streamlit can provide a relatively simple way to create this type of interface while keeping frontend development within the Python ecosystem.

This makes it a candidate for Hirely's frontend, especially during prototyping and MVP development.


### Streamlit and Python

One of Streamlit's main advantages for Hirely is its integration with Python.

Our existing technology stack already includes:

    Python
    FastAPI
    Pydantic
    SQLAlchemy
    AI / LLM Libraries
    Document Processing

Streamlit can be added to this Python-based ecosystem:

    Python
       ├── Streamlit
       ├── FastAPI
       ├── Pydantic
       ├── SQLAlchemy
       └── AI Libraries

This can reduce the need to introduce a completely separate frontend development stack during the early stages of the project.


### Streamlit Applications

A Streamlit application is generally created using Python code.

The Python application defines the interface and the interactions that users can perform.

Conceptually:

    Python Application
          ↓
       Streamlit
          ↓
       Web Browser

This makes the development process relatively straightforward for Python developers.


### Streamlit Widgets

Streamlit provides built-in interface components called widgets.

Common examples include:

- Text input
- Button
- File uploader
- Select box
- Checkbox
- Radio button
- Slider
- Text area

These widgets can be used to create interactive workflows.

For Hirely, possible widgets include:

    File Uploader
        ↓
    Resume Upload

    Button
        ↓
    Analyze Resume

    Select Box
        ↓
    Select Job

    Text Area
        ↓
    Additional Information


### Resume Upload

Resume upload is one of the most important frontend interactions in Hirely.

A possible workflow is:

    User
       ↓
    Streamlit File Uploader
       ↓
    Resume File
       ↓
    Backend / Processing Layer
       ↓
    Document Processing
       ↓
    Resume Parser

The frontend can provide the upload interface while the backend and document-processing components handle the actual processing.


### Streamlit and FastAPI

Streamlit and FastAPI have different responsibilities.

Streamlit is primarily responsible for:

    User Interface
    User Interaction
    Displaying Results

FastAPI is primarily responsible for:

    API
    Request Handling
    Backend Services
    Communication with Business Logic

Therefore, they can work together.

Conceptually:

    User
       ↓
    Streamlit
       ↓
    FastAPI
       ↓
    Backend
       ↓
    Database / AI


### Streamlit Does Not Replace FastAPI

Streamlit should not automatically be considered a replacement for the backend.

A possible Hirely architecture is:

    Streamlit
        ↓
    FastAPI
        ↓
    Pydantic
        ↓
    Business Logic
        ↓
    SQLAlchemy
        ↓
    Database

In this architecture:

    Streamlit
    → Frontend

    FastAPI
    → Backend API

    Pydantic
    → Data Validation

    Business Logic
    → Application Decisions

    SQLAlchemy
    → Database Interaction


### Streamlit and REST APIs

The backend architecture we have already researched uses REST APIs.

A possible flow is:

    Streamlit
        ↓
    REST API
        ↓
    FastAPI
        ↓
    Business Logic
        ↓
    Database / AI

The frontend sends requests to the backend, and the backend returns the required data.

This allows the frontend and backend responsibilities to remain separated.


### Streamlit and Pydantic

Pydantic is responsible for data validation and structured data.

A possible flow is:

    Streamlit
        ↓
    API Request
        ↓
    FastAPI
        ↓
    Pydantic
        ↓
    Validation
        ↓
    Business Logic

This ensures that data received by the backend follows the expected structure.


### Streamlit and SQLAlchemy

SQLAlchemy is responsible for database interaction.

Streamlit should not directly contain database logic throughout the application.

Instead, a cleaner architecture is:

    Streamlit
        ↓
    FastAPI
        ↓
    Service Layer
        ↓
    SQLAlchemy
        ↓
    Database

This keeps the frontend separate from database implementation details.


### Streamlit and AI

Hirely will contain AI-powered functionality.

A simplified workflow can be:

    User
       ↓
    Streamlit
       ↓
    FastAPI
       ↓
    AI / LLM
       ↓
    Analysis Result
       ↓
    Streamlit
       ↓
    User

This makes Streamlit useful for creating interfaces around AI functionality.


### Resume Analysis Interface

A possible Hirely interface could provide:

    Hirely
    ─────────────────────

    Upload Resume

    [ Select Resume ]

    Job Description

    [ Enter Job Description ]

    [ Analyze Resume ]

    ─────────────────────

    Resume Score

    Skills

    Experience Analysis

    Missing Skills

    Recommendations

The exact UI will be decided later after researching the frontend requirements and alternatives.


### Displaying Analysis Results

Hirely will eventually generate structured results.

For example:

    Resume Score
         ↓
    Skills
         ↓
    Experience Analysis
         ↓
    Missing Skills
         ↓
    Recommendations

Streamlit provides components that can be used to display information such as:

- Text
- Metrics
- Tables
- Charts
- Expandable sections
- Status information

This can make AI-generated analysis easier for users to understand.


### Streamlit for Rapid Prototyping

One of Streamlit's important advantages is rapid development.

Suppose Hirely already has:

    Resume Parser
          ↓
    Analysis Engine
          ↓
    AI Model

A Streamlit interface can be added relatively quickly:

    Resume Parser
          ↓
    Analysis Engine
          ↓
    AI Model
          ↓
    Streamlit Interface

This allows the team to test the user workflow before investing heavily in a complex frontend.


### Streamlit for MVP

Streamlit can be useful for creating an MVP.

An initial Hirely MVP might contain:

    Upload Resume
         ↓
    Analyze
         ↓
    Resume Score
         ↓
    Skills
         ↓
    Recommendations

The purpose of an MVP is to validate the core product idea with the minimum necessary functionality.

Streamlit can help reduce the time required to create this initial interface.


### Streamlit and AI/ML Applications

Streamlit is particularly suitable for applications involving:

- Data science
- Machine learning
- AI
- Data visualization
- Model demonstrations
- Interactive analysis

Hirely falls into the AI application category because it will use AI/LLMs for resume analysis and recommendations.

Therefore, Streamlit is relevant to the project from a prototyping perspective.


### Streamlit Advantages

Important advantages include:

- Python-based development
- Rapid UI development
- Simple interactive components
- Easy integration with Python applications
- Useful for AI/ML applications
- Useful for prototypes
- Useful for MVP development
- Reduced frontend complexity during early development


### Streamlit Limitations

Streamlit also has limitations.

Important considerations include:

- Less control over complex frontend behavior
- Less customization compared with dedicated frontend frameworks
- Limited control over highly customized user interfaces
- May not be ideal for every production-scale frontend
- Traditional frontend frameworks provide greater control over frontend architecture

Therefore, Streamlit should be evaluated against alternative frontend technologies before making the final decision for Hirely.


### Streamlit vs Traditional Frontend

A traditional frontend architecture might look like:

    React / Next.js
          ↓
       FastAPI
          ↓
       Backend

A Streamlit architecture might look like:

    Streamlit
          ↓
       FastAPI
          ↓
       Backend

The major difference is the development approach.

Traditional frontend frameworks provide greater control over:

    HTML
    CSS
    JavaScript
    Components
    Routing
    UI State
    Animations
    Frontend Architecture

Streamlit focuses more on making interactive applications quickly using Python.


### Streamlit and Hirely Architecture

A possible Hirely architecture using Streamlit is:

                       User
                         ↓
                     Streamlit
                         ↓
                      FastAPI
                         ↓
                     Pydantic
                         ↓
               Service / Business Logic
                    ↙          ↘
             SQLAlchemy       AI / LLM
                 ↓                ↓
             Database       Analysis Result
                                  ↓
                              Pydantic
                                  ↓
                              Streamlit
                                  ↓
                                User


### Separation of Responsibilities

The architecture should maintain clear responsibilities.

    Streamlit
    → User interface

    FastAPI
    → API layer

    REST API
    → Frontend/backend communication

    Pydantic
    → Data validation

    Business Logic
    → Application decisions

    SQLAlchemy
    → Database interaction

    AI / LLM
    → Intelligent analysis

This separation helps keep the system modular and maintainable.


### Streamlit and Scalability

Streamlit can be useful for prototypes and early versions of Hirely.

However, the final frontend decision should consider:

- Number of users
- UI complexity
- Performance requirements
- Customization requirements
- Authentication requirements
- Application architecture
- Deployment requirements
- Long-term maintainability

Therefore, scalability should be considered before selecting Streamlit as the permanent frontend.


### Streamlit and MVP vs Production

Streamlit may be a strong choice when the priority is:

    Fast Development
        ↓
    Prototype
        ↓
    MVP
        ↓
    Validate Product Idea

A dedicated frontend framework may become more attractive when the priority becomes:

    Advanced UI
        ↓
    High Customization
        ↓
    Complex Frontend Architecture
        ↓
    Production User Experience

This distinction is important for Hirely because the best technology for the MVP does not necessarily have to be the final production technology.


### Decision for Hirely

Based on the current research, **Streamlit is a strong candidate for Hirely's early frontend and MVP development**.

The main reasons are:

- Python-based development
- Fast development
- Simple interactive UI
- Strong suitability for AI applications
- Easy integration with Python-based AI workflows
- Useful for validating the Hirely user experience

However, we will not make the final frontend decision yet.

The roadmap also requires researching:

    Alternative Frontend Frameworks
          ↓
    UI/UX Considerations
          ↓
    Final Frontend Decision


### Current Hirely Frontend Concept

The current concept can be represented as:

    User
      ↓
    Streamlit
      ↓
    FastAPI
      ↓
    Pydantic
      ↓
    Business Logic
      ↓
    SQLAlchemy
      ↓
    Database

For AI functionality:

    User
      ↓
    Streamlit
      ↓
    FastAPI
      ↓
    AI / LLM
      ↓
    Pydantic
      ↓
    SQLAlchemy
      ↓
    Database


### Key Takeaways

Remember Streamlit using this simple idea:

> **Streamlit allows us to build interactive web applications using Python, making it particularly useful for AI/ML applications, prototypes, and MVPs.**

For Hirely:

    Streamlit
    → User Interface

    FastAPI
    → Backend API

    Pydantic
    → Data Validation

    SQLAlchemy
    → Database Interaction

    AI / LLM
    → Resume Analysis

The most important architectural principle is:

> **The frontend should remain separated from the backend, business logic, and database layers.**

Streamlit is therefore a strong candidate for the early Hirely frontend, but the final decision should be made after comparing it with alternative frontend technologies and considering the required user experience.