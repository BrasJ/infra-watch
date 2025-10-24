from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.routers import host, metric, snapshot, alert, alert_rules, dashboard
from backend.app.api import snapshot, alerts, auth

app = FastAPI(
    title="Infra-Watch API",
    version="0.1.0",
    description="Backend API for collection and serving infrastructure telemetry data."
)

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