import io
import os
import uuid

import magic
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image

router = APIRouter(prefix="/uploads", tags=["الرفع"])

UPLOAD_DIR = "uploads/offers"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}
MIME_TO_EXTENSION = {"image/jpeg": ".jpg", "image/png": ".png"}
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/images")
async def upload_images(files: list[UploadFile] = File(...)):
    uploaded = []

    for file in files:
        content = await file.read()

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds 5 MB limit")

        detected_mime = magic.from_buffer(content, mime=True)
        if detected_mime not in ALLOWED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file type")

        ext = MIME_TO_EXTENSION[detected_mime]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        image = Image.open(io.BytesIO(content))
        if detected_mime == "image/jpeg":
            image = image.convert("RGB")
            image.save(filepath, format="JPEG")
        else:
            image.save(filepath, format="PNG")

        uploaded.append(f"/uploads/offers/{filename}")

    return JSONResponse({"images": uploaded})
