from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseModel):
    algorithm: str = ''
    expire_minutes: int = 0
    secret_key: str = ''


class Settings(BaseSettings):
    db_connection_string: str = ''
    jwt: JwtSettings = JwtSettings()

    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='.')

settings = Settings()
