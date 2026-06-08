# Cortex ICU Platform – Run Guide

This run guide explains how to set up, run and test the Cortex ICU Platform locally using Docker Compose. It also covers manual steps for running the backend and front‑end without Docker, seeding the database, running the device simulator and working with offline mode.

## 1. Requirements

To run the application via Docker you need:

* Docker 20.10+ and Docker Compose v2 installed on your machine.
* At least 4 GB of RAM and 2 CPU cores.

For manual setup you need Python 3.11+, Node.js 18+ and a PostgreSQL database with the TimescaleDB extension.

## 2. Running with Docker Compose (recommended)

The repository includes a [`docker-compose.yml`](../docker-compose.yml) file that orchestrates three services: `db` (TimescaleDB), `backend` (FastAPI), and `frontend` (React + Nginx). To start the stack:

```bash
git clone <repository>
cd cortex_icu_full
cp .env.example .env      # if provided; set environment variables here
docker compose up --build
```

* The **database** listens on `localhost:5432` and uses default credentials `postgres/postgres` defined in `.env`. Feel free to change them.
* The **backend API** is exposed at `http://localhost:8000`. FastAPI generates interactive docs at `/docs` and `/redoc`.
* The **front‑end PWA** is served by Nginx at `http://localhost:5173`. You can also access the API from the browser because `vite.config.ts` proxies `/api` calls to the backend.

Stop the services with `Ctrl+C` and cleanup with `docker compose down`.

### 2.1 Seeding the database

After starting the stack you may populate the database with sample data for testing. A seed script is provided under [`scripts/seed.py`](../scripts/seed.py). Run it in a temporary container:

```bash
docker compose exec backend bash -c "python -m scripts.seed"
```

This script creates default roles, a super admin user (`admin/admin`), hospitals, branches, ICUs, beds, patients, devices and random vitals. Adjust the script as needed.

### 2.2 Running the device simulator

To simulate vital sign streams, run the device simulator in another terminal. It connects to the backend and periodically POSTs random vitals for the seeded patients/devices:

```bash
docker compose exec backend bash -c "python -m scripts.device_simulator"
```

As the simulator runs you should see vital measurements appear in the front‑end’s dashboard and a continuous stream on the `/ws` WebSocket endpoint.

## 3. Manual setup (without Docker)

If you prefer to run the services directly on your machine:

1. **Database** – Install PostgreSQL and TimescaleDB. Create a database named `cortexicu` and run the SQL script `db/001_init.sql` to create tables and convert the `vitals` table to a hypertable. For example:
   ```bash
   psql -U postgres -c "CREATE DATABASE cortexicu;"
   psql -U postgres -d cortexicu -f db/001_init.sql
   ```

2. **Backend** – Install dependencies and start the API:
   ```bash
   cd cortex_icu_full/backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   Create a `.env` file (see `.env.example`) specifying `DATABASE_URL` and secret keys. The backend reads configuration from environment variables via `app/core/config.py`.

3. **Front‑end** – Install Node modules and run the development server:
   ```bash
   cd cortex_icu_full/frontend
   npm install
   npm run dev
   ```
   The Vite dev server runs at `http://localhost:5173` and proxies `/api` to `http://localhost:8000`.

4. **Seed and simulate** – Run the seed script and device simulator as described above in your activated Python environment.

## 4. Using the Application

1. Open the front‑end in your browser (`http://localhost:5173`).
2. Log in with the seeded super admin credentials (`admin` / `admin` unless you changed them). Change the password immediately after first login.
3. Explore the modules:
   - **Dashboard** – shows the bed overview and the latest vital sign for each patient. Click on a bed row to view a specific patient’s details.
   - **Patients** – lists all admitted patients. Click a patient to open the patient detail view where you can see demographics, AI suggestions and lines/tubes. You can also create, edit or discharge patients.
   - **Patient Detail** – provides a comprehensive view of an individual patient. It displays demographics, current bed assignment, AI‑driven risk score and recommendations, and a list of lines and tubes attached to the patient. Clinicians can add a new line or mark an existing one as removed. Overdue lines are highlighted in orange and removed lines in red.
   - **Devices** – lists monitoring devices attached to beds. You can add devices to a bed or edit them.
   - **Alerts** – shows active and historical alerts. You can acknowledge an alert and provide a reason.
   - **Admin** – exposes the master data and user/role/audit management pages. Within Admin you can:
     * **Device Types** – add or edit device types with vendor, output specification and adapter name so the system can ingest data from any ICU device.
     * **Users** – onboard new users and assign them to roles.
     * **Roles** – create or modify roles and attach permissions.
     * **Audit Logs** – review audit entries for create/update/delete actions across the system.
   - **Settings** – placeholder for user‑specific preferences (theme, language). Future versions will allow users to configure alert rules and notification preferences.

The patient detail view also surfaces AI suggestions returned by the `/api/patients/{patient_id}/ai-suggestions` endpoint. In the MVP this is stubbed with static output but it can be wired up to a real AI engine later. An offline indicator banner appears whenever the browser loses connectivity, informing the user that their actions will be queued and synchronised once the network returns.

The PWA caches the application for offline use. If you lose connectivity to the backend you can still view cached data and queue actions locally. When the connection is restored, queued changes are synchronised automatically.

## 5. Configuration & Environment Variables

Environment variables control the backend:

| Variable | Description | Default |
|---------|-------------|--------|
| `DATABASE_URL` | Connection string for PostgreSQL/TimescaleDB | `postgresql://postgres:postgres@db:5432/postgres` |
| `SECRET_KEY` | Secret key used to sign JWT tokens | `CHANGE_ME` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Lifespan of access tokens | 30 |
| `REFRESH_TOKEN_EXPIRE_MINUTES` | Lifespan of refresh tokens | 43200 (30 days) |
| `ALLOWED_ORIGINS` | CORS origins allowed to call the API | `*` |

Adjust these values by creating a `.env` file at the project root or by injecting them into the Docker Compose environment.

## 6. Production considerations

This MVP is designed to be production‑ready but requires additional hardening before deployment in a hospital:

* **TLS** – Terminate TLS at a reverse proxy (e.g. Nginx or Traefik) and configure HTTPS for both the front‑end and backend.
* **Passwords and Secrets** – Use secure secrets management (e.g. Docker secrets, Vault) instead of storing secrets in `.env`.
* **Database Backups** – Schedule regular backups of the TimescaleDB database and ensure retention policies meet your compliance requirements.
* **Load Balancing** – Scale the backend and database if handling multiple ICUs or hospitals. TimescaleDB can cluster for scalability.
* **Monitoring & Logging** – Deploy logging and monitoring stacks (e.g. Prometheus, Grafana, ELK) to monitor performance, errors and capacity.
* **Compliance** – Perform HIPAA risk assessments, penetration tests and data de‑identification procedures before moving to production.

Refer to the [architecture document](architecture.md) for more details about extensibility, offline operation and security design.
