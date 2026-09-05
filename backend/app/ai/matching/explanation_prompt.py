from app.ai.matching.explanation import MatchExplanationInput


class ExplanationPromptBuilder:
    def build(self, data: MatchExplanationInput) -> str:
        preferred_score = (
            str(data.preferred_skill_score)
            if data.preferred_skill_score is not None
            else "Unavailable"
        )

        preferred_matched = (
            ", ".join(data.preferred_matched)
            if data.preferred_matched
            else "None"
        )

        preferred_missing = (
            ", ".join(data.preferred_missing)
            if data.preferred_missing
            else "None"
        )

        required_matched = (
            ", ".join(data.required_matched)
            if data.required_matched
            else "None"
        )

        required_missing = (
            ", ".join(data.required_missing)
            if data.required_missing
            else "None"
        )

        return f"""
You are generating an explanation for an already-calculated
candidate-job match.

Your task is to explain the provided matching evidence clearly
for a recruiter.

IMPORTANT RULES:

- Do not calculate, modify, or reinterpret the overall match score.
- Use only the evidence provided below.
- Do not invent skills, experience, qualifications, achievements,
  or other candidate information.
- Use matched skills as evidence for strengths.
- Use missing skills as evidence for gaps.
- If a signal is marked as unavailable, do not treat it as zero.
- Do not make hiring decisions.
- Do not claim that the candidate is definitely qualified or
  unqualified.
- Keep the explanation concise, factual, and recruiter-friendly.
- A matched skill only indicates that the skill is present in the
  provided matching evidence. Do not infer proficiency, expertise,
  depth of knowledge, or years of experience.
- Do not describe a candidate as experienced, proficient, expert,
  highly skilled, or similar unless that information is explicitly
  supported by the provided evidence.

MATCHING EVIDENCE:

Candidate ID:
{data.candidate_id}

Overall Match Score:
{data.overall_score}

Required Skill Score:
{data.required_skill_score}

Preferred Skill Score:
{preferred_score}

Semantic Similarity:
{data.semantic_similarity}

Required Skills Matched:
{required_matched}

Required Skills Missing:
{required_missing}

Preferred Skills Matched:
{preferred_matched}

Preferred Skills Missing:
{preferred_missing}

Generate a structured explanation containing:

- summary
- strengths
- gaps
- evidence
- caveats

The evidence values must correspond to the provided matching
evidence. Do not create or change numerical values.
""".strip()


explanation_prompt_builder = ExplanationPromptBuilder()