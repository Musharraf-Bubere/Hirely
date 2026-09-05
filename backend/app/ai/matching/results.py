from pydantic import BaseModel

from app.ai.matching.scoring import MatchScoreResult
from app.ai.matching.skill_matching import SkillMatchResult


class CompleteMatchResult(BaseModel):
    score: MatchScoreResult
    skills: SkillMatchResult