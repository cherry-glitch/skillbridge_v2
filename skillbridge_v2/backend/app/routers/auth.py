from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Student, Branch
from ..schemas import UserRegister, UserLogin, Token, UserResponse
from ..security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )

    clean_branch = user_data.branch_id.strip().lower() if user_data.branch_id else None
    if clean_branch:
        branch_exists = db.query(Branch).filter(Branch.id == clean_branch).first()
        if not branch_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid branch '{clean_branch}'."
            )

    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        role=user_data.role or "student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if new_user.role == "student":
        student = Student(
            user_id=new_user.id,
            branch_id=clean_branch,
            target_role=user_data.target_role or "",
            readiness_score=0.0
        )
        db.add(student)
        db.commit()

    return new_user


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}