import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration"""

    # Binance API Configuration
    API_KEY: str = os.getenv('apiKey', '')
    SECRET_KEY: str = os.getenv('secretKey', '')
    BASE_URL: str = 'https://api.binance.com'

    # Server Configuration
    APP_NAME: str = "Binance P2P Orders API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'

    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        # Add your frontend URLs here
    ]

    # Cache Configuration
    CACHE_TTL: int = int(os.getenv('CACHE_TTL', '300'))  # 5 minutes default

    # API Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60'))

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        if not cls.API_KEY or not cls.SECRET_KEY:
            raise ValueError("API_KEY and SECRET_KEY must be set in .env file")
        return True


# Create global settings instance
settings = Settings()
