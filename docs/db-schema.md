# 🗃️ Database Schema

## 📌 Project: Infra-Watch

**Backend:** PostgreSQL + TimescaleDB (for time-series optimization)

---

## 🧱 Overview

The Infra-Watch system uses a relational database with time-series capabilities (via [TimescaleDB](https://www.timescale.com/)) to store metrics, snapshots, alerts, and user/account metadata.

All timestamps are stored in UTC ISO 8601 format. Metrics are indexed by time and `host_id`.

---

## 📋 Core Tables

### 📊 `metrics`

Stores time-series telemetry data from the agent.

| Field       | Type        | Notes                     |
| ----------- | ----------- | ------------------------- |
| `id`        | UUID        | Primary key               |
| `host_id`   | TEXT        | Foreign key to `hosts.id` |
| `timestamp` | TIMESTAMPTZ | Time of measurement       |
| `cpu`       | FLOAT       | CPU usage (%)             |
| `memory`    | FLOAT       | Memory usage (%)          |
| `disk`      | FLOAT       | Disk usage (%)            |
| `uptime`    | INTEGER     | System uptime (seconds)   |

🔹 **TimescaleDB hypertable partitioned on `timestamp`**

---

### 🧠 `snapshots`

Stores periodic configuration snapshots for drift detection.

| Field       | Type        | Notes                        |
| ----------- | ----------- | ---------------------------- |
| `id`        | UUID        | Primary key                  |
| `host_id`   | TEXT        | Foreign key to `hosts.id`    |
| `timestamp` | TIMESTAMPTZ | Time of snapshot             |
| `os_info`   | TEXT        | OS name + version            |
| `kernel`    | TEXT        | Kernel version               |
| `packages`  | JSONB       | Python packages + versions   |
| `env_vars`  | JSONB       | Whitelisted environment vars |

Snapshots are diffed against the most recent prior snapshot per host.

---

### 🚨 `alerts`

Defines and logs threshold-based alerts.

| Field            | Type        | Notes                             |
| ---------------- | ----------- | --------------------------------- |
| `id`             | UUID        | Primary key                       |
| `host_id`        | TEXT        | Foreign key to `hosts.id`         |
| `metric`         | TEXT        | One of: `"cpu"`, `"memory"`, etc  |
| `threshold`      | FLOAT       | Trigger threshold value           |
| `duration`       | INTERVAL    | Required exceedance duration      |
| `created_at`     | TIMESTAMPTZ | Rule creation time                |
| `last_triggered` | TIMESTAMPTZ | When last alert was fired         |
| `log`            | JSONB       | Optional: historical alert events |

---

### 🖥️ `hosts`

Tracks all registered VMs or containers.

| Field        | Type        | Notes                          |
| ------------ | ----------- | ------------------------------ |
| `id`         | TEXT        | Primary key (e.g., `host-abc`) |
| `name`       | TEXT        | Human-readable label           |
| `registered` | TIMESTAMPTZ | Time of registration           |
| `tags`       | JSONB       | Optional metadata (e.g. `env`) |
| `last_seen`  | TIMESTAMPTZ | Time of last telemetry ping    |

---

### 👤 `users`

Stores authenticated users and their roles.

| Field        | Type        | Notes                         |
| ------------ | ----------- | ----------------------------- |
| `id`         | UUID        | Primary key                   |
| `email`      | TEXT        | Unique user email             |
| `password`   | TEXT        | Hashed via bcrypt             |
| `role`       | TEXT        | `admin`, `operator`, `viewer` |
| `created_at` | TIMESTAMPTZ | Signup time                   |

---

## 🔑 Relationships

```plaintext
users     1 ── N  alerts
hosts     1 ── N  metrics
hosts     1 ── N  snapshots
hosts     1 ── N  alerts
```

---

## 📈 Indexing Plan

| Table       | Field(s)                 | Purpose                      |
| ----------- | ------------------------ | ---------------------------- |
| `metrics`   | (`host_id`, `timestamp`) | Time-series queries by host  |
| `snapshots` | `host_id`, `timestamp`   | Retrieve recent config diffs |
| `alerts`    | `host_id`, `metric`      | Fast rule evaluation         |
| `hosts`     | `last_seen`              | Host activity tracking       |
| `users`     | `email` (unique)         | Login auth                   |

---

## 🧪 Retention Policy (Optional)

* **Telemetry metrics** older than 30 days may be archived or deleted.
* Snapshots and alert logs are retained for audit purposes unless explicitly deleted.