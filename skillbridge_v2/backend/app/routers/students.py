from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Student, Skill, User
from ..schemas import StudentProfileResponse, StudentSkillUpdate, StudentProfileUpdate
from ..deps import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/me", response_model=StudentProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found."
        )
    return student


@router.put("/me/skills", response_model=StudentProfileResponse)
def update_student_skills(
    payload: StudentSkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")

    selected_skills = db.query(Skill).filter(Skill.id.in_(payload.skill_ids)).all()
    student.skills = selected_skills
    # Simple LinkedIn-style "profile strength" meter: more skills tagged = higher score,
    # capped at 100. This is cosmetic profile completeness, separate from the per-internship
    # match score computed in matching.py.
    student.readiness_score = min(100.0, len(selected_skills) * 10.0)
    db.commit()
    db.refresh(student)
    return student


@router.put("/me/profile", response_model=StudentProfileResponse)
def update_profile_details(
    payload: StudentProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found.")

    if payload.branch_id is not None:
        student.branch_id = payload.branch_id.lower()
    if payload.target_role is not None:
        student.target_role = payload.target_role

    db.commit()
    db.refresh(student)
    return student