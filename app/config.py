from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "SmartFactory Monitor"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./smartfactory.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    API_KEY: str = "change-me-in-production"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Telegram
    TELEGRAM_BOT_TOKEN: str = "8515000886:AAHcB6MJN8bnlxUfp3axYP2cprgzuCnfXzo"
    TELEGRAM_CHAT_ID: str = "597253503"

    # Anomaly detection thresholds
    TEMPERATURE_MAX: float = 85.0
    PRESSURE_MAX: float = 10.0
    VIBRATION_MAX: float = 5.0


settings = Settings()
