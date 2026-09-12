from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Internship, Student, User, Application
from ..schemas import InternshipResponse, MatchResultResponse, ApplicationResponse
from ..deps import get_current_user
from ..matching import compute_match_score

router = APIRouter(prefix="/internships", tags=["internships"])


def _get_student_or_404(db: Session, current_user: User) -> Student:
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")
    return student

@router.get("", response_model=List[InternshipResponse])
def get_internships(
    branch: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Internship)
    if branch:
        query = query.filter(Internship.eligible_branches.ilike(f"%{branch.lower()}%"))
    return query.all()


@router.get("/matches", response_model=List[MatchResultResponse])
def get_my_matches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")

    student_branch = student.branch_id or ""
    student_skill_ids = {s.id for s in student.skills}

    all_internships = db.query(Internship).all()
    results = []

    for item in all_internships:
        req_ids = {s.id for s in item.required_skills}
        pref_ids = {s.id for s in item.preferred_skills}

        match_data = compute_match_score(
            student_branch=student_branch,
            student_skill_ids=student_skill_ids,
            internship_eligible_branches=item.eligible_branches,
            required_skill_ids=req_ids,
            preferred_skill_ids=pref_ids
        )

        results.append(MatchResultResponse(
            internship_id=item.id,
            company_name=item.company_name,
            title=item.title,
            score=match_data["score"],
            is_eligible=match_data["is_eligible"],
            status=match_data["status"],
            matched_skills=match_data["matched_skills"],
            missing_skills=match_data["missing_skills"]
        ))

    # Sort descending by match score
    results.sort(key=lambda x: x.score, reverse=True)
    return results


@router.post("/{internship_id}/apply", response_model=ApplicationResponse)
def apply_to_internship(
    internship_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = _get_student_or_404(db, current_user)
    internship = db.query(Internship).filter(Internship.id == internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found.")

    existing = (
        db.query(Application)
        .filter(Application.student_id == student.id, Application.internship_id == internship_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this internship.")

    req_ids = {s.id for s in internship.required_skills}
    pref_ids = {s.id for s in internship.preferred_skills}
    match_data = compute_match_score(
        student_branch=student.branch_id or "",
        student_skill_ids={s.id for s in student.skills},
        internship_eligible_branches=internship.eligible_branches,
        required_skill_ids=req_ids,
        preferred_skill_ids=pref_ids,
    )

    application = Application(
        student_id=student.id,
        internship_id=internship_id,
        status="applied",
        match_score=match_data["score"],
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    return ApplicationResponse(
        id=application.id,
        internship_id=internship.id,
        company_name=internship.company_name,
        title=internship.title,
        status=application.status,
        match_score=application.match_score,
        applied_at=application.applied_at,
    )


@router.get("/applications/me", response_model=List[ApplicationResponse])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = _get_student_or_404(db, current_user)
    apps = (
        db.query(Application)
        .filter(Application.student_id == student.id)
        .order_by(Application.applied_at.desc())
        .all()
    )
    return [
        ApplicationResponse(
            id=a.id,
            internship_id=a.internship_id,
            company_name=a.internship.company_name,
            title=a.internship.title,
            status=a.status,
            match_score=a.match_score,
            applied_at=a.applied_at,
        )
        for a in apps
    ]