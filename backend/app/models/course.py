"""
Course and Elective Group Database Models

This module defines two related SQLAlchemy models for academic course management:
1. ElectiveGroup - Groups of optional courses students can choose from
2. Course - Individual courses with theory/lab hour specifications

Epic 1: User Stories 1.4 and 1.5
- User Story 1.4: Define course details (theory hours, lab hours, credits)
- User Story 1.5: Define elective groups for student choice

Database Tables: elective_groups, courses

Relationships:
    - ElectiveGroup has many Courses (one-to-many)
    - Course belongs to one Department (many-to-one)
    - Course optionally belongs to one ElectiveGroup (many-to-one)
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ElectiveGroup(Base):
    """
    ElectiveGroup model representing a collection of elective courses.
    
    An elective group contains multiple courses from which students can
    choose a subset. For example, "Engineering Electives Group 1" might
    contain 5 courses, and students must select 2 of them.
    
    Attributes:
        id (int): Primary key, unique identifier
        name (str): Group name (e.g., "Engineering Electives Group 1")
        description (str): Optional detailed description
        semester_id (int): Foreign key to semester this group belongs to
        created_at (datetime): Record creation timestamp
    
    Relationships:
        semester: The semester this elective group is offered in
        courses: All courses that are part of this elective group
    
    Example:
        group = ElectiveGroup(
            name="Engineering Electives Group 1",
            description="First set of engineering electives for Sem 5",
            semester_id=1
        )
    """
    __tablename__ = "elective_groups"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Core Fields
    name = Column(String(100), nullable=False)  # E.g., "Engineering Electives Group 1"
    description = Column(String, nullable=True)  # Optional detailed description
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)  # Parent semester
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships (commented until circular imports resolved)
    # semester = relationship("Semester", back_populates="elective_groups")
    # courses = relationship("Course", back_populates="elective_group")
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<ElectiveGroup(id={self.id}, name='{self.name}')>"


class Course(Base):
    """
    Course model representing an academic course with theory and lab components.
    
    Courses can be core (required) or elective (optional). They specify the number
    of theory hours, lab hours, and total credits. Courses requiring labs must be
    scheduled in lab-type rooms with appropriate equipment.
    
    Attributes:
        id (int): Primary key, unique identifier
        code (str): Unique course code (e.g., "CS301")
        name (str): Full course name
        theory_hours (int): Weekly theory lecture hours (0-10)
        lab_hours (int): Weekly lab practice hours (0-10)
        credits (int): Academic credits awarded for completion
        department_id (int): Department offering this course
        is_elective (bool): True if course is elective, False if core/required
        elective_group_id (int): Optional foreign key if course is an elective
        requires_lab (bool): True if course needs lab facilities
        min_room_capacity (int): Minimum room capacity needed
        created_at (datetime): Record creation timestamp
    
    Constraints:
        - At least one of theory_hours or lab_hours must be > 0
        - Both theory_hours and lab_hours must be >= 0
        - Credits must be > 0
        - Course code must be unique
    
    Relationships:
        department: The department offering this course
        elective_group: The elective group this course belongs to (if elective)
    
    Example:
        course = Course(
            code="CS301",
            name="Data Structures and Algorithms",
            theory_hours=3,
            lab_hours=2,
            credits=4,
            department_id=1,
            requires_lab=True,
            min_room_capacity=60
        )
    """
    __tablename__ = "courses"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Core Identification Fields
    code = Column(String(20), nullable=False, unique=True, index=True)  # E.g., "CS301"
    name = Column(String(200), nullable=False)  # Full course name
    
    # Course Structure Fields
    theory_hours = Column(Integer, default=0, nullable=False)  # Weekly theory hours
    lab_hours = Column(Integer, default=0, nullable=False)  # Weekly lab hours
    credits = Column(Integer, nullable=False)  # Academic credits (typically 1-6)
    
    # Organizational Fields
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)  # Owning department
    is_elective = Column(Boolean, default=False)  # Core vs Elective flag
    elective_group_id = Column(Integer, ForeignKey("elective_groups.id"), nullable=True)  # Group if elective
    
    # Scheduling Requirements
    requires_lab = Column(Boolean, default=False)  # Needs lab facilities
    min_room_capacity = Column(Integer, nullable=True)  # Minimum seats required
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Database-level constraints to ensure data integrity
    # These are enforced by PostgreSQL
    __table_args__ = (
        CheckConstraint("theory_hours + lab_hours > 0", name="check_hours_positive"),
        CheckConstraint("theory_hours >= 0", name="check_theory_hours_nonnegative"),
        CheckConstraint("lab_hours >= 0", name="check_lab_hours_nonnegative"),
        CheckConstraint("credits > 0", name="check_credits_positive"),
    )
    
    # Relationships (commented until circular imports resolved)
    # department = relationship("Department", back_populates="courses")
    # elective_group = relationship("ElectiveGroup", back_populates="courses")
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<Course(id={self.id}, code='{self.code}', name='{self.name}')>"
