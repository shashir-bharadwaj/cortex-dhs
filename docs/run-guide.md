# Cortex DHS / ICU Platform – Run Guide

How to set up, run, seed, and test the Cortex platform locally. This reflects
the current stack: **PostgreSQL 15 + Alembic + idempotent seed scripts +
FastAPI + React (Vite)**, with a state-based vital simulator and live
WebSocket streaming.

---

## 1. Requirements

To run via Docker:

- Docker 20.10+ and Docker Compose **v2** (`docker compose`, not `docker-compose`)
- ~4 GB RAM, 2 CPU cores

For manual (non-Docker) setup: Python 3.12+, Node.js 18+, PostgreSQL 15.

---

## 2. Quick start (Docker)

```bash
git clone <repository>
cd cortex-dhs

# Full stack INCLUDING the live vital simulator:
make up            # == docker compose --profile simulator up -d

# …or without the simulator:
docker compose up --build
```

On startup the **backend** container runs, in order:

1. `alembic upgrade head` – create/upgrade all tables
2. `python scripts/seed_dev_data.py` – seed reference + demo data (idempotent)
3. `uvicorn app.main:app --reload` – start the API

Because seeding finishes **before** Uvicorn (and therefore before the
simulator) starts, there is no first-run data race.

### Services

| Service           | URL / Address                  | Notes                                    |
| ----------------- | ------------------------------ | ---------------------------------------- |
| Frontend (Vite)   | http://localhost:5173          | React PWA, dev server with HMR           |
| Backend (FastAPI) | http://localhost:8000          | Swagger at `/docs`, ReDoc at `/redoc`    |
| Live vitals WS    | ws://localhost:8000/api/v1/ws/live-vitals/{unitId} | per-ICU-unit stream    |
| Database (PG 15)  | internal only (`db:5432`)      | **not** published to the host by default |

> The DB port is intentionally **not** exposed to the host (the backend reaches
> it over the Docker network as `db:5432`). To get host `psql` access, add
> `ports: ["5433:5432"]` to the `db` service in `docker-compose.yml`.

---

## 3. Make targets

A `Makefile` at the repo root wraps the common operations:

| Command                            | What it does                                          |
| ---------------------------------- | ----------------------------------------------------- |
| `make up`                          | Start the full stack **including** the simulator      |
| `make down`                        | Stop & remove the stack **with `--remove-orphans`**   |
| `make reseed`                      | **Race-proof** reseed: pause simulator → seed → resume |
| `make seed`                        | Alias for `reseed`                                    |
| `make sim-stop` / `make sim-start` | Control only the vital simulator                      |
| `make restart-backend`             | Restart the backend container                         |
| `make logs`                        | Tail backend logs                                     |
| `make ps`                          | Container status                                      |

`make down` uses `--remove-orphans` to avoid the "network is still in use"
error caused by the simulator container outliving a plain `docker compose down`.

---

## 4. Default logins

Authentication is by **email + password** (JSON body to `POST /api/v1/auth/login`).
The seed creates three users:

| Role   | Email               | Password |
| ------ | ------------------- | -------- |
| Admin  | `admin@cortex.com`  | `admin`  |
| Doctor | `doctor@cortex.com` | `doctor` |
| Nurse  | `nurse@cortex.com`  | `nurse`  |

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"nurse@cortex.com","password":"nurse"}'
# -> { "token": "...", "user": { ... } }
```

Send the token as `Authorization: Bearer <token>` on subsequent requests.

---

## 5. Seeded data

`backend/scripts/seed_dev_data.py` is **idempotent** — it clears prior seed
data (and realigns identity sequences so IDs restart at 1) before inserting:

- Roles (admin / doctor / nurse) + RBAC permissions
  - Nurse has `PATIENTS: VIEW, CREATE, MODIFY` (can add/edit/delete patients)
- 1 hospital → 3 ICU units: **MICU-1, SICU-1, NICU-1**
- Beds `B1–B10`, `S1–S8`, `N1–N8` and a monitor device per bed
- 26 patients (`MRN-100001…`) with vitals, alarms, clinical notes, timeline,
  and the clinical modules: **ventilator settings, lab results, fluid balance,
  medication orders**
- Staff assignments

### Reseeding safely

Run a reseed at any time (e.g. after adding patients through the UI):

```bash
make reseed
```

> Do **not** run the seed script directly while the simulator is streaming —
> it inserts vitals for live patients and will trip a foreign-key error during
> the clear. `make reseed` handles this by stopping the simulator first.

---

## 6. Vital simulator

State-based simulator that drifts each bed's vitals realistically and only
raises alarms on threshold crossings (2 beds run "critical" by default).

```bash
make sim-start
# or directly:
docker compose --profile simulator up -d vital_simulator
```

It posts batched device events to `POST /api/v1/ingestion/device-events` every
**5 seconds**; the backend persists them and broadcasts live updates over the
per-unit WebSocket. Adjust cadence / critical beds via the `--interval` and
`--critical-beds` flags in `docker-compose.yml`.

---

## 7. Verifying the setup

```bash
# Containers
make ps

