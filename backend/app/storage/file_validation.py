from pathlib import Path
import zipfile

from fastapi import UploadFile


ALLOWED_RESUME_EXTENSIONS = {".pdf", ".docx"}
MAX_RESUME_SIZE = 10 * 1024 * 1024  # 10 MB upload limit
MAX_DOCX_UNCOMPRESSED_SIZE = 50 * 1024 * 1024  # 50 MB safe decompression limit
MAX_DOCX_ENTRIES = 1_000  # Maximum zip archive members
PDF_MAGIC_BYTES = b"%PDF-"
ZIP_MAGIC_BYTES = b"PK\x03\x04"


def validate_resume_file(file: UploadFile) -> None:
    """
    Validate uploaded resume files for allowed extension, maximum file size,
    and binary content signatures (magic bytes and structure).

    Guarantees:
    - Rejects empty, oversized, mismatched, or unsupported file formats.
    - PDF: Verifies %PDF- signature.
    - DOCX: Verifies ZIP signature and confirms Word document structure
      requiring both [Content_Types].xml and word/document.xml.
    - Pre-parse DOS defense: Bounds DOCX uncompressed size (<= 50 MB) and entry count (<= 1,000)
      to prevent zip-bomb decompression attacks before document extraction.
    - Performs in-memory structure inspection without extracting archives to disk.
    - Restores the underlying file stream position to 0 upon completion or error.
    - Emits safe validation errors without leaking server filesystem paths or file content.
    """
    if not file.filename:
        raise ValueError("Resume file is required")

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_RESUME_EXTENSIONS:
        raise ValueError("Only PDF and DOCX resume files are allowed")

    # Determine file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size == 0:
        raise ValueError("Resume file is empty")

    if file_size > MAX_RESUME_SIZE:
        raise ValueError("Resume file size must not exceed 10 MB")

    try:
        if extension == ".pdf":
            header = file.file.read(len(PDF_MAGIC_BYTES))
            if not header.startswith(PDF_MAGIC_BYTES):
                raise ValueError("Invalid PDF file: missing expected PDF file signature")

        elif extension == ".docx":
            header = file.file.read(len(ZIP_MAGIC_BYTES))
            if not header.startswith(ZIP_MAGIC_BYTES):
                raise ValueError("Invalid DOCX file: missing expected ZIP archive signature")

            file.file.seek(0)
            try:
                with zipfile.ZipFile(file.file, "r") as zf:
                    infolist = zf.infolist()
                    if len(infolist) > MAX_DOCX_ENTRIES:
                        raise ValueError(
                            "Invalid DOCX file: archive contains too many files"
                        )

                    total_uncompressed = sum(info.file_size for info in infolist)
                    if total_uncompressed > MAX_DOCX_UNCOMPRESSED_SIZE:
                        raise ValueError(
                            "Invalid DOCX file: archive contents exceed safe decompression limits"
                        )

                    namelist = [info.filename for info in infolist]
                    has_content_types = "[Content_Types].xml" in namelist
                    has_word_doc = any(
                        name in namelist for name in ("word/document.xml", "word/document2.xml")
                    )
                    if not (has_content_types and has_word_doc):
                        raise ValueError(
                            "Invalid DOCX file: archive does not contain a valid Word document structure"
                        )
            except (zipfile.BadZipFile, zipfile.LargeZipFile, EOFError, KeyError) as exc:
                raise ValueError("Invalid DOCX file: archive is corrupted or malformed") from exc
            except ValueError:
                raise
            except Exception as exc:
                raise ValueError("Invalid DOCX file: archive is corrupted or malformed") from exc
    finally:
        file.file.seek(0)
