from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.utils import ProjectUtils, UserUtils
from app.config.database import get_db
from app.model.authentication import User
from app.model.projects import Project
from app.schema.authentication import MyDetailsResponseSchema
from app.schema.projects import ProjectRequestSchema, ProjectResponseSchema


router = APIRouter(prefix="/projects")


@router.post("", response_model=ProjectResponseSchema)
async def create_project(project: ProjectRequestSchema, db: Session = Depends(get_db), current_user: User = Depends(UserUtils.get_current_user)):
    print(project)
    new_project = ProjectUtils.create_project(project, current_user, db)
    return ProjectResponseSchema(
        id=new_project.id,
        title=new_project.title,
        description=new_project.description,
        goal_amount=new_project.goal_amount,
        deadline=new_project.deadline,
        current_user=MyDetailsResponseSchema.from_orm(new_project.creator)
    )