# 🚀 Deployment Guide

## 📌 Project: Infra-Watch

This document outlines how to deploy Infra-Watch in both **local development** and **cloud production** environments using Docker, environment variables, and optional AWS infrastructure.

---

## 🧪 Local Development (via Docker Compose)

Infra-Watch is designed for full local deployment with a single command.

### 📁 Prerequisites

* Docker
* Docker Compose
* Git

### 🧱 Architecture (Local)

```plaintext
[Telemetry Agent] --> [FastAPI Backend] --> [PostgreSQL (TimescaleDB)]
                                 |
                         [React Frontend]
```

### ▶️ Start Locally

From the project root:

```bash
docker-compose up --build
```

### 📌 Services

| Service     | URL                                            |
| ----------- | ---------------------------------------------- |
| Frontend    | [http://localhost:3000](http://localhost:3000) |
| Backend API | [http://localhost:8000](http://localhost:8000) |
| Database    | localhost:5432 (internal only)                 |

---

## ☁️ Production Deployment (Recommended Options)

### Option A: 🚀 Deploy to AWS EC2

**Use Case:** Manual VM provisioning or Infra-as-Code setup

1. Provision an EC2 instance (Ubuntu 22.04 preferred)
2. Install Docker + Docker Compose
3. Clone the repo + set up `.env` file (see below)
4. Run:

   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```
5. Open ports:

   * 80/443 (frontend, Nginx reverse proxy)
   * 8000 (API, optional internal)
   * 5432 (PostgreSQL, internal only)

### Option B: 🌐 Deploy with Render or Railway

1. Push repo to GitHub
2. Link frontend and backend services to Render:

   * Frontend: Build command `npm run build`, static site
   * Backend: Python web service with `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Set environment variables via dashboard
4. Use managed PostgreSQL service

### Option C: 🐳 Self-host via Docker Swarm or Kubernetes

Advanced users may deploy via:

* Docker Swarm (`docker stack deploy`)
* Kubernetes (K8s manifest in future update)
* Helm (optional package support)

---

## 🔐 Environment Variables

| Key                   | Purpose                       |
| --------------------- | ----------------------------- |
| `DATABASE_URL`        | PostgreSQL connection string  |
| `JWT_SECRET`          | Secret for signing tokens     |
| `JWT_EXPIRE_MINUTES`  | Token expiration duration     |
| `FRONTEND_URL`        | Allowed CORS origin           |
| `AGENT_AUTH_TOKEN`    | Pre-shared token for agents   |
| `ALERT_EVAL_INTERVAL` | How often to run alert checks |

Stored securely in `.env` (locally) or in CI/CD secrets (production).

---

## 📦 Docker Compose Setup

**Standard: `docker-compose.yml`**

```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    env_file: .env
    depends_on: [db]

  frontend:
    build: ./frontend
    ports: ["3000:80"]
    env_file: .env

  db:
    image: timescale/timescaledb:latest-pg14
    ports: ["5432:5432"]
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
```

---

## 🔁 CI/CD Pipeline (Optional GitHub Actions)

**Path:** `.github/workflows/ci.yml`

### Suggested Steps:

* Install Python & Node
* Lint backend + frontend
* Run backend unit tests
* Build Docker images (optional)
* Deploy to staging branch (optional)

```yaml
name: Infra-Watch CI

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install backend deps
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Lint + Test Backend
        run: |
          cd backend
          pytest

      # Similar steps for frontend (npm install + lint/build)
```

---

## 📁 Deployment Checklist

* [ ] `.env` file created with required secrets
* [ ] HTTPS configured (via Nginx + Let's Encrypt or Render)
* [ ] Database is persistent (volume or cloud)
* [ ] Alert engine enabled and scheduled
* [ ] Monitoring/logging tools added (optional)