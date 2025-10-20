# oxapy-template

Minimal template for services built with oxapy + SQLAlchemy.

## Overview
This repository provides a small starter application demonstrating typical layers:
- API (routes)
- Services (business logic)
- Repositories (DB access)
- Serializers (validation + persistence helpers)
- Models (SQLAlchemy models)
- Core (config, middlewares, utilities)

The app exposes simple authentication endpoints (register, login) using JWT.

## Prerequisites
- Python 3.12
- A database reachable via DATABASE_URL (and optional Turso sync settings)
- Recommended: create a virtual environment

## Environment variables
Create a `.env` file or export these before running:
- DATABASE_URL - SQLAlchemy connection URL (required)
- TURSO_DB_URL - (optional) sync URL used by sql library integration
- TURSO_DB_AUTH_TOKEN - (optional) auth token for Turso
- SECRET_KEY - secret used to sign JWTs

## Install & run
1. Create venv and install:
   - python -m venv .venv
   - source .venv/bin/activate
   - pip install -e .

2. Set environment variables (see above).

3. Run migrations (Alembic)
   - Configure `sqlalchemy.url` in `alembic.ini` or ensure DATABASE_URL is set and env handling in env.py points at your ENGINE.
   - Create an initial revision:
     - alembic revision --autogenerate -m "init"
   - Apply migrations:
     - alembic upgrade head

4. Start the server:
   - python -m app.main
   - Server host/port are defined in `app/core/config.py` (ADDR).

## API Endpoints
All endpoints return JSON and a tuple (body, Status) per oxapy conventions.

- POST /api/auth/register
  - Description: Register a new user.
  - Request body:
    {
      "name": "Full Name",
      "email": "user@example.com",
      "password": "strongpassword"
    }
  - Response: 201 CREATED
    {
      "users": { "id": "...", "name": "...", "email": "..." }
    }

- POST /api/auth/login
  - Description: Login and receive JWT token.
  - Request body:
    {
      "email": "user@example.com",
      "password": "strongpassword"
    }
  - Response: 202 ACCEPTED
    { "token": "<jwt>" }

- Protected routes: any router using `jwt_middleware` expects header:
  Authorization: Bearer <token>

Example curl:
curl -X POST http://localhost:8000/api/auth/register -H "Content-Type: application/json" -d '{"name":"Joe","email":"joe@example.com","password":"password123"}'

## Code layout (key files)
- app/main.py
  - Server bootstrap and route attachment.
- app/api/
  - auth.py — authentication routes
  - user.py — protected user routes (middleware attached)
- app/services/
  - auth_srvs.py — login, register business logic
  - user_srvs.py — (placeholder for user-related services)
- app/repositories/
  - user_repo.py — DB access helper for User
- app/serializers/
  - user_serializer.py — validation + create logic for User and credentials
- app/models/
  - models.py — SQLAlchemy models (User)
- app/core/
  - config.py — DB engine, JWT and app settings
  - middlewares.py — jwt & db session middlewares
  - utils.py — helpers (new_id)

## Important implementation notes
- Serializers use oxapy.serializer and integrate with SQLAlchemy sessions for create.
- JWT helper is instantiated in `app/core/config.py` as JWT = jwt.Jwt(SECRET_KEY).
- DB session factory is `DB` from sessionmaker(ENGINE). Middlewares attach `request.db` and `request.user` as appropriate.

## Migrations
Alembic is configured in `alembic/`. `alembic/env.py` imports `app.models` and uses `models.BaseModel.metadata` as target metadata for autogenerate.

## Tests
No tests provided in the template. Recommended:
- Add pytest and create unit tests for services, repositories and middlewares.
- Use a test database URL and run migrations before tests.

## Contributing
- Follow the code layout and add service/repository pairs for new resources.
- Keep business logic in services, DB access in repositories, request validation in serializers.

## Troubleshooting
- "Authorization header missing": ensure Authorization header present for protected routes.
- "Email already registered": register endpoint enforces unique emails via repository check.
- If Alembic autogenerate doesn't detect models: ensure models are imported in `alembic/env.py` (they are via `from app import models`).

## License
Add your preferred license or remove this section.

