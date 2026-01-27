from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class RoomBase(BaseModel):
    """Base Room schema"""
    room_number: str = Field(..., min_length=1, max_length=50, examples=["Lab 201"])
    room_type: Literal['classroom', 'lab', 'auditorium', 'seminar_hall'] = Field(..., examples=["classroom"])
    capacity: int = Field(..., gt=0, examples=[60])
    has_projector: bool = Field(default=False)
    has_lab_equipment: bool = Field(default=False)
    has_ac: bool = Field(default=False)
    building: Optional[str] = Field(None, max_length=100, examples=["Engineering Block A"])
    floor: Optional[int] = Field(None, examples=[2])
    location_x: Optional[float] = Field(None, examples=[100.5])
    location_y: Optional[float] = Field(None, examples=[50.3])


class RoomCreate(RoomBase):
    """Schema for creating a room"""
    pass


class RoomUpdate(BaseModel):
    """Schema for updating a room"""
    room_number: Optional[str] = Field(None, min_length=1, max_length=50)
    room_type: Optional[Literal['classroom', 'lab', 'auditorium', 'seminar_hall']] = None
    capacity: Optional[int] = Field(None, gt=0)
    has_projector: Optional[bool] = None
    has_lab_equipment: Optional[bool] = None
    has_ac: Optional[bool] = None
    building: Optional[str] = Field(None, max_length=100)
    floor: Optional[int] = None
    location_x: Optional[float] = None
    location_y: Optional[float] = None


class RoomResponse(RoomBase):
    """Schema for room responses"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class RoomListResponse(BaseModel):
    """Schema for listing rooms"""
    data: list[RoomResponse]
    total: int
