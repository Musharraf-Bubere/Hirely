from pathlib import Path
import logging

from langchain_docling import DoclingLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

# Document processing limits
MAX_RESUME_DOCUMENTS = 10
MAX_EXTRACTED_TEXT_CHARS = 50_000


class ResumeLoader:
    """
    Document loader for extracting text from resume files (PDF and DOCX) via Docling.

    Operational & Architecture Note:
    Docling's document conversion pipeline relies on synchronous native C/C++ libraries (docling-parse).
    In CPython, synchronous native routines cannot be safely interrupted by Python signals or thread
    timeouts within the same process. While pre-parse validation, max_num_pages, and character bounds
    constrain memory and LLM prompt consumption, true deterministic execution timeouts and hard denial-of-service
    resilience require process isolation (e.g., executing parser jobs in separate subprocesses or dedicated
    Celery task workers with OS-level SIGKILL timeouts). Process isolation is identified as a required
    architecture enhancement for distributed multi-instance production deployments.
    """

    def __init__(
        self,
        max_documents: int = MAX_RESUME_DOCUMENTS,
        max_extracted_chars: int = MAX_EXTRACTED_TEXT_CHARS,
    ):
        self.max_documents = max_documents
        self.max_extracted_chars = max_extracted_chars

    def load(self, file_path: str | Path) -> list[Document]:
        try:
            # Instruct Docling to bound page processing up to max_documents during conversion
            loader = DoclingLoader(
                file_path=str(file_path),
                convert_kwargs={"max_num_pages": self.max_documents},
            )
            documents = loader.load()
        except FileNotFoundError:
            raise
        except Exception as exc:
            # Privacy-preserving logging: do not log file contents or raw path
            logger.warning(
                "DoclingLoader failed to parse resume document: %s",
                type(exc).__name__,
            )
            raise ValueError("Unable to read resume document: malformed or corrupted file") from exc

        if not documents:
            raise RuntimeError("No content could be extracted from the resume")

        if len(documents) > self.max_documents:
            logger.warning(
                "Resume exceeded maximum allowed document count (%d > %d); truncating to %d",
                len(documents),
                self.max_documents,
                self.max_documents,
            )
            documents = documents[: self.max_documents]

        return documents

    def load_text(self, file_path: str | Path) -> str:
        documents = self.load(file_path)

        text = "\n\n".join(
            document.page_content
            for document in documents
            if document.page_content.strip()
        )

        if not text.strip():
            raise RuntimeError("No text could be extracted from the resume")

        if len(text) > self.max_extracted_chars:
            logger.warning(
                "Extracted resume text (%d chars) exceeds maximum bound (%d chars); truncating",
                len(text),
                self.max_extracted_chars,
            )
            text = text[: self.max_extracted_chars]

        return text
