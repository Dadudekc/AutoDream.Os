import pytest
from src.services.language_analyzer_service import LanguageAnalyzerService


@pytest.fixture
def language_analyzer():
    return LanguageAnalyzerService()
