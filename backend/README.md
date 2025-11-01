# Jaque.ai Backend API

Backend API for Jaque.ai - AI for Manufacturing Quality Excellence

## Features

- FastAPI web framework
- PostgreSQL database with SQLAlchemy ORM
- Redis for caching
- Celery for background tasks
- JWT authentication
- AI integrations (OpenAI, Anthropic)
- CAD file processing capabilities
- Computer vision and ML features

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (optional, for caching)

### Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Set up environment variables:
```bash
cp ../.env.example .env
# Edit .env with your configuration
```

3. Set up the database:
```bash
# Create database
createdb jaque_db

# Or using psql
psql -U postgres -c "CREATE DATABASE jaque_db;"
```

4. Run database migrations (tables will be created automatically on first run):
```bash
python -m uvicorn app.main:app --reload
```

### Running the Server

Development mode:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the run script:
```bash
chmod +x run.sh
./run.sh
```

Production mode:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Demo Requests

- `POST /api/demo/request` - Submit a demo request
- `GET /api/demo/requests` - Get all demo requests (admin)
- `GET /api/demo/requests/{id}` - Get specific demo request
- `PATCH /api/demo/requests/{id}/status` - Update demo request status

### Health Check

- `GET /` - Root endpoint with health status
- `GET /health` - Detailed health check

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Settings and configuration
│   ├── routers/
│   │   ├── __init__.py
│   │   └── demo.py          # Demo request endpoints
│   └── services/
│       └── __init__.py
├── README.md
└── run.sh                   # Startup script
```

## Database Models

### DemoRequest
- Stores demo requests from the landing page
- Fields: name, email, company, role, message, status, contacted
- Timestamps: created_at, updated_at

### User
- User authentication and management
- Fields: email, hashed_password, full_name, is_active, is_superuser

## Development

### Adding New Endpoints

1. Create a new router in `app/routers/`
2. Define Pydantic schemas in `app/schemas.py`
3. Create database models in `app/models.py`
4. Include the router in `app/main.py`

### Database Migrations

For production, use Alembic for migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Testing

```bash
pytest
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

Proprietary - Jaque.ai
