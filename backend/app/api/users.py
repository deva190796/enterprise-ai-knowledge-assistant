from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

from app.auth.hashing import hash_password

from fastapi import HTTPException
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token
from app.schemas.token import Token

from app.auth.dependencies import get_current_user

from app.schemas.login import LoginRequest

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
        status_code=400,
        detail="Email already registered"
        )
    
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# @router.post("/login", response_model=Token)
# def login(user: LoginRequest, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.email == user.email).first()

#     if not db_user:
#         raise HTTPException(status_code=401, detail="Invalid Email or Password")

#     if not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid Email or Password")

#     token = create_access_token(
#         {"sub": db_user.email}
#     )

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }
    
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email
    }