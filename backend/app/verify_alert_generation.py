from app.db.session import SessionLocal
from sqlalchemy import text

def verify_alerts():
    db = SessionLocal()
    try:
        print("🔍 Verifying alert generation...")
        metrics_count = db.execute(text("SELECT COUNT(*) FROM metrics")).scalar()
        snapshots_count = db.execute(text("SELECT COUNT(*) FROM snapshots")).scalar()
        rules_count = db.execute(text("SELECT COUNT(*) FROM alert_rules")).scalar()
        alerts_count = db.execute(text("SELECT COUNT(*) FROM alerts")).scalar()

        print(f"📊 Metrics: {metrics_count}")
        print(f"🗂️ Snapshots: {snapshots_count}")
        print(f"⚙️ Alert Rules: {rules_count}")
        print(f"🚨 Alerts Generated: {alerts_count}")

        if alerts_count > 0:
            print("✅ Alert generation verified successfully!")
        else:
            print("⚠️ No alerts found — check thresholds and metric ranges.")
    except Exception as e:
        print("❌ Verification failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    verify_alerts()
