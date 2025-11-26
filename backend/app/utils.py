import os, uuid
from pathlib import Path
from .config import settings

def ensure_upload_dir():
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

def temp_filename(original_name: str) -> str:
    ensure_upload_dir()
    uid = uuid.uuid4().hex
    return os.path.join(settings.UPLOAD_DIR, f"{uid}_{os.path.basename(original_name)}")
