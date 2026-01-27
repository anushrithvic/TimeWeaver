"""
Constraints API Endpoints

This module provides RESTful CRUD operations and AI-powered explainability
for scheduling constraints in the TimeWeaver system.

Epic 1: User Story 1.2 - Set fixed rules and flexible preferences

Constraints are the foundation of the intelligent timetabling system. This API
allows administrators to define, manage, and understand scheduling rules.

**Special Features:**
- Full CRUD operations for constraint management
- Filtering by constraint type, hard/soft, and active status
- **AI Explainability**: `/explain` endpoint provides human-readable explanations
- Support for both hard constraints (must satisfy) and soft constraints (preferences)
- JSONB parameter storage for flexible constraint configuration

Endpoints:
    POST / - Create new constraint
    GET / - List constraints with filters
    GET /{id} - Get constraint details
    GET /{id}/explain - Get AI-generated explanation ⭐
    PUT /{id} - Update constraint
    DELETE /{id} - Delete constraint

The explainability feature makes the AI's decision-making transparent,
helping administrators understand why certain scheduling decisions are made.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db.session import get_db
from app.models.constraint import Constraint
from app.schemas.constraint import (
    ConstraintCreate,
    ConstraintUpdate,
    ConstraintResponse,
    ConstraintListResponse,
    ConstraintExplanation
)

router = APIRouter()


@router.post("/", response_model=ConstraintResponse, status_code=status.HTTP_201_CREATED)
async def create_constraint(
    constraint_in: ConstraintCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new scheduling constraint.
    
    **Epic 1: User Story 1.2** - Set fixed rules and flexible preferences
    
    Constraints can be either hard (must be satisfied) or soft (preferences to optimize).
    Use the `is_hard` field to distinguish between the two types.
    
    Args:
        constraint_in: Constraint creation data including type, priority, and parameters
        db: Database session (injected dependency)
    
    Returns:
        ConstraintResponse: The created constraint with database-generated ID
    
    Example Request:
        POST /api/v1/constraints
        {
            "name": "No faculty double booking",
            "constraint_type": "NO_FACULTY_CLASH",
            "rule_definition": "Faculty cannot teach two classes simultaneously",
            "priority": 100,
            "is_hard": true,
            "parameters": {"strict_mode": true}
        }
    
    Example Response (201 Created):
        {
            "id": 1,
            "name": "No faculty double booking",
            "constraint_type": "NO_FACULTY_CLASH",
            ...
        }
    """
    # Create constraint instance from request data
    constraint = Constraint(**constraint_in.model_dump())
    
    # Add to database and commit
    db.add(constraint)
    await db.commit()
    await db.refresh(constraint)
    
    return constraint


@router.get("/", response_model=ConstraintListResponse)
async def list_constraints(
    skip: int = 0,
    limit: int = 100,
    is_hard: bool = None,
    is_active: bool = None,
    constraint_type: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated list of constraints with optional filtering.
    
    Supports filtering by:
    - `is_hard`: True for hard constraints, False for soft constraints
    - `is_active`: True for active constraints, False for disabled
    - `constraint_type`: Filter by specific constraint type
    
    Args:
        skip: Number of records to skip (pagination offset)
        limit: Maximum number of records to return (pagination limit)
        is_hard: Optional filter for hard vs soft constraints
        is_active: Optional filter for active vs inactive constraints
        constraint_type: Optional filter by constraint type
        db: Database session (injected dependency)
    
    Returns:
        ConstraintListResponse: List of constraints and total count
    
    Example:
        GET /api/v1/constraints?is_hard=true&limit=10
        Returns first 10 hard constraints
    """
    # Build query with optional filters
    query = select(Constraint)
    
    # Apply filters based on query parameters
    if is_hard is not None:
        query = query.where(Constraint.is_hard == is_hard)
    if is_active is not None:
        query = query.where(Constraint.is_active == is_active)
    if constraint_type:
        query = query.where(Constraint.constraint_type == constraint_type)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    constraints = result.scalars().all()
    
    # Get total count (respecting filters) for pagination metadata
    count_query = select(func.count()).select_from(Constraint)
    if is_hard is not None:
        count_query = count_query.where(Constraint.is_hard == is_hard)
    if is_active is not None:
        count_query = count_query.where(Constraint.is_active == is_active)
    if constraint_type:
        count_query = count_query.where(Constraint.constraint_type == constraint_type)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    return ConstraintListResponse(data=constraints, total=total)


@router.get("/{constraint_id}", response_model=ConstraintResponse)
async def get_constraint(
    constraint_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a specific constraint.
    
    Args:
        constraint_id: Unique identifier of the constraint
        db: Database session (injected dependency)
    
    Returns:
        ConstraintResponse: Full constraint details
    
    Raises:
        HTTPException: 404 if constraint not found
    """
    query = select(Constraint).where(Constraint.id == constraint_id)
    result = await db.execute(query)
    constraint = result.scalar_one_or_none()
    
    if not constraint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Constraint with id {constraint_id} not found"
        )
    
    return constraint


