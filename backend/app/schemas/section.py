from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class SectionBase(BaseModel):
    """Base Section schema"""
    semester_id: int = Field(..., gt=0)
    department_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=50, examples=["Section A"])
    year: int = Field(..., ge=1, le=4, examples=[1])
    student_count: int = Field(..., gt=0, examples=[60])


class SectionCreate(SectionBase):
    """Schema for creating a section"""
    pass


class SectionUpdate(BaseModel):
    """Schema for updating a section"""
    semester_id: Optional[int] = Field(None, gt=0)
    department_id: Optional[int] = Field(None, gt=0)
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    year: Optional[int] = Field(None, ge=1, le=4)
    student_count: Optional[int] = Field(None, gt=0)


class SectionResponse(SectionBase):
    """Schema for section responses"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class SectionListResponse(BaseModel):
    """Schema for listing sections"""
    data: list[SectionResponse]
    total: int
