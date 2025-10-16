import random
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.db.models.metric import Metric

# Configuration
HOST_ID = 5
SNAPSHOT_IDS = [1, 2, 3, 4]
METRIC_NAMES = ['cpu_usage', 'memory_usage', 'disk_usage']
BASE_TIME = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

# Utility to generate a random metric value
def generate_value(metric_name):
    if metric_name == 'cpu_usage':
        return round(random.uniform(30, 95), 2)
    elif metric_name == 'memory_usage':
        return round(random.uniform(20, 90), 2)
    elif metric_name == 'disk_usage':
        return round(random.uniform(10, 80), 2)
    return 0.0

def seed_metrics():
    db = SessionLocal()

    try:
        # Each snapshot will get 24 metric entries spaced by 1 hour
        for snapshot_id in SNAPSHOT_IDS:
            for hour_offset in range(0, 24):
                timestamp = BASE_TIME + timedelta(hours=hour_offset)

                for metric_name in METRIC_NAMES:
                    metric = Metric(
                        name=metric_name,
                        value=generate_value(metric_name),
                        snapshot_id=snapshot_id,
                        host_id=HOST_ID,
                        created_at=timestamp
                    )
                    db.add(metric)

        db.commit()
        print("✅ Seeded 24 metrics per snapshot:", SNAPSHOT_IDS)

    except Exception as e:
        db.rollback()
        print("❌ Error seeding metrics:", e)

    finally:
        db.close()

if __name__ == "__main__":
    seed_metrics()
