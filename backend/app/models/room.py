from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.db.session import Base


class Room(Base):
    """
    Room model - represents a classroom or lab
    Epic 1: User Story 1.6
    """
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(50), nullable=False, unique=True, index=True)
    room_type = Column(
        String(50), 
        nullable=False,
        # Will validate in Pydantic schema
    )
    capacity = Column(Integer, nullable=False)
    has_projector = Column(Boolean, default=False)
    has_lab_equipment = Column(Boolean, default=False)
    has_ac = Column(Boolean, default=False)
    building = Column(String(100), nullable=True)
    floor = Column(Integer, nullable=True)
    location_x = Column(Float, nullable=True)
    location_y = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        CheckConstraint("capacity > 0", name="check_capacity_positive"),
        CheckConstraint("room_type IN ('classroom', 'lab', 'auditorium', 'seminar_hall')", name="check_room_type_valid"),
    )
    
    def __repr__(self):
        return f"<Room(id={self.id}, number='{self.room_number}', type='{self.room_type}')>"
