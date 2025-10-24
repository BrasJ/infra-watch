import os
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    frontend_url: str
    agent_auth_token: str
    alert_eval_interval: int
    SECRET_KEY: str = "your-secret-key"

    model_config = ConfigDict(env_file=".env")

settings = Settings()