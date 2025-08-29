"""Generic model evaluation utilities."""

from typing import Any, Dict, Optional

try:  # pragma: no cover - optional dependency
    import torch
    from torch import nn
except Exception:  # pragma: no cover - torch may not be installed
    torch = None
    nn = None


def evaluate_model(
    model: Any,
    data: Any = None,
    *,
    training_result: Optional[Dict[str, Any]] = None,
    criterion: Optional[Any] = None,
    device: Optional[Any] = None,
) -> Dict[str, float]:
    """Evaluate a model and return performance metrics.

    This helper first checks for ``training_result`` which contains a training
    history dictionary. When provided, final metrics are derived from that
    history. Otherwise, the function attempts to evaluate using the provided
    ``data`` loader. If the model implements an ``evaluate`` method it is used;
    otherwise a basic PyTorch evaluation loop is executed when ``torch`` is
    available.
    """

    # Evaluation based on recorded training history (used by ML robot modules)
    if training_result is not None:
        history = training_result.get("history", {})
        final_loss = history.get("loss", [1.0])[-1] if history.get("loss") else 1.0
        final_accuracy = (
            history.get("accuracy", [0.5])[-1] if history.get("accuracy") else 0.5
        )
        final_val_loss = (
            history.get("val_loss", [1.0])[-1] if history.get("val_loss") else 1.0
        )
        final_val_accuracy = (
            history.get("val_accuracy", [0.5])[-1]
            if history.get("val_accuracy")
            else 0.5
        )

        return {
            "loss": final_loss,
            "accuracy": final_accuracy,
            "val_loss": final_val_loss,
            "val_accuracy": final_val_accuracy,
            "overfitting_score": final_loss - final_val_loss,
        }

    if data is None:
        raise ValueError(
            "Either data or training_result must be provided for evaluation"
        )

    # Use model's own evaluation method if available
    if hasattr(model, "evaluate") and callable(getattr(model, "evaluate")):
        result = model.evaluate(data)
        if isinstance(result, dict):
            return result
        if isinstance(result, (list, tuple)):
            metrics: Dict[str, float] = {}
            if len(result) > 0:
                metrics["loss"] = float(result[0])
            if len(result) > 1:
                metrics["accuracy"] = float(result[1])
            return metrics
        return {"result": result}

    # Basic PyTorch evaluation loop
    if torch and isinstance(model, nn.Module):
        model.eval()
        correct = 0
        total = 0
        running_loss = 0.0
        crit = criterion or nn.CrossEntropyLoss()

        with torch.no_grad():
            for inputs, targets in data:
                if device is not None:
                    inputs, targets = inputs.to(device), targets.to(device)
                    model.to(device)
                outputs = model(inputs)
                loss = crit(outputs, targets)
                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += targets.size(0)
                correct += (predicted == targets).sum().item()

        accuracy = 100 * correct / total if total else 0.0
        avg_loss = running_loss / len(data) if len(data) else 0.0

        return {
            "accuracy": accuracy,
            "loss": avg_loss,
            "correct_predictions": correct,
            "total_samples": total,
        }

    raise ValueError("Unsupported model type for evaluation")
