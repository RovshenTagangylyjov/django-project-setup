# Django Project Template

A production-ready Django REST API template with JWT authentication, PostgreSQL, Redis caching, Celery task queues, and modern tooling.

## Features

- **Django 6.0+** with Django REST Framework
- **JWT Authentication** via `djangorestframework-simplejwt`
- **PostgreSQL** database with connection pooling
- **Redis** for caching and Celery broker
- **Celery** for async tasks with separate email queue
- **Docker** support with docker-compose
- **Modern Admin** with django-unfold
- **API Documentation** with Swagger UI (drf-spectacular)
- **Testing** with pytest and pytest-django
- **Code Quality** with black, isort, flake8, mypy, pylint

## Quick Start

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL (optional for local dev)
- Redis (optional for local dev)

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd django-project-setup
```

2. Install dependencies:
```bash
uv sync
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
uv run python manage.py migrate
```

5. Create a superuser:
```bash
uv run python manage.py createsuperuser
```

6. Start the development server:
```bash
uv run python manage.py runserver
```

The API is now available at http://localhost:8000/api/

### Docker Development

Start PostgreSQL and Redis for local development:
```bash
docker compose -f docker-compose.dev.yml up -d
```

Then update your `.env` to use PostgreSQL instead of SQLite.

### Production Deployment

Build and start all services:
```bash
docker compose up -d --build
```

## Project Structure

```
.
├── api/                    # REST API endpoints
│   ├── authentication/     # JWT token endpoints
│   ├── health/             # Health check endpoints
│   └── users/              # User CRUD endpoints
├── apps/                   # Django applications
│   └── users/              # Custom user model
├── config/                 # Django configuration
│   └── settings/
│       ├── base.py         # Shared settings
│       ├── local.py        # Development settings
│       └── production.py   # Production settings
├── tests/                  # Test suite
├── utils/                  # Shared utilities
├── docker-compose.yml      # Production Docker setup
├── docker-compose.dev.yml  # Development Docker setup
└── Makefile                # Common commands
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/token/` | POST | Obtain JWT tokens |
| `/api/token/refresh/` | POST | Refresh access token |
| `/api/users/me/` | GET | Current user profile |
| `/api/users/{id}/` | GET/PUT/DELETE | User CRUD |
| `/api/health/` | GET | Health check |
| `/api/health/ready/` | GET | Readiness check |
| `/api/docs/` | GET | Swagger UI |
| `/api/schema/` | GET | OpenAPI schema |

## Common Commands

```bash
# Development
uv run python manage.py runserver     # Start dev server
uv run python manage.py migrate       # Run migrations
uv run python manage.py makemigrations # Create migrations
uv run python manage.py createsuperuser # Create admin user

# Testing
uv run pytest                         # Run all tests
uv run pytest --cov                   # Run with coverage
uv run pytest -v                      # Verbose output

# Code Quality
uv run pre-commit run --all-files     # Run all linters
uv run black .                        # Format code
uv run isort .                        # Sort imports
uv run flake8                         # Lint code
uv run mypy .                         # Type check

# Celery (for local development with Redis)
celery -A config worker -l info       # Start worker
celery -A config beat -l info         # Start scheduler
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | `local` or `production` | `local` |
| `SECRET_KEY` | Django secret key | - |
| `POSTGRES_DB` | Database name | `project` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `ALLOWED_HOSTS` | Comma-separated hosts | - |
| `CORS_ALLOWED_ORIGINS` | Comma-separated origins | - |

## Key Patterns

### Soft Deletes
User deletion sets `is_active=False` rather than hard delete:
```python
def perform_destroy(self, instance):
    instance.is_active = False
    instance.save()
```

### Custom Manager + QuerySet
Models use the Manager.from_queryset() pattern:
```python
class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass
```

### List vs Detail Serializers
ViewSets can define separate serializers for list endpoints:
```python
class MyViewSet(BaseModelViewSet):
    serializer_class = DetailSerializer
    list_serializer_class = ListSerializer
```

### Image Compression
Use `CompressedImageField` for automatic WebP conversion:
```python
from utils.fields import CompressedImageField

class MyModel(models.Model):
    image = CompressedImageField(upload_to="images/")
```

## License

MIT
