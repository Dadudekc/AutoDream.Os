import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import os
import json
import logging

class PyTorchInfrastructure:
    """
    Provides PyTorch infrastructure for ML model deployment and management.
    Handles model creation, training, and prediction capabilities.
    """

    def __init__(self, model_path: str = "/app/models", data_path: str = "/app/data"):
        """
        Initializes the PyTorch infrastructure.

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
        self.loaded_models: Dict[str, nn.Module] = {}
        self.logger = logging.getLogger(__name__)

        # Ensure directories exist
        os.makedirs(model_path, exist_ok=True)
        os.makedirs(data_path, exist_ok=True)

        # Configure PyTorch for optimal performance
        self._configure_pytorch()

    def _configure_pytorch(self) -> None:
        """Configures PyTorch for optimal performance."""
        # Set device (GPU if available, otherwise CPU)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.logger.info(f"Using device: {self.device}")

        # Configure CUDA if available
        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = True
            self.logger.info(f"CUDA available: {torch.cuda.get_device_name(0)}")

    def create_sample_model(self, model_name: str, input_size: int = 784, num_classes: int = 10) -> nn.Module:
        """
        Creates a sample neural network model for demonstration.

        Args:
            model_name: Name identifier for the model.
            input_size: Size of input features.
            num_classes: Number of output classes.

        Returns:
            A PyTorch neural network model.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if input_size <= 0:
            raise ValueError("Input size must be positive.")
        if num_classes <= 0:
            raise ValueError("Number of classes must be positive.")

        class SampleNet(nn.Module):
            def __init__(self, input_size: int, num_classes: int):
                super(SampleNet, self).__init__()
                self.fc1 = nn.Linear(input_size, 128)
                self.fc2 = nn.Linear(128, 64)
                self.fc3 = nn.Linear(64, num_classes)
                self.relu = nn.ReLU()
                self.dropout = nn.Dropout(0.2)

            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.dropout(x)
                x = self.relu(self.fc2(x))
                x = self.dropout(x)
                x = self.fc3(x)
                return x

        model = SampleNet(input_size, num_classes)
        model = model.to(self.device)
        self.loaded_models[model_name] = model
        self.logger.info(f"Created sample model: {model_name}")
        return model

    def save_model(self, model: nn.Module, model_name: str, version: str = "1.0") -> str:
        """
        Saves a model to the specified path.

        Args:
            model: The PyTorch model to save.
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

        save_path = os.path.join(self.model_path, f"{model_name}_v{version}.pth")
        torch.save({
            'model_state_dict': model.state_dict(),
            'model_name': model_name,
            'version': version
        }, save_path)
        self.logger.info(f"Model saved: {save_path}")
        return save_path

    def load_model(self, model_name: str, version: str = "1.0") -> nn.Module:
        """
        Loads a model from the specified path.

        Args:
            model_name: Name identifier for the model.
            version: Version identifier for the model.

        Returns:
            The loaded PyTorch model.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if not version:
            raise ValueError("Version cannot be empty.")

        model_path = os.path.join(self.model_path, f"{model_name}_v{version}.pth")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        checkpoint = torch.load(model_path, map_location=self.device)
        model = self.loaded_models.get(model_name)
        if model is None:
            raise ValueError(f"Model '{model_name}' not found in loaded models.")

        model.load_state_dict(checkpoint['model_state_dict'])
        model = model.to(self.device)
        self.logger.info(f"Model loaded: {model_path}")
        return model

    def predict(self, model_name: str, data: torch.Tensor) -> torch.Tensor:
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
        model.eval()
        
        with torch.no_grad():
            data = data.to(self.device)
            predictions = model(data)
            predictions = torch.softmax(predictions, dim=1)

        self.logger.info(f"Predictions made using model: {model_name}")
        return predictions

    def train_model(self, model: nn.Module, x_train: np.ndarray, y_train: np.ndarray,
                   x_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None,
                   epochs: int = 10, batch_size: int = 32, learning_rate: float = 0.001) -> Dict[str, List[float]]:
        """
        Trains a model with the provided data.

        Args:
            model: The PyTorch model to train.
            x_train: Training input data.
            y_train: Training target data.
            x_val: Validation input data (optional).
            y_val: Validation target data (optional).
            epochs: Number of training epochs.
            batch_size: Batch size for training.
            learning_rate: Learning rate for optimization.

        Returns:
            Training history dictionary.
        """
        if not model:
            raise ValueError("Model cannot be None.")
        if not isinstance(x_train, np.ndarray) or not isinstance(y_train, np.ndarray):
            raise ValueError("Training data must be numpy arrays.")

        # Convert numpy arrays to PyTorch tensors
        x_train_tensor = torch.FloatTensor(x_train)
        y_train_tensor = torch.LongTensor(y_train)
        
        # Create data loaders
        train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

        val_loader = None
        if x_val is not None and y_val is not None:
            x_val_tensor = torch.FloatTensor(x_val)
            y_val_tensor = torch.LongTensor(y_val)
            val_dataset = TensorDataset(x_val_tensor, y_val_tensor)
            val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

        # Setup training
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        
        # Training history
        history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

        model.train()
        for epoch in range(epochs):
            # Training phase
            train_loss = 0.0
            train_correct = 0
            train_total = 0

            for batch_x, batch_y in train_loader:
                batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()

                train_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                train_total += batch_y.size(0)
                train_correct += (predicted == batch_y).sum().item()

            # Validation phase
            val_loss = 0.0
            val_correct = 0
            val_total = 0

            if val_loader:
                model.eval()
                with torch.no_grad():
                    for batch_x, batch_y in val_loader:
                        batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
                        outputs = model(batch_x)
                        loss = criterion(outputs, batch_y)

                        val_loss += loss.item()
                        _, predicted = torch.max(outputs.data, 1)
                        val_total += batch_y.size(0)
                        val_correct += (predicted == batch_y).sum().item()
                model.train()

            # Record history
            history['train_loss'].append(train_loss / len(train_loader))
            history['train_acc'].append(100 * train_correct / train_total)
            if val_loader:
                history['val_loss'].append(val_loss / len(val_loader))
                history['val_acc'].append(100 * val_correct / val_total)

            self.logger.info(f"Epoch {epoch+1}/{epochs}: "
                           f"Train Loss: {history['train_loss'][-1]:.4f}, "
                           f"Train Acc: {history['train_acc'][-1]:.2f}%")

        self.logger.info(f"Model training completed: {epochs} epochs")
        return history

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
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

        return {
            "name": model_name,
            "device": str(self.device),
            "total_params": total_params,
            "trainable_params": trainable_params,
            "model_type": type(model).__name__
        }



