from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    api_key: str = "your-secret-api-key-here"
    max_file_size_mb: int = 25
    video_quality: str = "worst"  # Optimized for AI analysis
    proxy_url: str | None = None  # Optional proxy URL
    po_token: str | None = None  # YouTube Proof of Origin token
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
