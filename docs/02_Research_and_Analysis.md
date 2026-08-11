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