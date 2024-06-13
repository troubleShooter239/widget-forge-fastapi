from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseModel):
    algorithm: str
    expire_minutes: int
    secret_key: str


class Settings(BaseSettings):
    db_connection_string: str
    jwt: JwtSettings

    model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='.')

settings = Settings()