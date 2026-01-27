from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.course import ElectiveGroup
from app.schemas.elective_group import (
    ElectiveGroupCreate,
    ElectiveGroupUpdate,
    ElectiveGroupResponse,
    ElectiveGroupListResponse
)

router = APIRouter()


@router.post("/", response_model=ElectiveGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_elective_group(
    group_in: ElectiveGroupCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new elective group
    
    **Epic 1: User Story 1.5** - Define elective groups
    """
    group = ElectiveGroup(**group_in.model_dump())
    
    db.add(group)
    await db.commit()
    await db.refresh(group)
    
    return group


@router.get("/", response_model=ElectiveGroupListResponse)
async def list_elective_groups(
    skip: int = 0,
    limit: int = 100,
    semester_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all elective groups
    """
    query = select(ElectiveGroup)
    
    if semester_id:
        query = query.where(ElectiveGroup.semester_id == semester_id)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    groups = result.scalars().all()
    
    count_query = select(func.count()).select_from(ElectiveGroup)
    if semester_id:
        count_query = count_query.where(ElectiveGroup.semester_id == semester_id)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return ElectiveGroupListResponse(data=groups, total=total)


@router.get("/{group_id}", response_model=ElectiveGroupResponse)
async def get_elective_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific elective group by ID
    """
    query = select(ElectiveGroup).where(ElectiveGroup.id == group_id)
    result = await db.execute(query)
    group = result.scalar_one_or_none()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elective group with id {group_id} not found"
        )
    
    return group


@router.put("/{group_id}", response_model=ElectiveGroupResponse)
async def update_elective_group(
    group_id: int,
    group_update: ElectiveGroupUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an elective group
    """
    query = select(ElectiveGroup).where(ElectiveGroup.id == group_id)
    result = await db.execute(query)
    group = result.scalar_one_or_none()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elective group with id {group_id} not found"
        )
    
    update_data = group_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)
    
    await db.commit()
    await db.refresh(group)
    
    return group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_elective_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an elective group
    """
    query = select(ElectiveGroup).where(ElectiveGroup.id == group_id)
    result = await db.execute(query)
    group = result.scalar_one_or_none()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Elective group with id {group_id} not found"
        )
    
    await db.delete(group)
    await db.commit()
    
    return None
