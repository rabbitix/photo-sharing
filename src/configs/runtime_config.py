from pydantic_settings import BaseSettings


class RuntimeConfig(BaseSettings):
    BOT_TOKEN: str
    CHANNEL_ID: str
    SERVE_PORT: int = 8086
    SERVE_HOST: str = "0.0.0.0"
