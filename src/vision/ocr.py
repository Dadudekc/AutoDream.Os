"""
OCR Text Extraction - V2 Compliant
=================================

OCR functionality for extracting text from captured images.
Provides text recognition with preprocessing for better accuracy.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
License: MIT
"""

import logging
import time

# Optional dependencies for OCR
try:
    import cv2
    import numpy as np
    import pytesseract

    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("pytesseract or opencv not available - OCR disabled")

# V2 Integration imports
try:
    from ..core.unified_config import get_unified_config
    from ..core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")

    # Fallback implementations
    def get_unified_config():
        return type("MockConfig", (), {"get_env": lambda x, y=None: y})()

    def get_logger(name):
        return logging.getLogger(name)


class TextExtractor:
    """
    OCR text extraction with preprocessing.

    Provides text recognition capabilities with:
    - Image preprocessing for better accuracy
    - Confidence thresholding
    - Text region detection
    - Multiple language support
    """

    def __init__(self, config: dict | None = None):
        """
        Initialize OCR text extractor.

        Args:
            config: Configuration dictionary (uses config/vision.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)

        # V2 Integration
        self.unified_config = get_unified_config()

        # OCR settings
        self.language = self.config.get("ocr", {}).get("language", "eng")
        self.confidence_threshold = self.config.get("ocr", {}).get("confidence_threshold", 60)

        # Preprocessing settings
        preprocessing_config = self.config.get("ocr", {}).get("preprocessing", {})
        self.denoise = preprocessing_config.get("denoise", True)
        self.threshold_method = preprocessing_config.get("threshold", "otsu")
        self.scale_factor = preprocessing_config.get("scale_factor", 2.0)

        # Validate Tesseract availability
        self.tesseract_available = TESSERACT_AVAILABLE
        if TESSERACT_AVAILABLE:
            try:
                pytesseract.get_tesseract_version()
                self.logger.info("Tesseract OCR engine available")
            except Exception as e:
                self.logger.warning(f"Tesseract not properly installed: {e}")
                self.tesseract_available = False
        else:
            self.logger.warning("OCR functionality disabled - dependencies not available")

    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from image using OCR.

        Args:
            image: Input image array

        Returns:
            Extracted text string
        """
        if not self.tesseract_available:
            self.logger.warning("OCR not available - returning empty string")
            return ""

        try:
            # Preprocess image for better OCR
            processed_image = self._preprocess_image(image)

            # Extract text
            text = pytesseract.image_to_string(
                processed_image,
                lang=self.language,
                config="--psm 6",  # Uniform block of text
            )

            # Clean up text
            text = text.strip()

            self.logger.info(f"Text extracted: {len(text)} characters")
            return text

        except Exception as e:
            self.logger.error(f"OCR failed: {e}")
            return ""

    def find_text_regions(self, image: np.ndarray) -> list[dict]:
        """
        Find regions containing text with confidence scores.

        Args:
            image: Input image array

        Returns:
            List of dictionaries with text regions and metadata
        """
        if not self.tesseract_available:
            self.logger.warning("OCR not available - returning empty regions")
            return []

        try:
            # Preprocess image
            processed_image = self._preprocess_image(image)

            # Get detailed OCR data
            data = pytesseract.image_to_data(
                processed_image, lang=self.language, output_type=pytesseract.Output.DICT
            )

            text_regions = []
            for i, text in enumerate(data["text"]):
                if text.strip() and data["conf"][i] >= self.confidence_threshold:
                    region = {
                        "text": text.strip(),
                        "position": (data["left"][i], data["top"][i]),
                        "size": (data["width"][i], data["height"][i]),
                        "confidence": data["conf"][i],
                        "bbox": (
                            data["left"][i],
                            data["top"][i],
                            data["left"][i] + data["width"][i],
                            data["top"][i] + data["height"][i],
                        ),
                    }
                    text_regions.append(region)

            self.logger.info(f"Found {len(text_regions)} text regions")
            return text_regions

        except Exception as e:
            self.logger.error(f"Text region detection failed: {e}")
            return []

    def extract_text_with_regions(self, image: np.ndarray) -> dict:
        """
        Extract text with region information.

        Args:
            image: Input image array

        Returns:
            Dictionary with extracted text and region data
        """
        return {
            "full_text": self.extract_text(image),
            "text_regions": self.find_text_regions(image),
            "extraction_time": time.time(),
            "language": self.language,
            "confidence_threshold": self.confidence_threshold,
        }

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy.

        Args:
            image: Input image array

        Returns:
            Preprocessed image array
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image.copy()

            # Scale up for better OCR
            if self.scale_factor > 1.0:
                height, width = gray.shape
                new_height = int(height * self.scale_factor)
                new_width = int(width * self.scale_factor)
                gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

            # Denoise if enabled
            if self.denoise:
                gray = cv2.fastNlMeansDenoising(gray)

            # Apply threshold
            if self.threshold_method == "otsu":
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            elif self.threshold_method == "adaptive":
                thresh = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
            elif self.threshold_method == "binary":
                _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            else:
                thresh = gray

            return thresh

        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {e}")
            return image

    def set_language(self, language: str) -> None:
        """Set OCR language."""
        self.language = language
        self.logger.info(f"OCR language set to: {language}")

    def set_confidence_threshold(self, threshold: int) -> None:
        """Set confidence threshold for text detection."""
        self.confidence_threshold = threshold
        self.logger.info(f"Confidence threshold set to: {threshold}")

    def get_available_languages(self) -> list[str]:
        """Get list of available OCR languages."""
        if not self.tesseract_available:
            return []

        try:
            languages = pytesseract.get_languages()
            return languages
        except Exception as e:
            self.logger.error(f"Failed to get available languages: {e}")
            return []

    def get_ocr_info(self) -> dict[str, any]:
        """Get information about OCR capabilities."""
        return {
            "tesseract_available": self.tesseract_available,
            "language": self.language,
            "confidence_threshold": self.confidence_threshold,
            "denoise_enabled": self.denoise,
            "threshold_method": self.threshold_method,
            "scale_factor": self.scale_factor,
            "available_languages": self.get_available_languages(),
        }
