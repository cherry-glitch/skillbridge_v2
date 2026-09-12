def compute_match_score(
    student_branch: str,
    student_skill_ids: set,
    internship_eligible_branches: str,
    required_skill_ids: set,
    preferred_skill_ids: set = None
) -> dict:
    """
    Branch-aware scoring engine between student profile and an internship opening.
    """
    if preferred_skill_ids is None:
        preferred_skill_ids = set()

    student_branch_clean = (student_branch or "").strip().lower()
    allowed_branches = [
        b.strip().lower()
        for b in (internship_eligible_branches or "").split(",")
        if b.strip()
    ]

    # Branch gate: check eligibility
    is_branch_eligible = (not allowed_branches) or (student_branch_clean in allowed_branches)

    if not is_branch_eligible:
        return {
            "score": 0.0,
            "is_eligible": False,
            "status": "Ineligible Branch",
            "matched_skills": [],
            "missing_skills": list(required_skill_ids)
        }

    matched_req = student_skill_ids.intersection(required_skill_ids)
    missing_req = required_skill_ids - student_skill_ids
    matched_pref = student_skill_ids.intersection(preferred_skill_ids)

    req_weight = 0.8
    pref_weight = 0.2

    req_ratio = len(matched_req) / len(required_skill_ids) if required_skill_ids else 1.0
    pref_ratio = len(matched_pref) / len(preferred_skill_ids) if preferred_skill_ids else 0.0

    final_score = round((req_weight * req_ratio + pref_weight * pref_ratio) * 100, 1)

    return {
        "score": final_score,
        "is_eligible": True,
        "status": "Ready" if final_score >= 70 else "Gap Identified",
        "matched_skills": list(matched_req | matched_pref),
        "missing_skills": list(missing_req)
    }


# Backwards compatibility alias for older routers
match_candidate = compute_match_score