from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.time_slot import TimeSlot
from app.schemas.time_slot import (
    TimeSlotCreate,
    TimeSlotUpdate,
    TimeSlotResponse,
    TimeSlotListResponse
)

router = APIRouter()


@router.post("/", response_model=TimeSlotResponse, status_code=status.HTTP_201_CREATED)
async def create_time_slot(
    slot_in: TimeSlotCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new time slot
    
    **Epic 1: User Story 1.1** - Define slot patterns, breaks, and durations
    """
    slot = TimeSlot(**slot_in.model_dump())
    
    db.add(slot)
    await db.commit()
    await db.refresh(slot)
    
    return slot


@router.get("/", response_model=TimeSlotListResponse)
async def list_time_slots(
    skip: int = 0,
    limit: int = 100,
    day_of_week: str = None,
    is_break: bool = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all time slots
    """
    query = select(TimeSlot)
    
    if day_of_week:
        query = query.where(TimeSlot.day_of_week == day_of_week)
    if is_break is not None:
        query = query.where(TimeSlot.is_break == is_break)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    slots = result.scalars().all()
    
    count_query = select(func.count()).select_from(TimeSlot)
    if day_of_week:
        count_query = count_query.where(TimeSlot.day_of_week == day_of_week)
    if is_break is not None:
        count_query = count_query.where(TimeSlot.is_break == is_break)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return TimeSlotListResponse(data=slots, total=total)


@router.get("/{slot_id}", response_model=TimeSlotResponse)
async def get_time_slot(
    slot_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific time slot by ID
    """
    query = select(TimeSlot).where(TimeSlot.id == slot_id)
    result = await db.execute(query)
    slot = result.scalar_one_or_none()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Time slot with id {slot_id} not found"
        )
    
    return slot


@router.put("/{slot_id}", response_model=TimeSlotResponse)
async def update_time_slot(
    slot_id: int,
    slot_update: TimeSlotUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a time slot
    """
    query = select(TimeSlot).where(TimeSlot.id == slot_id)
    result = await db.execute(query)
    slot = result.scalar_one_or_none()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Time slot with id {slot_id} not found"
        )
    
    update_data = slot_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(slot, field, value)
    
    await db.commit()
    await db.refresh(slot)
    
    return slot


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_time_slot(
    slot_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a time slot
    """
    query = select(TimeSlot).where(TimeSlot.id == slot_id)
    result = await db.execute(query)
    slot = result.scalar_one_or_none()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Time slot with id {slot_id} not found"
        )
    
    await db.delete(slot)
    await db.commit()
    
    return None
