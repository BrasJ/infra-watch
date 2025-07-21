from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import host, metric, snapshot, alert

app = FastAPI(
    title="Infra-Watch API",
    version="0.1.0",
    description="Backend API for collection and serving infrastructure telemetry data."
)

app.include_router(host.router)
app.include_router(metric.router)
app.include_router(snapshot.router)
app.include_router(alert.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}