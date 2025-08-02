from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    ## Env variables goes here
    
    model_config = ConfigDict(env_file=".env")


settings = Settings()