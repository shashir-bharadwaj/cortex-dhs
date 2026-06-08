🧠 Cortex ICU Backend – Architecture
🔹 Overview

The Cortex ICU backend follows a Layered Clean Architecture with a feature-first design.

This ensures:

clear separation of concerns
scalability across ICU modules
maintainability of business logic
ease of testing
🔹 Request Flow
API Route
→ Provider (Dependency Injection)
→ Use Case (Application Layer)
→ Domain Repository Contract
→ Infrastructure Repository
→ Database (SQLAlchemy)
🔹 High-Level Structure
app/
├── api/                # HTTP layer (FastAPI)
├── application/        # Business logic (use cases)
├── domain/             # Core business abstractions
├── infrastructure/     # DB + repository implementations
├── db/                 # DB setup (engine, session)
├── core/               # Config & shared settings
└── scripts/            # Dev utilities
🔹 Layer Breakdown
1. API Layer (app/api/)

Handles external HTTP interaction.

Components

endpoints/ → route handlers
schemas/ → request/response models
providers/ → dependency injection

Responsibilities

request parsing
response serialization
error handling
dependency wiring

Does NOT handle

business logic
database queries
2. Application Layer (app/application/)

Feature-based business logic.

application/
├── patients/
├── vitals/
├── devices/
└── timeline/

Each feature contains:

use_cases/

Responsibilities

implement workflows
enforce business rules
coordinate repositories

Examples

create patient
assign device
validate patient existence
create timeline events
3. Domain Layer (app/domain/)

Pure business abstraction.

Components

entities/ → core models
repositories/ → contracts/interfaces
enums/ → controlled values

Responsibilities

define business structure
define contracts
enforce domain meaning

Does NOT depend on

FastAPI
SQLAlchemy
4. Infrastructure Layer (app/infrastructure/)

Concrete implementation layer.

Components

database/models/ → SQLAlchemy models
repositories/ → DB implementations
mappers/ → Domain ↔ ORM conversion

Responsibilities

persistence
query execution
DB interaction
5. DB Layer (app/db/)

Shared database configuration.

Responsibilities

engine creation
session management
Base metadata
dependency (get_db)
6. Core (app/core/)

Application-wide configuration.

Responsibilities

environment config
constants
settings
7. Scripts (app/scripts/)

Development utilities.

Examples

reset database
seed data
🔹 Dependency Flow Rule
API → Application → Domain → Infrastructure

❌ No reverse dependency allowed
❌ Domain must not depend on FastAPI/ORM
❌ Application must not use SQLAlchemy models directly

🔹 Key Design Principles
✔ Thin Controllers

Routes only:

parse input
call use case
return response
✔ Provider-Based DI
central dependency wiring
clean routes
easy testing
✔ Feature-First Organization

Each module grows independently:

patients/
├── use_cases/
├── services/
├── validators/
└── policies/
✔ ORM Isolation
SQLAlchemy only in infrastructure
no leakage into application/domain
✔ Testability

Each layer is independently testable:

API tests
use case tests
repository tests
🔹 Example Flow
Assign Device to Patient
API Route
→ AssignDeviceUseCase
→ Validate patient + device
→ Create assignment
→ Persist via repository
→ Create timeline event (side effect)
→ Return response
🔹 Scalability Advantages
Low coupling → DB changes don’t break business logic
High cohesion → features evolve independently
Extensible → easy to add validators/services
Maintainable → clear boundaries
Testable → isolated layers
🔹 Current Features Implemented
Patients management
Vitals tracking
Timeline events
Device management
Patient-device assignment
🔹 Future Improvements
Role-based access (Admin, Doctor, Nurse)
Real-time streaming (WebSockets)
Pagination for large datasets
Audit logging
Event-driven architecture (optional)
🔹 Summary

This architecture ensures:

modular design
clear separation of concerns
scalable ICU workflows
maintainable and testable codebase