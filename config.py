from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    api_token: SecretStr
    db_url: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
