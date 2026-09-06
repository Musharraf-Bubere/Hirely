from io import BytesIO
from pathlib import Path

from fastapi import UploadFile

from app.storage.storage_service import StorageService


def test_save_resume(tmp_path: Path):
    storage_service = StorageService(tmp_path)

    file_content = b"Test resume content"
    upload_file = UploadFile(
        filename="resume.pdf",
        file=BytesIO(file_content),
    )

    saved_path = storage_service.save_resume(upload_file)

    saved_file = Path(saved_path)

    assert saved_file.exists()
    assert saved_file.suffix == ".pdf"
    assert saved_file.name != "resume.pdf"
    assert saved_file.read_bytes() == file_content