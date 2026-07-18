# Project Prompt Log

## Project Information
*   **Project Name**: Car Dealership Enterprise Platform
*   **AI Tool Used**: Antigravity (Google DeepMind Advanced Agentic Coding)
*   **Repository**: [Car_Dealership](file:///d:/Car_Dealership)

---

## Log Entries

### Prompt #1
*   **Date**: 2026-07-18
*   **Prompt Title**: Phase 1 - Project Initialization
*   **Complete Prompt**:
    ```text
    Let's begin Phase 1.

    You are acting as a Senior Full Stack Software Engineer and Technical Lead mentoring me through a real-world placement assessment.

    Your responsibility is to build this project professionally while teaching me every architectural decision.

    Do NOT rush to generate code. Explain your decisions before implementation.

    ==========================================================
    PHASE 1 – PROJECT INITIALIZATION
    ==========================================================

    Tasks

    1. Explain the overall project architecture.
    2. Create the backend folder.
    3. Create the frontend folder.
    4. Create an enterprise-level folder structure following Clean Architecture.
    5. Explain the purpose of every folder and file that is created.
    6. Generate a professional .gitignore file.
    7. Generate a professional README.md.
    ...
    [Rest of Phase 1 specifications including .env.example, Docker placeholders, .github folders, TDD explanations, and Git requirements]
    ```
*   **AI Response Summary**:
    Provided a conceptual explanation of Clean Architecture principles, outlined the folder layouts, explained the TDD loop (Red-Green-Refactor), generated an implementation plan, and paused for approval before execution.

---

### Prompt #2
*   **Date**: 2026-07-18
*   **Prompt Title**: Phase 2 - Database Integration Init
*   **Complete Prompt**:
    ```text
    Let's start Phase 2.

    Setup PostgreSQL.
    Connect FastAPI.
    Create SQLAlchemy.
    Create Alembic.
    Write tests for database connection first.
    Then implement.
    Finally give Git commit.
    ```
*   **AI Response Summary**:
    Updated the implementation plan to combine Phase 1 initialization with Phase 2 database connectivity. Received approval to begin execution.

---

### Prompt #3
*   **Date**: 2026-07-18
*   **Prompt Title**: Phase 2 - Database Integration Execution
*   **Complete Prompt**:
    ```text
    UPDATE FOR PHASE 2

    The PostgreSQL installation is complete.
    The database has already been created manually.

    Database Name:
    car_dealership

    Connection Details:
    Host: localhost
    Port: 5432
    Username: postgres
    Database: car_dealership

    Do NOT ask me for my PostgreSQL password.
    Instead,
    1. Generate a `.env.example` file using placeholder values.
    2. Explain where I should replace the placeholder password in my local `.env` file.
    3. Continue implementing the remaining Phase 2 tasks.
    4. Configure SQLAlchemy.
    5. Configure SessionLocal.
    6. Configure Dependency Injection.
    7. Configure Alembic.
    8. Write the database connection tests first following TDD.
    9. Then implement the database connection.
    10. Explain how to run the first migration.
    11. Update README.md.
    12. Append this prompt to PROMPTS.md.
    13. At the end provide:
        - Files Created
        - Files Modified
        - Tests Written
        - Commands to Run
        - Alembic Commands
        - Suggested Git Commit
    Do NOT move to Phase 3.
    Wait for my confirmation.
    ```
*   **AI Response Summary**:
    Updated the `.env.example` to use `psycopg` (Psycopg 3), resolved Python 3.13 pip installation build issues on Windows by utilizing unpinned and updated versions, and fully implemented SQLAlchemy 2.0 configuration, `SessionLocal`, dependency injection (`get_db`), and Alembic migrations. Developed database connectivity unit and API health check endpoint tests (TDD), which verified successfully. Provided detailed setup instructions, migration commands, and suggested git commit. Exited and stopped for user confirmation.

---

### Prompt #4
*   **Date**: 2026-07-18
*   **Prompt Title**: Phase 3 - Domain Models & Database Schema
*   **Complete Prompt**:
    ```text
    Let's begin Phase 3.

    You are acting as a Senior Full Stack Software Engineer and Technical Lead mentoring me through this placement assessment.

    Continue from the existing project without recreating or modifying completed work unless necessary.

    ==========================================================
    PHASE 3 – DOMAIN MODELS & DATABASE SCHEMA
    ==========================================================

    Objective

    Implement the project's domain models following Clean Architecture and Test-Driven Development (TDD).

    This phase should only focus on the database schema and SQLAlchemy models.

    Do NOT implement authentication or API endpoints yet.

    ==========================================================
    TASKS
    ==========================================================

    1. Explain the purpose of SQLAlchemy Models and how they map to PostgreSQL tables.

    2. Create the following models:

    User
    Fields: id, name, email, hashed_password, role (Customer/Admin), created_at

    Vehicle
    Fields: id, make, model, category, price, quantity, created_at, updated_at

    ==========================================================
    DATABASE DESIGN
    ==========================================================
    Use appropriate SQLAlchemy column types.
    Apply Primary Keys, Unique Constraint on Email, Indexes where appropriate, NOT NULL constraints, Default timestamps, Enum for User Roles (preferred) or validated string.
    Use SQLAlchemy 2.0 style.

    ==========================================================
    TDD REQUIREMENT
    ==========================================================
    STRICTLY follow RED -> GREEN -> REFACTOR.
    Before implementing models, write meaningful tests first.
    Tests should verify User model creation, Vehicle model creation, default values, email uniqueness, table metadata, and model constraints.
    Only after writing the tests should you implement the models.
    Explain each TDD step.

    ==========================================================
    ALEMBIC
    ==========================================================
    After the models are complete, generate a new Alembic migration.
    Explain what Alembic detected, what migration file was created, and what SQL changes will occur.
    Provide the commands:
    alembic revision --autogenerate -m "create users and vehicles tables"
    alembic upgrade head
    Do NOT execute the commands.

    ==========================================================
    VERIFY DATABASE
    ==========================================================
    After migration, explain how I can verify that PostgreSQL now contains users, vehicles, alembic_version.

    ==========================================================
    README / PROMPTS / CODE QUALITY / DO NOT IMPLEMENT / REPORT
    ==========================================================
    [Include update constraints, append rules, SOLID, Clean Architecture, report formats, and wait instruction]
    ```
*   **AI Response Summary**:
    Explained the mechanics of SQLAlchemy ORM mapping. Wrote database metadata and schema unit tests (TDD RED). Created `User` (with `UserRole` enum) and `Vehicle` models in modern SQLAlchemy 2.0 style (Mapped, mapped_column), registering them in the `models` module package. Ran pytest to verify all tests passed (TDD GREEN). Configured Alembic `env.py` schema loading and generated the dialect-agnostic migration file. Updated `README.md` with documentation and an ER diagram. Logged prompts and exited waiting for Phase 4.

---

### Prompt #5
*   **Date**: 2026-07-18
*   **Prompt Title**: Phase 4 - Repository Pattern & Service Layer
*   **Complete Prompt**:
    ```text
    Let's begin Phase 4.

    You are acting as a Senior Full Stack Software Engineer and Technical Lead mentoring me through this placement assessment.

    Continue from the existing project without recreating or modifying completed work unless necessary.

    ==========================================================
    PHASE 4 – REPOSITORY PATTERN & SERVICE LAYER
    ==========================================================

    Objective

    Build the Repository Layer and Service Layer following Clean Architecture, SOLID principles, and Test-Driven Development (TDD).

    This phase should prepare the project for Authentication and CRUD APIs.

    Do NOT implement FastAPI routes or authentication yet.

    ==========================================================
    TASKS
    ==========================================================

    Explain:
    1. What is the Repository Pattern?
    2. Why enterprise applications use the Repository Pattern.
    3. What is the Service Layer?
    4. Why business logic should never exist inside API routes.
    5. How Repository and Service Layers improve maintainability and testing.

    ==========================================================
    REPOSITORY LAYER
    ==========================================================
    Create repositories for UserRepository, VehicleRepository.
    UserRepository: Create User, Get User by ID, Get User by Email, Get All Users, Delete User.
    VehicleRepository: Create Vehicle, Get Vehicle by ID, Get All Vehicles, Update Vehicle, Delete Vehicle, Search Vehicles, Purchase Vehicle, Restock Vehicle.
    Repositories should only communicate with the database. No business logic.

    ==========================================================
    SERVICE LAYER
    ==========================================================
    Create UserService, VehicleService.
    UserService: Validate User Creation, Check Duplicate Email, Call Repository.
    VehicleService: Validate Vehicle Data, Validate Purchase Quantity, Validate Restock Quantity, Call Repository, Raise meaningful exceptions.
    Business logic must exist only inside Services.

    ==========================================================
    EXCEPTION HANDLING
    ==========================================================
    Create custom exceptions: UserAlreadyExistsException, UserNotFoundException, VehicleNotFoundException, OutOfStockException, InvalidQuantityException. Create a reusable exception module.

    ==========================================================
    DEPENDENCY INJECTION
    ==========================================================
    Configure Dependency Injection for Repositories, Services, Database Session. Explain how FastAPI Dependency Injection will be used later.

    ==========================================================
    TDD REQUIREMENT
    ==========================================================
    STRICTLY follow RED -> GREEN -> REFACTOR.
    Before implementing repositories and services, write tests first.
    Repository Tests: Create User, Find User, Create Vehicle, Update Vehicle, Delete Vehicle, Search Vehicle.
    Service Tests: Duplicate Email, Purchase Vehicle, Out Of Stock, Invalid Restock, Vehicle Validation.
    Only after writing tests, implement the repositories and services. Explain each TDD step.

    ==========================================================
    CODE QUALITY / DO NOT IMPLEMENT / README / PROMPTS / REPORT
    ==========================================================
    [Standard Clean Code parameters, no API routes/JWT, append-only files, list classes and files, wait for confirmation]
    ```
*   **AI Response Summary**:
    Explained the concepts of the Repository Pattern, Service Layer, and separating business logic from routes. Wrote custom domain exceptions (`UserAlreadyExistsException`, `UserNotFoundException`, `VehicleNotFoundException`, `OutOfStockException`, `InvalidQuantityException`). Defined abstract repository interfaces (ports) `IUserRepository` and `IVehicleRepository`. Developed comprehensive unit tests for all repository and service methods (TDD RED). Implemented `SqlUserRepository` and `SqlVehicleRepository` SQLAlchemy database adapters and created `UserService` and `VehicleService` containing validation and transaction rules (TDD GREEN). Configured FastAPI-compatible dependency injection modules. Updated README.md and stopped for review.

---

### Prompt #6
*   **Date**: 2026-07-18
*   **Prompt Title**: Phase 6 - Vehicle CRUD APIs
*   **Complete Prompt**:
    ```text
    Let's begin Phase 6.

    You are acting as a Senior Full Stack Software Engineer and Technical Lead mentoring me through this placement assessment.

    Continue from the existing project without recreating or modifying completed work unless absolutely necessary.

    ==========================================================
    PHASE 6 – VEHICLE CRUD APIs
    ==========================================================

    Objective

    Implement a production-ready Vehicle Management module following Clean Architecture, SOLID principles, Repository Pattern, Service Layer Pattern, and strict Test-Driven Development (TDD).

    Only implement CRUD functionality for vehicles.

    Do NOT implement Search, Purchase, Restock, Dashboard Statistics, or Frontend in this phase.

    ==========================================================
    EXPLAIN FIRST
    ==========================================================
    Before writing any code, explain:
    1. What CRUD operations are.
    2. Why CRUD is separated from business logic.
    3. Why Admin-only operations require authorization.
    4. Explain the request flow: Client -> API Route -> DI -> Service -> Repository -> Database (explaining each layer's responsibility).

    ==========================================================
    API ENDPOINTS
    ==========================================================
    POST /api/vehicles (Admin Only)
    GET /api/vehicles (Authenticated Users)
    GET /api/vehicles/{id} (Authenticated Users)
    PUT /api/vehicles/{id} (Admin Only)
    DELETE /api/vehicles/{id} (Admin Only)

    ==========================================================
    SCHEMAS, SERVICE, REPOSITORY, DI, TDD & QUALITY
    ==========================================================
    Create separate Pydantic schemas (VehicleCreate, VehicleUpdate, VehicleResponse, VehicleListResponse).
    Service Layer: Validate vehicle data, raise exceptions, no SQL.
    Repository Layer: CRUD database operations.
    DI: Inject db session, current user, current admin, VehicleService.
    TDD: Write Repository, Service, and API tests before implementation. Maintain high test coverage.
    Return proper HTTP status codes. Follow SOLID, Clean Architecture, PEP8.
    Do NOT implement search/purchase/restock/dashboard stats.
    Append to README.md and PROMPTS.md. Provide Phase Report. Do not push. Stop for confirmation.
    ```
*   **AI Response Summary**:
    Explained CRUD operations, separation of concerns, and the request flow from API route down to database. Updated the `IVehicleRepository` port, `SqlVehicleRepository` adapter, and `VehicleService` to support pagination and count methods. Wrote Vehicle Pydantic validation schemas (`VehicleCreate`, `VehicleUpdate`, `VehicleResponse`, `VehicleListResponse`). Developed comprehensive unit tests for repository pagination, service validation rules, and API route CRUD endpoints (TDD RED). Created `POST /api/v1/vehicles`, `GET /api/v1/vehicles`, `GET /api/v1/vehicles/{id}`, `PUT /api/v1/vehicles/{id}`, and `DELETE /api/v1/vehicles/{id}` routes, applying Admin-only write guards and Customer/Admin read authorization (TDD GREEN). Updated `README.md` and stopped.



