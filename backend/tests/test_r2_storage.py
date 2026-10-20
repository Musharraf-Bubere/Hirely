import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from botocore.exceptions import ClientError
from fastapi import UploadFile
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.ai.parsers.resume_parser import ResumeParserService
from app.ai.parsers.schemas import ResumeData
from app.core.config import Settings
from app.core.security import create_access_token, hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User, UserRole
from app.services.resume import create_resume, delete_resume
from app.storage.storage_service import MAX_RESUME_SIZE, StorageService


# ============================================================================
# 1. Configuration Validation Tests
# ============================================================================

def test_config_local_storage_backend_no_r2_keys():
    """Local storage backend should not require R2 credentials."""
    cfg = Settings(
        DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/hirely",
        JWT_SECRET_KEY="test_secret_key_for_testing_purposes",
        GEMINI_API_KEY="test_gemini_key",
        STORAGE_BACKEND="local",
    )
    assert cfg.storage_backend == "local"
    assert cfg.r2_account_id is None
    assert cfg.r2_access_key_id is None
    assert cfg.computed_r2_endpoint_url is None


def test_config_r2_storage_backend_missing_keys():
    """R2 storage backend requires account_id, access_key_id, secret_access_key, and bucket_name."""
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/hirely",
            JWT_SECRET_KEY="test_secret_key_for_testing_purposes",
            GEMINI_API_KEY="test_gemini_key",
            STORAGE_BACKEND="r2",
            # Missing all R2 credentials
        )
    err = str(exc_info.value)
    assert "R2 storage backend is configured, but required parameters are missing" in err


def test_config_r2_storage_backend_valid_keys():
    """R2 storage backend with all required keys auto-computes endpoint URL."""
    cfg = Settings(
        DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/hirely",
        JWT_SECRET_KEY="test_secret_key_for_testing_purposes",
        GEMINI_API_KEY="test_gemini_key",
        STORAGE_BACKEND="r2",
        R2_ACCOUNT_ID="abc123def456",
        R2_ACCESS_KEY_ID="test_access_key",
        R2_SECRET_ACCESS_KEY="test_secret_key",
        R2_BUCKET_NAME="test-resumes-bucket",
    )
    assert cfg.storage_backend == "r2"
    assert cfg.r2_bucket_name == "test-resumes-bucket"
    assert cfg.computed_r2_endpoint_url == "https://abc123def456.r2.cloudflarestorage.com"


def test_config_r2_storage_backend_custom_endpoint():
    """R2 custom endpoint URL takes precedence over computed endpoint URL."""
    cfg = Settings(
        DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/hirely",
        JWT_SECRET_KEY="test_secret_key_for_testing_purposes",
        GEMINI_API_KEY="test_gemini_key",
        STORAGE_BACKEND="r2",
        R2_ACCOUNT_ID="abc123def456",
        R2_ACCESS_KEY_ID="test_access_key",
        R2_SECRET_ACCESS_KEY="test_secret_key",
        R2_BUCKET_NAME="test-resumes-bucket",
        R2_ENDPOINT_URL="https://custom-r2.example.com",
    )
    assert cfg.computed_r2_endpoint_url == "https://custom-r2.example.com"


def test_config_rejects_unsupported_storage_backend():
    """Settings must explicitly reject unsupported storage backends like s3 or azure."""
    for invalid in ["s3", "azure", "gcs", "custom_cloud"]:
        with pytest.raises(ValidationError) as exc_info:
            Settings(
                DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/hirely",
                JWT_SECRET_KEY="test_secret_key_for_testing_purposes",
                GEMINI_API_KEY="test_gemini_key",
                STORAGE_BACKEND=invalid,
            )
        err = str(exc_info.value)
        assert "Unsupported STORAGE_BACKEND" in err
        assert "Only 'local' and 'r2' are accepted" in err


# ============================================================================
# 2. StorageService Initialization & R2 Upload Tests
# ============================================================================

def test_storage_service_r2_upload_fileobj(tmp_path: Path):
    """R2 upload streams file to S3 with a unique key under resumes/ and sets ContentType."""
    mock_s3 = MagicMock()

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    pdf_content = b"%PDF-1.4 test resume bytes"
    upload = UploadFile(
        filename="candidate_resume.pdf",
        file=BytesIO(pdf_content),
        headers={"content-type": "application/pdf"},
    )

    key = service.save_resume(upload)

    assert key.startswith("resumes/")
    assert key.endswith(".pdf")
    assert "candidate_resume" not in key

    mock_s3.upload_fileobj.assert_called_once()
    call_args, call_kwargs = mock_s3.upload_fileobj.call_args
    # call_args[0] is the file object, call_args[1] is bucket, call_args[2] is key
    assert call_args[1] == "my-bucket"
    assert call_args[2] == key
    assert call_kwargs.get("ExtraArgs", {}).get("ContentType") == "application/pdf"

    # Verify stream position was reset to 0
    assert upload.file.tell() == 0


