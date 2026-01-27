"""
Constraint Database Model

This module defines the Constraint SQLAlchemy model for representing scheduling
rules and preferences in the TimeWeaver timetable generation system.

Epic 1: User Story 1.2 - Set fixed rules and flexible preferences

Constraints are the core of the AI scheduling engine. They define both:
1. **Hard Constraints**: Must be satisfied (e.g., no room conflicts)
2. **Soft Constraints**: Preferences to optimize (e.g., preferred time slots)

The constraint engine uses these rules to generate valid timetables while
maximizing satisfaction of soft constraints within priority weights.

Database Table: constraints

Constraint Types:
    - NO_FACULTY_CLASH: Prevent faculty double-booking
    - NO_ROOM_CLASH: Prevent room double-booking
    - NO_STUDENT_CLASH: Prevent student schedule conflicts
    - WORKLOAD_LIMIT: Faculty workload restrictions
    - ROOM_CAPACITY: Ensure adequate room size
    - LAB_REQUIREMENT: Assign lab courses to lab rooms
    - PREFERENCE_TIME: Time slot preferences
    - PREFERENCE_DAY: Day of week preferences
    - MAX_CONSECUTIVE: Limit consecutive teaching hours
    - MIN_BREAK: Ensure minimum break time
    - MAX_COMMUTE: Limit travel between distant rooms
    - ELECTIVE_NO_CLASH: Prevent elective conflicts
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, CheckConstraint, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.session import Base


class Constraint(Base):
    """
    Constraint model representing scheduling rules and preferences.
    
    Constraints encode the business rules and preferences for timetable generation.
    Hard constraints must be satisfied for a valid timetable, while soft constraints
    are optimized using weighted scoring.
    
    The constraint system supports:
    - Flexible parameter storage using JSONB
    - Priority-based constraint ordering (0-1000)
    - Weight-based optimization for soft constraints (0.0-1.0)
    - Active/inactive toggling without deletion
    
    Attributes:
        id (int): Primary key
        name (str): Human-readable constraint name
        constraint_type (str): Type from predefined constraint types
        category (str): Organizational category (e.g., "institutional", "faculty")
        rule_definition (str): Plain English explanation of the rule
        priority (int): Priority level (0-1000, higher = more important)
        weight (float): Optimization weight for soft constraints (0.0-1.0)
        is_hard (bool): True if constraint must be satisfied, False if preference
        parameters (dict): JSON object with constraint-specific parameters
        is_active (bool): Whether constraint is currently in use
        created_at (datetime): Record creation timestamp
        updated_at (datetime): Last modification timestamp
    
    Constraint Types:
        NO_FACULTY_CLASH: Faculty cannot teach multiple classes simultaneously
        NO_ROOM_CLASH: Rooms cannot be double-booked
        NO_STUDENT_CLASH: Students cannot have conflicting schedules
        WORKLOAD_LIMIT: Faculty teaching hour limits per day/week
        ROOM_CAPACITY: Assigned room must fit all students
        LAB_REQUIREMENT: Lab courses need lab-equipped rooms
        PREFERENCE_TIME: Preferred time slots (soft)
        PREFERENCE_DAY: Preferred days of week (soft)
        MAX_CONSECUTIVE: Maximum consecutive teaching hours
        MIN_BREAK: Minimum break time between classes
        MAX_COMMUTE: Maximum walking distance between rooms
        ELECTIVE_NO_CLASH: Prevent conflicts in elective groups
    
    Example:
        # Hard constraint - no faculty conflicts
        constraint = Constraint(
            name="No faculty double booking",
            constraint_type="NO_FACULTY_CLASH",
            rule_definition="Faculty cannot teach two classes at the same time",
            priority=100,
            is_hard=True,
            parameters={"strict_mode": True}
        )
        
        # Soft constraint - morning preference
        preference = Constraint(
            name="Prefer morning slots for theory courses",
            constraint_type="PREFERENCE_TIME",
            rule_definition="Theory courses preferred before 12:00 PM",
            priority=50,
            weight=0.8,
            is_hard=False,
            parameters={"before_time": "12:00", "course_types": ["theory"]}
        )
    """
    __tablename__ = "constraints"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Identification Fields
    name = Column(String(200), nullable=False)  # Human-readable name
    constraint_type = Column(String(50), nullable=False)  # Predefined type from enum
    category = Column(String(50), default="institutional")  # Organizational grouping
    
    # Rule Definition
    rule_definition = Column(Text, nullable=False)  # Plain English explanation
    
    # Constraint Priority and Weight
    priority = Column(Integer, default=100, nullable=False)  # 0-1000, higher = more important
    weight = Column(Float, default=1.0, nullable=False)  # 0.0-1.0 for soft constraint optimization
    
    # Constraint Type
    is_hard = Column(Boolean, default=True)  # True = must satisfy, False = optimize
    
    # Flexible Parameters Storage
    # JSONB allows storing constraint-specific parameters without schema changes
    # Example: {"max_hours": 6, "time_slots": [1,2,3], "exemptions": ["faculty_id_123"]}
    parameters = Column(JSONB, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)  # Toggle constraints on/off
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Database-level validation constraints
    __table_args__ = (
        # Priority must be in valid range
        CheckConstraint("priority >= 0 AND priority <= 1000", name="check_priority_range"),
        # Weight must be normalized between 0 and 1
        CheckConstraint("weight >= 0 AND weight <= 1", name="check_weight_range"),
        # Constraint type must be one of the predefined types
        CheckConstraint(
            """constraint_type IN (
                'NO_FACULTY_CLASH', 'NO_ROOM_CLASH', 'NO_STUDENT_CLASH',
                'WORKLOAD_LIMIT', 'ROOM_CAPACITY', 'LAB_REQUIREMENT',
                'PREFERENCE_TIME', 'PREFERENCE_DAY', 'MAX_CONSECUTIVE',
                'MIN_BREAK', 'MAX_COMMUTE', 'ELECTIVE_NO_CLASH'
            )""",
            name="check_constraint_type_valid"
        ),
    )
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<Constraint(id={self.id}, name='{self.name}', type='{self.constraint_type}', hard={self.is_hard})>"
