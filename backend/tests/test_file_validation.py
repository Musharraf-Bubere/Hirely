from io import BytesIO
import zipfile

import pytest
from fastapi import UploadFile

from app.storage.file_validation import validate_resume_file


def _create_minimal_docx() -> bytes:
    """Helper to create a valid minimal in-memory DOCX archive."""
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types></Types>')
        zf.writestr("word/document.xml", '<?xml version="1.0" encoding="UTF-8"?><w:document></w:document>')
    return buffer.getvalue()


def test_valid_pdf_file():
    upload_file = UploadFile(
        filename="resume.pdf",
        file=BytesIO(b"%PDF-1.4 valid pdf content\n%%EOF"),
    )

    validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_valid_docx_file():
    docx_bytes = _create_minimal_docx()
    upload_file = UploadFile(
        filename="resume.docx",
        file=BytesIO(docx_bytes),
    )

    validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_invalid_file_extension():
    upload_file = UploadFile(
        filename="resume.exe",
        file=BytesIO(b"MZ\x90\x00executable content"),
    )

    with pytest.raises(ValueError, match="Only PDF and DOCX resume files are allowed"):
        validate_resume_file(upload_file)


def test_empty_pdf_file_rejected():
    upload_file = UploadFile(
        filename="empty.pdf",
        file=BytesIO(b""),
    )

    with pytest.raises(ValueError, match="Resume file is empty"):
        validate_resume_file(upload_file)


def test_empty_docx_file_rejected():
    upload_file = UploadFile(
        filename="empty.docx",
        file=BytesIO(b""),
    )

    with pytest.raises(ValueError, match="Resume file is empty"):
        validate_resume_file(upload_file)


def test_renamed_executable_as_pdf_rejected():
    upload_file = UploadFile(
        filename="resume.pdf",
        file=BytesIO(b"MZ\x90\x00\x03\x00\x00\x00fake pe header"),
    )

    with pytest.raises(ValueError, match="Invalid PDF file: missing expected PDF file signature"):
        validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_renamed_executable_as_docx_rejected():
    upload_file = UploadFile(
        filename="resume.docx",
        file=BytesIO(b"MZ\x90\x00\x03\x00\x00\x00fake pe header"),
    )

    with pytest.raises(ValueError, match="Invalid DOCX file: missing expected ZIP archive signature"):
        validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_generic_zip_renamed_as_docx_rejected():
    # Valid ZIP but missing word/document.xml
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("test.txt", "just plain text in a zip")
    generic_zip = buffer.getvalue()

    upload_file = UploadFile(
        filename="fake.docx",
        file=BytesIO(generic_zip),
    )

    with pytest.raises(ValueError, match="archive does not contain a valid Word document structure"):
        validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_corrupted_docx_rejected():
    # Valid ZIP header bytes followed by corrupted content
    corrupted_content = b"PK\x03\x04" + b"\x00" * 20 + b"corrupted trailing bytes"

    upload_file = UploadFile(
        filename="corrupt.docx",
        file=BytesIO(corrupted_content),
    )

    with pytest.raises(ValueError, match="archive is corrupted or malformed"):
        validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_file_size_exceeds_limit():
    large_content = b"%PDF-" + b"x" * (10 * 1024 * 1024 + 1)

    upload_file = UploadFile(
        filename="resume.pdf",
        file=BytesIO(large_content),
    )

    with pytest.raises(ValueError, match="must not exceed 10 MB"):
        validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_stream_position_restored_after_success():
    docx_bytes = _create_minimal_docx()
    upload_file = UploadFile(
        filename="resume.docx",
        file=BytesIO(docx_bytes),
    )

    validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0
    # Confirm stream can be read cleanly from beginning
    read_back = upload_file.file.read(4)
    assert read_back == b"PK\x03\x04"


def test_docx_missing_content_types_rejected():
    # Archive has word/document.xml but missing [Content_Types].xml
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("word/document.xml", "<w:document/>")
    incomplete_docx = buffer.getvalue()

    upload_file = UploadFile(
        filename="missing_content_types.docx",
        file=BytesIO(incomplete_docx),
    )

    with pytest.raises(ValueError, match="archive does not contain a valid Word document structure"):
        validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0


def test_docx_missing_word_document_rejected():
    # Archive has [Content_Types].xml but missing word/document.xml
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("[Content_Types].xml", "<Types/>")
    incomplete_docx = buffer.getvalue()

    upload_file = UploadFile(
        filename="missing_word_doc.docx",
        file=BytesIO(incomplete_docx),
    )

    with pytest.raises(ValueError, match="archive does not contain a valid Word document structure"):
        validate_resume_file(upload_file)
    assert upload_file.file.tell() == 0
