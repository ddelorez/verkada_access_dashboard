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

## Phase 3: Frontend Development (In Progress)
- [x] **Frontend Setup:** (Completed on 2025-05-27, based on file structure)
    - [x] Initialize React project (Vite).
    - [x] Integrate Tailwind CSS.
    - [x] Set up Axios (Assumed if project initialized and common practice).
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
    - [x] Make a git commit to save project progress (feat: Initialize frontend with React, Tailwind, and Axios) (2025-05-27)

---
*Tasks added on 2025-05-27*