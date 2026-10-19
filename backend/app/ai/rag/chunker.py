from app.ai.parsers.schemas import ResumeData
from app.ai.rag.schemas import EvidenceChunk


class ResumeEvidenceChunker:
    """
    Decomposes structured ResumeData into semantically typed EvidenceChunk objects
    with provenance metadata (section, organization, role, timeframe).

    Guarantees:
    - Never includes personal contact information (email, phone, address).
    - Preserves exact source text so quotes can be verified.
    - Handles null, sparse, or empty sections safely.
    - Generates deterministic, stable chunk IDs within the candidate's resume.
    """

    def chunk(self, resume_data: ResumeData) -> list[EvidenceChunk]:
        chunks: list[EvidenceChunk] = []

        if not resume_data:
            return chunks

        # 1. Summary / Headline
        summary_parts = []
        if resume_data.headline and resume_data.headline.strip():
            summary_parts.append(f"Professional Headline: {resume_data.headline.strip()}")
        if resume_data.summary and resume_data.summary.strip():
            summary_parts.append(resume_data.summary.strip())

        if summary_parts:
            chunks.append(
                EvidenceChunk(
                    chunk_id="summary_0",
                    section="summary",
                    title=resume_data.headline.strip() if resume_data.headline else "Professional Summary",
                    organization=None,
                    timeframe=None,
                    content="\n".join(summary_parts),
                )
            )

        # 2. Work Experience
        for idx, exp in enumerate(resume_data.experience or []):
            role = exp.job_title.strip() if exp.job_title else None
            company = exp.company.strip() if exp.company else None

            start = exp.start_date.strip() if exp.start_date else ""
            end = exp.end_date.strip() if exp.end_date else ""
            timeframe = f"{start} - {end}".strip(" -") if (start or end) else None

            desc = exp.description.strip() if exp.description else ""

            # Build substantive text content
            content_parts = []
            if role and company:
                content_parts.append(f"Role: {role} at {company}")
            elif role:
                content_parts.append(f"Role: {role}")
            elif company:
                content_parts.append(f"Company: {company}")

            if timeframe:
                content_parts.append(f"Timeframe: {timeframe}")

            if desc:
                content_parts.append(desc)

            content = "\n".join(content_parts).strip()
            if not content:
                continue

            chunks.append(
                EvidenceChunk(
                    chunk_id=f"exp_{idx}",
                    section="experience",
                    title=role,
                    organization=company,
                    timeframe=timeframe,
                    content=content,
                )
            )

        # 3. Projects
        for idx, proj in enumerate(resume_data.projects or []):
            name = proj.name.strip() if proj.name else None
            desc = proj.description.strip() if proj.description else ""
            techs = [t.strip() for t in (proj.technologies or []) if t and t.strip()]

            content_parts = []
            if name:
                content_parts.append(f"Project: {name}")
            if desc:
                content_parts.append(desc)
            if techs:
                content_parts.append(f"Technologies: {', '.join(techs)}")

            content = "\n".join(content_parts).strip()
            if not content:
                continue

            chunks.append(
                EvidenceChunk(
                    chunk_id=f"proj_{idx}",
                    section="projects",
                    title=name,
                    organization=None,
                    timeframe=None,
                    content=content,
                )
            )

        # 4. Education
        for idx, edu in enumerate(resume_data.education or []):
            degree = edu.degree.strip() if edu.degree else None
            inst = edu.institution.strip() if edu.institution else None
            field = edu.field_of_study.strip() if edu.field_of_study else None

            start = edu.start_date.strip() if edu.start_date else ""
            end = edu.end_date.strip() if edu.end_date else ""
            timeframe = f"{start} - {end}".strip(" -") if (start or end) else None

            content_parts = []
            if degree and field and inst:
                content_parts.append(f"{degree} in {field} from {inst}")
            elif degree and inst:
                content_parts.append(f"{degree} from {inst}")
            elif degree:
                content_parts.append(degree)
            elif inst:
                content_parts.append(f"Studied at {inst}")

            if timeframe:
                content_parts.append(f"Dates: {timeframe}")

            content = "\n".join(content_parts).strip()
            if not content:
                continue

            chunks.append(
                EvidenceChunk(
                    chunk_id=f"edu_{idx}",
                    section="education",
                    title=degree,
                    organization=inst,
                    timeframe=timeframe,
                    content=content,
                )
            )

        # 5. Certifications
        for idx, cert in enumerate(resume_data.certifications or []):
            name = cert.name.strip() if cert.name else None
            issuer = cert.issuer.strip() if cert.issuer else None
            date = cert.date.strip() if cert.date else None

            content_parts = []
            if name and issuer:
                content_parts.append(f"Certification: {name} issued by {issuer}")
            elif name:
                content_parts.append(f"Certification: {name}")

            if date:
                content_parts.append(f"Date: {date}")

            content = "\n".join(content_parts).strip()
            if not content:
                continue

            chunks.append(
                EvidenceChunk(
                    chunk_id=f"cert_{idx}",
                    section="certifications",
                    title=name,
                    organization=issuer,
                    timeframe=date,
                    content=content,
                )
            )

        # 6. Technical Skills list
        if resume_data.skills:
            clean_skills = [s.strip() for s in resume_data.skills if s and s.strip()]
            if clean_skills:
                chunks.append(
                    EvidenceChunk(
                        chunk_id="skills_0",
                        section="skills",
                        title="Documented Technical Skills",
                        organization=None,
                        timeframe=None,
                        content=f"Documented Skills: {', '.join(clean_skills)}",
                    )
                )

        return chunks


resume_evidence_chunker = ResumeEvidenceChunker()
