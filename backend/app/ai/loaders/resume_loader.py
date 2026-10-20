from pathlib import Path
import logging

from langchain_docling import DoclingLoader
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

# Document processing limits
MAX_RESUME_DOCUMENTS = 10
MAX_EXTRACTED_TEXT_CHARS = 50_000


class ResumeLoader:
    def __init__(
        self,
        max_documents: int = MAX_RESUME_DOCUMENTS,
        max_extracted_chars: int = MAX_EXTRACTED_TEXT_CHARS,
    ):
        self.max_documents = max_documents
        self.max_extracted_chars = max_extracted_chars

    def load(self, file_path: str | Path) -> list[Document]:
        try:
            loader = DoclingLoader(file_path=str(file_path))
            documents = loader.load()
        except FileNotFoundError:
            raise
        except Exception as exc:
            logger.warning("DoclingLoader failed to parse resume %s: %s", file_path, exc)
            raise ValueError("Unable to read resume document: malformed or corrupted file") from exc

        if not documents:
            raise RuntimeError("No content could be extracted from the resume")

        if len(documents) > self.max_documents:
            logger.warning(
                "Resume %s exceeded maximum allowed document count (%d > %d); truncating to %d",
                file_path,
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
