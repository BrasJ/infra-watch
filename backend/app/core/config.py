from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    frontend_url: str
    agent_auth_token: str
    alert_eval_interval: int

    class Config:
        env_file = ".env"

settings = Settings()