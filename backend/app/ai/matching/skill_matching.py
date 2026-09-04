from pydantic import BaseModel


class SkillMatchResult(BaseModel):
    required_score: float
    preferred_score: float

    required_matched: list[str]
    required_missing: list[str]

    preferred_matched: list[str]
    preferred_missing: list[str]

class SkillMatcher:
    def _normalize(self, skill: str) -> str:
        return skill.strip().casefold()

    def match(
        self,
        candidate_skills: list[str],
        required_skills: list[str],
        preferred_skills: list[str],
    ) -> SkillMatchResult:
        candidate_lookup = {
            self._normalize(skill)
            for skill in candidate_skills
            if skill.strip()
        }

        required_matched: list[str] = []
        required_missing: list[str] = []

        for skill in required_skills:
            normalized_skill = self._normalize(skill)

            if not normalized_skill:
                continue

            if normalized_skill in candidate_lookup:
                required_matched.append(skill)
            else:
                required_missing.append(skill)

        preferred_matched: list[str] = []
        preferred_missing: list[str] = []

        for skill in preferred_skills:
            normalized_skill = self._normalize(skill)

            if not normalized_skill:
                continue

            if normalized_skill in candidate_lookup:
                preferred_matched.append(skill)
            else:
                preferred_missing.append(skill)

        required_score = (
            len(required_matched) / len(required_skills)
            if required_skills
            else 1.0
        )

        preferred_score = (
            len(preferred_matched) / len(preferred_skills)
            if preferred_skills
            else 1.0
        )

        return SkillMatchResult(
            required_score=required_score,
            preferred_score=preferred_score,
            required_matched=required_matched,
            required_missing=required_missing,
            preferred_matched=preferred_matched,
            preferred_missing=preferred_missing,
        )


skill_matcher = SkillMatcher()