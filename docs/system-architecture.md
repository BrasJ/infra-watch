# 🧱 System Architecture

## 📌 Project: Infra-Watch

---

## 🧭 Overview

**Infra-Watch** is a modular infrastructure monitoring system designed to ingest, process, store, and visualize telemetry data from virtual machines. It also captures system configuration snapshots for drift detection and supports threshold-based alerting. The system is composed of three major components:

* **Agent**: Runs on VMs and sends telemetry/snapshot data
* **Backend API**: Handles ingestion, authentication, storage, and alerts
* **Frontend Dashboard**: Displays data and configuration insights to users

---

## 🧩 Component Breakdown

### 1. **Telemetry Agent**

* Collects:

  * CPU %, memory %, disk %, uptime
  * Hostname, IP, OS
  * Optional: system config snapshot (packages, env vars)
* Sends structured JSON via HTTP POST
* Scheduled via crontab, watchdog, or Docker interval
* Runs as a CLI or daemon

### 2. **Backend (FastAPI)**

* RESTful API with JWT-based auth
* Routes:

  * `/api/telemetry`: Accepts metric data
  * `/api/snapshot`: Accepts system snapshot
  * `/api/metrics`: Query time-series data
  * `/api/alerts`: Define + log alerts
* DB schema supports time-series data (PostgreSQL + TimescaleDB)
* Alert evaluation via background workers (e.g., Celery or asyncio loop)

### 3. **Frontend (React)**

* Authenticated dashboard with RBAC
* Pages:

  * Host overview
  * Host detail with charts + config diff
  * Alert log + thresholds UI
* Data fetched from backend via secure API

---

## 🔄 Data Flow Diagram

```plaintext
     +----------------+              +----------------+               +--------------------+
     |  Telemetry     |   HTTP POST  |     FastAPI     |   SQL Insert |   PostgreSQL/TSDB   |
     |    Agent       +------------->+   Ingestion API +------------->+   Time-Series Data  |
     +----------------+              +----------------+               +--------------------+

                                |                                |
                                | JWT Auth + Query Routes        |
                                v                                v

                     +----------------+               +---------------------+
                     |  React Frontend | <------------ |   API: /metrics     |
                     |   Dashboard     |   HTTPS GET   |   /snapshot /alerts |
                     +----------------+               +---------------------+

         [Optional]
         +-------------> Config Drift Diff Logic
                         Alert Rules Engine (Background Worker)
```

---

## 🔐 Authentication & Access Control

* **JWT Authentication** with refresh tokens
* **RBAC** roles:

  * `admin`: full access to hosts, users, and alerts
  * `operator`: view hosts, configure alerts
  * `viewer`: read-only access

Tokens are passed via Authorization headers to protected API endpoints.

---

## 🧱 Database Model Summary

| Table         | Description                             |
| ------------- | --------------------------------------- |
| `hosts`       | Registered VMs/agents                   |
| `metrics`     | Time-series resource usage data         |
| `snapshots`   | System configuration snapshots          |
| `alerts`      | Threshold rules and logs                |
| `users`       | Auth users with roles                   |
| `auth_tokens` | Refresh/access token storage (optional) |

A full schema breakdown will be included in [`db-schema.md`](./db-schema.md).

---

## 🛠 Background Services

* **Alert Evaluation Loop**:

  * Runs every X minutes
  * Queries recent metrics
  * Logs alert events if conditions are met

* **Snapshot Comparison Engine**:

  * On new snapshot upload, diff with last stored version
  * Flag added/removed packages, env changes, kernel version changes

---

## ☁️ Deployment Topology (Production)

```plaintext
+-------------------+      +---------------------+      +----------------------+
|   VM(s) with      | ---> |  FastAPI Backend     | ---> | PostgreSQL + TSDB     |
|   telemetry agent |      |  on EC2 or container |      | (managed or self-host)|
+-------------------+      +---------------------+      +----------------------+

           ^
           |
           |       +------------------+
           +-------+ React Dashboard  |
                   +------------------+
```

Backend + frontend can run in containers, while agents are either installed directly on VMs or run in isolated Docker containers.