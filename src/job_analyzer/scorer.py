from job_analyzer.models import (
    ExtractedSkill,
    MatchReport,
    SkillMatch,
    UserProfile
)

def get_priority(weight: int) -> str:
    if weight >= 3:
        return "high"
    elif weight == 2:
        return "medium"
    else:
        return "low"
    
def score_skills(
    job_skills: list[ExtractedSkill],
    profile: UserProfile
) -> MatchReport:
    # Use set to performance searching rate
    profile_skills = {
        skill.casefold()
        for skill in profile.skills
    }

    # Unique skill count
    unique_job_skill: dict[str, ExtractedSkill] = {}

    for skill in job_skills:
        key = skill.skill.casefold()

        current = unique_job_skill.get(key)

        # If skills repeat, save the skill with highest weight
        if current is None or skill.weight > current.weight:
            unique_job_skill[key] = skill
    
    total_weight = sum(
        skill.weight
        for skill in unique_job_skill.values()
    )

    matched_weight = 0
    matched_results: list[SkillMatch] = []
    missing_results: list[SkillMatch] = []

    for skill in unique_job_skill.values():
        is_matched = skill.skill.casefold() in profile_skills

        if is_matched:
            matched_weight += skill.weight

        result = SkillMatch(
            skill= skill.skill,
            category= skill.category,
            weight=skill.weight,
            matched=is_matched,
            evidence=[skill.evidence],
            priority= None if is_matched else get_priority(skill.weight),

        )

        if is_matched:
            matched_results.append(result)
        else:
            missing_results.append(result)
        
    score = (
        round(matched_weight/total_weight * 100, 2)
        if total_weight > 0
        else 0
    )

    missing_results.sort(
        key= lambda item: item.weight,
        reverse=True,
    )

    return MatchReport(
        score=score,
        matched_skills=matched_results,
        missing_skills=missing_results
    )
