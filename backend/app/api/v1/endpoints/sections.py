from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.section import Section
from app.schemas.section import (
    SectionCreate,
    SectionUpdate,
    SectionResponse,
    SectionListResponse
)

router = APIRouter()


@router.post("/", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
async def create_section(
    section_in: SectionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new section
    
    **Epic 1: User Story 1.3** - Define sections
    """
    section = Section(**section_in.model_dump())
    
    db.add(section)
    await db.commit()
    await db.refresh(section)
    
    return section


@router.get("/", response_model=SectionListResponse)
async def list_sections(
    skip: int = 0,
    limit: int = 100,
    semester_id: int = None,
    department_id: int = None,
    year: int = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all sections with optional filters
    """
    query = select(Section)
    
    if semester_id:
        query = query.where(Section.semester_id == semester_id)
    if department_id:
        query = query.where(Section.department_id == department_id)
    if year:
        query = query.where(Section.year == year)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    sections = result.scalars().all()
    
    count_query = select(func.count()).select_from(Section)
    if semester_id:
        count_query = count_query.where(Section.semester_id == semester_id)
    if department_id:
        count_query = count_query.where(Section.department_id == department_id)
    if year:
        count_query = count_query.where(Section.year == year)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return SectionListResponse(data=sections, total=total)


@router.get("/{section_id}", response_model=SectionResponse)
async def get_section(
    section_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific section by ID
   """
    query = select(Section).where(Section.id == section_id)
    result = await db.execute(query)
    section = result.scalar_one_or_none()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with id {section_id} not found"
        )
    
    return section


@router.put("/{section_id}", response_model=SectionResponse)
async def update_section(
    section_id: int,
    section_update: SectionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a section
    """
    query = select(Section).where(Section.id == section_id)
    result = await db.execute(query)
    section = result.scalar_one_or_none()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with id {section_id} not found"
        )
    
    update_data = section_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(section, field, value)
    
    await db.commit()
    await db.refresh(section)
    
    return section


@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(
    section_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a section
    """
    query = select(Section).where(Section.id == section_id)
    result = await db.execute(query)
    section = result.scalar_one_or_none()
    
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section with id {section_id} not found"
        )
    
    await db.delete(section)
    await db.commit()
    
    return None
