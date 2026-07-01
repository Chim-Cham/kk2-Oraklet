from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    url = os.getenv("URL")
    api_key = os.getenv("API_KEY")

settings = Settings()