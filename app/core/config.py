from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "OpenNotebookLM++"
    API_VERSION: str = "v1"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
