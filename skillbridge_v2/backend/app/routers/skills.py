from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import Skill, Branch
from .. import schemas

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("/branches", response_model=List[schemas.BranchOut])
def get_all_branches(db: Session = Depends(get_db)):
    """Fetch all available academic engineering branches."""
    return db.query(Branch).all()


@router.get("", response_model=List[schemas.SkillOut])
def list_skills(
    branch: Optional[str] = Query(None, description="Filter skills by branch (cse, ece, mech, eee)"),
    db: Session = Depends(get_db)
):
    """
    Returns universal skills plus any skills specific to the queried branch.
    If branch is omitted, returns all skills.
    """
    query = db.query(Skill)
    if branch:
        query = query.filter((Skill.branch_id == branch.lower()) | (Skill.is_universal == True))
    return query.all()