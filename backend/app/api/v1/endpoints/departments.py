from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.session import get_db
from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentListResponse
)

router = APIRouter()


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_in: DepartmentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new department
    
    **Epic 1: User Story 1.3** - Define departments
    """
    # Check if department code already exists
    query = select(Department).where(Department.code == department_in.code)
    result = await db.execute(query)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Department with code '{department_in.code}' already exists"
        )
    
    department = Department(**department_in.model_dump())
    
    db.add(department)
    await db.commit()
    await db.refresh(department)
    
    return department


@router.get("/", response_model=DepartmentListResponse)
async def list_departments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all departments
    """
    query = select(Department).offset(skip).limit(limit)
    result = await db.execute(query)
    departments = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(Department)
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return DepartmentListResponse(data=departments, total=total)


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific department by ID
    """
    query = select(Department).where(Department.id == department_id)
    result = await db.execute(query)
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found"
        )
    
    return department


@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department_update: DepartmentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a department
    """
    query = select(Department).where(Department.id == department_id)
    result = await db.execute(query)
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found"
        )
    
    update_data = department_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(department, field, value)
    
    await db.commit()
    await db.refresh(department)
    
    return department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a department
    """
    query = select(Department).where(Department.id == department_id)
    result = await db.execute(query)
    department = result.scalar_one_or_none()
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id {department_id} not found"
        )
    
    await db.delete(department)
    await db.commit()
    
    return None
