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
