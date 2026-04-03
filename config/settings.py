from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    kiwoom_app_key: str = Field(..., description="Kiwoom App Key")
    kiwoom_app_secret: str = Field(..., description="Kiwoom App Secret")
    kiwoom_account_no: str = Field(..., description="Kiwoom Account Number")
    telegram_bot_token: str = Field(..., description="Telegram Bot Token")
    telegram_chat_id: str = Field(..., description="Telegram Chat ID")
    live_trading_enabled: bool = Field(False, description="Enable Live Trading")
    
    # API endpoints
    kiwoom_api_host: str = "https://api.kiwoom.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