@router.get("/{constraint_id}/explain", response_model=ConstraintExplanation)
async def explain_constraint(
    constraint_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI-powered human-readable explanation of a constraint. ⭐
    
    **AI Explainability Feature** - Epic 1
    
    This endpoint provides transparent, understandable explanations of what each
    constraint means, how it affects scheduling, and practical examples of its impact.
    This makes the AI's decision-making process transparent to administrators.
    
    The explanation includes:
    - Plain English description of the constraint's purpose
    - Real-world examples of the constraint in action
    - Impact analysis (hard vs soft, scheduling implications)
    
    Args:
        constraint_id: Unique identifier of the constraint to explain
        db: Database session (injected dependency)
    
    Returns:
        ConstraintExplanation: Human-readable explanation with examples
    
    Raises:
        HTTPException: 404 if constraint not found
    
    Example Request:
        GET /api/v1/constraints/1/explain
    
    Example Response:
        {
            "constraint_id": 1,
            "name": "No faculty double booking",
            "constraint_type": "NO_FACULTY_CLASH",
            "is_hard": true,
            "explanation": "This constraint ensures that no faculty member is...",
            "examples": [
                "Prof. Smith cannot teach CS101 and CS102 simultaneously",
                ...
            ],
            "impact": "This is a hard constraint - violations will prevent..."
        }
    """
    # Fetch the constraint from database
    query = select(Constraint).where(Constraint.id == constraint_id)
    result = await db.execute(query)
    constraint = result.scalar_one_or_none()
    
    if not constraint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Constraint with id {constraint_id} not found"
        )
    
    # Knowledge base of constraint explanations
    # This maps each constraint type to its explanation, examples, and impact
    # In a production system, this could be enhanced with:
    # - Dynamic example generation based on actual timetable data
    # - Machine learning to improve explanations over time
    # - Multi-language support
    explanations = {
        "NO_FACULTY_CLASH": {
            "explanation": "This constraint ensures that no faculty member is scheduled to teach two different classes at the same time.",
            "examples": [
                "Prof. Smith cannot teach CS101 and CS102 simultaneously",
                "If Prof. Jones is teaching at 10:00 AM on Monday, they cannot have another class at that time"
            ],
            "impact": "This is a hard constraint - violations will prevent timetable generation."
        },
        "NO_ROOM_CLASH": {
            "explanation": "This constraint ensures that a room is not double-booked at any time slot.",
            "examples": [
                "Room 101 cannot host both CS101 and MATH201 at 9:00 AM",
                "Lab 201 can only be used for one class at a time"
            ],
            "impact": "This is a hard constraint - violations will prevent timetable generation."
        },
        "NO_STUDENT_CLASH": {
            "explanation": "This constraint ensures students in a section don't have overlapping classes.",
            "examples": [
                "Section A students cannot have CS101 and MATH101 at the same time",
                "Students must be able to attend all their enrolled courses"
            ],
            "impact": "This is a hard constraint - violations will prevent timetable generation."
        },
        "ROOM_CAPACITY": {
            "explanation": "This constraint ensures the assigned room has sufficient capacity for the number of students.",
            "examples": [
                "A class with 60 students cannot be scheduled in a room with 45 seats",
                "Lab courses requiring equipment need appropriately sized lab rooms"
            ],
            "impact": "This is a hard constraint - rooms must accommodate all students."
        },
        "LAB_REQUIREMENT": {
            "explanation": "This constraint ensures courses requiring lab facilities are scheduled in appropriate lab rooms.",
            "examples": [
                "CS301 (Data Structures Lab) must be in a computer lab, not a regular classroom",
                "Physics lab sessions need rooms with lab equipment"
            ],
            "impact": "This is a hard constraint - lab courses must have proper facilities."
        },
        "PREFERENCE_TIME": {
            "explanation": "This soft constraint represents preferred time slots for scheduling (e.g., faculty preferences).",
            "examples": [
                "Faculty may prefer morning slots over afternoon slots",
                "Some courses work better in longer continuous slots"
            ],
            "impact": "This is a soft constraint - violations are allowed but penalized in optimization."
        }
    }
    
    # Fallback explanation for constraint types not in knowledge base
    default_explanation = {
        "explanation": constraint.rule_definition,
        "examples": ["Specific examples depend on your timetable configuration"],
        "impact": f"This is a {'hard' if constraint.is_hard else 'soft'} constraint."
    }
    
    # Get explanation from knowledge base or use default
    explanation_data = explanations.get(constraint.constraint_type, default_explanation)
    
    # Construct and return explanation response
    return ConstraintExplanation(
        constraint_id=constraint.id,
        name=constraint.name,
        constraint_type=constraint.constraint_type,
        is_hard=constraint.is_hard,
        **explanation_data
    )


@router.put("/{constraint_id}", response_model=ConstraintResponse)
async def update_constraint(
    constraint_id: int,
    constraint_update: ConstraintUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing constraint.
    
    Allows partial updates - only provided fields will be modified.
    Useful for:
    - Toggling constraints on/off (is_active field)
    - Adjusting priorities and weights
    - Modifying constraint parameters
    
    Args:
        constraint_id: Unique identifier of the constraint to update
        constraint_update: Fields to update (partial update supported)
        db: Database session (injected dependency)
    
    Returns:
        ConstraintResponse: Updated constraint data
    
    Raises:
        HTTPException: 404 if constraint not found
    
    Example:
        PUT /api/v1/constraints/1
        {"is_active": false}
        
        Disables constraint without deleting it
    """
    # Fetch existing constraint
    query = select(Constraint).where(Constraint.id == constraint_id)
    result = await db.execute(query)
    constraint = result.scalar_one_or_none()
    
    if not constraint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Constraint with id {constraint_id} not found"
        )
    
    # Apply partial updates (only fields provided in request)
    update_data = constraint_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(constraint, field, value)
    
    # Save changes to database
    await db.commit()
    await db.refresh(constraint)
    
    return constraint


@router.delete("/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_constraint(
    constraint_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a constraint permanently.
    
    **Note**: Consider using PUT to set `is_active=False` instead of deleting
    to preserve historical data and allow re-enabling the constraint later.
    
    Args:
        constraint_id: Unique identifier of the constraint to delete
        db: Database session (injected dependency)
    
    Returns:
        None (HTTP 204 No Content on success)
    
    Raises:
        HTTPException: 404 if constraint not found
    """
    # Fetch constraint to delete
    query = select(Constraint).where(Constraint.id == constraint_id)
    result = await db.execute(query)
    constraint = result.scalar_one_or_none()
    
    if not constraint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Constraint with id {constraint_id} not found"
        )
    
    # Delete from database
    await db.delete(constraint)
    await db.commit()
    
    return None
