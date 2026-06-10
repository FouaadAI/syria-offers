import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

async def send_verification_email(email: str, code: str):
    message = MIMEMultipart("alternative")
    message["From"] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
    message["To"] = email
    message["Subject"] = "رمز التحقق - Offria"

    html = f"""
    <div style="font-family: Cairo, sans-serif; text-align: right; direction: rtl;">
        <h2>مرحباً بك في Offria!</h2>
        <p>رمز التحقق الخاص بك هو:</p>
        <h1 style="color: #003580;">{code}</h1>
        <p>يرجى إدخال هذا الرمز في التطبيق لتأكيد حسابك.</p>
    </div>
    """
    message.attach(MIMEText(html, "html", "utf-8"))

    await aiosmtplib.send(
        message,
        hostname=settings.MAIL_SERVER,
        port=settings.MAIL_PORT,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD,
        start_tls=True,
    )
async def send_password_reset_email(email: str, code: str):
    html = f"""
    <div style="font-family: Cairo, sans-serif; text-align: right; direction: rtl;">
        <h2>إعادة تعيين كلمة المرور</h2>
        <p>رمز إعادة تعيين كلمة المرور الخاص بك هو:</p>
        <h1 style="color: #003580;">{code}</h1>
        <p>يرجى إدخال هذا الرمز في التطبيق لتعيين كلمة مرور جديدة.</p>
    </div>
    """
    message = MIMEMultipart("alternative")
    message["From"] = f"{settings.MAIL_FROM_NAME} <{settings.MAIL_FROM}>"
    message["To"] = email
    message["Subject"] = "إعادة تعيين كلمة المرور - Offria"
    message.attach(MIMEText(html, "html", "utf-8"))

    await aiosmtplib.send(
        message,
        hostname=settings.MAIL_SERVER,
        port=settings.MAIL_PORT,
        username=settings.MAIL_USERNAME,
        password=settings.MAIL_PASSWORD,
        start_tls=True,
    )    