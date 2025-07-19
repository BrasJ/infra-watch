# 🤖 Agent Specification

## 📌 Project: Infra-Watch

**Component:** Telemetry Agent

---

## 🎯 Purpose

The Infra-Watch Agent is a lightweight Python service that runs on a host system (physical or virtual machine) and periodically collects telemetry data and system configuration snapshots. It then securely sends this data to the Infra-Watch backend via authenticated HTTP requests.

This agent simulates a real-world VM-side process and is designed to run on:

* Linux servers (e.g., Ubuntu, CentOS)
* Containers
* Optional: Windows (with minor adaptations)

---

## 📥 Data Collected

### Telemetry Payload (sent every interval):

* `host_id`: Unique identifier for the host
* `timestamp`: UTC timestamp of collection
* `cpu`: CPU usage percentage (float)
* `memory`: Memory usage percentage (float)
* `disk`: Disk usage percentage (float)
* `uptime`: System uptime in seconds (int)

### Optional Config Snapshot:

* `os_info`: OS name and version
* `kernel`: Kernel version
* `packages`: List of installed Python packages with versions
* `env_vars`: Selected environment variables

---

## 🔁 Communication

* Method: HTTP POST
* Format: JSON
* Headers:

  * `Authorization: Bearer <JWT>`
  * `Content-Type: application/json`

| Endpoint              | Purpose                                       |
| --------------------- | --------------------------------------------- |
| `POST /api/telemetry` | Submit metrics                                |
| `POST /api/snapshot`  | Submit system snapshot (optional or periodic) |

---

## ⚙️ Configuration

The agent is configured via a simple `config.yaml` file:

```yaml
api_url: "http://localhost:8000/api"
auth_token: "your-jwt-token"
host_id: "host-abc-123"
interval_seconds: 60
snapshot_interval: 3600  # optional
collect_snapshot: true
env_whitelist:
  - "APP_ENV"
  - "DEBUG"
```

---

## 📋 Example Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Run manually
python telemetry_agent.py

# Run on a schedule (e.g., cron or systemd)
* * * * * /usr/bin/python3 /path/to/telemetry_agent.py
```

---

## 🧪 Agent Behavior

### At startup:

1. Load `config.yaml`
2. Validate required fields

### Every N seconds:

1. Collect telemetry via `psutil`
2. POST metrics to `/api/telemetry`
3. If time since last snapshot > `snapshot_interval`, collect and POST snapshot
4. Log success/failure locally to console or file

---

## 📂 File Structure

```
agent/
├── telemetry_agent.py       # Main agent script
├── config.yaml              # Agent configuration
├── requirements.txt         # Dependencies
└── utils/
    ├── metrics.py           # Metric collection logic
    ├── snapshot.py          # Snapshot/diff logic
    └── http.py              # API request helpers
```

---

## 🛡️ Security Considerations

* JWT is read from config (can be fetched dynamically in future)
* Agent should **not** log sensitive data (e.g., env values)
* You can restrict API token to specific hosts/IPs on backend

---

## 📌 Future Enhancements (Post-MVP)

* Auto-register host with `/api/hosts/register`
* Pull config remotely from backend instead of local YAML
* Add retry queue for failed submissions (with exponential backoff)
* Windows support (currently Linux/Unix-focused)
* Package into standalone binary (e.g., PyInstaller)