# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 6.0 REST API backend template with JWT authentication, PostgreSQL, Redis caching, Celery task queues, and a modern Unfold admin interface.

## Common Commands

```bash
# Install dependencies
uv sync

# Run development server
uv run python manage.py runserver
# or: make dev

# Run migrations
uv run python manage.py migrate
# or: make migrate

# Create migrations
uv run python manage.py makemigrations
# or: make makemigrations

# Run tests
uv run pytest
# or: make test

# Run tests with coverage
uv run pytest --cov
# or: make test-cov

# Run all pre-commit hooks (black, isort, flake8, mypy, pylint)
uv run pre-commit run --all-files
# or: make lint

# Format code
uv run black . && uv run isort .
# or: make format

# Docker (development services)
docker compose -f docker-compose.dev.yml up -d
# or: make docker-up

# Docker (production)
docker compose up -d --build
# or: make docker-build
```

## Architecture

### Configuration (`config/`)
- `settings/__init__.py` - Loads `local.py` or `production.py` based on `ENVIRONMENT` env var
- `settings/base.py` - Shared settings for all environments
- `settings/local.py` - Development: SQLite, debug mode, eager Celery, in-memory cache
- `settings/production.py` - PostgreSQL, Redis cache, async Celery, Gmail SMTP, security headers

### Apps (`apps/`)
Django applications containing models, managers, querysets, and admin configuration. Currently has `users` app with `User` model extending `AbstractUser`.

### API (`api/`)
REST API endpoints using Django REST Framework:
- `api/authentication/` - JWT token endpoints (`/api/token/`, `/api/token/refresh/`)
- `api/users/` - User CRUD with `/users/me/` endpoint for current user
- `api/health/` - Health check endpoints (`/api/health/`, `/api/health/ready/`)
- API docs at `/api/docs/` (Swagger UI)

### Utils (`utils/`)
Shared utilities:
- `models.py` - `BaseModel` with `date_created`/`date_updated` timestamps (DateTimeField)
- `viewsets.py` - `BaseModelViewSet` supporting separate `list_serializer_class`
- `fields.py` - `CompressedImageField` (WebP, 75% quality), `PriceField`
- `files.py` - UUID-based file upload organization
- `exceptions.py` - Custom API exceptions (BadRequest, NotFound, Conflict, etc.)
- `exception_handler.py` - Custom DRF exception handler with consistent error format
- `middleware.py` - RequestIDMiddleware, RequestLoggingMiddleware

### Tests (`tests/`)
pytest test suite with fixtures in `conftest.py`:
- `tests/api/` - API endpoint tests
- `tests/apps/` - Model and business logic tests

## Key Patterns

- **Soft deletes**: User deletion sets `is_active=False` rather than hard delete
- **Custom managers**: Models use custom Manager + QuerySet pattern (see `apps/users/managers.py`)
- **List vs detail serializers**: ViewSets can define `list_serializer_class` for list endpoints
- **Image compression**: Use `CompressedImageField` for automatic WebP conversion
- **Request tracing**: X-Request-ID header added to all requests/responses

## Environment Variables

Required in `.env` (see `.env.example`):
```
ENVIRONMENT=local|production
SECRET_KEY=

# Database
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=

# Cache
REDIS_URL=redis://localhost:6379

# Production only
ALLOWED_HOSTS=example.com,www.example.com
CORS_ALLOWED_ORIGINS=https://example.com
CSRF_TRUSTED_ORIGINS=https://example.com
```

## Code Style

- Line length: 100 characters (black, flake8)
- Import sorting: isort with black profile
- Type checking: mypy enabled
- Django-aware linting: pylint with pylint_django plugin
- Testing: pytest with pytest-django
