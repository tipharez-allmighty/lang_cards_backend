from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLMs
    GEMINI_API_KEY: str

    # Cloud Translation
    GOOGLE_APPLICATION_CREDENTIALS: str

    # Models
    GOOGLE_TEXT_LITE: str
    GOOGLE_IMAGE: str

    # SUPABASE
    SUPABASE_KEY: str
    SUPABASE_URL: str

    # Images
    IMAGE_BUCKET: str
    IMAGE_FOLDER: str

    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    model_config = ConfigDict(env_file=".env")


settings = Settings()
