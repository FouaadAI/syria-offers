import io
import re
from pathlib import Path

from PIL import Image

from app.api.v1 import uploads as uploads_api


def _jpeg_bytes(with_exif=False):
    image = Image.new("RGB", (32, 32), color="red")
    buffer = io.BytesIO()
    if with_exif:
        exif = Image.Exif()
        exif[271] = "CameraBrand"
        exif[272] = "CameraModel"
        image.save(buffer, format="JPEG", exif=exif)
    else:
        image.save(buffer, format="JPEG")
    return buffer.getvalue()


def test_upload_rejects_invalid_magic_bytes(client):
    files = {"files": ("fake.jpg", b"not an image", "image/jpeg")}
    response = client.post("/api/v1/uploads/images", files=files)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"


def test_upload_rejects_files_over_5mb(client):
    large_content = b"a" * (5 * 1024 * 1024 + 1)
    files = {"files": ("too_big.jpg", large_content, "image/jpeg")}
    response = client.post("/api/v1/uploads/images", files=files)
    assert response.status_code == 413
    assert response.json()["detail"] == "File size exceeds 5 MB limit"


def test_upload_uses_uuid_filename(client, tmp_path, monkeypatch):
    upload_dir = tmp_path / "offers"
    upload_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(uploads_api, "UPLOAD_DIR", str(upload_dir))

    files = {"files": ("../../traversal.jpg", _jpeg_bytes(), "image/jpeg")}
    response = client.post("/api/v1/uploads/images", files=files)
    assert response.status_code == 200
    image_path = response.json()["images"][0]

    basename = Path(image_path).name
    assert basename != "traversal.jpg"
    assert re.match(r"^[0-9a-fA-F-]{36}\.jpg$", basename)
    assert (upload_dir / basename).exists()


def test_upload_strips_exif_metadata(client, tmp_path, monkeypatch):
    upload_dir = tmp_path / "offers"
    upload_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(uploads_api, "UPLOAD_DIR", str(upload_dir))

    files = {"files": ("photo.jpg", _jpeg_bytes(with_exif=True), "image/jpeg")}
    response = client.post("/api/v1/uploads/images", files=files)
    assert response.status_code == 200

    stored_name = Path(response.json()["images"][0]).name
    stored_path = upload_dir / stored_name
    saved = Image.open(stored_path)
    exif = saved.getexif()
    assert len(exif) == 0
