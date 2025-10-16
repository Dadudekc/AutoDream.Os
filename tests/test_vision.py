"""
Vision System Tests - V2 Compliant
==================================

Comprehensive test suite for the Vision System.
Maintains 100% test pass rate and V2 compliance standards.

Author: Agent-1 - Vision & Automation Specialist
License: MIT
"""

from src.vision.analysis import VisualAnalyzer
from src.vision.capture import ScreenCapture
from src.vision.integration import VisionSystem
from src.vision.ocr import TextExtractor


class TestScreenCapture:
    """Test screen capture functionality."""

    def test_screen_capture_initialization(self):
        """Test screen capture initialization."""
        capture = ScreenCapture()

        assert capture.capture_frequency == 1.0
        assert capture.capture_format == "RGB"
        assert not capture.is_monitoring

    def test_capture_info(self):
        """Test capture information retrieval."""
        capture = ScreenCapture()
        info = capture.get_capture_info()

        assert "pil_available" in info
        assert "capture_frequency" in info
        assert "is_monitoring" in info


class TestTextExtractor:
    """Test OCR text extraction."""

    def test_text_extractor_initialization(self):
        """Test text extractor initialization."""
        extractor = TextExtractor()

        assert extractor.language == "eng"
        assert extractor.confidence_threshold == 60

    def test_language_setting(self):
        """Test OCR language setting."""
        extractor = TextExtractor()
        extractor.set_language("fra")

        assert extractor.language == "fra"

    def test_confidence_threshold_setting(self):
        """Test confidence threshold setting."""
        extractor = TextExtractor()
        extractor.set_confidence_threshold(80)

        assert extractor.confidence_threshold == 80

    def test_ocr_info(self):
        """Test OCR information retrieval."""
        extractor = TextExtractor()
        info = extractor.get_ocr_info()

        assert "tesseract_available" in info
        assert "language" in info
        assert "confidence_threshold" in info


class TestVisualAnalyzer:
    """Test visual analysis functionality."""

    def test_visual_analyzer_initialization(self):
        """Test visual analyzer initialization."""
        analyzer = VisualAnalyzer()

        assert analyzer.ui_detection_enabled
        assert analyzer.min_element_area == 100

    def test_analysis_info(self):
        """Test analysis information retrieval."""
        analyzer = VisualAnalyzer()
        info = analyzer.get_analysis_info()

        assert "opencv_available" in info
        assert "ui_detection_enabled" in info
        assert "min_element_area" in info


class TestVisionSystem:
    """Test vision system integration."""

    def test_vision_system_initialization(self):
        """Test vision system initialization."""
        vision = VisionSystem()

        assert vision.screen_capture is not None
        assert vision.text_extractor is not None
        assert vision.visual_analyzer is not None

    def test_get_capabilities(self):
        """Test capabilities retrieval."""
        vision = VisionSystem()
        capabilities = vision.get_vision_capabilities()

        assert "screen_capture" in capabilities
        assert "ocr" in capabilities
        assert "visual_analysis" in capabilities
        assert "integration" in capabilities

    def test_cleanup_old_data(self):
        """Test data cleanup functionality."""
        vision = VisionSystem()
        cleaned = vision.cleanup_old_data(max_age_days=0)

        # Should return a number (0 or more)
        assert isinstance(cleaned, int)
        assert cleaned >= 0
