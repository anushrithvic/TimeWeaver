from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.course import Course
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse
)

router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new course
    
    **Epic 1: User Story 1.4** - Define course details
    """
    # Check if course code already exists
    query = select(Course).where(Course.code == course_in.code)
    result = await db.execute(query)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with code '{course_in.code}' already exists"
        )
    
    course = Course(**course_in.model_dump())
    
    db.add(course)
    await db.commit()
    await db.refresh(course)
    
    return course


@router.get("/", response_model=CourseListResponse)
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    department_id: int = None,
    is_elective: bool = None,
    requires_lab: bool = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all courses with optional filters
    """
    query = select(Course)
    
    if department_id:
        query = query.where(Course.department_id == department_id)
    if is_elective is not None:
        query = query.where(Course.is_elective == is_elective)
    if requires_lab is not None:
        query = query.where(Course.requires_lab == requires_lab)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    courses = result.scalars().all()
    
    count_query = select(func.count()).select_from(Course)
    if department_id:
        count_query = count_query.where(Course.department_id == department_id)
    if is_elective is not None:
        count_query = count_query.where(Course.is_elective == is_elective)
    if requires_lab is not None:
        count_query = count_query.where(Course.requires_lab == requires_lab)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return CourseListResponse(data=courses, total=total)


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific course by ID
    """
    query = select(Course).where(Course.id == course_id)
    result = await db.execute(query)
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    return course


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_update: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a course
    """
    query = select(Course).where(Course.id == course_id)
    result = await db.execute(query)
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    await db.commit()
    await db.refresh(course)
    
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a course
    """
    query = select(Course).where(Course.id == course_id)
    result = await db.execute(query)
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    
    await db.delete(course)
    await db.commit()
    
    return None
