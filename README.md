# Jaque.ai - AI for Manufacturing Quality & Supplier Excellence

A comprehensive solution for manufacturing quality management, featuring an AI-powered backend and a modern landing page.

## 🚀 Features

- **Landing Page**: Modern, responsive landing page with demo request form
- **FastAPI Backend**: High-performance Python backend with async support
- **Database**: PostgreSQL for reliable data storage
- **Caching**: Redis for high-performance caching
- **AI Integration**: OpenAI and Anthropic API support
- **CAD Processing**: Support for CAD file analysis and processing
- **Docker Support**: Easy deployment with Docker Compose

## 📋 Prerequisites

### Option 1: Docker (Recommended)
- Docker 20.10+
- Docker Compose 2.0+

### Option 2: Local Development
- Python 3.10+
- PostgreSQL 14+
- Redis 6+ (optional)
- Node.js 18+ (for frontend development)

## 🏃 Quick Start

### Using Docker (Easiest)

1. Clone the repository:
```bash
git clone <repository-url>
cd Jaque-landing-page
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start all services:
```bash
docker-compose up -d
```

4. Access the application:
- Landing Page: http://localhost
- API Documentation: http://localhost/docs
- Backend API: http://localhost:8000

### Manual Setup

#### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL:
```bash
# Create database
createdb jaque_db

# Or using psql
psql -U postgres -c "CREATE DATABASE jaque_db;"
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Start the backend:
```bash
cd backend
./run.sh
```

Or manually:
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

The landing page is a static HTML file. You can:

1. **Serve with Python**:
```bash
python -m http.server 8080
```

2. **Serve with Node.js**:
```bash
npx serve .
```

3. **Use any web server** (nginx, Apache, etc.)

## 📁 Project Structure

```
Jaque-landing-page/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── database.py     # Database configuration
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── core/
│   │   │   └── config.py   # Settings
│   │   ├── routers/
│   │   │   └── demo.py     # Demo request endpoints
│   │   └── services/
│   ├── README.md
│   └── run.sh             # Startup script
├── index.html             # Landing page
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker services
├── Dockerfile            # Backend Docker image
├── nginx.conf            # Nginx configuration
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔌 API Endpoints

### Demo Requests
- `POST /api/demo/request` - Submit a demo request
- `GET /api/demo/requests` - Get all demo requests
- `GET /api/demo/requests/{id}` - Get specific demo request
- `PATCH /api/demo/requests/{id}/status` - Update request status

### Health & Info
- `GET /` - Health check
- `GET /health` - Detailed health status
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## 🔧 Configuration

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jaque_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here

# AI APIs
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

See `.env.example` for all available options.

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Access backend shell
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U postgres -d jaque_db
```

## 🧪 Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=backend
```

## 📊 Database

### Schema

**demo_requests**
- id (Primary Key)
- name, email, company, role, message
- status, contacted
- created_at, updated_at

**users**
- id (Primary Key)
- email, hashed_password, full_name
- is_active, is_superuser
- created_at, updated_at

### Migrations

Using Alembic:
```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🚀 Deployment

### Production Checklist

- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Configure proper `DATABASE_URL`
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS allowed origins
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up rate limiting
- [ ] Use production-grade WSGI server (gunicorn)

### Deployment Options

1. **Docker Compose** (Simple)
2. **Kubernetes** (Scalable)
3. **Cloud Platforms**: AWS, GCP, Azure
4. **Platform as a Service**: Heroku, Railway, Render

## 🔐 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- SQL injection prevention (SQLAlchemy)
- Input validation (Pydantic)

## 📝 License

Proprietary - Jaque.ai

## 🤝 Support

For support, email support@jaque.ai or open an issue in the repository.

## 🛠️ Technology Stack

**Backend:**
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Redis (Cache)
- Pydantic (Validation)
- Uvicorn (ASGI Server)

**AI/ML:**
- OpenAI API
- Anthropic Claude API
- PyTorch
- Transformers
- Scikit-learn

**File Processing:**
- ezdxf (CAD files)
- OpenCV (Computer Vision)
- Pillow (Image Processing)
- PyTesseract (OCR)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (Reverse Proxy)
- Alembic (Migrations)
