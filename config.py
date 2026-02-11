import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    REDIS_URL = os.getenv("REDIS_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set")
    if not all([AWS_ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY]):
        raise ValueError("Invalid backblaze variable")
