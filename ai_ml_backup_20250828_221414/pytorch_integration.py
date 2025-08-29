from pathlib import Path
from typing import Any, Dict, List

    import torch
    import torch.nn as nn
    import torch.optim as optim
from .integration_common import logger
from __future__ import annotations

"""PyTorch framework integration for deep learning."""




try:
except ImportError as exc:  # pragma: no cover - dependency not installed
    raise ImportError(
        "PyTorch package not available. Install with: pip install torch"
    ) from exc


class PyTorchIntegration:
    """Convenience wrapper around common PyTorch operations."""

    def __init__(self) -> None:
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.is_initialized = False
        logger.info("PyTorch integration initialized on device: %s", self.device)

    def initialize(self) -> bool:
        """Initialize PyTorch framework."""
        try:
            if torch.cuda.is_available():
                logger.info("CUDA available: %s", torch.cuda.get_device_name(0))
                logger.info("CUDA version: %s", torch.version.cuda)

            if self.device.type == "cuda":
                torch.set_default_tensor_type(torch.cuda.FloatTensor)

            self.is_initialized = True
            logger.info("PyTorch framework initialized successfully")
            return True
        except Exception as err:  # pragma: no cover - hardware dependent
            logger.error("Error initializing PyTorch: %s", err)
            return False

    def create_neural_network(
        self, layers: List[int], activation: str = "relu"
    ) -> nn.Module:
        """Create a simple feed-forward neural network."""
        try:
            if not self.is_initialized:
                self.initialize()

            class SimpleNN(nn.Module):
                def __init__(self, layer_sizes: List[int], activation_func: str):
                    super().__init__()
                    self.layers = nn.ModuleList()

                    for i in range(len(layer_sizes) - 1):
                        self.layers.append(
                            nn.Linear(layer_sizes[i], layer_sizes[i + 1])
                        )
                        if i < len(layer_sizes) - 2:
                            if activation_func.lower() == "relu":
                                self.layers.append(nn.ReLU())
                            elif activation_func.lower() == "tanh":
                                self.layers.append(nn.Tanh())
                            elif activation_func.lower() == "sigmoid":
                                self.layers.append(nn.Sigmoid())

                def forward(self, x):  # type: ignore[override]
                    for layer in self.layers:
                        x = layer(x)
                    return x

            model = SimpleNN(layers, activation)
            model.to(self.device)
            logger.info("Created neural network with layers: %s", layers)
            return model
        except Exception as err:  # pragma: no cover - runtime errors
            logger.error("Error creating neural network: %s", err)
            raise

    def train_model(
        self,
        model: nn.Module,
        train_loader: Any,
        epochs: int = 100,
        learning_rate: float = 0.001,
    ) -> Dict[str, Any]:
        """Train a PyTorch model."""
        try:
            if not self.is_initialized:
                self.initialize()

            model.train()
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=learning_rate)
            history: Dict[str, List[float]] = {
                "epochs": [],
                "losses": [],
                "accuracies": [],
            }

            for epoch in range(epochs):
                running_loss = 0.0
                correct = 0
                total = 0

                for data, targets in train_loader:
                    data, targets = data.to(self.device), targets.to(self.device)
                    optimizer.zero_grad()
                    outputs = model(data)
                    loss = criterion(outputs, targets)
                    loss.backward()
                    optimizer.step()

                    running_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += targets.size(0)
                    correct += (predicted == targets).sum().item()

                epoch_loss = running_loss / len(train_loader)
                epoch_accuracy = 100 * correct / total

                history["epochs"].append(epoch)
                history["losses"].append(epoch_loss)
                history["accuracies"].append(epoch_accuracy)

                if epoch % 10 == 0:
                    logger.info(
                        "Epoch %s: Loss = %.4f, Accuracy = %.2f%%",
                        epoch,
                        epoch_loss,
                        epoch_accuracy,
                    )

            logger.info("Model training completed")
            return history
        except Exception as err:  # pragma: no cover - runtime errors
            logger.error("Error training model: %s", err)
            raise

    def evaluate_model(self, model: nn.Module, test_loader: Any) -> Dict[str, float]:
        """Evaluate a trained PyTorch model."""
        try:
            if not self.is_initialized:
                self.initialize()

            model.eval()
            correct = 0
            total = 0
            running_loss = 0.0
            criterion = nn.CrossEntropyLoss()

            with torch.no_grad():
                for data, targets in test_loader:
                    data, targets = data.to(self.device), targets.to(self.device)
                    outputs = model(data)
                    loss = criterion(outputs, targets)
                    running_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += targets.size(0)
                    correct += (predicted == targets).sum().item()

            accuracy = 100 * correct / total
            avg_loss = running_loss / len(test_loader)
            logger.info(
                "Model evaluation completed: Accuracy = %.2f%%, Loss = %.4f",
                accuracy,
                avg_loss,
            )
            return {
                "accuracy": accuracy,
                "loss": avg_loss,
                "correct_predictions": correct,
                "total_samples": total,
            }
        except Exception as err:  # pragma: no cover - runtime errors
            logger.error("Error evaluating model: %s", err)
            raise

    def save_model(self, model: nn.Module, path: str) -> bool:
        """Save a PyTorch model to disk."""
        try:
            if not self.is_initialized:
                self.initialize()

            save_path = Path(path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), path)
            logger.info("Model saved to: %s", path)
            return True
        except Exception as err:  # pragma: no cover - file system errors
            logger.error("Error saving model: %s", err)
            return False

    def load_model(
        self, path: str, model_class: type[nn.Module], *args: Any, **kwargs: Any
    ) -> nn.Module:
        """Load a PyTorch model from disk."""
        try:
            if not self.is_initialized:
                self.initialize()

            model = model_class(*args, **kwargs)
            model.load_state_dict(torch.load(path, map_location=self.device))
            model.to(self.device)
            logger.info("Model loaded from: %s", path)
            return model
        except Exception as err:  # pragma: no cover - file system errors
            logger.error("Error loading model: %s", err)
            raise

    def get_model_summary(self, model: nn.Module) -> Dict[str, Any]:
        """Get a summary of model architecture and parameters."""
        try:
            total_params = sum(p.numel() for p in model.parameters())
            trainable_params = sum(
                p.numel() for p in model.parameters() if p.requires_grad
            )
            summary = {
                "total_parameters": total_params,
                "trainable_parameters": trainable_params,
                "non_trainable_parameters": total_params - trainable_params,
                "device": str(self.device),
                "model_class": model.__class__.__name__,
                "layers": [],
            }

            for name, layer in model.named_modules():
                if len(list(layer.children())) == 0:
                    layer_info = {
                        "name": name,
                        "type": layer.__class__.__name__,
                        "parameters": sum(p.numel() for p in layer.parameters()),
                        "shape": str(layer) if hasattr(layer, "weight") else "N/A",
                    }
                    summary["layers"].append(layer_info)

            logger.info("Model summary generated: %s total parameters", total_params)
            return summary
        except Exception as err:  # pragma: no cover - runtime errors
            logger.error("Error generating model summary: %s", err)
            return {"error": str(err)}
