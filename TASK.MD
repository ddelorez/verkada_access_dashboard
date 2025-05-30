# Project Tasks: Verkada Access Control Dashboard

This document tracks the status of development tasks for the Verkada Access Control Dashboard.

## Phase 1: Project Setup & Core Backend (Completed on 2025-05-27)
- [x] **Initialize Project Structure:**
    - [x] Create main project directory (`Verkada_Access_Dashboard`). (Already exists as workspace)
    - [x] Set up subdirectories: `backend/`, `frontend/`, `docs/`, `tests/`, `deploy/`.
    - [x] Initialize Git repository.
    - [x] Create `PLANNING.MD` stub. (Created with full plan)
    - [x] Create `TASK.MD` stub.
    - [x] Create `README.md` stub.
- [x] **Backend - FastAPI Setup:**
    - [x] Set up a virtual environment for Python.
    - [x] Install FastAPI, Uvicorn, SQLAlchemy, Pydantic, python-dotenv, passlib, python-jose[cryptography], bcrypt, requests, pydantic-settings, pandas.
    - [x] Create a basic FastAPI application structure.
- [x] **Backend - User Authentication:**
    - [x] Design SQLite schema for users (username, hashed_password).
    - [x] Implement user registration and login endpoints.
    - [x] Implement password hashing.
    - [x] Implement token-based authentication (e.g., JWTs).
- [x] **Backend - Verkada API Integration:**
    - [x] Integrate existing Python module for Verkada API authentication.
    - [x] Securely manage Verkada API key (via .env).
    - [x] Develop a test endpoint to fetch sample Verkada data (tested /test-token).

## Phase 2: Backend API Development for Dashboard Features (Completed on 2025-05-27)
- [x] **Events Endpoint:**
    - [x] Create API endpoint (`/api/v1/verkada/events`) for access control events.
    - [x] Implement pagination (basic pass-through).
    - [x] Implement filtering by date range and user (basic pass-through).
- [x] **Peak Times Chart Data Endpoint:**
    - [x] Create API endpoint (`/api/v1/verkada/peak-times`) for chart data.
    - [x] Integrate Pandas for data aggregation.

## Phase 3: Frontend Development (Completed on 2025-05-28)
- [x] **Frontend Setup:** (Completed on 2025-05-27, based on file structure)
    - [x] Initialize React project (Vite).
    - [x] Integrate Tailwind CSS.
    - [x] Set up Axios (Assumed if project initialized and common practice).
- [x] **Authentication UI:** (Completed on 2025-05-28)
    - [x] Create Login/Registration pages. (2025-05-28)
    - [x] Implement frontend auth logic. (2025-05-28)
    - [x] Implement protected routes. (2025-05-28)
- [x] **Dashboard UI - Event Timeline:** (Completed on 2025-05-28)
    - [x] Create main dashboard layout. (2025-05-28)
    - [x] Develop event timeline component. (2025-05-28)
    - [x] Implement UI for filtering. (2025-05-28)
- [x] **Dashboard UI - Peak Access Times Chart:** (Completed on 2025-05-28)
    - [x] Integrate a charting library. (2025-05-28)
    - [x] Develop chart component. (2025-05-28)

## Phase 4: Deployment to Proxmox VM (Completed on 2025-05-30)
- [x] **Containerization:**
    - [x] `Dockerfile` for FastAPI backend.
    - [x] `Dockerfile` for React frontend.
- [x] **Proxmox VM Setup (using VM 101 - ASAP-Docker-Host):**
    - [x] Switched from LXC to existing VM 101. Ensured QEMU Guest Agent running.
    - [x] Install Docker Engine & Docker Compose plugin on VM 101.
    - [x] Deploy containers (created `docker-compose.yml`).
    - [x] Configure networking and persistent storage (via `docker-compose.yml`).

## Phase 5: Testing, Documentation & Refinement (Ongoing)
- [x] **Testing:**
    - [x] Backend unit tests (Pytest) - Initial tests for auth endpoints created.
    - [x] Frontend component tests (Vitest) - Initial test for LoginPage created.
- [ ] **Documentation:**
    - [ ] Update `README.md`, `PLANNING.md`, `TASK.MD`.
    - [ ] Docstrings and comments.
- [ ] **Refinement:**
    - [ ] Code reviews, performance optimization, security hardening.
    - [ ] Implement Container Vulnerability Scanning.
    - [x] Make a git commit to save project progress (feat: Initialize frontend with React, Tailwind, and Axios) (2025-05-27)
    - [x] Make a git commit to save project progress (feat: Implement Phase 3 frontend UI components and auth) (2025-05-28)

---
*Tasks added on 2025-05-27, updated 2025-05-30*
## Resuming with Software Planning MCP

To resume using the `github.com/NightTrek/Software-planning-mcp`:
1.  Retrieve the project goal from `PLANNING.MD`.
2.  Use the MCP's `start_planning` tool with this goal.
3.  Use the MCP's `get_todos` tool to check its current task list.
4.  If the MCP's list is empty or outdated compared to this `TASK.MD` file, use this file as the source of truth to populate/synchronize the MCP's to-do list. This involves:
    *   Adding tasks listed here (that are not yet in the MCP or are marked incomplete) using the `add_todo` tool.
    *   Updating the status of tasks in the MCP to `isComplete: true` if they are marked `[x]` in this `TASK.MD` file, using the `update_todo_status` tool.