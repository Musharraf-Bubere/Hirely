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