# Car Dealership Enterprise Web Application

An enterprise-grade car dealership platform designed with **Clean Architecture** principles, strict **Test-Driven Development (TDD)** practices, and a modern containerized ecosystem.

---

## Project Overview

This project serves as a real-world vehicle inventory and booking management platform. The architecture is built to support high-scalability, loose coupling, and rich developer experiences, adhering to standard practices for robust software engineering placement assessments.

---

## Assessment Objective

The goal of this project is to demonstrate competency in:
1. **Clean Architecture separation of concerns**: Decoupling domain business models from infrastructure adapters and frameworks.
2. **Strict Test-Driven Development (TDD)**: Ensuring 100% test coverage for core components, moving from Red to Green to Refactor.
3. **Advanced Backend-Frontend Integration**: Connecting a highly responsive React frontend with a FastAPI web services backend, backed by PostgreSQL.
4. **DevOps & Containerization**: Standardizing dev, test, and prod environments using Docker.

---

## Features

- [ ] User Authentication & Authorization (JWT-based, Secure Cookies) *(Pending)*
- [ ] Vehicle Inventory Management (Add, Edit, Remove, Search, Filter) *(Pending)*
- [ ] Booking & Appointment Scheduler (Customer test drives, maintenance slots) *(Pending)*
- [ ] Dynamic Analytics Dashboard (Admin metrics, sales numbers, inventory levels) *(Pending)*
- [ ] Real-time Notifications (Email booking confirmations, reminders) *(Pending)*
- [x] Enterprise Clean Architecture skeleton (Backend & Frontend)
- [x] PostgreSQL & SQLAlchemy database connection infrastructure
- [x] Alembic migration setup
- [x] Health-check route verifying DB connectivity

---

