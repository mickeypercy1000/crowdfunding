from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.common.utils import ProjectUtils, UserUtils
from app.config.database import get_db
from app.model.authentication import User
from app.model.projects import Contribution, Project
from app.schema.authentication import MyDetailsResponseSchema
from app.schema.projects import ContributionRequestSchema, ContributionResponseSchema, ModifiedProjectResponseSchema, ProjectContributors, ProjectRequestSchema, ProjectResponseSchema


router = APIRouter(prefix="/projects")


@router.post("", response_model=ProjectResponseSchema)
async def create_project(project: ProjectRequestSchema, db: Session = Depends(get_db), current_user: User = Depends(UserUtils.get_current_user)):
    new_project = ProjectUtils.create_project(project, current_user, db)
    total_contributors = db.query(Contribution.contributor_id).filter(Contribution.project_id == new_project.id).distinct().count()

    return ProjectResponseSchema(
        id=new_project.id,
        title=new_project.title.title(),
        description=new_project.description,
        goal_amount=new_project.goal_amount,
        total_contribution=new_project.total_contribution,
        deadline=new_project.deadline,
        total_contributors=total_contributors,
        creator=MyDetailsResponseSchema.model_validate(new_project.creator),
    )


@router.post("/{project_id}/contributions")
async def contribute_to_project(
    project_id: uuid.UUID,
    contribution: ContributionRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(UserUtils.get_current_user)
):
    project = ProjectUtils.get_project_by_id(project_id, db)
    contribute = ProjectUtils.create_contribution(contribution, project, current_user, db)
    return ContributionResponseSchema(
        id=contribute.id,
        amount=contribute.amount,
        contributor=MyDetailsResponseSchema.model_validate(contribute.contributor),
        project=ProjectResponseSchema.model_validate(project)
    )


@router.get("", response_model=List[ProjectResponseSchema])
async def get_projects(
    db: Session = Depends(get_db),
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100)
):
    projects = db.query(Project).offset(skip).limit(limit).all()
    return [
        ProjectResponseSchema(
            id=project.id,
            title=project.title,
            description=project.description or "",
            goal_amount=project.goal_amount,
            deadline=project.deadline,
            total_contribution=project.total_contribution,
            creator=MyDetailsResponseSchema.model_validate(project.creator),
        )
        for project in projects
    ]


@router.get("/{project_id}", response_model=ModifiedProjectResponseSchema)
async def get_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    project = ProjectUtils.get_project_by_id(project_id, db)
    contributors_query = (
        db.query(User.username, func.sum(Contribution.amount).label("total_contribution"))
        .join(Contribution, Contribution.contributor_id == User.id)
        .filter(Contribution.project_id == project_id)
        .group_by(User.username)
        .all()
    )
    contributors_data = [
        ProjectContributors(username=contributor.username, amount=contributor.total_contribution)
        for contributor in contributors_query
    ]
    return ModifiedProjectResponseSchema(
        project=ProjectResponseSchema(
            id=project.id,
            title=project.title,
            description=project.description,
            goal_amount=project.goal_amount,
            total_contribution=project.total_contribution,
            deadline=project.deadline,
            creator=MyDetailsResponseSchema.model_validate(project.creator),
        ),
        contributors=contributors_data,
    )

@router.get("/{project_id}/contributions", response_model=List[ContributionResponseSchema])
async def get_contribution(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, le=100)
):
    project = ProjectUtils.get_project_by_id(project_id, db)
    contributions_query = (
        db.query(Contribution)
        .filter(Contribution.project_id == project_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        ContributionResponseSchema(
            id=contribution.id,
            amount=contribution.amount,
            project=project,
            contributor=MyDetailsResponseSchema.model_validate(contribution.contributor)
        )
        for contribution in contributions_query
    ]


@router.get("/{project_id}/contributions/{contribution_id}", response_model=ContributionResponseSchema)
async def get_single_contribution(
    project_id: uuid.UUID,
    contribution_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    project = ProjectUtils.get_project_by_id(project_id, db)
    
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id, Contribution.project_id == project_id).first()

    if not contribution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contribution not found"
        )
    
    return ContributionResponseSchema(
        id=contribution.id,
        amount=contribution.amount,
        project=project,
        contributor=MyDetailsResponseSchema.model_validate(contribution.contributor)
    )
