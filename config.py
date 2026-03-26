import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls", "json"}
    DATABASE_URL = "sqlite:///database/analysis.db"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")