from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Section(Base):
    """
    Section model - represents a class section
    Epic 1: User Story 1.3
    """
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id", ondelete="CASCADE"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    name = Column(String(50), nullable=False)
    year = Column(Integer, CheckConstraint("year >= 1 AND year <= 4"), nullable=False)
    student_count = Column(Integer, CheckConstraint("student_count > 0"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    # semester = relationship("Semester", back_populates="sections")
    # department = relationship("Department", back_populates="sections")
    
    def __repr__(self):
        return f"<Section(id={self.id}, name='{self.name}', year={self.year})>"
