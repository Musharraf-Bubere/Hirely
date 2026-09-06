from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class StorageService:
    def __init__(self, storage_dir: str | Path = "app/storage/resumes"):
        self.storage_dir = Path(storage_dir)
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