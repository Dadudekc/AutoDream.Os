import tensorflow as tf
import numpy as np
from typing import Dict, Any, Optional, List
import os
import json
import logging

class TensorFlowInfrastructure:
    """
    Provides TensorFlow infrastructure for ML model deployment and management.
    Handles model loading, prediction, and basic training capabilities.
    """

    def __init__(self, model_path: str = "/app/models", data_path: str = "/app/data"):
        """
        Initializes the TensorFlow infrastructure.

        Args:
            model_path: Path to store and load models.
            data_path: Path to training and validation data.
        """
        if not model_path:
            raise ValueError("Model path cannot be empty.")
        if not data_path:
            raise ValueError("Data path cannot be empty.")

        self.model_path = model_path
        self.data_path = data_path
        self.loaded_models: Dict[str, tf.keras.Model] = {}
        self.logger = logging.getLogger(__name__)

        # Ensure directories exist
        os.makedirs(model_path, exist_ok=True)
        os.makedirs(data_path, exist_ok=True)

        # Configure TensorFlow for optimal performance
        self._configure_tensorflow()

    def _configure_tensorflow(self) -> None:
        """Configures TensorFlow for optimal performance."""
        # Enable mixed precision for better performance
        tf.keras.mixed_precision.set_global_policy('mixed_float16')
        
        # Configure GPU memory growth
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                self.logger.info(f"Configured {len(gpus)} GPU(s) for memory growth")
            except RuntimeError as e:
                self.logger.warning(f"GPU configuration failed: {e}")
        else:
            self.logger.info("No GPU devices found, using CPU")

    def create_sample_model(self, model_name: str, input_shape: tuple = (28, 28, 1)) -> tf.keras.Model:
        """
        Creates a sample neural network model for demonstration.

        Args:
            model_name: Name identifier for the model.
            input_shape: Shape of input data.

        Returns:
            A compiled Keras model.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if not isinstance(input_shape, tuple) or len(input_shape) != 3:
            raise ValueError("Input shape must be a 3-tuple (height, width, channels).")

        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        self.loaded_models[model_name] = model
        self.logger.info(f"Created sample model: {model_name}")
        return model

    def save_model(self, model: tf.keras.Model, model_name: str, version: str = "1.0") -> str:
        """
        Saves a model to the specified path.

        Args:
            model: The Keras model to save.
            model_name: Name identifier for the model.
            version: Version identifier for the model.

        Returns:
            Path where the model was saved.
        """
        if not model:
            raise ValueError("Model cannot be None.")
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if not version:
            raise ValueError("Version cannot be empty.")

        save_path = os.path.join(self.model_path, f"{model_name}_v{version}")
        model.save(save_path)
        self.logger.info(f"Model saved: {save_path}")
        return save_path

    def load_model(self, model_name: str, version: str = "1.0") -> tf.keras.Model:
        """
        Loads a model from the specified path.

        Args:
            model_name: Name identifier for the model.
            version: Version identifier for the model.

        Returns:
            The loaded Keras model.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if not version:
            raise ValueError("Version cannot be empty.")

        model_path = os.path.join(self.model_path, f"{model_name}_v{version}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        model = tf.keras.models.load_model(model_path)
        self.loaded_models[model_name] = model
        self.logger.info(f"Model loaded: {model_path}")
        return model

    def predict(self, model_name: str, data: np.ndarray) -> np.ndarray:
        """
        Makes predictions using a loaded model.

        Args:
            model_name: Name of the model to use for prediction.
            data: Input data for prediction.

        Returns:
            Model predictions.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if model_name not in self.loaded_models:
            raise ValueError(f"Model '{model_name}' not loaded.")

        model = self.loaded_models[model_name]
        predictions = model.predict(data)
        self.logger.info(f"Predictions made using model: {model_name}")
        return predictions

    def train_model(self, model: tf.keras.Model, x_train: np.ndarray, y_train: np.ndarray, 
                   x_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None,
                   epochs: int = 10, batch_size: int = 32) -> Dict[str, List[float]]:
        """
        Trains a model with the provided data.

        Args:
            model: The Keras model to train.
            x_train: Training input data.
            y_train: Training target data.
            x_val: Validation input data (optional).
            y_val: Validation target data (optional).
            epochs: Number of training epochs.
            batch_size: Batch size for training.

        Returns:
            Training history dictionary.
        """
        if not model:
            raise ValueError("Model cannot be None.")
        if not isinstance(x_train, np.ndarray) or not isinstance(y_train, np.ndarray):
            raise ValueError("Training data must be numpy arrays.")

        validation_data = None
        if x_val is not None and y_val is not None:
            validation_data = (x_val, y_val)

        history = model.fit(
            x_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )

        self.logger.info(f"Model training completed: {epochs} epochs")
        return history.history

    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Gets information about a loaded model.

        Args:
            model_name: Name of the model.

        Returns:
            Dictionary containing model information.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if model_name not in self.loaded_models:
            raise ValueError(f"Model '{model_name}' not loaded.")

        model = self.loaded_models[model_name]
        return {
            "name": model_name,
            "input_shape": model.input_shape,
            "output_shape": model.output_shape,
            "total_params": model.count_params(),
            "trainable_params": sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
        }



