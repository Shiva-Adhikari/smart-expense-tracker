from pydantic import SecretStr, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # === Database ===
    DATABASE_URL = SecretStr
    DEBUG = SecretStr
    
    # Class Config:
    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        extra = 'forbid')


settings = Settings()
