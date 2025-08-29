"""Filter processing utilities for the webcam system."""
import logging
from typing import Dict, Any, List, Optional
import cv2
import numpy as np

logger = logging.getLogger(__name__)


class WebcamFilterProcessor:
    """Manage filter pipeline and apply filter effects."""

    def __init__(self):
        self.active_filters: Dict[str, Dict[str, Any]] = {}
        self.filter_pipeline: List[Dict[str, Any]] = []
        self.available_filters: Dict[str, Any] = {}
        self._load_available_filters()

    # --- pipeline management ---
    def add_filter(
        self, filter_name: str, parameters: Optional[Dict[str, Any]] = None
    ) -> bool:
        if filter_name not in self.available_filters:
            logger.error(f"❌ Filter '{filter_name}' not found")
            return False
        filter_config = {
            "name": filter_name,
            "function": self.available_filters[filter_name],
            "parameters": parameters or {},
            "enabled": True,
        }
        self.filter_pipeline.append(filter_config)
        self.active_filters[filter_name] = filter_config
        logger.info(f"✅ Added filter: {filter_name}")
        return True

    def remove_filter(self, filter_name: str) -> bool:
        for i, filter_config in enumerate(self.filter_pipeline):
            if filter_config["name"] == filter_name:
                del self.filter_pipeline[i]
                self.active_filters.pop(filter_name, None)
                logger.info(f"✅ Removed filter: {filter_name}")
                return True
        logger.warning(f"⚠️ Filter '{filter_name}' not found in pipeline")
        return False

    def clear_filters(self) -> bool:
        self.filter_pipeline.clear()
        self.active_filters.clear()
        logger.info("✅ Cleared all filters")
        return True

    # --- processing ---
    def apply_filter_pipeline(self, frame: np.ndarray) -> np.ndarray:
        processed_frame = frame.copy()
        for filter_config in self.filter_pipeline:
            if filter_config["enabled"]:
                try:
                    filter_func = filter_config["function"]
                    params = filter_config["parameters"]
                    processed_frame = filter_func(processed_frame, **params)
                except Exception as e:
                    logger.error(f"❌ Filter '{filter_config['name']}' failed: {e}")
        return processed_frame

    # --- available filters ---
    def _load_available_filters(self):
        self.available_filters = {
            "blur": self._apply_blur_filter,
            "sharpen": self._apply_sharpen_filter,
            "smooth": self._apply_smooth_filter,
            "emboss": self._apply_emboss_filter,
            "edge_enhance": self._apply_edge_enhance_filter,
            "grayscale": self._apply_grayscale_filter,
            "sepia": self._apply_sepia_filter,
            "invert": self._apply_invert_filter,
            "posterize": self._apply_posterize_filter,
            "solarize": self._apply_solarize_filter,
            "cartoon": self._apply_cartoon_filter,
            "sketch": self._apply_sketch_filter,
            "oil_painting": self._apply_oil_painting_filter,
            "watercolor": self._apply_watercolor_filter,
            "pixelate": self._apply_pixelate_filter,
            "glitch": self._apply_glitch_filter,
            "vintage": self._apply_vintage_filter,
            "neon": self._apply_neon_filter,
            "hologram": self._apply_hologram_filter,
            "matrix": self._apply_matrix_filter,
            "face_detection": self._apply_face_detection_filter,
            "face_swap": self._apply_face_swap_filter,
            "age_progression": self._apply_age_progression_filter,
            "emotion_detection": self._apply_emotion_detection_filter,
            "background_blur": self._apply_background_blur_filter,
            "background_replacement": self._apply_background_replacement_filter,
            "green_screen": self._apply_green_screen_filter,
            "virtual_background": self._apply_virtual_background_filter,
        }
        logger.info(f"✅ Loaded {len(self.available_filters)} available filters")

    def get_available_filters(self) -> List[str]:
        return list(self.available_filters.keys())

    def get_filter_parameters(self, filter_name: str) -> Optional[Dict[str, Any]]:
        default_params = {
            "blur": {"intensity": 0.5},
            "sharpen": {"intensity": 0.5},
            "smooth": {"intensity": 0.5},
            "emboss": {"intensity": 0.5},
            "edge_enhance": {"intensity": 0.5},
            "sepia": {"intensity": 0.8},
            "posterize": {"levels": 4},
            "solarize": {"threshold": 128},
            "cartoon": {"intensity": 0.5},
            "sketch": {"intensity": 0.5},
            "oil_painting": {"intensity": 0.5},
            "watercolor": {"intensity": 0.5},
            "pixelate": {"pixel_size": 10},
            "glitch": {"intensity": 0.3},
            "vintage": {"intensity": 0.6},
            "neon": {"intensity": 0.5},
            "hologram": {"intensity": 0.4},
            "matrix": {"intensity": 0.6},
            "face_detection": {"intensity": 0.5},
            "face_swap": {"intensity": 0.5},
            "age_progression": {"intensity": 0.5},
            "emotion_detection": {"intensity": 0.5},
            "background_blur": {"intensity": 0.7},
            "background_replacement": {"intensity": 0.6},
            "green_screen": {"intensity": 0.8},
            "virtual_background": {"intensity": 0.7},
        }
        return default_params.get(filter_name, {})

    # ===== FILTER IMPLEMENTATIONS =====
    def _apply_blur_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        kernel_size = int(15 * intensity) + 1
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

    def _apply_sharpen_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) * intensity
        return cv2.filter2D(frame, -1, kernel)

    def _apply_smooth_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        kernel_size = int(10 * intensity) + 1
        if kernel_size % 2 == 0:
            kernel_size += 1
        return cv2.medianBlur(frame, kernel_size)

    def _apply_emboss_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]]) * intensity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        embossed = cv2.filter2D(gray, -1, kernel) + 128
        return cv2.cvtColor(embossed.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def _apply_edge_enhance_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        enhanced = cv2.addWeighted(gray, 1 - intensity, edges, intensity, 0)
        return cv2.cvtColor(enhanced.astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def _apply_grayscale_filter(self, frame: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def _apply_sepia_filter(
        self, frame: np.ndarray, intensity: float = 0.8
    ) -> np.ndarray:
        sepia_matrix = np.array(
            [[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]]
        )
        sepia_frame = cv2.transform(frame, sepia_matrix)
        return cv2.addWeighted(frame, 1 - intensity, sepia_frame, intensity, 0)

    def _apply_invert_filter(self, frame: np.ndarray) -> np.ndarray:
        return cv2.bitwise_not(frame)

    def _apply_posterize_filter(self, frame: np.ndarray, levels: int = 4) -> np.ndarray:
        factor = 256 // levels
        return (frame // factor) * factor

    def _apply_solarize_filter(
        self, frame: np.ndarray, threshold: int = 128
    ) -> np.ndarray:
        solarized = frame.copy()
        solarized[frame > threshold] = 255 - frame[frame > threshold]
        return solarized

    def _apply_cartoon_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
        )
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))
        return cv2.addWeighted(frame, 1 - intensity, cartoon, intensity, 0)

    def _apply_sketch_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256)
        return cv2.addWeighted(
            frame, 1 - intensity, cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR), intensity, 0
        )

    def _apply_oil_painting_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        kernel_size = int(5 * intensity) + 1
        if kernel_size % 2 == 0:
            kernel_size += 1
        oil_painted = cv2.bilateralFilter(frame, kernel_size, 75, 75)
        return cv2.addWeighted(frame, 1 - intensity, oil_painted, intensity, 0)

    def _apply_watercolor_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        watercolor = cv2.bilateralFilter(frame, 9, 75, 75)
        watercolor = cv2.GaussianBlur(watercolor, (3, 3), 0)
        return cv2.addWeighted(frame, 1 - intensity, watercolor, intensity, 0)

    def _apply_pixelate_filter(
        self, frame: np.ndarray, pixel_size: int = 10
    ) -> np.ndarray:
        height, width = frame.shape[:2]
        small = cv2.resize(frame, (width // pixel_size, height // pixel_size))
        return cv2.resize(small, (width, height), interpolation=cv2.INTER_NEAREST)

    def _apply_glitch_filter(
        self, frame: np.ndarray, intensity: float = 0.3
    ) -> np.ndarray:
        glitched = frame.copy()
        if np.random.random() < intensity:
            shift = np.random.randint(-20, 20)
            glitched = np.roll(glitched, shift, axis=1)
        if np.random.random() < intensity:
            channel = np.random.randint(0, 3)
            shift = np.random.randint(-10, 10)
            glitched[:, :, channel] = np.roll(glitched[:, :, channel], shift, axis=1)
        return glitched

    def _apply_vintage_filter(
        self, frame: np.ndarray, intensity: float = 0.6
    ) -> np.ndarray:
        vintage = frame.astype(np.float32) / 255.0
        vintage[:, :, 0] *= 1.2
        vintage[:, :, 1] *= 0.8
        vintage[:, :, 2] *= 0.9
        vintage = np.clip(vintage, 0, 1)
        vintage = (vintage * 255).astype(np.uint8)
        return cv2.addWeighted(frame, 1 - intensity, vintage, intensity, 0)

    def _apply_neon_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges = cv2.GaussianBlur(edges, (5, 5), 0)
        colored_edges = cv2.applyColorMap(edges, cv2.COLORMAP_HOT)
        return cv2.addWeighted(frame, 1 - intensity, colored_edges, intensity, 0)

    def _apply_hologram_filter(
        self, frame: np.ndarray, intensity: float = 0.4
    ) -> np.ndarray:
        hologram = cv2.applyColorMap(frame, cv2.COLORMAP_WINTER)
        hologram = cv2.addWeighted(frame, 1 - intensity, hologram, intensity, 0)
        return hologram

    def _apply_matrix_filter(
        self, frame: np.ndarray, intensity: float = 0.6
    ) -> np.ndarray:
        matrix = np.zeros_like(frame)
        green_channel = np.random.randint(0, 255, frame.shape[:2], dtype=np.uint8)
        matrix[:, :, 1] = green_channel
        return cv2.addWeighted(frame, 1 - intensity, matrix, intensity, 0)

    def _apply_face_detection_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame

    def _apply_face_swap_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        return frame  # Placeholder for complex implementation

    def _apply_age_progression_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        return frame  # Placeholder

    def _apply_emotion_detection_filter(
        self, frame: np.ndarray, intensity: float = 0.5
    ) -> np.ndarray:
        return frame  # Placeholder

    def _apply_background_blur_filter(
        self, frame: np.ndarray, intensity: float = 0.7
    ) -> np.ndarray:
        blurred = cv2.GaussianBlur(frame, (0, 0), sigmaX=15)
        return cv2.addWeighted(frame, 1 - intensity, blurred, intensity, 0)

    def _apply_background_replacement_filter(
        self, frame: np.ndarray, intensity: float = 0.6
    ) -> np.ndarray:
        background = np.full_like(frame, [255, 0, 0])
        return cv2.addWeighted(frame, 1 - intensity, background, intensity, 0)

    def _apply_green_screen_filter(
        self, frame: np.ndarray, intensity: float = 0.8
    ) -> np.ndarray:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        background = np.full_like(frame, [0, 0, 255])
        green_screened = np.where(mask[:, :, np.newaxis] == 255, background, frame)
        return cv2.addWeighted(frame, 1 - intensity, green_screened, intensity, 0)

    def _apply_virtual_background_filter(
        self, frame: np.ndarray, intensity: float = 0.7
    ) -> np.ndarray:
        height, width = frame.shape[:2]
        virtual_bg = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(0, height, 20):
            for j in range(0, width, 20):
                color = np.random.randint(0, 255, 3)
                virtual_bg[i : i + 20, j : j + 20] = color
        return cv2.addWeighted(frame, 1 - intensity, virtual_bg, intensity, 0)
