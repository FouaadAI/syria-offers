import os
from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables from .env file (project root / backend folder)
load_dotenv()


class Settings:
    """إعدادات التطبيق المركزية، تُقرأ من متغيرات البيئة أو ملف .env"""

    # قاعدة البيانات
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://syriaoffers:strongpassword@127.0.0.1:5432/syriaoffers")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HTTP_PROXY: str = os.getenv("HTTP_PROXY", "")
    HTTPS_PROXY: str = os.getenv("HTTPS_PROXY", "")
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # الأمان
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production-to-a-very-long-random-string")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # إعدادات عامة
    APP_NAME: str = os.getenv("APP_NAME", "Syria Offers")
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "aa4863001@smtp-brevo.com")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "ferow30@gmail.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Offria")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp-relay.brevo.com")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True").lower() in ("true", "1", "yes")
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False").lower() in ("true", "1", "yes")


@lru_cache()
def get_settings() -> Settings:
    """دالة مساعدة لاستدعاء الإعدادات بشكل مُخزَّن مؤقتاً"""
    return Settings()


settings = get_settings()