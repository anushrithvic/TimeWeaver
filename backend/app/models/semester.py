"""
Semester Database Model

This module defines the Semester SQLAlchemy model representing academic
semesters or terms in the TimeWeaver system.

Epic 1: User Story 1.3 - Define semesters and sections

A semester represents a distinct academic period (e.g., Fall 2026, Spring 2027)
with specific start and end dates. Semesters contain sections and elective groups.

Database Table: semesters

Relationships:
    - One semester has many sections (one-to-many)
    - One semester has many elective groups (one-to-many)
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Semester(Base):
    """
    Semester model representing an academic term/semester.
    
    A semester defines a time-bound academic period during which courses
    are taught. It serves as a container for sections and elective groups,
    and helps organize academic data by time period.
    
    Attributes:
        id (int): Primary key, auto-incrementing unique identifier
        name (str): Semester name (e.g., "Fall 2026", "Spring 2027")
        academic_year (str): Academic year in format "YYYY-YYYY" (e.g., "2026-2027")
        start_date (date): First day of the semester
        end_date (date): Last day of the semester
        is_active (bool): Whether this semester is currently active
        created_at (datetime): Timestamp when record was created
        updated_at (datetime): Timestamp when record was last modified
    
    Relationships:
        sections: All sections belonging to this semester
        elective_groups: All elective groups for this semester
    
    Example:
        semester = Semester(
            name="Fall 2026",
            academic_year="2026-2027",
            start_date=date(2026, 8, 15),
            end_date=date(2026, 12, 20),
            is_active=True
        )
    """
    __tablename__ = "semesters"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Core Fields
    name = Column(String(100), nullable=False)  # E.g., "Fall 2026"
    academic_year = Column(String(20), nullable=False)  # E.g., "2026-2027"
    start_date = Column(Date, nullable=False)  # Semester start date
    end_date = Column(Date, nullable=False)  # Semester end date
    is_active = Column(Boolean, default=True)  # Active/inactive flag
    
    # Timestamps - automatically managed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships (commented out until circular import issues are resolved)
    # When uncommented, these will enable:
    # - semester.sections to access all sections in this semester
    # - semester.elective_groups to access all elective groups
    # - CASCADE delete: deleting semester also deletes its sections
    # sections = relationship("Section", back_populates="semester", cascade="all, delete-orphan")
    # elective_groups = relationship("ElectiveGroup", back_populates="semester")
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<Semester(id={self.id}, name='{self.name}', year='{self.academic_year}')>"
