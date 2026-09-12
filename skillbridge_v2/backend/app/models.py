from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    Table,
    Text,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Association: Student <-> Skills
student_skills = Table(
    "student_skills",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", String(50), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)

# Association: Internship <-> Required Skills
internship_required_skills = Table(
    "internship_required_skills",
    Base.metadata,
    Column("internship_id", Integer, ForeignKey("internships.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", String(50), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)

# Association: Internship <-> Preferred Skills
internship_preferred_skills = Table(
    "internship_preferred_skills",
    Base.metadata,
    Column("internship_id", Integer, ForeignKey("internships.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", String(50), ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")  # student / recruiter / admin
    created_at = Column(DateTime, default=datetime.utcnow)

    student_profile = relationship("Student", back_populates="user", uselist=False)


class Branch(Base):
    __tablename__ = "branches"

    id = Column(String(10), primary_key=True)  # 'cse', 'ece', 'mech', 'eee'
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    students = relationship("Student", back_populates="branch")
    skills = relationship("Skill", back_populates="branch")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(String(50), primary_key=True)  # slug identifier
    name = Column(String(100), nullable=False)
    domain = Column(String(100), nullable=False)
    branch_id = Column(String(10), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True)
    is_universal = Column(Boolean, default=False)

    branch = relationship("Branch", back_populates="skills")
    students = relationship("Student", secondary=student_skills, back_populates="skills")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    branch_id = Column(String(10), ForeignKey("branches.id"), nullable=True)
    target_role = Column(String(100), nullable=True)
    readiness_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="student_profile")
    branch = relationship("Branch", back_populates="students")
    skills = relationship("Skill", secondary=student_skills, back_populates="students")
    applications = relationship("Application", back_populates="student", cascade="all, delete-orphan")


class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    eligible_branches = Column(String(100), default="cse,ece,mech,eee")
    min_readiness_score = Column(Float, default=0.0)

    required_skills = relationship("Skill", secondary=internship_required_skills)
    preferred_skills = relationship("Skill", secondary=internship_preferred_skills)
    applications = relationship("Application", back_populates="internship", cascade="all, delete-orphan")


class Application(Base):
    """A student's application to one internship, with a status they can track
    (like Internshala's 'applied / shortlisted / rejected / selected' tracker)."""
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("student_id", "internship_id", name="uq_student_internship"),)

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    internship_id = Column(Integer, ForeignKey("internships.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default="applied")  # applied | shortlisted | rejected | selected
    match_score = Column(Float, default=0.0)
    applied_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="applications")
    internship = relationship("Internship", back_populates="applications")