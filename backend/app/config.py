"""
Configuration Management
Environment-based settings with validation
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "CryptoTradeAI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = DEBUG
    
    # API Configuration
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list = ["*"]
    
    # Binance API
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
    BINANCE_TESTNET_ENABLED: bool = os.getenv("BINANCE_TESTNET", "true").lower() == "true"
    BINANCE_REST_API: str = "https://testnet.binance.vision"
    BINANCE_WS_URL: str = "wss://stream.binance.com:9443/ws"
    
    # OpenAI API
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    OPENAI_MODEL: str = "gpt-4"
    USE_AI_ANALYSIS: bool = os.getenv("USE_AI_ANALYSIS", "false").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    DB_ECHO: bool = DEBUG
    
    # Firebase (optional)
    FIREBASE_PROJECT_ID: Optional[str] = os.getenv("FIREBASE_PROJECT_ID", None)
    FIREBASE_PRIVATE_KEY: Optional[str] = os.getenv("FIREBASE_PRIVATE_KEY", None)
    FIREBASE_CLIENT_EMAIL: Optional[str] = os.getenv("FIREBASE_CLIENT_EMAIL", None)
    
    # Trading Parameters
    DEFAULT_LEVERAGE: float = 1.0
    MAX_LEVERAGE: float = 10.0
    MAX_DAILY_LOSS_PERCENT: float = 5.0  # 5% of balance
    MAX_OPEN_POSITIONS: int = 5
    MAX_TRADES_PER_HOUR: int = 10
    DEFAULT_TRADING_MODE: str = "manual"  # manual, semi_auto, auto
    
    # Risk Management
    MIN_RISK_REWARD_RATIO: float = 1.0
    MAX_SINGLE_TRADE_RISK_PERCENT: float = 2.0
    STOP_LOSS_DISTANCE_PERCENT: float = 2.0
    LEVERAGE_WARNING_THRESHOLD: float = 5.0
    
    # Market Data
    CANDLE_HISTORY_LIMIT: int = 500
    ORDER_BOOK_DEPTH: int = 20
    PRICE_UPDATE_INTERVAL_SECONDS: int = 1
    
    # Alerts & Notifications
    ENABLE_TELEGRAM_ALERTS: bool = os.getenv("ENABLE_TELEGRAM", "false").lower() == "true"
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN", None)
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID", None)
    ENABLE_DESKTOP_ALERTS: bool = True
    ENABLE_EMAIL_ALERTS: bool = False
    SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER", None)
    SMTP_PORT: int = 587
    
    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Feature Flags
    ENABLE_BACKTESTING: bool = True
    ENABLE_PAPER_TRADING: bool = True
    ENABLE_LIVE_TRADING: bool = os.getenv("ENABLE_LIVE_TRADING", "false").lower() == "true"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Dependency for FastAPI endpoints"""
    return settings
