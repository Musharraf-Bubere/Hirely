from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    def __init__(self, storage_dir: str | Path | None = None):
        dir_path = storage_dir if storage_dir is not None else settings.resume_storage_dir
        self.storage_dir = Path(dir_path)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_resume(self, file: UploadFile) -> str:
        extension = Path(file.filename or "").suffix.lower()
        filename = f"{uuid4()}{extension}"

        file_path = self.storage_dir / filename

        with file_path.open("wb") as buffer:
            while chunk := file.file.read(1024 * 1024):
                buffer.write(chunk)

        return str(file_path)


storage_service = StorageService()
