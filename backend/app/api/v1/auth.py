import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.services.mail_service import send_verification_email, send_password_reset_email
from pydantic import BaseModel
import random
from datetime import datetime, timedelta
from jose import jwt

router = APIRouter(prefix="/auth", tags=["المصادقة"])

# ---------- Schemas ----------
class RegisterRequest(BaseModel):
    phone: str
    email: str
    full_name: str
    role: str = "customer"

class VerifyRequest(BaseModel):
    email: str
    code: str

class SetPasswordRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str

class PhoneLoginRequest(BaseModel):
    phone: str

# ---------- Hilfsfunktion ----------
def create_access_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ---------- Telefon-Login (alt) ----------
@router.post("/login")
async def phone_login(request: PhoneLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(status_code=401, detail="رقم الهاتف غير مسجل")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="الحساب غير مفعل")
    token = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
    }

# ---------- Registrierung ----------
@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.phone == request.phone) | (User.email == request.email)
    ).first()

    if existing_user:
        code = str(random.randint(100000, 999999))
        existing_user.verification_code = code
        db.commit()
        await send_verification_email(request.email, code)
        return {"message": "رقم الهاتف أو البريد الإلكتروني مسجل مسبقاً. تم إرسال رمز تحقق جديد."}

    code = str(random.randint(100000, 999999))
    user = User(
        phone=request.phone,
        email=request.email,
        full_name=request.full_name,
        role=request.role,
        is_active=False,
        verification_code=code,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    await send_verification_email(request.email, code)
    return {"message": "تم التسجيل بنجاح. يرجى التحقق من بريدك الإلكتروني."}

# ---------- Verifizierung ----------
@router.post("/verify")
async def verify(request: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    if user.verification_code != request.code:
        raise HTTPException(status_code=400, detail="رمز التحقق غير صحيح")

    user.is_active = True
    user.verification_code = None
    db.commit()
    return {"message": "تم تفعيل الحساب بنجاح"}

# ---------- Passwort setzen ----------
@router.post("/set-password")
async def set_password(request: SetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="الحساب غير مفعل بعد")

    # استخدام bcrypt الأصلي
    hashed = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.hashed_password = hashed
    db.commit()
    return {"message": "تم تعيين كلمة المرور بنجاح"}

# ---------- E-Mail-Login ----------
@router.post("/email-login")
async def email_login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not user.is_active or not user.hashed_password:
        raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")
    if not bcrypt.checkpw(request.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="بيانات الدخول غير صحيحة")
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer", "role": user.role}

# ---------- Passwort vergessen ----------
@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        return {"message": "إذا كان البريد الإلكتروني مسجلاً، تم إرسال رمز إعادة تعيين كلمة المرور."}

    code = str(random.randint(100000, 999999))
    user.verification_code = code
    db.commit()
    await send_password_reset_email(request.email, code)
    return {"message": "إذا كان البريد الإلكتروني مسجلاً، تم إرسال رمز إعادة تعيين كلمة المرور."}

# ---------- Passwort zurücksetzen ----------
@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    if user.verification_code != request.code:
        raise HTTPException(status_code=400, detail="رمز التحقق غير صحيح")

    hashed = bcrypt.hashpw(request.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.hashed_password = hashed
    user.verification_code = None
    db.commit()
    return {"message": "تم تعيين كلمة المرور الجديدة بنجاح"}