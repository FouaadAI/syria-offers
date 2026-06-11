from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.database import engine, Base, SessionLocal
from app.core.config import settings
from app.models.user import User
from app.api.v1 import categories, offers, bookings
from app.api.v1 import recommendations
from app.api.v1 import flash_deals
from app.api.v1 import chatbot
from app.api.v1 import admin
from app.api.v1 import auth
from app.api.v1 import uploads
from app.api.v1 import payments
from app.api.v1 import merchant
from app.api.v1 import travel_planner

# --------------- Rate Limiting ---------------
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def apply_rate_limiting(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)


# --------------- Cache Middleware ---------------
class ForceNoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.method == "GET":
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response


# --------------- Gastbenutzer (ohne feste ID!) ---------------
def create_default_user():
    """Erstellt einen Gastbenutzer, falls noch keiner existiert (ID automatisch)."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.phone == "0000000000").first()
        if not user:
            default_user = User(
                phone="0000000000",
                full_name="زائر",
                hashed_password="not_set",
                is_active=True,
            )
            db.add(default_user)
            db.commit()
            print("[OK] Gastbenutzer angelegt")
        else:
            print("[INFO] Gastbenutzer existiert bereits")
    finally:
        db.close()


# --------------- Tabellen anlegen ---------------
Base.metadata.create_all(bind=engine)

# Gastbenutzer anlegen (nur im Entwicklungsmodus)
if settings.DEBUG:
    create_default_user()


# ========== FastAPI-App erstellen ==========
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="تطبيق العروض والحجوزات - سوريا",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --------------- Middleware ---------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ForceNoCacheMiddleware)
apply_rate_limiting(app)

# --------------- Router ---------------
app.include_router(categories.router, prefix=settings.API_V1_PREFIX)
app.include_router(offers.router, prefix=settings.API_V1_PREFIX)
app.include_router(bookings.router, prefix=settings.API_V1_PREFIX)
app.include_router(recommendations.router, prefix=settings.API_V1_PREFIX)
app.include_router(flash_deals.router, prefix=settings.API_V1_PREFIX)
app.include_router(chatbot.router, prefix=settings.API_V1_PREFIX)
app.include_router(admin.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(uploads.router, prefix=settings.API_V1_PREFIX)
app.include_router(payments.router, prefix=settings.API_V1_PREFIX)
app.include_router(merchant.router, prefix=settings.API_V1_PREFIX)
app.include_router(travel_planner.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}