from sqlalchemy import Column, Integer, String, Time, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.db.session import Base


class TimeSlot(Base):
    """
    TimeSlot model - represents a time slot in the timetable
    Epic 1: User Story 1.1
    """
    __tablename__ = "time_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(String(10), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_break = Column(Boolean, default=False)
    slot_type = Column(String(50), default="regular")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        CheckConstraint(
            "day_of_week IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')", 
            name="check_day_valid"
        ),
        # Note: end_time > start_time will be validated in Pydantic
    )
    
    def __repr__(self):
        return f"<TimeSlot(id={self.id}, day='{self.day_of_week}', time={self.start_time}-{self.end_time})>"
