# TimeWeaver Backend API

FastAPI-based backend for the TimeWeaver intelligent timetable and academic workload optimization system.

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API endpoint modules
│   │       └── router.py      # Main API router
│   ├── core/
│   │   └── config.py          # Application configuration
│   ├── db/
│   │   ├── base.py           # Database base
│   │   └── session.py        # Database session management
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic services
│   └── main.py              # FastAPI application entry point
├── alembic/                  # Database migrations
├── tests/                    # Test suite
├── requirements.txt          # Python dependencies
└── .env.example             # Environment variables template
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Install PostgreSQL (if not already installed)
# Create database
createdb timeweaver_db

# Or use PostgreSQL shell
psql -U postgres
CREATE DATABASE timeweaver_db;
CREATE USER timeweaver_user WITH PASSWORD 'timeweaver_password';
GRANT ALL PRIVILEGES ON DATABASE timeweaver_db TO timeweaver_user;
```

### 3. Environment Configuration

```bash
# Copy example env file
copy .env.example .env

# Edit .env with your database credentials
```

### 4. Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Run the Application

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py directly
python -m app.main
```

### 6. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Epic 1: Academic & Infrastructure Configuration

- `POST /api/v1/semesters` - Create semester
- `GET /api/v1/semesters` - List semesters
- `POST /api/v1/departments` - Create department
- `POST /api/v1/sections` - Create section
- `POST /api/v1/courses` - Create course
- `POST /api/v1/elective-groups` - Create elective group
- `POST /api/v1/rooms` - Create room
- `POST /api/v1/time-slots` - Create time slot
- `POST /api/v1/constraints` - Define constraint
- `GET /api/v1/constraints/explain/{id}` - Get constraint explanation

## Development

### Running Tests

```bash
pytest
pytest --cov=app tests/
```

### Code Formatting

```bash
ruff check .
ruff format .
```

## Features

### Epic 1: Configuration
- ✅ Semesters and academic year management
- ✅ Department and section management
- ✅ Course configuration (theory/lab hours)
- ✅ Elective group management
- ✅ Room management with capacity and equipment tracking
- ✅ Time slot patterns and breaks
- ✅ Constraint modeling (hard and soft)
- ✅ AI Explainability for constraint decisions

### Epic 7: Access Control (Next)
- 🔄 Role-based access control (RBAC)
- 🔄 JWT authentication
- 🔄 Audit logging
- 🔄 Secure endpoints

## Technology Stack

- **FastAPI**: Modern, high-performance web framework
- **SQLAlchemy**: Async ORM for database operations
- **PostgreSQL**: Primary database
- **Pydantic**: Data validation and serialization
- **Alembic**: Database migrations
- **pytest**: Testing framework

## License

Proprietary - TimeWeaver Project
