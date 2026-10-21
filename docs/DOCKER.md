# Hirely Docker Desktop & Compose Guide

> [← Back to Main Documentation (README.md)](../README.md)

This guide covers running Hirely locally as a unified multi-container application using Docker Compose.

---

## 1. Architecture Overview

Hirely runs as four orchestrated services inside a single Docker Compose network:

| Service | Container Name | Base / Build | Exposed Port | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **`db`** | `hirely-postgres` | `postgres:15-alpine` | `5433:5432` | Persistent PostgreSQL database. |
| **`migration`** | `hirely-migration` | `backend/Dockerfile` | None (one-off) | Runs `alembic upgrade head` before backend starts. |
| **`backend`** | `hirely-backend` | `backend/Dockerfile` | `8000:8000` | FastAPI application server running under non-root `appuser`. |
| **`frontend`** | `hirely-frontend` | `frontend/Dockerfile` | `3000:80` | Multi-stage built React 19 / Vite SPA served via Nginx. |

### Volumes & Persistence

- `postgres_data`: Named volume storing PostgreSQL database records (`/var/lib/postgresql/data`). Data persists across container restarts and `docker compose down`.
- `resume_uploads`: Named volume storing locally uploaded resume files (`/app/backend/uploads`).

---

## 2. Port Mappings & Host PostgreSQL Note

- **Frontend**: Accessible on the host at `http://localhost:3000`.
- **Backend API**: Accessible on the host at `http://localhost:8000` (e.g. Swagger docs at `http://localhost:8000/docs`).
- **PostgreSQL**: Bound to host port `5433` (mapped to container port `5432`).
  - *Why port 5433?* If your local Windows machine already has a native PostgreSQL service running on default port `5432`, this prevents binding collisions. Inside the Docker network, the backend and migration services communicate directly with the database at `db:5432`.
  - You can customize this port in your `.env` file via `POSTGRES_PORT=<port>`.

---

## 3. Quick Start

### Step 1: Start the Entire Application

From the project root:

```bash
docker compose up --build -d
```

Compose automatically:
1. Builds the `backend` and `frontend` images.
2. Starts `hirely-postgres` and waits until its healthcheck passes.
3. Spawns `hirely-migration`, runs `alembic upgrade head`, and exits cleanly (`code 0`).
4. Launches `hirely-backend` once migrations succeed and verifies health via `/health`.
5. Launches `hirely-frontend` once the backend is healthy.

### Step 2: Verify Service Status

```bash
docker compose ps
```

All long-running services (`db`, `backend`, `frontend`) should display `Up (healthy)`. The `migration` service should display `Exited (0)`.

### Step 3: Access the Application

- **Web UI**: Open [http://localhost:3000](http://localhost:3000)
- **API Documentation**: Open [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Check**: Open [http://localhost:8000/health](http://localhost:8000/health)
- **Database Health Check**: Open [http://localhost:8000/health/db](http://localhost:8000/health/db)

---

## 4. Operational Commands

### View Logs

Stream logs for all services:
```bash
docker compose logs -f
```

Stream logs for a specific service:
```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
docker compose logs -f migration
```

### Stop the Application (Preserving Data)

```bash
docker compose down
```

This stops and removes the containers and networks while preserving your database and uploaded files in named volumes.

### Restart Services

```bash
docker compose restart
```

Or restart a single service:
```bash
docker compose restart backend
```

### Reset Database & Uploads (Destructive)

To remove all persistent data (database tables and uploaded resumes) and start fresh:

```bash
docker compose down -v
```

---

## 5. Configuration & Environment Variables

Default variables are preconfigured in `docker-compose.yml` for local development. You can override any of these by creating or updating `.env` in the repository root:

```ini
# Database
POSTGRES_PORT=5433
POSTGRES_DB=hirely_dev
POSTGRES_USER=hirely_user
POSTGRES_PASSWORD=hirely_dev_password

# Ports
FRONTEND_PORT=3000
BACKEND_PORT=8000

# Backend Authentication & AI
JWT_SECRET_KEY=your_jwt_secret_key_minimum_32_characters
GEMINI_API_KEY=your_gemini_api_key

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173
```

---

## 6. Troubleshooting

### Port Already in Use
- If port `3000` or `8000` is already in use by another application on your host, change `FRONTEND_PORT` or `BACKEND_PORT` in `.env`.
- If port `5433` is already in use, change `POSTGRES_PORT` in `.env`.

### Applying New Migrations
When you create a new Alembic migration in `backend/alembic/versions/`:
```bash
docker compose run --rm migration alembic upgrade head
```
Or simply restart the stack with `docker compose up -d`.

### Direct Database Access
To connect directly to the containerized database from your host machine using `psql` or a GUI client (like DBeaver, TablePlus, or pgAdmin):
- **Host**: `localhost`
- **Port**: `5433`
- **Database**: `hirely_dev` (or your configured `POSTGRES_DB`)
- **Username**: `hirely_user` (or your configured `POSTGRES_USER`)
- **Password**: `hirely_dev_password` (or your configured `POSTGRES_PASSWORD`)
