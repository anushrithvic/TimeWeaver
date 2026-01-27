from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Department(Base):
    """
    Department model - represents an academic department
    Epic 1: User Story 1.3
    """
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    code = Column(String(10), nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # sections = relationship("Section", back_populates="department")
    # courses = relationship("Course", back_populates="department")
    
    def __repr__(self):
        return f"<Department(id={self.id}, code='{self.code}', name='{self.name}')>"
