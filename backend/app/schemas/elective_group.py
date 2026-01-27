from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ElectiveGroupBase(BaseModel):
    """Base ElectiveGroup schema"""
    name: str = Field(..., min_length=1, max_length=100, examples=["Engineering Electives Group 1"])
    description: Optional[str] = Field(None, examples=["First set of engineering electives"])
    semester_id: int = Field(..., gt=0)


class ElectiveGroupCreate(ElectiveGroupBase):
    """Schema for creating an elective group"""
    pass


class ElectiveGroupUpdate(BaseModel):
    """Schema for updating an elective group"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    semester_id: Optional[int] = Field(None, gt=0)


class ElectiveGroupResponse(ElectiveGroupBase):
    """Schema for elective group responses"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class ElectiveGroupListResponse(BaseModel):
    """Schema for listing elective groups"""
    data: list[ElectiveGroupResponse]
    total: int
