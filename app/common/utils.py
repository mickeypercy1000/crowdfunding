import random
import uuid
from app.common.email_setup import send_email_notif
from app.config.database import get_db
from sqlalchemy import or_
from passlib.context import CryptContext
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.model.authentication import User
from app.model.projects import Project
from app.schema.authentication import SignupResponseSchema
from app.config.settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserUtils:

    @staticmethod
    def check_user_exists(data: dict, db) -> bool:
        print("inside util")
        if _ := db.query(User).filter(
            or_(
                User.email == data.email,
                User.username == data.username
            )
        ).first():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
            )
        return UserUtils.signup_user(data, db)
    
    @staticmethod
    def check_user_exist_with_id(verification_id: uuid.UUID, db) -> bool:
        if db.query(User).filter(
            User.verification_id == verification_id
        ).exists():
            return True
        return False
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        print(credentials_exception)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            print(payload)
            email: str = payload.get("sub")
            print(email)
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        print(user)
        return user
    
    @staticmethod
    def signup_user(signup_data: dict, db) -> User:
    
        hashed_password = UserUtils.hash_password(signup_data.password)  # Securely hash the password
        
        user = User(
            firstname=signup_data.firstname,
            lastname=signup_data.lastname,
            email=signup_data.email,
            username=signup_data.username,
            password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return SignupResponseSchema(status=True, id=user.id, message="Signup successful")
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


class CommonUtils:

    @staticmethod
    def send_email(verification_id, background_tasks, email: str, otp: str, type: str):
        print("inside email")
        if type.lower() == "signup":
            subject = "Email Verification"
            message = f"Your email verification code is {otp}"
        
            email_notif = send_email_notif(verification_id, background_tasks, subject, message, email)
            return email_notif
        
    @staticmethod
    def generate_otp() -> str:
        return random.randrange(100000, 999999)
    

class ProjectUtils:

    @staticmethod
    def check_project_exists(data: dict, db) -> bool:
        print("inside util")
        if _ := db.query(Project).filter((Project.title == data.title)).first():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with this title already exists"
            )
        return None
        
    def create_project(data: dict, current_user: object, db) -> Project:
        check_project = ProjectUtils.check_project_exists(data, db)
        if check_project is None:
            new_project = Project(
            title=data.title,
            description=data.description,
            goal_amount=data.goal_amount,
            deadline=data.deadline,
            creator=current_user
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project
    