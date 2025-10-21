import random
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.db.models.metric import Metric
from app.db.models.snapshot import Snapshot
from app.db.models.host import Host
from app.services.alert_rule import evaluate_rules_and_generate_alerts

# Settings
HOST_IDS = [5, 6, 7, 8]
SNAPSHOT_COUNT = 4
METRICS_PER_TYPE = 100
METRIC_NAMES = ['cpu_usage', 'memory_usage', 'disk_usage']
VALUE_RANGES = {
    'cpu_usage': (20, 95),
    'memory_usage': (10, 90),
    'disk_usage': (5, 85),
}

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
            # Ensure host exists
            host = db.query(Host).filter(Host.id == host_id).first()
            if not host:
                host = Host(id=host_id, hostname=f"host-{host_id}")
                hostname = f"host-{host_id}",
                ip_address = f"192.168.1.{host_id}",
                os = random.choice(["Ubuntu", "Debian", "CentOS"]),
                status = random.choice(["active", "inactive"])
                db.add(host)
                db.commit()

            # Generate aligned timestamps once per host
            aligned_times = generate_aligned_timestamps(base_date, METRICS_PER_TYPE)

            for _ in range(SNAPSHOT_COUNT):
                snapshot_time = base_date + timedelta(minutes=random.randint(0, 1439))
                snapshot = Snapshot(host_id=host_id, created_at=snapshot_time)
                db.add(snapshot)
                db.commit()  # Needed for snapshot.id

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

if __name__ == "__main__":
    seed_fresh_data()

    # Run rule evaluation after seeding
    db = SessionLocal()
    try:
        # Assuming you have snapshot IDs available
        snapshot_ids = [s.id for s in db.execute("SELECT id FROM snapshots").fetchall()]
        for sid in snapshot_ids:
            evaluate_rules_and_generate_alerts(db, sid)
        print("✅ Evaluated alert rules for all seeded snapshots.")
    finally:
        db.close()