# Verkada Access Control Dashboard

This project is a modern dashboard for viewing and analyzing access control events from a Verkada system.

## Overview

The dashboard provides the following core features:
- A timeline of access control events with details.
- Filtering capabilities for events by user and date.
- A chart displaying peak access times.
- User authentication to secure dashboard access.

## Technology Stack

- **Backend:** Python 3.x, FastAPI
- **Frontend:** React, Tailwind CSS, Axios, Vite
- **Database (for dashboard users):** SQLite
- **Verkada API Access:** Custom Python module
- **Containerization:** Docker, Docker Compose
- **Deployment Target:** Proxmox VM (Ubuntu Server)

## Project Structure

```
Verkada_Access_Dashboard/
├── backend/        # FastAPI backend application
│   └── Dockerfile
├── frontend/       # React frontend application
│   └── dashboard/
│       └── Dockerfile
├── deploy/         # (Currently unused, Docker config is in service dirs)
├── docs/           # Project documentation (e.g., API specs, design docs)
├── tests/          # Automated tests (backend and frontend)
│   ├── conftest.py # Pytest configuration for backend tests
│   └── api/
│       └── endpoints/
│           └── test_auth.py # Backend auth endpoint tests
├── .env.example    # Example environment file (copy to .env and fill)
├── .git/           # Git repository data
├── docker-compose.yml # Docker Compose file for local development and deployment
├── PLANNING.md     # Detailed project plan and architecture
├── TASK.MD         # Task tracking for development
└── README.md       # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your local machine or deployment VM.
- Git (for cloning the repository).
- A Verkada API key.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Verkada_Access_Dashboard
    ```
2.  **Configure Environment Variables:**
    Copy `.env.example` to `.env` and fill in your `VERKADA_API_KEY` and any other necessary configurations.
    ```bash
    cp .env.example .env
    # Edit .env with your details
    ```
    The `.env` file should be in the project root.

### Running the Application with Docker Compose

1.  **Build and run the containers:**
    From the project root directory:
    ```bash
    docker compose up -d --build
    ```
2.  **Access the application:**
    - Frontend: `http://localhost` (or your VM's IP address)
    - Backend API: `http://localhost:8000` (or your VM's IP address on port 8000)

    *Note: If deploying on a VM, ensure port 80 and 8000 are accessible and not blocked by a firewall.*

3.  **To stop the application:**
    ```bash
    docker compose down
    ```

## Testing

### Backend Tests (Pytest)

1.  Ensure `pytest` and `httpx` are installed in your Python environment (see `backend/requirements.txt`).
2.  Navigate to the project root.
3.  Set `PYTHONPATH` if necessary (e.g., `export PYTHONPATH=.`)
4.  Run tests:
    ```bash
    pytest tests/
    ```

### Frontend Tests (Vitest)

1.  Navigate to the `frontend/dashboard` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run tests (you might need to add a "test" script to `frontend/dashboard/package.json` like `"test": "vitest"`):
    ```bash
    npm test 
    ```
    or directly:
    ```bash
    npx vitest
    ```

## Deployment

The application is designed to be deployed using Docker containers orchestrated by Docker Compose.
1.  Set up a Proxmox VM (e.g., Ubuntu Server).
2.  Install Docker Engine and Docker Compose on the VM.
3.  Clone the project repository onto the VM.
4.  Create and configure the `.env` file in the project root on the VM.
5.  Run `docker compose up -d --build` in the project root on the VM.
6.  Ensure networking (static IP/DHCP reservation for VM) and firewall rules (allow access to port 80) are configured.
7.  The SQLite database for user authentication will be stored in a `backend_data` directory created in the project root on the VM, as defined in `docker-compose.yml`.

## Contributing

(Guidelines for contributing to the project to be added)

## License

(License information to be added)