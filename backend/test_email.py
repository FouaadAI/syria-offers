import asyncio
from app.services.mail_service import send_verification_email

async def main():
    try:
        await send_verification_email("werofofo@gmail.com", "123456")
        print("✅ تم الإرسال بنجاح")
    except Exception as e:
        print(f"❌ فشل: {e}")

asyncio.run(main())