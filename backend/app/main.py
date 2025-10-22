from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import host, metric, snapshot, alert, alert_rules
from app.api import snapshot, alerts, auth

app = FastAPI(
    title="Infra-Watch API",
    version="0.1.0",
    description="Backend API for collection and serving infrastructure telemetry data."
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",  # <- Add this!
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
app.include_router(auth.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}