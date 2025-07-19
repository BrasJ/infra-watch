from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="Infra-Watch API",
    version="0.1.0",
    description="Backend API for collection and serving infrastructure telemetry data."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["settings.frontend_url"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}