# DB readiness (exec inside the db container — port isn't on the host)
docker exec -it cortex_db pg_isready -U postgres -d cortex_icu   # -> accepting connections

# Tables / seeded users
docker exec -it cortex_db psql -U postgres -d cortex_icu -c "\dt"
docker exec -it cortex_db psql -U postgres -d cortex_icu -c "SELECT email, role_id FROM users;"

# Backend logs (expect alembic OK, seed OK, Uvicorn started)
make logs
```

---

## 8. Using the application

Open http://localhost:5173 and log in.

- **Dashboard** – live ICU overview: stat cards, ICU-unit tabs, and patient
  cards that auto-refresh every 5s. Critical patients pulse; click a card to
  open the patient detail page.
- **Patients** – paginated table (10/page) with MRN, name, age/gender, contact,
  diagnosis, admitted date, status, and **Add / Edit / Delete** actions. MRNs
  are auto-generated (`MRN-1000xx`).
- **Patient Detail** – 7 tabs, all fed by `GET /patients/{id}/details`:
  **Overview** (vital cards + Demographics + **live** trend chart + Ventilator /
  Lab / Fluid panels), **Flowsheet** (hourly grid), **Devices**, **Medication**
  (orders + active infusions), **Notes** (add/list), **Timeline**, **Reports**
  (CSV download, daily & discharge summaries). Vital cards and the trend chart
  update in real time over the WebSocket.
- **Alerts** – active/critical alarms with acknowledge.
- **Medication / Notes / Tasks / Handover** – operational modules.

A red **critical-alert banner** appears under the header when any critical
alarm is active, with Acknowledge / View Alerts actions.

---

## 9. Manual setup (without Docker)

**Database**

```bash
psql -U postgres -c "CREATE DATABASE cortex_icu;"
```

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_dev_data.py
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

**Simulator** (optional, against a host backend)

```bash
cd backend
python scripts/simulate_live_vitals.py --api-base-url http://localhost:8000 --interval 5
```

---

## 10. Environment variables

**Backend** — `backend/.env`:

| Variable                      | Description                                         |
| ----------------------------- | --------------------------------------------------- |
| `DATABASE_URL`                | `postgresql://postgres:postgres@db:5432/cortex_icu` |
| `SECRET_KEY`                  | JWT signing key                                     |
| `ALGORITHM`                   | JWT algorithm (e.g. `HS256`)                        |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access-token lifespan                               |
| `BACKEND_CORS_ORIGINS`        | Allowed CORS origins                                |
| `ALLOWED_HOSTS`               | Allowed hosts                                       |

> Inside Docker the DB host **must** be `db` (the service name), not `localhost`.

**Frontend** — `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Axios uses this base URL; API paths are written **without** repeating `/api/v1`
(e.g. `/auth/login`, `/patients`, `/dashboard/overview`).

---

## 11. Common issues & fixes

**`Network cortex-dhs_default ... resource is still in use`**
The simulator container outlived `docker compose down`. Use `make down`
(it adds `--remove-orphans`), or:

```bash
docker rm -f cortex_vital_simulator && docker compose down --remove-orphans
```

**Port already in use (`8000` / `5173`)**

```bash
lsof -ti :8000 | xargs kill -9      # repeat per port as needed
```

The DB port isn't published by default, so host `5432` should be free.

**Login is slow / hangs**
Resolved: the DB connection pool is sized up and device ingestion runs off the
event loop (threadpool). If it recurs, check the simulator isn't flooding a
single-worker backend and that the pool isn't exhausted.

**Reseed fails with a foreign-key error**
You ran the seed while the simulator was live. Use `make reseed`.

**Login returns 401 / "patient not found"**
Ensure the seed ran (`make logs`), then reseed (`make reseed`). IDs restart at 1
after a clean reseed.

**Backend can't reach DB**
Use `db` as the host (Docker network), not `localhost`.

---

## 12. Production considerations

- Terminate **TLS** at a reverse proxy (Nginx/Traefik) for frontend and API.
- Manage **secrets** via Vault / Docker secrets, not `.env`.
- Schedule **DB backups** and define retention.
- Add **monitoring/logging** (Prometheus, Grafana, ELK).
- Perform **HIPAA** risk assessment, pen-testing, and de-identification.

See [architecture.md](architecture.md) for design details.
