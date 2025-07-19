# 📊 Infra-Watch

**Infra-Watch** is a backend-focused infrastructure telemetry and lifecycle dashboard. It simulates an internal platform tool used in DevOps and infrastructure engineering teams to monitor virtual machine (VM) performance, track configuration changes, and surface operational insights through visual dashboards.

---

## 🚀 Features

* Lightweight telemetry agent for collecting CPU, memory, disk, and uptime stats
* FastAPI backend with RESTful endpoints for ingesting and querying metrics
* React dashboard with charts, host health summaries, and alert views
* System config snapshot tracking and drift detection
* JWT-based authentication with role-based access control (RBAC)
* Dockerized for local development and cloud deployment

---

## 🧱 Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
* **Frontend:** React (TypeScript), Chart.js/Recharts
* **Agent:** Python + `psutil`
* **Database:** PostgreSQL (+ TimescaleDB optional)
* **DevOps:** Docker, Docker Compose, GitHub Actions
* **Optional:** AWS EC2 or Render for deployment

---

## 📁 Project Structure

```bash
infra-watch/
├── agent/           # Python-based telemetry agent
├── backend/         # FastAPI application
├── frontend/        # React dashboard
├── docs/            # Requirements, architecture, specs
├── docker-compose.yml
└── .github/         # CI/CD workflows
```

---

## 🧪 Getting Started

### Prerequisites

* Docker + Docker Compose
* Python 3.11+ (optional local backend dev)
* Node.js + npm (for frontend dev)

### Clone the Repo

```bash
git clone https://github.com/BrasJ/infra-watch.git
cd infra-watch
```

### Run Locally

```bash
docker-compose up --build
```

* API available at `http://localhost:8000`
* Dashboard at `http://localhost:3000`

---

## 📚 Documentation

* [Requirements](docs/requirements.md)
* [System Architecture](docs/system-architecture.md)
* [API Spec](docs/api-spec.md)
* [Agent Spec](docs/agent-spec.md)
* [Database Schema](docs/db-schema.md)
* [Deployment Guide](docs/deployment.md)
* [Roadmap](docs/planning/roadmap.md)

---

## 📄 License

MIT License © 2025 Justin Bras
[LinkedIn](https://linkedin.com/in/justin-bras) • [Portfolio](https://justinbras.vercel.app)