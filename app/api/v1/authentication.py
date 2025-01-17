from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.common.utils import UserUtils
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.model.authentication import User
from app.schema.authentication import LoginRequestSchema, LoginResponseSchema, MyDetailsResponseSchema, SignUpRequestSchema, SignupResponseSchema
from app.config.settings import settings

router = APIRouter(prefix="/users")


@router.post("/register", response_model=SignupResponseSchema, status_code=status.HTTP_201_CREATED)
async def signup(data: SignUpRequestSchema, db: Session = Depends(get_db)):
    user = UserUtils.check_user_exists(data, db)        
    return user


@router.post("/login", response_model=LoginResponseSchema)
async def login(data: LoginRequestSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not UserUtils.verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = UserUtils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return LoginResponseSchema(
        status=True,
        user_id = user.id,
        message="Login successful",
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        access_token = access_token,    
    )

@router.get("/me", response_model=MyDetailsResponseSchema)
async def get_profile(current_user: User = Depends(UserUtils.get_current_user)):
    return MyDetailsResponseSchema(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        firstname=current_user.firstname,
        lastname=current_user.lastname,
        created_at=current_user.created_at
    )
    