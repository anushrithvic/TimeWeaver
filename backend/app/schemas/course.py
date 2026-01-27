from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional


class CourseBase(BaseModel):
    """Base Course schema"""
    code: str = Field(..., min_length=2, max_length=20, examples=["CS301"])
    name: str = Field(..., min_length=1, max_length=200, examples=["Data Structures and Algorithms"])
    theory_hours: int = Field(default=0, ge=0, examples=[3])
    lab_hours: int = Field(default=0, ge=0, examples=[2])
    credits: int = Field(..., gt=0, examples=[4])
    department_id: int = Field(..., gt=0)
    is_elective: bool = Field(default=False)
    elective_group_id: Optional[int] = Field(None, gt=0)
    requires_lab: bool = Field(default=False)
    min_room_capacity: Optional[int] = Field(None, gt=0)
    
    @field_validator('theory_hours', 'lab_hours')
    @classmethod
    def validate_hours(cls, v, info):
        """Ensure at least one of theory_hours or lab_hours is > 0"""
        return v


class CourseCreate(CourseBase):
    """Schema for creating a course"""
    
    @field_validator('theory_hours')
    @classmethod
    def validate_total_hours(cls, v, info):
        """Ensure theory_hours + lab_hours > 0"""
        data = info.data
        if 'lab_hours' in data and v + data['lab_hours'] == 0:
            raise ValueError('Course must have at least theory or lab hours')
        return v


class CourseUpdate(BaseModel):
    """Schema for updating a course"""
    code: Optional[str] = Field(None, min_length=2, max_length=20)
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    theory_hours: Optional[int] = Field(None, ge=0)
    lab_hours: Optional[int] = Field(None, ge=0)
    credits: Optional[int] = Field(None, gt=0)
    department_id: Optional[int] = Field(None, gt=0)
    is_elective: Optional[bool] = None
    elective_group_id: Optional[int] = Field(None, gt=0)
    requires_lab: Optional[bool] = None
    min_room_capacity: Optional[int] = Field(None, gt=0)


class CourseResponse(CourseBase):
    """Schema for course responses"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class CourseListResponse(BaseModel):
    """Schema for listing courses"""
    data: list[CourseResponse]
    total: int
