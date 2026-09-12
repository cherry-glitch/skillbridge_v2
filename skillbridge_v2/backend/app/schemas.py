from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# --- Branch Schemas ---
class BranchBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

BranchOut = BranchBase


# --- Role Schemas ---
class RoleOut(BaseModel):
    id: Optional[str] = None
    title: str
    branch_id: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# --- Skill Schemas ---
class SkillResponse(BaseModel):
    id: str
    name: str
    domain: str
    branch_id: Optional[str] = None
    is_universal: bool

    class Config:
        from_attributes = True

SkillOut = SkillResponse
SkillCreate = SkillResponse


# --- Auth / User Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "student"
    branch_id: Optional[str] = None
    target_role: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

UserOut = UserResponse


# --- Student Profile Schemas ---
class StudentSkillUpdate(BaseModel):
    skill_ids: List[str]


class StudentProfileUpdate(BaseModel):
    branch_id: Optional[str] = None
    target_role: Optional[str] = None


class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    branch_id: Optional[str] = None
    target_role: Optional[str] = None
    readiness_score: float
    skills: List[SkillResponse] = []

    class Config:
        from_attributes = True

StudentOut = StudentProfileResponse


# --- Internship Schemas ---
class InternshipResponse(BaseModel):
    id: int
    company_name: str
    title: str
    description: str
    eligible_branches: str
    min_readiness_score: float
    required_skills: List[SkillResponse] = []
    preferred_skills: List[SkillResponse] = []

    class Config:
        from_attributes = True

InternshipOut = InternshipResponse


# --- Match / Score Schemas ---
class MatchResultResponse(BaseModel):
    internship_id: int
    company_name: str
    title: str
    score: float
    is_eligible: bool
    status: str
    matched_skills: List[str]
    missing_skills: List[str]

MatchOut = MatchResultResponse


# --- Application Schemas ---
class ApplicationResponse(BaseModel):
    id: int
    internship_id: int
    company_name: str
    title: str
    status: str
    match_score: float
    applied_at: datetime

    class Config:
        from_attributes = True

ApplicationOut = ApplicationResponse