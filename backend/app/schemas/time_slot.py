from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Literal
from datetime import time


class TimeSlotBase(BaseModel):
    """Base TimeSlot schema"""
    day_of_week: Literal['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] = Field(
        ..., examples=["Monday"]
    )
    start_time: time = Field(..., examples=["09:00:00"])
    end_time: time = Field(..., examples=["10:00:00"])
    duration_minutes: int = Field(..., gt=0, examples=[60])
    is_break: bool = Field(default=False)
    slot_type: str = Field(default="regular", max_length=50, examples=["regular"])
    
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, v, info):
        """Ensure end_time > start_time"""
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class TimeSlotCreate(TimeSlotBase):
    """Schema for creating a time slot"""
    pass


class TimeSlotUpdate(BaseModel):
    """Schema for updating a time slot"""
    day_of_week: Optional[Literal['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    duration_minutes: Optional[int] = Field(None, gt=0)
    is_break: Optional[bool] = None
    slot_type: Optional[str] = Field(None, max_length=50)


class TimeSlotResponse(TimeSlotBase):
    """Schema for time slot responses"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class TimeSlotListResponse(BaseModel):
    """Schema for listing time slots"""
    data: list[TimeSlotResponse]
    total: int
