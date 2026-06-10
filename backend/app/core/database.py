from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# إنشاء محرك قاعدة البيانات مع إعدادات اتصال متقدمة
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # للتحقق من صلاحية الاتصال قبل الاستخدام
    echo=settings.DEBUG,  # طباعة استعلامات SQL عند التطوير
)

# مصنع الجلسات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# الأساس الذي ترث منه جميع النماذج
Base = declarative_base()


def get_db():
    """
    تابع تابع يُستخدم كحقنة تبعية (Dependency Injection) في المسارات.
    يُنشئ جلسة قاعدة بيانات جديدة لكل طلب، ويُغلقها بعد انتهاء المعالجة.
    """
    db = SessionLocal()
    db.expire_on_commit = False
    try:
        yield db
    finally:
        db.close()