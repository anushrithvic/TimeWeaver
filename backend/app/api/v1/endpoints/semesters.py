from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.session import get_db
from app.models.semester import Semester
from app.schemas.semester import (
    SemesterCreate,
    SemesterUpdate,
    SemesterResponse,
    SemesterListResponse
)

router = APIRouter()


@router.post("/", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
async def create_semester(
    semester_in: SemesterCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new semester
    
    **Epic 1: User Story 1.3** - Define semesters and sections
    """
    # Create new semester instance
    semester = Semester(**semester_in.model_dump())
    
    db.add(semester)
    await db.commit()
    await db.refresh(semester)
    
    return semester


@router.get("/", response_model=SemesterListResponse)
async def list_semesters(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all semesters
    
    **Query Parameters:**
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    - active_only: Filter for only active semesters
    """
    # Build query
    query = select(Semester)
    
    if active_only:
        query = query.where(Semester.is_active == True)
    
    query = query.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    semesters = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(Semester)
    if active_only:
        count_query = count_query.where(Semester.is_active == True)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return SemesterListResponse(data=semesters, total=total)


@router.get("/{semester_id}", response_model=SemesterResponse)
async def get_semester(
    semester_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific semester by ID
    """
    query = select(Semester).where(Semester.id == semester_id)
    result = await db.execute(query)
    semester = result.scalar_one_or_none()
    
    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semester with id {semester_id} not found"
        )
    
    return semester


@router.put("/{semester_id}", response_model=SemesterResponse)
async def update_semester(
    semester_id: int,
    semester_update: SemesterUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a semester
    """
    # Get existing semester
    query = select(Semester).where(Semester.id == semester_id)
    result = await db.execute(query)
    semester = result.scalar_one_or_none()
    
    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semester with id {semester_id} not found"
        )
    
    # Update fields
    update_data = semester_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(semester, field, value)
    
    await db.commit()
    await db.refresh(semester)
    
    return semester


@router.delete("/{semester_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_semester(
    semester_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a semester
    
    **Warning:** This will cascade delete all related sections and data
    """
    query = select(Semester).where(Semester.id == semester_id)
    result = await db.execute(query)
    semester = result.scalar_one_or_none()
    
    if not semester:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Semester with id {semester_id} not found"
        )
    
    await db.delete(semester)
    await db.commit()
    
    return None
