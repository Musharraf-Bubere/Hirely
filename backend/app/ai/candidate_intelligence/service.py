from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.candidate_intelligence.schemas import (
    CandidateApplicationInfo,
    CandidateEducationItem,
    CandidateExperienceItem,
    CandidateIntelligenceFilterRequest,
    CandidateIntelligenceItem,
    CandidateIntelligenceResponse,
    CandidateProfileSummary,
)
from app.ai.matching.results import FinalMatchResult, RankedMatchResult
from app.ai.parsers.schemas import ResumeData
from app.ai.services.recruiter_matching_service import (
    RecruiterMatchingService,
    recruiter_matching_service,
)
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.recruiter import Recruiter
from app.services.candidate_skill import get_candidate_skills
from app.services.resume import get_active_resume


def _normalize_skill_list(skills: list[str]) -> list[str]:
    seen = set()
    result = []
    for skill in skills:
        cleaned = skill.strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)
    return sorted(result)


class CandidateIntelligenceService:
    """
    Coordinates advanced recruiter candidate search, relevance ranking,
    deterministic scoring breakdown, and optional AI explanations.
    """

    def __init__(
        self,
        matching_service: RecruiterMatchingService | None = None,
    ):
        self.matching_service = matching_service or recruiter_matching_service

    def get_candidate_intelligence(
        self,
        *,
        db: Session,
        recruiter: Recruiter,
        job: Job,
        filters: CandidateIntelligenceFilterRequest | None = None,
    ) -> CandidateIntelligenceResponse:
        """
        Retrieves, ranks, correlates, and filters candidate intelligence for a recruiter job.
        Strictly enforces recruiter ownership and performs zero database mutations.
        """
        if job.recruiter_id != recruiter.id:
            raise ValueError(
                "You do not have permission to view candidate intelligence for this job."
            )

        if not job.is_active:
            raise ValueError("Target job is inactive.")

        filter_req = filters or CandidateIntelligenceFilterRequest()

        # Step 1: Execute deterministic matching & ranking
        if filter_req.include_explanations and filter_req.explanation_limit > 0:
            final_results = self.matching_service.rank_and_explain_candidates(
                db=db,
                job=job,
                explanation_limit=filter_req.explanation_limit,
            )
            # Unpack FinalMatchResult items
            match_items: list[tuple[RankedMatchResult, any]] = [
                (fr.match, fr.explanation) for fr in final_results
            ]
        else:
            ranked_results = self.matching_service.rank_candidates(
                db=db,
                job=job,
            )
            match_items = [(rr, None) for rr in ranked_results]

        if not match_items:
            return CandidateIntelligenceResponse(
                job_id=job.id,
                job_title=job.title,
                total_candidates=0,
                matched_count=0,
                results=[],
                available_skills=[],
            )

        # Step 2: Correlate candidate profile, parsed resume metadata, and application status
        candidate_ids = [m[0].candidate_id for m in match_items]
        candidates = (
            db.query(Candidate)
            .filter(Candidate.id.in_(candidate_ids))
            .all()
        )
        candidates_by_id = {c.id: c for c in candidates}

        applications = (
            db.query(Application)
            .filter(
                Application.candidate_id.in_(candidate_ids),
                Application.job_id == job.id,
            )
            .all()
        )
        applications_by_candidate_id = {
            a.candidate_id: a for a in applications
        }

        all_available_skills: set[str] = set()
        unfiltered_items: list[CandidateIntelligenceItem] = []

        for ranked_match, explanation in match_items:
            cand = candidates_by_id.get(ranked_match.candidate_id)
            if not cand:
                continue

            resume = get_active_resume(db=db, candidate=cand)
            resume_data: ResumeData | None = None
            if resume and resume.parsed_data:
                try:
                    resume_data = ResumeData.model_validate(resume.parsed_data)
                except Exception:
                    resume_data = None

            # Collect skills without PII
            db_skills = [
                cs.skill.name.strip()
                for cs in get_candidate_skills(db=db, candidate=cand)
                if cs.skill and cs.skill.name
            ]
            resume_skills = [
                s.strip()
                for s in (resume_data.skills if resume_data else [])
                if s and s.strip()
            ]
            combined_skills = _normalize_skill_list(db_skills + resume_skills)

            for s in combined_skills:
                all_available_skills.add(s)
            for s in ranked_match.required_matched + ranked_match.preferred_matched:
                all_available_skills.add(s)

            # Extract experience snippet
            experience_items: list[CandidateExperienceItem] = []
            if resume_data and resume_data.experience:
                for exp in resume_data.experience[:5]:
                    experience_items.append(
                        CandidateExperienceItem(
                            job_title=exp.job_title.strip() if exp.job_title else None,
                            company=exp.company.strip() if exp.company else None,
                            start_date=exp.start_date.strip() if exp.start_date else None,
                            end_date=exp.end_date.strip() if exp.end_date else None,
                            description=exp.description.strip() if exp.description else None,
                        )
                    )

            # Extract education snippet
            education_items: list[CandidateEducationItem] = []
            if resume_data and resume_data.education:
                for edu in resume_data.education[:3]:
                    education_items.append(
                        CandidateEducationItem(
                            degree=edu.degree.strip() if edu.degree else None,
                            institution=edu.institution.strip() if edu.institution else None,
                            field_of_study=edu.field_of_study.strip() if edu.field_of_study else None,
                            start_date=edu.start_date.strip() if edu.start_date else None,
                            end_date=edu.end_date.strip() if edu.end_date else None,
                        )
                    )

            full_name = f"{cand.first_name} {cand.last_name}".strip()
            headline = (
                cand.headline.strip()
                if cand.headline
                else (resume_data.headline.strip() if resume_data and resume_data.headline else None)
            )
            location = (
                cand.location.strip()
                if cand.location
                else (resume_data.location.strip() if resume_data and resume_data.location else None)
            )

            profile_summary = CandidateProfileSummary(
                id=cand.id,
                first_name=cand.first_name,
                last_name=cand.last_name,
                full_name=full_name,
                headline=headline,
                location=location,
                bio=cand.bio.strip() if cand.bio else None,
                skills=combined_skills,
                experience=experience_items,
                education=education_items,
            )

            # Application info
            app = applications_by_candidate_id.get(cand.id)
            app_info = (
                CandidateApplicationInfo(
                    application_id=app.id,
                    status=app.status.value if hasattr(app.status, "value") else str(app.status),
                    created_at=app.created_at,
                )
                if app
                else None
            )

            unfiltered_items.append(
                CandidateIntelligenceItem(
                    rank=ranked_match.rank,
                    candidate=profile_summary,
                    application=app_info,
                    overall_score=ranked_match.overall_score,
                    required_skill_score=ranked_match.required_skill_score,
                    preferred_skill_score=ranked_match.preferred_skill_score,
                    semantic_similarity=ranked_match.semantic_similarity,
                    required_matched=ranked_match.required_matched,
                    required_missing=ranked_match.required_missing,
                    preferred_matched=ranked_match.preferred_matched,
                    preferred_missing=ranked_match.preferred_missing,
                    explanation=explanation,
                )
            )

        total_candidates = len(unfiltered_items)

        # Step 3: Apply Practical Filters
        filtered_items = unfiltered_items

        # A. Query Search
        if filter_req.query and filter_req.query.strip():
            query_term = filter_req.query.strip().lower()

            def matches_query(item: CandidateIntelligenceItem) -> bool:
                if query_term in item.candidate.full_name.lower():
                    return True
                if item.candidate.headline and query_term in item.candidate.headline.lower():
                    return True
                if item.candidate.bio and query_term in item.candidate.bio.lower():
                    return True
                if any(query_term in s.lower() for s in item.candidate.skills):
                    return True
                for exp in item.candidate.experience:
                    if exp.company and query_term in exp.company.lower():
                        return True
                    if exp.job_title and query_term in exp.job_title.lower():
                        return True
                return False

            filtered_items = [it for it in filtered_items if matches_query(it)]

        # B. Minimum Score Filter
        if filter_req.min_score is not None:
            min_score = filter_req.min_score
            filtered_items = [
                it for it in filtered_items if it.overall_score >= min_score
            ]

        # C. Skill Filter
        if filter_req.skill and filter_req.skill.strip():
            target_skill = filter_req.skill.strip().lower()

            def matches_skill(item: CandidateIntelligenceItem) -> bool:
                if any(target_skill in s.lower() for s in item.candidate.skills):
                    return True
                if any(target_skill in s.lower() for s in item.required_matched):
                    return True
                if any(target_skill in s.lower() for s in item.preferred_matched):
                    return True
                return False

            filtered_items = [it for it in filtered_items if matches_skill(it)]

        # D. Application Status Filter
        if filter_req.application_status and filter_req.application_status.strip():
            status_term = filter_req.application_status.strip().lower()
            if status_term != "all":
                if status_term == "not_applied":
                    filtered_items = [
                        it for it in filtered_items if it.application is None
                    ]
                else:
                    filtered_items = [
                        it
                        for it in filtered_items
                        if it.application and it.application.status.lower() == status_term
                    ]

        # Step 4: Sorting
        sort_by = (filter_req.sort_by or "overall_score").lower()
        sort_order = (filter_req.sort_order or "desc").lower()
        reverse = sort_order == "desc"

        if sort_by == "overall_score":
            filtered_items.sort(key=lambda x: x.overall_score, reverse=reverse)
        elif sort_by == "required_skills":
            filtered_items.sort(key=lambda x: x.required_skill_score, reverse=reverse)
        elif sort_by == "preferred_skills":
            filtered_items.sort(key=lambda x: x.preferred_skill_score or 0.0, reverse=reverse)
        elif sort_by == "semantic_similarity":
            filtered_items.sort(key=lambda x: x.semantic_similarity, reverse=reverse)
        elif sort_by == "name":
            filtered_items.sort(key=lambda x: x.candidate.full_name.lower(), reverse=reverse)
        elif sort_by == "rank":
            filtered_items.sort(key=lambda x: x.rank, reverse=reverse)

        return CandidateIntelligenceResponse(
            job_id=job.id,
            job_title=job.title,
            total_candidates=total_candidates,
            matched_count=len(filtered_items),
            results=filtered_items,
            available_skills=sorted(all_available_skills),
        )


candidate_intelligence_service = CandidateIntelligenceService()
