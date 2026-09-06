from pathlib import Path

from fastapi import UploadFile


ALLOWED_RESUME_EXTENSIONS = {".pdf", ".docx"}
MAX_RESUME_SIZE = 10 * 1024 * 1024


def validate_resume_file(file: UploadFile) -> None:
    if not file.filename:
        raise ValueError("Resume file is required")

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_RESUME_EXTENSIONS:
        raise ValueError("Only PDF and DOCX resume files are allowed")

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_RESUME_SIZE:
        raise ValueError("Resume file size must not exceed 10 MB")