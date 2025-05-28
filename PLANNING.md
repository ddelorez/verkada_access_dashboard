## Project Plan: Verkada Access Control Dashboard

**Goal:** Develop a modern dashboard for Verkada access control events, hosted on Proxmox LXC containers, leveraging an existing Python authentication module for Verkada API access, FastAPI for the backend, React/Tailwind for the frontend, and SQLite for user authentication.

**Core Features:**
1.  Display a timeline of access control events with details.
2.  Filter events by user and date.
3.  Show a chart of peak access times.
4.  Secure the dashboard with username/password authentication.

**Technology Stack:**
*   **Backend:** Python 3.x, FastAPI
*   **Frontend:** React, Tailwind CSS, Axios (for API calls)
*   **Database (for dashboard users):** SQLite
*   **Verkada API Access:** Existing Python module
*   **Deployment:** Docker, Proxmox LXC

---

### High-Level Architecture

```mermaid
graph TD
    User[Dashboard User] -- HTTPS --> Browser[User's Browser]

    subgraph Browser
        Frontend[React + Tailwind CSS App]
    end

    Browser -- API Calls (HTTPS) --> LXC[Proxmox LXC Container]

    subgraph LXC
        subgraph DashboardBackend[FastAPI Application]
            AuthAPI[User Auth API (login, logout)] -- R/W --> UserDB[(SQLite User DB)]
            EventsAPI[Access Events API (timeline, filter, chart data)] -- Uses --> VerkadaAuthMod[Verkada Auth Module]
        end
        VerkadaAuthMod -- API Key + Session Token --> VerkadaAPI[Verkada Cloud API]
    end

    style User fill:#f9f,stroke:#333,stroke-width:2px
    style Browser fill:#ccf,stroke:#333,stroke-width:2px
    style LXC fill:#lightgrey,stroke:#333,stroke-width:2px
    style DashboardBackend fill:#lightblue,stroke:#333,stroke-width:2px
    style VerkadaAPI fill:#bbf,stroke:#333,stroke-width:2px
```

---

### Development Phases & Key Tasks:

**Phase 1: Project Setup & Core Backend (Complexity: 6/10) [COMPLETED - 2025-05-27]**
1.  **Initialize Project Structure:** [DONE]
    *   Create main project directory (`Verkada_Access_Dashboard`).
    *   Set up subdirectories: `backend/`, `frontend/`, `docs/`, `tests/`, `deploy/`.
    *   Initialize Git repository.
2.  **Backend - FastAPI Setup:** [DONE]
    *   Set up a virtual environment for Python.
    *   Install FastAPI, Uvicorn, SQLAlchemy, Pydantic, python-dotenv, passlib, python-jose[cryptography], bcrypt, requests, pydantic-settings, pandas.
    *   Create a basic FastAPI application structure.
3.  **Backend - User Authentication:** [DONE]
    *   Design SQLite schema for users (username, hashed_password).
    *   Implement user registration and login endpoints.
    *   Implement password hashing.
    *   Implement token-based authentication (e.g., JWTs).
4.  **Backend - Verkada API Integration:** [DONE]
    *   Integrate existing Python module for Verkada API authentication.
    *   Securely manage Verkada API key.
    *   Develop a test endpoint to fetch sample Verkada data.

**Phase 2: Backend API Development for Dashboard Features (Complexity: 7/10) [COMPLETED - 2025-05-27]**
1.  **Events Endpoint:** [DONE]
    *   Create API endpoint (`/api/v1/verkada/events`) for access control events.
    *   Implement pagination (basic pass-through).
    *   Implement filtering by date range and user (basic pass-through).
2.  **Peak Times Chart Data Endpoint:** [DONE]
    *   Create API endpoint (`/api/v1/verkada/peak-times`) for chart data.
    *   Integrate Pandas for data aggregation.

**Phase 3: Frontend Development (Complexity: 8/10) [COMPLETED - 2025-05-28]**
1.  **Frontend Setup:** [DONE]
    *   Initialize React project. [DONE - 2025-05-27]
    *   Integrate Tailwind CSS. [DONE - 2025-05-27]
    *   Set up Axios. [DONE - 2025-05-27]
2.  **Authentication UI:** [DONE]
    *   Create Login/Registration pages. [DONE]
    *   Implement frontend auth logic. [DONE]
    *   Implement protected routes. [DONE]
3.  **Dashboard UI - Event Timeline:** [DONE]
    *   Create main dashboard layout. [DONE]
    *   Develop event timeline component. [DONE]
    *   Implement UI for filtering. [DONE]
4.  **Dashboard UI - Peak Access Times Chart:** [DONE]
    *   Integrate a charting library. [DONE]
    *   Develop chart component. [DONE]

**Phase 4: Deployment to Proxmox LXC (Complexity: 7/10)**
1.  **Containerization:**
    *   `Dockerfile` for FastAPI backend.
    *   `Dockerfile` for React frontend (or serve via FastAPI).
2.  **Proxmox LXC Setup:**
    *   Create LXC container.
    *   Install Docker in LXC.
    *   Deploy containers (Docker Compose).
    *   Configure networking and persistent storage.

**Phase 5: Testing, Documentation & Refinement (Ongoing, Complexity: 6/10)**
1.  **Testing:**
    *   Backend unit tests (Pytest).
    *   Frontend component tests.
2.  **Documentation:**
    *   Update `README.md`, `PLANNING.md`, `TASK.MD`.
    *   Docstrings and comments.
3.  **Refinement:**
    *   Code reviews, performance optimization, security hardening.