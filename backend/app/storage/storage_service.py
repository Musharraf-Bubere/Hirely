from contextlib import contextmanager
import logging
from pathlib import Path
import tempfile
from typing import Any, Generator
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.storage.file_validation import MAX_RESUME_SIZE

logger = logging.getLogger(__name__)


class StorageService:
    """
    Storage service supporting local filesystem storage and Cloudflare R2
    (S3-compatible) object storage for candidate resumes.

    Local development uses the local filesystem by default without requiring
    any cloud credentials. When STORAGE_BACKEND=r2 is configured, uploads stream
    directly to Cloudflare R2, and temporary files are securely managed during
    Docling document extraction with guaranteed cleanup.
    """

    def __init__(
        self,
        storage_dir: str | Path | None = None,
        storage_backend: str | None = None,
        backend: str | None = None,
        s3_client: Any = None,
        bucket_name: str | None = None,
        endpoint_url: str | None = None,
    ):
        chosen_backend = (backend or storage_backend or settings.storage_backend).strip().lower()
        if chosen_backend not in {"local", "r2"}:
            raise ValueError(
                f"Unsupported storage backend: '{chosen_backend}'. Only 'local' and 'r2' are accepted."
            )
        self.storage_backend = chosen_backend
        self.backend = self.storage_backend
        dir_path = storage_dir if storage_dir is not None else settings.resume_storage_dir
        self.storage_dir = Path(dir_path)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self._s3_client = s3_client
        self.bucket_name = bucket_name or settings.r2_bucket_name
        self.endpoint_url = endpoint_url or settings.computed_r2_endpoint_url

    @staticmethod
    def _validate_object_key(file_path_or_key: str | Path) -> str:
        """
        Validates an R2 object key.
        Explicitly rejects keys with leading slashes, backslashes, or unsafe
        path traversal components before any normalization occurs.
        """
        raw_key = str(file_path_or_key)
        if not raw_key or not raw_key.strip():
            raise ValueError("Invalid storage object key: key cannot be empty")

        if raw_key.startswith("/") or raw_key.startswith("\\"):
            raise ValueError("Invalid storage object key: leading slashes are not allowed")

        normalized = raw_key.replace("\\", "/")
        parts = normalized.split("/")
        if any(part in {"..", "."} for part in parts) or ".." in normalized:
            raise ValueError("Invalid storage object key: unsafe traversal components are not allowed")

        return normalized

    @property
    def s3_client(self) -> Any:
        if self._s3_client is None:
            import boto3
            from botocore.config import Config

            self._s3_client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                aws_access_key_id=settings.r2_access_key_id,
                aws_secret_access_key=settings.r2_secret_access_key,
                config=Config(signature_version="s3v4"),
                region_name="auto",
            )
        return self._s3_client

    def save_resume(self, file: UploadFile) -> str:
        """
        Save an uploaded resume.
        In local mode: streams to local disk under storage_dir.
        In R2 mode: streams directly to R2 bucket under key 'resumes/<uuid><ext>'.
        Returns the local file path string (local) or object key (R2).
        """
        raw_ext = Path(file.filename or "").suffix.lower()
        extension = raw_ext if raw_ext in {".pdf", ".docx"} else ".pdf"
        unique_id = uuid4()

        # Ensure file stream position is at the start
        file.file.seek(0)

        if self.storage_backend == "r2":
            key = f"resumes/{unique_id}{extension}"
            content_type = file.content_type or (
                "application/pdf"
                if extension == ".pdf"
                else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            try:
                self.s3_client.upload_fileobj(
                    file.file,
                    self.bucket_name,
                    key,
                    ExtraArgs={"ContentType": content_type},
                )
            except Exception as exc:
                logger.warning("R2 upload failed: %s", type(exc).__name__)
                raise IOError("Failed to upload resume to object storage") from exc
            finally:
                file.file.seek(0)

            return key
        else:
            filename = f"{unique_id}{extension}"
            file_path = self.storage_dir / filename
            try:
                with file_path.open("wb") as buffer:
                    while chunk := file.file.read(1024 * 1024):
                        buffer.write(chunk)
            finally:
                file.file.seek(0)

            return str(file_path)

    @contextmanager
    def open_file_for_reading(self, file_path_or_key: str | Path) -> Generator[Path, None, None]:
        """
        Context manager providing a local filesystem Path for document reading
        (required by Docling).

        - If the file exists on the local filesystem (backward compatibility and local mode),
          yields it directly without creating a temporary file.
        - If the file is stored in R2, downloads it to a unique temporary file,
          enforcing the 10 MB maximum size limit, and unlinks the temporary file
          in the finally block regardless of success or failure.
        """
        # 1. Local path check (Backward compatibility for local files & test fixtures)
        candidate_local_path = Path(file_path_or_key)
        if candidate_local_path.is_file():
            yield candidate_local_path
            return

        rel_path = self.storage_dir / candidate_local_path.name
        if rel_path.is_file():
            yield rel_path
            return

        if self.storage_backend == "local":
            raise FileNotFoundError(f"Resume file not found: {file_path_or_key}")

        # 2. R2 Object retrieval
        key = self._validate_object_key(file_path_or_key)

        raw_ext = Path(key).suffix.lower()
        extension = raw_ext if raw_ext in {".pdf", ".docx"} else ".pdf"

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
            prefix="hirely_resume_",
        )
        temp_path = Path(temp_file.name)
        temp_file.close()

        try:
            # Check head object for existence and size bounds before downloading
            try:
                head = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            except Exception as exc:
                error_code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
                if error_code in ("404", "NoSuchKey", "NotFound"):
                    raise FileNotFoundError(f"Resume object not found: {key}") from exc
                logger.warning("R2 head_object failed: %s", type(exc).__name__)
                raise IOError("Failed to access resume object in storage") from exc

            content_length = head.get("ContentLength", 0)
            if content_length > MAX_RESUME_SIZE:
                raise ValueError("Resume object size exceeds maximum allowed limit (10 MB)")

            # Stream download to the temporary file with byte counting protection
            bytes_downloaded = 0
            with temp_path.open("wb") as out_f:
                def download_callback(chunk_size):
                    nonlocal bytes_downloaded
                    bytes_downloaded += chunk_size
                    if bytes_downloaded > MAX_RESUME_SIZE:
                        raise ValueError("Downloaded resume exceeds maximum allowed limit (10 MB)")

                try:
                    self.s3_client.download_fileobj(
                        self.bucket_name,
                        key,
                        out_f,
                        Callback=download_callback,
                    )
                except Exception as exc:
                    logger.warning("R2 download_fileobj failed: %s", type(exc).__name__)
                    raise IOError("Failed to download resume from object storage") from exc

            yield temp_path
        finally:
            if temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass

    def read_file_bytes(self, file_path_or_key: str | Path) -> bytes:
        """
        Reads the raw content bytes of a resume file.
        """
        local_path = Path(file_path_or_key)
        if local_path.is_file():
            return local_path.read_bytes()

        rel_path = self.storage_dir / local_path.name
        if rel_path.is_file():
            return rel_path.read_bytes()

        if self.storage_backend == "local":
            raise FileNotFoundError(f"Resume file not found: {file_path_or_key}")

        key = self._validate_object_key(file_path_or_key)

        try:
            head = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            if head.get("ContentLength", 0) > MAX_RESUME_SIZE:
                raise ValueError("Resume object size exceeds maximum allowed limit (10 MB)")

            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            return response["Body"].read()
        except Exception as exc:
            error_code = getattr(exc, "response", {}).get("Error", {}).get("Code", "")
            if error_code in ("404", "NoSuchKey", "NotFound"):
                raise FileNotFoundError(f"Resume object not found: {key}") from exc
            logger.warning("R2 read_file_bytes failed: %s", type(exc).__name__)
            raise IOError("Failed to read resume from object storage") from exc

    def delete_file(self, file_path_or_key: str | Path) -> bool:
        """
        Deletes a resume from local disk or R2 bucket.
        Guarantees only the specific object or file is removed.
        """
        local_path = Path(file_path_or_key)
        if local_path.is_file():
            try:
                local_path.unlink()
                return True
            except OSError as exc:
                logger.warning("Failed to delete local resume file: %s", type(exc).__name__)
                return False

        rel_path = self.storage_dir / local_path.name
        if rel_path.is_file():
            try:
                rel_path.unlink()
                return True
            except OSError as exc:
                logger.warning("Failed to delete local resume file: %s", type(exc).__name__)
                return False

        if self.backend == "local":
            return True

        key = self._validate_object_key(file_path_or_key)

        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except Exception as exc:
            logger.warning("R2 delete_object failed: %s", type(exc).__name__)
            return False


storage_service = StorageService()
