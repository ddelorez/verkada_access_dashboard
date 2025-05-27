# Project Tasks: Verkada Access Control Dashboard

This document tracks the status of development tasks for the Verkada Access Control Dashboard.

## Phase 1: Project Setup & Core Backend
- [ ] **Initialize Project Structure:**
    - [x] Create main project directory (`Verkada_Access_Dashboard`). (Already exists as workspace)
    - [x] Set up subdirectories: `backend/`, `frontend/`, `docs/`, `tests/`, `deploy/`.
    - [x] Initialize Git repository.
    - [ ] Create `PLANNING.MD` stub. (Already created with full plan)
    - [ ] Create `TASK.MD` stub.
    - [ ] Create `README.md` stub.
- [ ] **Backend - FastAPI Setup:**
    - [ ] Set up a virtual environment for Python.
    - [ ] Install FastAPI, Uvicorn, SQLAlchemy, Pydantic.
    - [ ] Create a basic FastAPI application structure.
- [ ] **Backend - User Authentication:**
    - [ ] Design SQLite schema for users (username, hashed_password).
    - [ ] Implement user registration and login endpoints.
    - [ ] Implement password hashing.
    - [ ] Implement token-based authentication (e.g., JWTs).
- [ ] **Backend - Verkada API Integration:**
    - [ ] Integrate existing Python module for Verkada API authentication.
    *   [ ] Securely manage Verkada API key.
    *   [ ] Develop a test endpoint to fetch sample Verkada data.

## Phase 2: Backend API Development for Dashboard Features
- [ ] **Events Endpoint:**
    - [ ] Create API endpoint (`/api/events`) for access control events.
    - [ ] Implement pagination.
    - [ ] Implement filtering by date range and user.
- [ ] **Peak Times Chart Data Endpoint:**
    - [ ] Create API endpoint (`/api/events/peak-times`) for chart data.
    - [ ] Consider Pandas for data aggregation.

## Phase 3: Frontend Development
- [ ] **Frontend Setup:**
    - [ ] Initialize React project.
    - [ ] Integrate Tailwind CSS.
    - [ ] Set up Axios.
- [ ] **Authentication UI:**
    - [ ] Create Login/Registration pages.
    - [ ] Implement frontend auth logic.
    - [ ] Implement protected routes.
- [ ] **Dashboard UI - Event Timeline:**
    - [ ] Create main dashboard layout.
    - [ ] Develop event timeline component.
    - [ ] Implement UI for filtering.
- [ ] **Dashboard UI - Peak Access Times Chart:**
    - [ ] Integrate a charting library.
    - [ ] Develop chart component.

## Phase 4: Deployment to Proxmox LXC
- [ ] **Containerization:**
    - [ ] `Dockerfile` for FastAPI backend.
    - [ ] `Dockerfile` for React frontend (or serve via FastAPI).
- [ ] **Proxmox LXC Setup:**
    - [ ] Create LXC container.
    - [ ] Install Docker in LXC.
    - [ ] Deploy containers (Docker Compose).
    - [ ] Configure networking and persistent storage.

## Phase 5: Testing, Documentation & Refinement (Ongoing)
- [ ] **Testing:**
    - [ ] Backend unit tests (Pytest).
    - [ ] Frontend component tests.
- [ ] **Documentation:**
    - [ ] Update `README.md`, `PLANNING.md`, `TASK.MD`.
    - [ ] Docstrings and comments.
- [ ] **Refinement:**
    - [ ] Code reviews, performance optimization, security hardening.

---
*Tasks added on 2025-05-27*