from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Core Service"
    api_version: str = "v1"
    websocket_url: str = "/ws"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()