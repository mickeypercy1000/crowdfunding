from decimal import Decimal
import random
import re
import uuid
from app.config.database import get_db
from sqlalchemy import func, or_
from passlib.context import CryptContext
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from app.model.authentication import User
from app.model.projects import Contribution, Project
from app.schema.authentication import SignupResponseSchema
from app.config.settings import settings
from sqlalchemy import func

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserUtils:

    @staticmethod
    def check_user_exists(data: dict, db) -> bool:
        if _ := db.query(User).filter(User.email == data.email).first():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
            )
        if _ := db.query(User).filter(User.username == data.username).first():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
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
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    
    @staticmethod
    def signup_user(signup_data: dict, db) -> User:
    
        hashed_password = UserUtils.hash_password(signup_data.password)
        
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
    
    @staticmethod
    def validate_password(value: str) -> str:
        conditions = [
            (r'\d', "The password must contain at least one number."),
            (r'[A-Z]', "The password must contain at least one capital letter."),
            (r'[a-z]', "The password must contain at least one lowercase letter."),
            (r'[!@#$%^&*()\-=_+`~[\]{}|;:,.<>?]', "The password must contain at least one special character."),
        ]
        if len(value) < 8 or len(value) > 100:
            raise ValueError("The password must be between 8 and 100 characters.")
        errors = [msg for pattern, msg in conditions if not re.search(pattern, value)]
        if errors:
            raise ValueError(" ".join(errors))
        return value


class ProjectUtils:

    @staticmethod
    def check_project_exists(data: dict, db) -> bool:
        if _ := db.query(Project).filter(func.lower(Project.title) == func.lower(data.title)).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this title already exists"
            )
        return None
        
    @staticmethod
    def get_project_by_id(project_id: str, db: object) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        return project
    
    @staticmethod
    def contribution_deadline_check(project: Project) -> bool:
        if datetime.now().date() > project.deadline:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The project deadline has passed. Contributions are no longer allowed."
            )
        return True
    
    @staticmethod
    def create_project(data: dict, current_user: object, db: object) -> Project:
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
    
    @staticmethod
    def create_contribution(contribution: object, project: object, current_user: object, db: Session) -> Contribution:
        check_deadline = ProjectUtils.contribution_deadline_check(project)
        if not check_deadline:
            return {"status": False, "message": "Deadline for the project has passed. Contributions are no longer accepted.", "code": 400}
        new_contribution = Contribution(
            contributor=current_user,
            project=project,
            amount=contribution.amount
        )
        db.add(new_contribution)
        project.total_contribution += Decimal(str(contribution.amount))
        db.commit()
        db.refresh(new_contribution)
        db.refresh(project)
        return new_contribution


class ContributionsUtils:
    def get_contributors_and_total(project_id: str, db: Session, page: int = 1, page_size: int = 10):
        Contributor = aliased(User)
        contributors_query = (
            db.query(
                Contributor.username,
                func.sum(Contribution.amount).label('total_contribution')
            )
            .join(Contribution, Contribution.contributor_id == Contributor.id)
            .filter(Contribution.project_id == project_id)
            .group_by(Contributor.id)
            .order_by(func.sum(Contribution.amount).desc())
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )

        return contributors_query
            

    @staticmethod
    def get_contributions_by_project(project_id: uuid.UUID, db: object) -> list:
        contributions = db.query(Contribution).filter(Contribution.project_id == project_id).all()
        if not contributions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No contributions found for this project"
            )
        return contributions
