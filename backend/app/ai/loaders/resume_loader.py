from pathlib import Path

from langchain_docling import DoclingLoader
from langchain_core.documents import Document


class ResumeLoader:
    def load(self, file_path: str | Path) -> list[Document]:
        loader = DoclingLoader(
            file_path=str(file_path)
        )

        documents = loader.load()

        if not documents:
            raise RuntimeError("No content could be extracted from the resume")

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

        return text