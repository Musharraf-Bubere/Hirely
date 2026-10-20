from pathlib import Path
from unittest.mock import Mock

from app.ai.loaders.resume_loader import ResumeLoader


def test_resume_loader_returns_documents():
    mock_document = Mock()

    mock_docling_loader = Mock()
    mock_docling_loader.load.return_value = [mock_document]

    loader = ResumeLoader()

    # Replace the DoclingLoader used inside the module with our mock.
    import app.ai.loaders.resume_loader as resume_loader_module

    original_loader = resume_loader_module.DoclingLoader
    resume_loader_module.DoclingLoader = Mock(return_value=mock_docling_loader)

    try:
        documents = loader.load(Path("test_resume.pdf"))

        assert documents == [mock_document]
        mock_docling_loader.load.assert_called_once()
    finally:
        resume_loader_module.DoclingLoader = original_loader


def test_resume_loader_rejects_empty_documents():
    mock_docling_loader = Mock()
    mock_docling_loader.load.return_value = []

    loader = ResumeLoader()

    import app.ai.loaders.resume_loader as resume_loader_module

    original_loader = resume_loader_module.DoclingLoader
    resume_loader_module.DoclingLoader = Mock(return_value=mock_docling_loader)

    try:
        try:
            loader.load(Path("test_resume.pdf"))
            assert False, "Expected RuntimeError"
        except RuntimeError as exc:
            assert str(exc) == "No content could be extracted from the resume"
    finally:
        resume_loader_module.DoclingLoader = original_loader


def test_resume_loader_returns_combined_text():
    mock_documents = [
        Mock(page_content="Contact information"),
        Mock(page_content="Professional Summary"),
        Mock(page_content="Technical Skills"),
    ]

    mock_docling_loader = Mock()
    mock_docling_loader.load.return_value = mock_documents

    loader = ResumeLoader()

    import app.ai.loaders.resume_loader as resume_loader_module

    original_loader = resume_loader_module.DoclingLoader
    resume_loader_module.DoclingLoader = Mock(return_value=mock_docling_loader)

    try:
        text = loader.load_text(Path("test_resume.pdf"))

        assert text == (
            "Contact information\n\n"
            "Professional Summary\n\n"
            "Technical Skills"
        )
    finally:
        resume_loader_module.DoclingLoader = original_loader


def test_resume_loader_bounds_document_count():
    # 15 documents returned by loader; should be capped at max_documents (10)
    mock_documents = [Mock(page_content=f"Page {i}") for i in range(15)]

    mock_docling_loader = Mock()
    mock_docling_loader.load.return_value = mock_documents

    loader = ResumeLoader(max_documents=10)

    import app.ai.loaders.resume_loader as resume_loader_module
    original_loader = resume_loader_module.DoclingLoader
    resume_loader_module.DoclingLoader = Mock(return_value=mock_docling_loader)

    try:
        documents = loader.load(Path("test_resume.pdf"))
        assert len(documents) == 10
        assert documents[0].page_content == "Page 0"
        assert documents[9].page_content == "Page 9"
    finally:
        resume_loader_module.DoclingLoader = original_loader


def test_resume_loader_bounds_oversized_text():
    # Extracted text exceeding max_extracted_chars should be truncated
    mock_documents = [Mock(page_content="A" * 60_000)]

    mock_docling_loader = Mock()
    mock_docling_loader.load.return_value = mock_documents

    loader = ResumeLoader(max_extracted_chars=50_000)

    import app.ai.loaders.resume_loader as resume_loader_module
    original_loader = resume_loader_module.DoclingLoader
    resume_loader_module.DoclingLoader = Mock(return_value=mock_docling_loader)

    try:
        text = loader.load_text(Path("test_resume.pdf"))
        assert len(text) == 50_000
    finally:
        resume_loader_module.DoclingLoader = original_loader


def test_resume_loader_corrupted_document_raises_value_error():
    mock_docling_loader = Mock()
    mock_docling_loader.load.side_effect = Exception("Malformed PDF stream syntax error")

    loader = ResumeLoader()

    import app.ai.loaders.resume_loader as resume_loader_module
    original_loader = resume_loader_module.DoclingLoader
    resume_loader_module.DoclingLoader = Mock(return_value=mock_docling_loader)

    try:
        import pytest
        with pytest.raises(ValueError, match="Unable to read resume document: malformed or corrupted file"):
            loader.load(Path("corrupt.pdf"))
    finally:
        resume_loader_module.DoclingLoader = original_loader