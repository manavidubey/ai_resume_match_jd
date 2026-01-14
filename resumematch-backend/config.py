import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL", 
        "postgresql://username:password@localhost:5432/resumematch"
    )
    
    # Vector Database
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    
    # AI Services
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # File Uploads
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {"pdf", "docx", "doc"}
    
    # Embedding Model
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", 
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Similarity Threshold
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
    
    # Scoring weights
    SKILLS_WEIGHT = float(os.getenv("SKILLS_WEIGHT", "0.4"))
    EXPERIENCE_WEIGHT = float(os.getenv("EXPERIENCE_WEIGHT", "0.3"))
    ROLE_FIT_WEIGHT = float(os.getenv("ROLE_FIT_WEIGHT", "0.2"))
    BONUS_SIGNALS_WEIGHT = float(os.getenv("BONUS_SIGNALS_WEIGHT", "0.1"))
    
    # Debug
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

config = Config()
