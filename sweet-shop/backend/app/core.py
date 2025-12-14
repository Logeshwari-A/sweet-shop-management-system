from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017/sweetshop"
    JWT_SECRET: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_SECRET: str = "admin-secret"

    class Config:
        env_file = ".env"

settings = Settings()
