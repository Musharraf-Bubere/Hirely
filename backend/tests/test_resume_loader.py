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