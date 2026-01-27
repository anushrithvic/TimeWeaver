from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Dict, Any


ConstraintType = Literal[
    'NO_FACULTY_CLASH', 'NO_ROOM_CLASH', 'NO_STUDENT_CLASH',
    'WORKLOAD_LIMIT', 'ROOM_CAPACITY', 'LAB_REQUIREMENT',
    'PREFERENCE_TIME', 'PREFERENCE_DAY', 'MAX_CONSECUTIVE',
    'MIN_BREAK', 'MAX_COMMUTE', 'ELECTIVE_NO_CLASH'
]


class ConstraintBase(BaseModel):
    """Base Constraint schema"""
    name: str = Field(..., min_length=1, max_length=200, examples=["No faculty double booking"])
    constraint_type: ConstraintType = Field(..., examples=["NO_FACULTY_CLASH"])
    category: str = Field(default="institutional", max_length=50, examples=["institutional"])
    rule_definition: str = Field(..., min_length=1, examples=["A faculty member cannot teach two classes at the same time"])
    priority: int = Field(default=100, ge=0, le=1000, examples=[100])
    weight: float = Field(default=1.0, ge=0.0, le=1.0, examples=[1.0])
    is_hard: bool = Field(default=True, examples=[True])
    parameters: Optional[Dict[str, Any]] = Field(default=None, examples=[{"max_hours_per_day": 6}])
    is_active: bool = Field(default=True)


class ConstraintCreate(ConstraintBase):
    """Schema for creating a constraint"""
    pass


class ConstraintUpdate(BaseModel):
    """Schema for updating a constraint"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    constraint_type: Optional[ConstraintType] = None
    category: Optional[str] = Field(None, max_length=50)
    rule_definition: Optional[str] = Field(None, min_length=1)
    priority: Optional[int] = Field(None, ge=0, le=1000)
    weight: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_hard: Optional[bool] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ConstraintResponse(ConstraintBase):
    """Schema for constraint responses"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class ConstraintListResponse(BaseModel):
    """Schema for listing constraints"""
    data: list[ConstraintResponse]
    total: int


class ConstraintExplanation(BaseModel):
    """Schema for constraint explanation responses"""
    constraint_id: int
    name: str
    constraint_type: str
    is_hard: bool
    explanation: str
    examples: list[str]
    impact: str