## Technology Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13)
- **Database ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Driver**: [Psycopg 3](https://www.psycopg.org/psycopg3/) (Modern PostgreSQL client)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Database**: [PostgreSQL 15](https://www.postgresql.org/)
- **Frontend Framework**: [React.js](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Testing Suite**: [pytest](https://docs.pytest.org/) (Backend), [Vitest](https://vitest.dev/) (Frontend)
- **Containerization**: [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/)

---

## Project Architecture

The application strictly follows Uncle Bob's **Clean Architecture** patterns, ensuring dependencies only point inwards.

```
       ┌─────────────────────────────────────────────────────────┐
       │                  Frameworks & Drivers                   │
       │           (FastAPI / React / PostgreSQL / Docker)       │
       └────────────────────────────┬────────────────────────────┘
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                    Interface Adapters                   │
       │        (HTTP Routers / Repositories / Redux State)      │
       └────────────────────────────┬────────────────────────────┘
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                       Use Cases                         │
       │           (Application workflows & interfaces)          │
       └────────────────────────────┬────────────────────────────┘
                                    ▼
       ┌─────────────────────────────────────────────────────────┐
       │                     Domain Entities                     │
       │          (Core Business Objects & Rules - No deps)      │
       └─────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
Car_Dealership/
├── .github/                    # CI/CD Workflows
│   └── workflows/
│       └── ci.yml              # Automated test runner workflow
├── backend/
│   ├── app/
│   │   ├── domain/             # Core Domain entities & rules
│   │   ├── use_cases/          # Business logic & repository interfaces
│   │   ├── infrastructure/     # Framework integrations & adapters
│   │   │   ├── persistence/    # DB models, repositories, and config
│   │   │   ├── security/       # Encryption & token auth logic
│   │   │   └── web/            # FastAPI Routers, schemas, and entry point
│   │   ├── tests/              # Test suites (Unit & Integration)
│   │   ├── config.py           # Configuration loader
│   │   └── main.py             # API application entry point
│   ├── alembic.ini             # Alembic configuration
│   ├── Dockerfile              # Container instruction placeholder
│   ├── pytest.ini              # pytest settings
│   └── requirements.txt        # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── domain/             # Entities and interfaces
│   │   ├── use_cases/          # State flow coordinators
│   │   ├── infrastructure/     # HTTP & local storage adapters
│   │   ├── presentation/       # UI Components, pages, styles, store
│   │   └── tests/              # Vitest suite
│   ├── Dockerfile              # Container instruction placeholder
│   └── package.json            # Frontend packages
├── docker-compose.yml          # Container composer configuration
├── .env.example                # Example configuration keys
└── README.md                   # Project documentation
```

---

## Database Schema & Entities

The relational database schema is configured in `app/infrastructure/persistence/models/` and managed using Alembic.

### Entity-Relationship Diagram
```mermaid
erDiagram
    users {
        int id PK "auto-increment"
        varchar name "NOT NULL (100)"
        varchar email UK "NOT NULL (255), INDEX"
        varchar hashed_password "NOT NULL (255)"
        enum role "NOT NULL (Customer/Admin)"
        timestamp created_at "NOT NULL, DEFAULT now()"
    }
    vehicles {
        int id PK "auto-increment"
        varchar make "NOT NULL (100), INDEX"
        varchar model "NOT NULL (100), INDEX"
        varchar category "NOT NULL (50)"
        numeric price "NOT NULL (12,2)"
        int quantity "NOT NULL, DEFAULT 0"
        timestamp created_at "NOT NULL, DEFAULT now()"
        timestamp updated_at "NOT NULL, DEFAULT now()"
    }
```

### User Entity Schema
*   **Table Name**: `users`
*   **Primary Key**: `id` (Integer, auto-incrementing)
*   **Fields**:
    *   `name`: `VARCHAR(100)`, NOT NULL — User's display name.
    *   `email`: `VARCHAR(255)`, NOT NULL, UNIQUE, INDEX — User's email address.
    *   `hashed_password`: `VARCHAR(255)`, NOT NULL — Cryptographic hash of the password.
    *   `role`: `ENUM('Customer', 'Admin')`, NOT NULL, default `'Customer'` — Authorization role.
    *   `created_at`: `TIMESTAMP`, NOT NULL, default server-side current timestamp.

### Vehicle Entity Schema
*   **Table Name**: `vehicles`
*   **Primary Key**: `id` (Integer, auto-incrementing)
*   **Fields**:
    *   `make`: `VARCHAR(100)`, NOT NULL, INDEX — Car manufacturer.
    *   `model`: `VARCHAR(100)`, NOT NULL, INDEX — Car model.
    *   `category`: `VARCHAR(50)`, NOT NULL — Vehicle segment (e.g. Sedan, SUV).
    *   `price`: `NUMERIC(12, 2)`, NOT NULL — Vehicle price.
    *   `quantity`: `INTEGER`, NOT NULL, default `0` — In-stock count.
    *   `created_at`: `TIMESTAMP`, NOT NULL, default server-side current timestamp.
    *   `updated_at`: `TIMESTAMP`, NOT NULL, default server-side current timestamp, auto-updated.

### Database Migration Instructions
To generate and apply database schema updates using Alembic:
1.  **Generate Migration Script**:
    ```bash
    cd backend
    .venv\Scripts\alembic.exe revision --autogenerate -m "create users and vehicles tables"
    ```
2.  **Apply Migration to Database**:
    ```bash
    .venv\Scripts\alembic.exe upgrade head
    ```

---

## Installation Guide

### Prerequisites
- Python 3.13+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup
1. Clone the project repository.
2. Navigate to `backend/` directory:
   ```bash
   cd backend
   ```
3. Create a python virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   - **Windows PowerShell**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Bash/macOS**:
     ```bash
     source .venv/bin/activate
     ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Copy the `.env.example` file to `.env` in the root:
   ```bash
   cp ../.env.example ../.env
   ```
7. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
*(Instructions will be detailed in Phase 3)*

---

## Environment Variables

Copy the `.env.example` file from the project root to `.env` and adjust the database credentials and security keys.

```env
# Database configuration
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/car_dealership
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_PASSWORD
POSTGRES_DB=car_dealership
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Security settings
SECRET_KEY=replace_with_a_secure_token
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> [!WARNING]
> Never commit your `.env` file containing actual passwords to version control. The `.gitignore` file is pre-configured to block it.

---

## API Documentation

FastAPI automatically generates interactive documentation accessible at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Testing Strategy

This project adheres to a strict **Test-Driven Development (TDD)** loop:
1. **Red**: Write a test verifying missing behavior, run it, and observe failure.
2. **Green**: Write minimal implementation code to pass the test.
3. **Refactor**: Clean up the design while verifying that all tests remain green.

### Running Backend Tests
To run all tests from the `backend/` directory:
```bash
cd backend
.venv\Scripts\pytest.exe
```

---

## Domain Design Patterns & Architecture Layers

To comply with SOLID principles and Clean Architecture, Phase 4 establishes key design layers.

### 1. Repository Pattern (Data Access Layer)
The Repository Pattern decouples our core application logic from the details of the database access technology (SQLAlchemy ORM).
- **Interfaces (Ports)**: Declared as abstract classes (`IUserRepository`, `IVehicleRepository`) in the Application layer (`app/use_cases/interfaces/`).
- **Implementations (Adapters)**: Implemented as concrete classes (`SqlUserRepository`, `SqlVehicleRepository`) in the Infrastructure layer (`app/infrastructure/persistence/repositories/`).

This separation allows the business logic to remain completely agnostic of the database engine and ORM structure, making it possible to swap SQL database adapters with mock or alternate database systems without rewriting application workflows.

### 2. Service Layer (Business Logic Layer)
The Service Layer coordinates transactions, executes core calculations, and runs domain validations.
- **UserService**: Performs validation logic, handles user registration constraints, and coordinates user CRUD adapters.
- **VehicleService**: Validates incoming car specifications, handles inventory stock adjustments (purchasing and restocking logic), and triggers exceptions.

*Why avoid logic in API Routes?* API Route handlers (Controllers) should only be responsible for parsing HTTP requests, serializing models to JSON DTOs, and mapping response codes. Keeping business logic out of routers simplifies controllers, makes use cases reusable across other delivery mechanisms (like CLI runners or task workers), and enables clean unit testing of application rules without spawning HTTP server instances.

### 3. Exception Handling (Domain Exceptions)
We established a dedicated exception layer (`app/domain/exceptions/`) containing custom domain exceptions:
- `UserAlreadyExistsException`: Triggered on user email duplication checks.
- `UserNotFoundException`: Triggered when queried users do not exist.
- `VehicleNotFoundException`: Triggered when queried vehicles do not exist.
- `OutOfStockException`: Triggered when vehicle purchases exceed stock inventory.
- `InvalidQuantityException`: Triggered when purchasing or restocking with negative/zero inputs.

### 4. Dependency Injection (FastAPI Integration)
We configure a modular dependency injection file `app/infrastructure/web/dependencies.py`. It uses FastAPI's `Depends` mechanisms to inject dependencies down the layers:
```
      FastAPI Router Endpoint
                 │
                 ▼
       get_vehicle_service() [Depends]
                 │
                 ▼
     get_vehicle_repository() [Depends]
                 │
                 ▼
            get_db() [Depends]
```
This hierarchical injection facilitates modular mocking during integration and API testing by overriding dependencies at the router level.

---

## Secure Authentication & Role-Based Authorization

We implement a robust, production-ready JWT authentication system utilizing `bcrypt` password hashing, token validation, and role-based permissions checks.

### 1. Password Hashing Utility
Passwords are cryptographically hashed using **Bcrypt** before they are committed to the database. We avoid storing raw passwords to protect users in the event of data breaches. Bcrypt adds a random salt value and runs key stretching to make brute-force cracking mathematically infeasible. 

### 2. JWT Access Token Flow
The JWT (JSON Web Token) authentication mechanism follows this sequence:
```
  Client (Frontend)            FastAPI (Backend)
         │                             │
         │────── POST /login ─────────>│  [Verify password with bcrypt]
         │<───── Return Token ─────────│  [Generate JWT: id, email, role]
         │                             │
    [Store Token]                      │
         │                             │
         │─── Request with Header ────>│  [Inject HTTPBearer dependency]
         │    (Authorization: Bearer)  │  [Verify signature & exp time]
         │                             │  [Load User to verify Role]
         │<────── Return Data ─────────│  [Return requested resource]
         ▼                             ▼
```

### 3. Role-Based Authorization
The platform defines two user roles (`Customer`, `Admin`) representing distinct access tiers:
*   **Customer Tier**: Authenticated users can query listings and schedule test drives.
*   **Admin Tier**: Administrator privilege checks (`Depends(get_current_admin)`) block Customers with a `403 Forbidden` response and allow read/write management actions.

### 4. API Endpoints Reference
*   `POST /api/v1/auth/register` — Creates a new user record. Normalizes email addresses to lowercase and trims name fields. Requires strong password limits (minimum 8 characters).
*   `POST /api/v1/auth/login` — Verifies user credentials and returns a bearer JWT access token.

### 5. Authentication Examples

#### Registration Request Example
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice Smith", "email": "alice@example.com", "password": "securepassword123", "confirm_password": "securepassword123"}'
```

#### Registration Response (201 Created)
```json
{
  "id": 1,
  "name": "Alice Smith",
  "email": "alice@example.com",
  "role": "Customer",
  "created_at": "2026-07-18T17:50:00Z"
}
```

#### Login Request Example
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "alice@example.com", "password": "securepassword123"}'
```

#### Login Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "role": "Customer",
    "created_at": "2026-07-18T17:50:00Z"
  }
}
```

---

## Deployment Guide
*(To be completed in future deployment phases)*

---

## AI Usage

- **AI Assistant**: Antigravity (Google DeepMind Advanced Agentic Coding)
- **Role**: Technical Lead & Co-Developer
- **Actions Logged**: Prompt history is systematically logged in [PROMPTS.md](file:///d:/Car_Dealership/PROMPTS.md).

---

## Future Improvements
- [ ] Implement Redis-based session caching.
- [ ] Set up end-to-end integration workflows using Playwright.
- [ ] Configure automatic backup schedules for PostgreSQL database volumes.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
