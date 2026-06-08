# Cortex ICU Platform – Run Guide (Updated)

This guide explains how to set up, run, and test the Cortex ICU Platform locally using Docker Compose. It reflects the current architecture using **PostgreSQL + Alembic + Seed Scripts**.

---

# 1. Requirements

To run via Docker:

* Docker 20.10+
* Docker Compose v2
* Minimum: 4GB RAM, 2 CPU cores

---

# 2. Running with Docker (Recommended)

```bash
git clone <repository>
cd cortex_icu_full_app_v3
docker compose up --build
```

---

## Services

| Service  | URL                        |
| -------- | -------------------------- |
| Frontend | http://localhost:5173      |
| Backend  | http://localhost:8000/docs |
| DB       | localhost:5432             |

---

# 3. Database Initialization Flow

Startup sequence:

1. PostgreSQL container starts
2. Backend waits for DB health
3. Alembic runs migrations
4. Seed script inserts initial data
5. Backend API starts

---

## Migrations

Automatically executed on startup:

```bash
python -m alembic upgrade head
```

This creates all tables:

* users
* roles
* patients
* vitals
* devices
* etc.

---

## Seeding

Seed script runs after migrations:

```bash
python -m app.scripts.seed_data
```

### Seeded Data Includes:

* Default roles (admin, doctor, nurse)
* Admin user
* Base hospital/unit structure

---

# 4. Default Login

```json
{
  "user_id": "admin",
  "password": "admin"
}
```

---

# 5. Verifying Setup

## Check containers

```bash
docker ps
```

---

## Check DB readiness

```bash
docker exec -it cortex_db pg_isready -U postgres -d cortex_icu
```

Expected:

```text
accepting connections
```

---

## Check tables

```bash
docker exec -it cortex_db psql -U postgres -d cortex_icu -c "\dt"
```

---

## Check seeded data

```bash
docker exec -it cortex_db psql -U postgres -d cortex_icu -c "SELECT * FROM users;"
```

---

## Check backend logs

```bash
docker logs cortex_backend
```

Expected:

* Alembic runs successfully
* No errors
* Uvicorn starts

---

# 6. Running Seed Manually

If needed:

```bash
docker compose exec backend bash -c "python -m app.scripts.seed_data"
```

---

# 7. Device Simulator

```bash
docker compose exec backend bash -c "python -m app.scripts.device_simulator"
```

Simulates real-time vitals streaming.

---

# 8. Manual Setup (Optional)

## Database

```bash
psql -U postgres -c "CREATE DATABASE cortex_icu;"
```

---

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# 9. Environment Variables

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/cortex_icu
SECRET_KEY=CHANGE_ME
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=43200
```

---

# 10. Common Issues & Fixes

## Port 5432 already in use

```bash
sudo systemctl stop postgresql
```

---

## DB not initializing correctly

```bash
docker compose down -v
docker compose up --build
```

---

## Tables not created

* Check Alembic logs
* Ensure `alembic upgrade head` runs

---

## Login returns 401

* Ensure seed script ran
* Verify user exists:

```bash
docker exec -it cortex_db psql -U postgres -d cortex_icu -c "SELECT * FROM users;"
```

---

## Backend cannot connect to DB

* Ensure using `db` as host, not `localhost`

---

# 11. Important Notes

* Use `docker compose` (not `docker-compose`)
* Container-to-container communication uses service name (`db`)
* Avoid running destructive scripts (`reset_db.py`) at startup
* Seed scripts should be idempotent

---

# 12. Production Considerations

* Use HTTPS (reverse proxy like Nginx)
* Secure secrets (Vault / Docker secrets)
* Enable DB backups
* Add monitoring (Prometheus/Grafana)
* Implement audit + compliance (HIPAA)

---

# 🎯 Summary

You now have:

* Fully containerized stack
* Automated DB migration (Alembic)
* Automated seed data
* Real-time device simulation capability

The Cortex ICU platform is ready for development and testing 🚀
