from fastapi import FastAPI
import asyncio
import logging
from alembic import command
from alembic.config import Config
from fastapi.middleware.cors import CORSMiddleware
import sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

try:
    # ✅ Local (run from project root)
    from app.db.session import engine
    from app.core.config import settings
    from app.routers import host, metric, snapshot, alert, alert_rules, dashboard
    from app.api import snapshot as api_snapshot, alerts, auth
    from app.seed_metrics import seed_if_needed
except ModuleNotFoundError:
    # ✅ Render (root directory is /backend)
    from backend.app.db.session import engine
    from backend.app.core.config import settings
    from backend.app.routers import host, metric, snapshot, alert, alert_rules, dashboard
    from backend.app.api import snapshot as api_snapshot, alerts, auth
    from backend.app.seed_metrics import seed_if_needed

app = FastAPI(
    title="Infra-Watch API",
    version="0.1.0",
    description="Backend API for collection and serving infrastructure telemetry data."
)

@app.on_event("startup")
async def on_startup():
    """Runs automatically on container startup (Render + local)."""
    logging.basicConfig(level=logging.INFO)
    logging.info("🚀 Starting Infra-Watch backend...")

    try:
        logging.info("🔧 Applying Alembic migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logging.info("✅ Database schema up to date.")
    except Exception as e:
        logging.error(f"❌ Error running Alembic migrations: {e}")

    try:
        logging.info("🌱 Checking seed state...")
        await asyncio.to_thread(seed_if_needed)
        logging.info("✅ Seeding check complete.")
    except Exception as e:
        logging.error(f"❌ Error seeding database: {e}")

    logging.info("✅ Startup sequence complete. Server ready.")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(host.router)
app.include_router(metric.router)
app.include_router(snapshot.router)
app.include_router(alert.router)
app.include_router(alert_rules.router)
app.include_router(dashboard.router)
app.include_router(auth.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/health")
def health():
    return {"status": "ok"}