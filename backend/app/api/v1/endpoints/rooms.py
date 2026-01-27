from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.room import Room
from app.schemas.room import (
    RoomCreate,
    RoomUpdate,
    RoomResponse,
    RoomListResponse
)

router = APIRouter()


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_in: RoomCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new room
    
    **Epic 1: User Story 1.6** - Define rooms with capacity, type, and location
    """
    # Check if room number already exists
    query = select(Room).where(Room.room_number == room_in.room_number)
    result = await db.execute(query)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room with number '{room_in.room_number}' already exists"
        )
    
    room = Room(**room_in.model_dump())
    
    db.add(room)
    await db.commit()
    await db.refresh(room)
    
    return room


@router.get("/", response_model=RoomListResponse)
async def list_rooms(
    skip: int = 0,
    limit: int = 100,
    room_type: str = None,
    has_lab_equipment: bool = None,
    min_capacity: int = None,
    building: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all rooms with optional filters
    """
    query = select(Room)
    
    if room_type:
        query = query.where(Room.room_type == room_type)
    if has_lab_equipment is not None:
        query = query.where(Room.has_lab_equipment == has_lab_equipment)
    if min_capacity:
        query = query.where(Room.capacity >= min_capacity)
    if building:
        query = query.where(Room.building == building)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    rooms = result.scalars().all()
    
    count_query = select(func.count()).select_from(Room)
    if room_type:
        count_query = count_query.where(Room.room_type == room_type)
    if has_lab_equipment is not None:
        count_query = count_query.where(Room.has_lab_equipment == has_lab_equipment)
    if min_capacity:
        count_query = count_query.where(Room.capacity >= min_capacity)
    if building:
        count_query = count_query.where(Room.building == building)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return RoomListResponse(data=rooms, total=total)


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific room by ID
    """
    query = select(Room).where(Room.id == room_id)
    result = await db.execute(query)
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )
    
    return room


@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int,
    room_update: RoomUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a room
    """
    query = select(Room).where(Room.id == room_id)
    result = await db.execute(query)
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )
    
    update_data = room_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)
    
    await db.commit()
    await db.refresh(room)
    
    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a room
    """
    query = select(Room).where(Room.id == room_id)
    result = await db.execute(query)
    room = result.scalar_one_or_none()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )
    
    await db.delete(room)
    await db.commit()
    
    return None
