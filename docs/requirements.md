# 📋 Project Requirements

## 📌 Project Name

**Infra-Watch** – Infrastructure Telemetry and Lifecycle Monitoring Dashboard

---

## 🎯 Goal

Build a backend-focused system that collects and visualizes telemetry data from virtual machines (VMs) and detects configuration drift over time. The system should be secure, modular, and deployable to simulate real-world infrastructure monitoring tools.

---

## ✅ Functional Requirements

### 1. Telemetry Collection

* A lightweight agent collects system-level metrics:

  * CPU usage (%)
  * Memory usage (%)
  * Disk usage (%)
  * System uptime
  * Hostname, IP, OS
* Agent sends this data to the backend at configurable intervals

### 2. Configuration Snapshot

* Agent captures a JSON-formatted system configuration snapshot:

  * Installed packages
  * Environment variables
  * OS info and kernel version
* Backend stores snapshots and compares against the last known config to detect drift

### 3. Ingestion API (Backend)

* Accepts authenticated POST requests from telemetry agents
* Validates and stores time-series data
* Stores and compares snapshots
* Provides endpoints for querying:

  * Raw metrics
  * Aggregated trends
  * Drift results
  * Alert history

### 4. Web Dashboard (Frontend)

* Login/logout with role-based access
* Host overview page:

  * Current metrics
  * Status indicators (green/yellow/red)
* Host detail page:

  * Metric charts over time
  * System info + configuration diff
* Alert log page and basic alert rule management

### 5. Authentication

* JWT-based login
* Role-based access: Admin, Operator, Viewer
* Admins can create/edit alerts and manage hosts
* Operators can view data
* Viewers can only access metrics

### 6. Alerting Engine

* Threshold-based alerts (e.g. CPU > 90% for 5 min)
* Alerts logged and viewable in the frontend
* (Optional) Alerts sent via email or webhook

---

## ❌ Out of Scope (for MVP)

* Real-time streaming (WebSockets)
* Multi-tenant support
* Cloud-native agent deployment (Ansible, Terraform, etc.)
* External integrations (e.g., Slack, PagerDuty)

---

## 🛡️ Non-Functional Requirements

| Category            | Requirement                                                           |
| ------------------- | --------------------------------------------------------------------- |
| **Security**        | All API endpoints must be protected via JWT auth                      |
| **Validation**      | All incoming data must be schema-validated (Pydantic)                 |
| **Performance**     | Backend should handle at least 10 agents posting every 30 seconds     |
| **Scalability**     | Data ingestion and querying should be async and optimized             |
| **Portability**     | Entire stack should be Dockerized and deployable via `docker-compose` |
| **Maintainability** | Backend and frontend should follow clean modular structure            |
| **Observability**   | Basic logs should track ingestion success/failure and alert events    |

---

## 🧪 Test & Verification Plan (MVP)

| Area                     | How It Will Be Verified                                                |
| ------------------------ | ---------------------------------------------------------------------- |
| Agent sending data       | Manual run of agent script with logs showing successful POST           |
| Data ingestion           | FastAPI logs and DB entries confirm valid entries                      |
| Auth system              | Access to protected routes is role-dependent                           |
| Charts & trends          | React dashboard shows real-time and historical metrics                 |
| Snapshot drift detection | Backend correctly computes and displays diff                           |
| Alerts                   | Alert rules trigger when thresholds are exceeded and appear in logs/UI |