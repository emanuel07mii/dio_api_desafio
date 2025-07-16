from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()
url = defult=os.getenv("DATABASE_URL")
class Settings(BaseSettings):
    DB_URL: str = Field(url)

settings = Settings()
