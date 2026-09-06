from io import BytesIO

import pytest
from fastapi import UploadFile

from app.storage.file_validation import validate_resume_file


def test_valid_pdf_file():
    upload_file = UploadFile(
        filename="resume.pdf",
        file=BytesIO(b"valid resume content"),
    )

    validate_resume_file(upload_file)


def test_invalid_file_extension():
    upload_file = UploadFile(
        filename="resume.exe",
        file=BytesIO(b"invalid file"),
    )

    with pytest.raises(ValueError, match="Only PDF and DOCX"):
        validate_resume_file(upload_file)


def test_file_size_exceeds_limit():
    large_content = b"x" * (10 * 1024 * 1024 + 1)

    upload_file = UploadFile(
        filename="resume.pdf",
        file=BytesIO(large_content),
    )

    with pytest.raises(ValueError, match="must not exceed 10 MB"):
        validate_resume_file(upload_file)