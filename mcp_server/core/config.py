import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
