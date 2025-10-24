import os
import time
import random
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from backend.app.db.session import SessionLocal
from backend.app.db.models.metric import Metric
from backend.app.db.models.snapshot import Snapshot
from backend.app.db.models.host import Host
from backend.app.db.models.alert_rule import AlertRule
from backend.app.services.alert_rule import evaluate_rules_and_generate_alerts
from backend.app.schemas.alert import AlertSeverity

HOST_IDS = [5, 6, 7, 8]
SNAPSHOT_COUNT = 4
METRICS_PER_TYPE = 100
METRIC_NAMES = ['cpu_usage', 'memory_usage', 'disk_usage']
VALUE_RANGES = {
    'cpu_usage': (20, 95),
    'memory_usage': (10, 90),
    'disk_usage': (5, 85),
}


# ✅ 1. Wait for DB to be ready (critical for Docker safety)
def wait_for_db(max_retries=10, delay=3):
    print("⏳ Waiting for database connection...")
    for i in range(max_retries):
        try:
            db = SessionLocal()
            db.execute(text("SELECT 1"))
            db.close()
            print("✅ Database is ready.")
            return
        except OperationalError as e:
            print(f"Attempt {i+1}/{max_retries}: Database not ready ({e})")
            time.sleep(delay)
    raise RuntimeError("❌ Database not reachable after multiple attempts.")


def generate_aligned_timestamps(base_day: datetime, count: int) -> list[datetime]:
    return sorted([
        base_day + timedelta(minutes=random.randint(0, 1439))
        for _ in range(count)
    ])


def generate_value(metric_name: str) -> float:
    low, high = VALUE_RANGES.get(metric_name, (0, 100))
    return round(random.uniform(low, high), 2)


def seed_fresh_data():
    db = SessionLocal()
    base_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        for host_id in HOST_IDS:
            print(f"🔧 Seeding Host {host_id}...")
            host = db.query(Host).filter(Host.id == host_id).first()
            if not host:
                host = Host(
                    id=host_id,
                    hostname=f"host-{host_id}",
                    ip_address=f"192.168.1.{host_id}",
                    os=random.choice(["Ubuntu", "Debian", "CentOS"]),
                    status=random.choice(["active", "inactive"])
                )
                db.add(host)
                db.commit()

            aligned_times = generate_aligned_timestamps(base_date, METRICS_PER_TYPE)

            for _ in range(SNAPSHOT_COUNT):
                snapshot_time = base_date + timedelta(minutes=random.randint(0, 1439))
                snapshot = Snapshot(host_id=host_id, created_at=snapshot_time)
                db.add(snapshot)
                db.commit()

                rows = []
                for ts in aligned_times:
                    for name in METRIC_NAMES:
                        metric = Metric(
                            name=name,
                            value=generate_value(name),
                            snapshot_id=snapshot.id,
                            host_id=host_id,
                            created_at=ts
                        )
                        rows.append(metric)

                db.bulk_save_objects(rows)
                db.commit()
                print(f"✅ Snapshot {snapshot.id} for Host {host_id}")

        print("🎉 Seeding complete.")

    except Exception as e:
        db.rollback()
        print("❌ Error during seeding:", e)

    finally:
        db.close()


def seed_alert_rules():
    db = SessionLocal()
    rules = [
        AlertRule(
            host_id=None,
            metric_name="cpu_usage",
            operator=">",
            threshold=80.0,
            severity=AlertSeverity.critical,
            message="High CPU usage detected",
            enabled=True
        ),
        AlertRule(
            host_id=None,
            metric_name="memory_usage",
            operator=">",
            threshold=75.0,
            severity=AlertSeverity.warning,
            message="Elevated memory usage",
            enabled=True
        ),
        AlertRule(
            host_id=None,
            metric_name="disk_usage",
            operator=">",
            threshold=85.0,
            severity=AlertSeverity.critical,
            message="Disk usage critically high",
            enabled=True
        ),
        AlertRule(
            host_id=None,
            metric_name="cpu_usage",
            operator="<",
            threshold=10.0,
            severity=AlertSeverity.info,
            message="CPU usage abnormally low",
            enabled=True
        ),
    ]

    try:
        db.bulk_save_objects(rules)
        db.commit()
        print("✅ Default alert rules seeded.")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding alert rules:", e)
    finally:
        db.close()


if __name__ == "__main__":
    # Ensure DB is ready before seeding
    wait_for_db()

    seed_fresh_data()
    seed_alert_rules()

    db = SessionLocal()
    try:
        snapshot_ids = [row[0] for row in db.execute(text("SELECT id FROM snapshots")).fetchall()]
        for sid in snapshot_ids:
            evaluate_rules_and_generate_alerts(db, sid)
        print("✅ Evaluated alert rules for all seeded snapshots.")
    finally:
        db.close()
