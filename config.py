from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']
    LOG_LEVEL: Literal['DEBUG', 'INFO']

    DB_PORT: int
    DB_NAME: str
    DB_HOST: str
    DB_PASS: str
    DB_USER: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_HOST: str
    TEST_DB_PASS: str
    TEST_DB_USER: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    ALGORITHM: str
    RANDOM_KEY: str

    BROKER: str
    CELERY: str
    CELERY_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    EMAIL: str
    GM_PASS: str

    @property
    def CELERY_URL(self):
        return f'{self.BROKER}://{self.CELERY}:{self.CELERY_PORT}'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