def test_storage_service_r2_upload_docx(tmp_path: Path):
    """R2 upload preserves .docx extension and MIME type."""
    mock_s3 = MagicMock()

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    upload = UploadFile(
        filename="document.docx",
        file=BytesIO(b"PK\x03\x04test docx content"),
        headers={"content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
    )

    key = service.save_resume(upload)
    assert key.startswith("resumes/")
    assert key.endswith(".docx")

    call_args, call_kwargs = mock_s3.upload_fileobj.call_args
    assert call_kwargs.get("ExtraArgs", {}).get("ContentType") == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


# ============================================================================
# 3. StorageService R2 File Retrieval & Cleanup Tests
# ============================================================================

def test_storage_service_r2_open_file_for_reading_success(tmp_path: Path):
    """Context manager downloads R2 object to temporary file and deletes it on exit."""
    mock_s3 = MagicMock()
    mock_s3.head_object.return_value = {"ContentLength": 500}

    def fake_download(bucket, key, fileobj, Callback=None):
        data = b"%PDF-1.5 fake resume content"
        fileobj.write(data)
        if Callback:
            Callback(len(data))

    mock_s3.download_fileobj.side_effect = fake_download

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    temp_path_captured = None
    with service.open_file_for_reading("resumes/abc-123.pdf") as temp_path:
        temp_path_captured = temp_path
        assert temp_path.exists()
        assert temp_path.suffix == ".pdf"
        assert temp_path.read_bytes() == b"%PDF-1.5 fake resume content"

    # Temp file must be deleted upon context manager exit
    assert not temp_path_captured.exists()


def test_storage_service_r2_open_file_for_reading_cleanup_on_error(tmp_path: Path):
    """Context manager ensures temporary file is deleted even if an exception occurs."""
    mock_s3 = MagicMock()
    mock_s3.head_object.return_value = {"ContentLength": 200}

    def fake_download(bucket, key, fileobj, Callback=None):
        fileobj.write(b"data")

    mock_s3.download_fileobj.side_effect = fake_download

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    temp_path_captured = None
    with pytest.raises(RuntimeError, match="Simulated parsing crash"):
        with service.open_file_for_reading("resumes/err-test.pdf") as temp_path:
            temp_path_captured = temp_path
            assert temp_path.exists()
            raise RuntimeError("Simulated parsing crash")

    # Temp file must be deleted even after exception
    assert temp_path_captured is not None
    assert not temp_path_captured.exists()


def test_storage_service_r2_open_file_for_reading_not_found(tmp_path: Path):
    """R2 404 raises FileNotFoundError."""
    mock_s3 = MagicMock()
    error_response = {"Error": {"Code": "404", "Message": "Not Found"}}
    mock_s3.head_object.side_effect = ClientError(error_response, "HeadObject")

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    with pytest.raises(FileNotFoundError, match="Resume object not found"):
        with service.open_file_for_reading("resumes/missing.pdf"):
            pass


def test_storage_service_r2_open_file_for_reading_exceeds_size_limit(tmp_path: Path):
    """Objects larger than 10 MB are rejected before or during download."""
    mock_s3 = MagicMock()
    mock_s3.head_object.return_value = {"ContentLength": MAX_RESUME_SIZE + 1}

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    with pytest.raises(ValueError, match="Resume object size exceeds maximum allowed limit"):
        with service.open_file_for_reading("resumes/huge.pdf"):
            pass


def test_storage_service_r2_streaming_download_callback_size_limit(tmp_path: Path):
    """Streaming callback aborts download if byte count exceeds limit."""
    mock_s3 = MagicMock()
    mock_s3.head_object.return_value = {"ContentLength": 1024}

    def fake_overflow_download(bucket, key, fileobj, Callback=None):
        if Callback:
            Callback(MAX_RESUME_SIZE + 500)

    mock_s3.download_fileobj.side_effect = fake_overflow_download

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    with pytest.raises((ValueError, IOError)):
        with service.open_file_for_reading("resumes/stream-overflow.pdf"):
            pass


def test_storage_service_rejects_unsupported_backend(tmp_path: Path):
    """StorageService must explicitly reject backends other than 'local' and 'r2'."""
    for invalid in ["s3", "azure", "invalid"]:
        with pytest.raises(ValueError, match="Unsupported storage backend"):
            StorageService(storage_dir=tmp_path, backend=invalid)


def test_storage_service_rejects_unsafe_object_keys(tmp_path: Path):
    """Leading slashes, backslashes, and traversal components must be rejected explicitly."""
    mock_s3 = MagicMock()
    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    invalid_keys = [
        "/resumes/secret.pdf",
        "//resumes/secret.pdf",
        "\\resumes\\secret.pdf",
        "../secret.pdf",
        "resumes/../../secret.pdf",
        "resumes/./secret.pdf",
        "resumes/..\\secret.pdf",
        "",
        "   ",
    ]

    for bad_key in invalid_keys:
        # Test open_file_for_reading
        with pytest.raises(ValueError, match="Invalid storage object key"):
            with service.open_file_for_reading(bad_key):
                pass

        # Test read_file_bytes
        with pytest.raises(ValueError, match="Invalid storage object key"):
            service.read_file_bytes(bad_key)

        # Test delete_file
        with pytest.raises(ValueError, match="Invalid storage object key"):
            service.delete_file(bad_key)


def test_storage_service_accepts_valid_generated_r2_keys(tmp_path: Path):
    """Standard generated R2 keys are accepted without error."""
    mock_s3 = MagicMock()
    mock_s3.head_object.return_value = {"ContentLength": 100}

    def fake_download(bucket, key, fileobj, Callback=None):
        fileobj.write(b"content")

    mock_s3.download_fileobj.side_effect = fake_download

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    valid_keys = [
        "resumes/d683bfb2-111d-4599-936f-b4e1165cd84e.pdf",
        "resumes/00000000-0000-0000-0000-000000000000.docx",
        Path("resumes/d683bfb2-111d-4599-936f-b4e1165cd84e.pdf"),
    ]

    for key in valid_keys:
        with service.open_file_for_reading(key) as temp_p:
            assert temp_p.exists()
        assert not temp_p.exists()


def test_storage_service_backward_compatibility_existing_local_file(tmp_path: Path):
    """Existing local file is yielded directly without R2 interaction even when backend is r2."""
    mock_s3 = MagicMock()
    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    existing_file = tmp_path / "local_resume.pdf"
    existing_file.write_bytes(b"%PDF-1.4 local file content")

    with service.open_file_for_reading(existing_file) as yielded_path:
        assert yielded_path == existing_file
        assert yielded_path.exists()

    # R2 client should not have been called
    mock_s3.head_object.assert_not_called()
    mock_s3.download_fileobj.assert_not_called()
    # Local file must not be deleted
    assert existing_file.exists()


# ============================================================================
# 4. StorageService Deletion Tests
# ============================================================================

def test_storage_service_delete_file_local_mode(tmp_path: Path):
    """Local file deletion removes file and is idempotent for missing files."""
    service = StorageService(storage_dir=tmp_path, backend="local")

    f = tmp_path / "to_delete.pdf"
    f.write_bytes(b"temp")

    assert service.delete_file(f) is True
    assert not f.exists()

    # Idempotent: deleting already deleted file returns True
    assert service.delete_file(f) is True


def test_storage_service_delete_file_r2_mode(tmp_path: Path):
    """R2 deletion calls s3_client.delete_object and is idempotent."""
    mock_s3 = MagicMock()
    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    assert service.delete_file("resumes/uuid-123.pdf") is True
    mock_s3.delete_object.assert_called_once_with(
        Bucket="my-bucket",
        Key="resumes/uuid-123.pdf",
    )


def test_storage_service_delete_file_r2_handles_error(tmp_path: Path):
    """R2 deletion handles s3 client failure gracefully by returning False."""
    mock_s3 = MagicMock()
    mock_s3.delete_object.side_effect = Exception("AWS Network Error")

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    assert service.delete_file("resumes/uuid-fail.pdf") is False


# ============================================================================
# 5. Docling & ResumeParserService with R2 Storage
# ============================================================================

def test_resume_parser_service_parses_r2_object(tmp_path: Path):
    """ResumeParserService downloads from R2 to temp file, parses, and cleans up."""
    mock_s3 = MagicMock()
    mock_s3.head_object.return_value = {"ContentLength": 500}

    def fake_download(bucket, key, fileobj, Callback=None):
        fileobj.write(b"%PDF-1.4 candidate resume text")

    mock_s3.download_fileobj.side_effect = fake_download

    service = StorageService(
        storage_dir=tmp_path,
        backend="r2",
        s3_client=mock_s3,
        bucket_name="my-bucket",
    )

    mock_loader = MagicMock()
    mock_loader.load_text.return_value = "Jane Doe\nSkills: Python, AWS"

    mock_ai_service = MagicMock()
    expected_data = ResumeData(
        name="Jane Doe",
        skills=["Python", "AWS"],
    )
    mock_ai_service.generate_structured.return_value = expected_data

    parser = ResumeParserService(
        ai_service=mock_ai_service,
        resume_loader=mock_loader,
    )

    with patch("app.storage.storage_service.storage_service", service):
        result = parser.parse_file("resumes/jane-doe.pdf")

    assert result.name == "Jane Doe"
    assert result.skills == ["Python", "AWS"]
    mock_loader.load_text.assert_called_once()
    loaded_arg = mock_loader.load_text.call_args[0][0]
    # Verify temp path was passed and subsequently deleted
    assert not Path(loaded_arg).exists()


# ============================================================================
# 6. Service & API Endpoint: Resume Deletion
# ============================================================================

def test_resume_service_delete_resume():
    """Service delete_resume removes DB record and calls storage_service.delete_file."""
    db = SessionLocal()
    user = None
    candidate = None
    resume = None

    try:
        user = User(
            email=f"del-service-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.commit()

        candidate = Candidate(
            user_id=user.id,
            first_name="Service",
            last_name="Test",
        )
        db.add(candidate)
        db.commit()

        resume = create_resume(
            db=db,
            candidate=candidate,
            original_filename="resume_to_delete.pdf",
            file_path="resumes/service-del.pdf",
        )
        resume_id = resume.id

        mock_storage = MagicMock()
        with patch("app.storage.storage_service.storage_service", mock_storage):
            success = delete_resume(db=db, candidate=candidate, resume=resume)

        assert success is True
        mock_storage.delete_file.assert_called_once_with("resumes/service-del.pdf")

        # Record should no longer be in DB
        found = db.query(Resume).filter(Resume.id == resume_id).first()
        assert found is None

    finally:
        if candidate:
            db.delete(candidate)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_resume_service_delete_resume_unauthorized_candidate():
    """Attempting to delete a resume belonging to another candidate raises ValueError."""
    db = SessionLocal()
    user1 = user2 = None
    cand1 = cand2 = None
    resume = None

    try:
        user1 = User(email=f"u1-{uuid4()}@example.com", password_hash=hash_password("P123!"), role=UserRole.CANDIDATE)
        user2 = User(email=f"u2-{uuid4()}@example.com", password_hash=hash_password("P123!"), role=UserRole.CANDIDATE)
        db.add_all([user1, user2])
        db.commit()

        cand1 = Candidate(user_id=user1.id, first_name="C1", last_name="T1")
        cand2 = Candidate(user_id=user2.id, first_name="C2", last_name="T2")
        db.add_all([cand1, cand2])
        db.commit()

        resume = create_resume(db=db, candidate=cand1, original_filename="c1.pdf", file_path="resumes/c1.pdf")

        with pytest.raises(ValueError, match="Resume does not belong to candidate"):
            delete_resume(db=db, candidate=cand2, resume=resume)

    finally:
        if resume:
            db.delete(resume)
        if cand1:
            db.delete(cand1)
        if cand2:
            db.delete(cand2)
        if user1:
            db.delete(user1)
        if user2:
            db.delete(user2)
        db.commit()
        db.close()


def test_api_delete_resume_endpoint():
    """API endpoint DELETE /resumes/{id} deletes resume, calls storage, and clears cache."""
    test_client = TestClient(app)
    db = SessionLocal()
    user = None
    candidate = None
    resume = None

    try:
        user = User(
            email=f"api-del-{uuid4()}@example.com",
            password_hash=hash_password("Password123!"),
            role=UserRole.CANDIDATE,
        )
        db.add(user)
        db.commit()

        candidate = Candidate(
            user_id=user.id,
            first_name="API",
            last_name="Deleter",
        )
        db.add(candidate)
        db.commit()

        resume = create_resume(
            db=db,
            candidate=candidate,
            original_filename="api_resume.pdf",
            file_path="resumes/api-del.pdf",
        )
        resume_id = resume.id

        token = create_access_token(user_id=str(user.id), role=user.role.value)

        mock_storage = MagicMock()
        mock_storage.delete_file.return_value = True

        with patch("app.storage.storage_service.storage_service", mock_storage):
            response = test_client.delete(
                f"/resumes/{resume_id}",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Resume deleted successfully" in data["message"]
        mock_storage.delete_file.assert_called_once_with("resumes/api-del.pdf")

        # Verify DB record is deleted
        assert db.query(Resume).filter(Resume.id == resume_id).first() is None

        # Repeat delete returns 404
        response_repeat = test_client.delete(
            f"/resumes/{resume_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response_repeat.status_code == 404

    finally:
        if candidate:
            db.delete(candidate)
        if user:
            db.delete(user)
        db.commit()
        db.close()
