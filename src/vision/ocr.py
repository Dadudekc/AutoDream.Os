"""
OCR Text Extraction - V2 Compliant
=================================

OCR functionality for extracting text from captured images.
Provides text recognition with preprocessing for better accuracy.

V2 Compliance: ≤200 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
Optimized: Agent-7 - Repository Cloning Specialist (V2 consolidation)
License: MIT
"""

import logging

import numpy as np

# Optional dependencies for OCR
try:
    import cv2
    import pytesseract

    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("pytesseract or opencv not available - OCR disabled")

# V2 Integration imports (uses fallbacks if unavailable)
from .utils import get_logger, get_unified_config


class TextExtractor:
    """
    OCR text extraction with preprocessing.

    Capabilities:
    - Image preprocessing for better accuracy
    - Confidence thresholding
    - Text region detection
    - Multiple language support
    """

    def __init__(self, config: dict | None = None):
        """Initialize OCR text extractor."""
        self.config = config or {}
        self.logger = get_logger(__name__)

        # V2 Integration
        self.unified_config = get_unified_config()

        # OCR settings
        ocr_config = self.config.get("ocr", {})
        self.language = ocr_config.get("language", "eng")
        self.confidence_threshold = ocr_config.get("confidence_threshold", 60)

        # Preprocessing settings
        preprocessing = ocr_config.get("preprocessing", {})
        self.denoise = preprocessing.get("denoise", True)
        self.threshold_method = preprocessing.get("threshold", "otsu")
        self.scale_factor = preprocessing.get("scale_factor", 2.0)

        # Validate Tesseract
        self.tesseract_available = self._check_tesseract()

    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from image using OCR.

        Args:
            image: Input image array

        Returns:
            Extracted text string
        """
        if not self.tesseract_available:
            return ""

        try:
            processed = self.preprocess_image(image)
            text = pytesseract.image_to_string(processed, lang=self.language)
            self.logger.info(f"Text extracted: {len(text)} characters")
            return text.strip()

        except Exception as e:
            self.logger.error(f"Text extraction failed: {e}")
            return ""

    def extract_text_with_regions(self, image: np.ndarray) -> dict:
        """
        Extract text with bounding box regions.

        Args:
            image: Input image array

        Returns:
            Dictionary with text and region information
        """
        if not self.tesseract_available:
            return {"text": "", "regions": [], "word_count": 0}

        try:
            processed = self.preprocess_image(image)

            # Get detailed OCR data
            data = pytesseract.image_to_data(
                processed, lang=self.language, output_type=pytesseract.Output.DICT
            )

            # Extract regions with confidence filtering
            regions = self._extract_regions(data)

            # Get full text
            text = pytesseract.image_to_string(processed, lang=self.language).strip()

            return {
                "text": text,
                "regions": regions,
                "word_count": len(regions),
                "average_confidence": (
                    sum(r["confidence"] for r in regions) / len(regions) if regions else 0
                ),
            }

        except Exception as e:
            self.logger.error(f"Text extraction with regions failed: {e}")
            return {"text": "", "regions": [], "word_count": 0}

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy.

        Args:
            image: Input image array

        Returns:
            Preprocessed image array
        """
        if not TESSERACT_AVAILABLE:
            return image

        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image.copy()

            # Scale up for better recognition
            if self.scale_factor != 1.0:
                gray = cv2.resize(
                    gray,
                    None,
                    fx=self.scale_factor,
                    fy=self.scale_factor,
                    interpolation=cv2.INTER_CUBIC,
                )

            # Denoise
            if self.denoise:
                gray = cv2.fastNlMeansDenoising(gray)

            # Apply thresholding
            if self.threshold_method == "otsu":
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            elif self.threshold_method == "adaptive":
                thresh = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                )
            else:
                thresh = gray

            return thresh

        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {e}")
            return image

    def _check_tesseract(self) -> bool:
        """Check if Tesseract is available and properly installed."""
        if not TESSERACT_AVAILABLE:
            self.logger.warning("OCR disabled - dependencies not available")
            return False

        try:
            pytesseract.get_tesseract_version()
            self.logger.info("Tesseract OCR engine available")
            return True
        except Exception as e:
            self.logger.warning(f"Tesseract not properly installed: {e}")
            return False

    def _extract_regions(self, data: dict) -> list[dict]:
        """Extract text regions with confidence filtering."""
        regions = []

        for i, text in enumerate(data["text"]):
            conf = int(data["conf"][i])

            # Filter by confidence threshold
            if conf >= self.confidence_threshold and text.strip():
                regions.append(
                    {
                        "text": text,
                        "confidence": conf,
                        "bbox": (
                            data["left"][i],
                            data["top"][i],
                            data["width"][i],
                            data["height"][i],
                        ),
                    }
                )

        return regions

    def get_extractor_info(self) -> dict:
        """Get information about extractor capabilities."""
        return {
            "tesseract_available": self.tesseract_available,
            "language": self.language,
            "confidence_threshold": self.confidence_threshold,
            "preprocessing": {
                "denoise": self.denoise,
                "threshold_method": self.threshold_method,
                "scale_factor": self.scale_factor,
            },
        }
