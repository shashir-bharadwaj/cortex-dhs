# Cortex ICU Platform Architecture

This document provides a high-level overview of the Cortex ICU Platform, its system design, and how components interact. The platform is designed for **real-time ICU monitoring**, **offline-first reliability**, and **scalable hospital deployments**.

---

# 1. System Overview

The platform follows a **modular monolith architecture** deployed via Docker with three core services:

1. Frontend (PWA)
2. Backend API (FastAPI)
3. Database (PostgreSQL)

It is designed for **edge-first deployment**, allowing hospitals to operate independently and optionally sync with a central system.

---

# 2. Architecture Layers

## 2.1 Frontend (PWA)

* React + TypeScript + Vite
* Progressive Web App (PWA)
* Uses:

  * WebSockets for real-time vitals
  * HTTP fallback
* Offline support:

  * Service Worker caching
  * IndexedDB queue for actions

### Key Capabilities

* Offline-first interaction
* Real-time monitoring dashboards
* Sync reconciliation when network returns

---

## 2.2 Backend API

* FastAPI-based modular monolith
* Clean architecture:

  * API layer
  * Application (use-cases)
  * Domain layer
  * Infrastructure (repositories)

### Features

* REST APIs
* WebSocket streaming
* JWT authentication + refresh tokens
* Role-Based Access Control (RBAC)
* Audit logging

---

## 2.3 Database Layer

* PostgreSQL (single instance)
* Managed via **SQLAlchemy + Alembic**

### Responsibilities

* Transactional storage
* Time-series vitals storage (standard tables)

### Key Design Decision

Using a single DB:

* simplifies deployment
* ensures consistency
* avoids distributed complexity

---

# 3. Database Migration & Seeding Strategy

## 3.1 Migrations (Alembic)

Schema is managed via:

```bash
python -m alembic upgrade head
```

This ensures:

* version-controlled schema
* reproducible environments
* safe upgrades

---

## 3.2 Seeding Strategy

Seed scripts populate:

* roles
* admin user
* hospital/unit data

```bash
python -m app.scripts.seed_data
```

### Design Principles

* Idempotent (safe to run multiple times)
* Runs after migrations
* Never destructive

---

# 4. Core Data Model

| Entity          | Purpose               |
| --------------- | --------------------- |
| Hospital / Unit | Location hierarchy    |
| User / Role     | Authentication & RBAC |
| Patient         | ICU admission data    |
| Device          | Monitoring devices    |
| DeviceType      | Device metadata       |
| Vital           | Patient measurements  |
| Alert           | Generated alarms      |
| Timeline        | Clinical events       |
| AuditLog        | Compliance tracking   |

---

# 5. Offline-First Design

* IndexedDB stores user actions
* Sync queue handles retries
* Conflict resolution:

  * non-critical → last write wins
  * critical → manual resolution

---

# 6. Alerts & Escalation

* Threshold-based triggers
* Stored in DB
* Broadcast via WebSockets
* Escalation rules:

  * time-based
  * role-based

---

# 7. Security & Compliance

* JWT authentication
* Optional MFA (TOTP)
* RBAC permissions
* Audit logging
* Encrypted sensitive fields
* HIPAA-aligned design

---

# 8. Docker Deployment Architecture

Services:

| Service  | Responsibility |
| -------- | -------------- |
| db       | PostgreSQL     |
| backend  | FastAPI        |
| frontend | React app      |

### Startup Flow

1. DB container starts
2. Backend waits for DB health
3. Alembic migrations run
4. Seed script runs
5. API starts
6. Frontend connects

---

# 9. Service Communication

| Source                | Target                | Method           |
| --------------------- | --------------------- | ---------------- |
| Frontend              | Backend               | HTTP / WebSocket |
| Backend               | DB                    | SQLAlchemy       |
| Container → Container | Docker network (`db`) |                  |

---

# 10. Extensibility

Future enhancements:

## 10.1 Device Integration Layer

* HL7 ingestion
* Vendor-specific adapters
* Edge processing

## 10.2 Analytics & Reporting

* Aggregations
* ICU KPIs
* Export modules

## 10.3 Multi-Hospital Sync

* Central command center
* Multi-tenant architecture

## 10.4 AI Integration

* Risk prediction
* Anomaly detection
* Clinical recommendations

---

# 11. Design Principles

* Simplicity over microservices (for MVP)
* Edge-first reliability
* Modular extensibility
* Observability-ready

---

# 12. Production Considerations

* TLS termination
* Secrets management
* Backup strategy
* Monitoring stack
* Compliance validation

---

# 🎯 Summary

The Cortex ICU platform combines:

* Real-time monitoring
* Offline-first resilience
* Clean architecture backend
* Containerized deployment

This provides a strong foundation for a scalable ICU monitoring system.
