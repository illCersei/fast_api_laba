from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_SECONDS : int
    REFRESH_TOKEN_EXPIRE_SECONDS : int

    class Config:
        env_file = ".env"

settings = Settings()
