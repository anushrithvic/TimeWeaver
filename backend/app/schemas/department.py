from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class DepartmentBase(BaseModel):
    """
    Base Department schema - shared properties
    """
    name: str = Field(..., min_length=1, max_length=200, examples=["Computer Science & Engineering"])
    code: str = Field(..., min_length=2, max_length=10, examples=["CSE"])
    description: Optional[str] = Field(None, examples=["Department of Computer Science and Engineering"])


class DepartmentCreate(DepartmentBase):
    """
    Schema for creating a department
    """
    pass


class DepartmentUpdate(BaseModel):
    """
    Schema for updating a department - all fields optional
    """
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, min_length=2, max_length=10)
    description: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    """
    Schema for department responses - includes database fields
    """
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class DepartmentListResponse(BaseModel):
    """
    Schema for listing departments
    """
    data: list[DepartmentResponse]
    total: int
