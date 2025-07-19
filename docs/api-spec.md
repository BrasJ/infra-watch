# 📡 API Specification

## 📌 Project: Infra-Watch

This document describes the REST API contract for the Infra-Watch backend, built with FastAPI. The API supports telemetry ingestion, configuration snapshot uploads, metric queries, and alert management. All endpoints use JSON over HTTPS and require authentication unless explicitly marked public.

---

## 🔐 Authentication

* **Auth Method:** JWT Bearer tokens
* **Login Endpoint:** `POST /api/auth/login`
* **Header Format:**

  ```
  Authorization: Bearer <access_token>
  ```

Roles: `admin`, `operator`, `viewer`
Role-based access is enforced on protected routes.

---

## 🧾 Endpoint Summary

| Method | Endpoint                       | Auth Required | Description                           |
| ------ | ------------------------------ | ------------- | ------------------------------------- |
| POST   | `/api/auth/login`              | ❌             | Login and receive JWT tokens          |
| GET    | `/api/users/me`                | ✅             | Retrieve current user profile         |
| POST   | `/api/telemetry`               | ✅             | Ingest telemetry from agent           |
| POST   | `/api/snapshot`                | ✅             | Upload a system config snapshot       |
| GET    | `/api/metrics`                 | ✅             | Query metrics by host/date/type       |
| GET    | `/api/snapshot/{host_id}`      | ✅             | Get latest snapshots for a host       |
| GET    | `/api/snapshot/{host_id}/diff` | ✅             | Get diff between latest two snapshots |
| GET    | `/api/alerts`                  | ✅             | List current alert rules and history  |
| POST   | `/api/alerts`                  | ✅ (admin)     | Create a new alert rule               |
| GET    | `/api/hosts`                   | ✅             | List registered hosts                 |
| POST   | `/api/hosts/register`          | ✅             | Register a new host (auto or manual)  |

---

## 📤 Example: POST `/api/telemetry`

**Ingest system resource metrics**

### Request Headers:

```http
Authorization: Bearer <JWT>
Content-Type: application/json
```

### Request Body:

```json
{
  "host_id": "host-abc-123",
  "timestamp": "2025-07-19T16:03:00Z",
  "cpu": 42.3,
  "memory": 71.0,
  "disk": 80.5,
  "uptime": 14400
}
```

### Response:

```json
{
  "status": "ok",
  "message": "Telemetry recorded"
}
```

---

## 📤 Example: POST `/api/snapshot`

**Upload a configuration snapshot**

### Request Body:

```json
{
  "host_id": "host-abc-123",
  "timestamp": "2025-07-19T16:03:00Z",
  "os_info": "Ubuntu 22.04",
  "kernel": "5.15.0-86-generic",
  "packages": ["psutil==5.9.0", "uvicorn==0.23.2"],
  "env_vars": {
    "APP_ENV": "prod",
    "DEBUG": "false"
  }
}
```

### Response:

```json
{
  "status": "ok",
  "message": "Snapshot stored"
}
```

---

## 📥 Example: GET `/api/metrics?host_id=host-abc-123&type=cpu&range=1h`

**Query recent metrics by host, type, and time range**

### Response:

```json
{
  "host_id": "host-abc-123",
  "metric": "cpu",
  "points": [
    ["2025-07-19T15:00:00Z", 40.1],
    ["2025-07-19T15:30:00Z", 44.9],
    ["2025-07-19T16:00:00Z", 42.3]
  ]
}
```

---

## 🧪 Example: GET `/api/snapshot/{host_id}/diff`

**Compare latest two snapshots and return the config diff**

### Response:

```json
{
  "added_packages": ["uvicorn==0.23.2"],
  "removed_packages": [],
  "changed_env_vars": {
    "DEBUG": {
      "from": "true",
      "to": "false"
    }
  }
}
```

---

## 🚨 Example: POST `/api/alerts`

**Create a new threshold-based alert**

```json
{
  "host_id": "host-abc-123",
  "metric": "cpu",
  "threshold": 90.0,
  "duration": "5m"
}
```

---

## 📋 Notes

* All timestamps should be in ISO 8601 format (`UTC`)
* For metrics, allowed types are: `cpu`, `memory`, `disk`, `uptime`
* Role enforcement:

  * Only `admin` can create/edit alert rules
  * All roles can view metrics and snapshots
* Rate limits can be added at agent level (e.g. 1 POST per 30s)