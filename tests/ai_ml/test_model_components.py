from importlib import util
from pathlib import Path
from unittest.mock import MagicMock
import sys

SRC_ROOT = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC_ROOT))
ROOT = SRC_ROOT / "ai_ml" / "managers"


def _load(name):
    spec = util.spec_from_file_location(f"ai_ml.managers.{name}", ROOT / f"{name}.py")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


ModelManager = _load("model_manager").ModelManager
TrainingManager = _load("training_manager").TrainingManager
EvaluationManager = _load("evaluation_manager").EvaluationManager


class DummyFramework:
    def __init__(self):
        self.create_model = MagicMock(return_value="model")
        self.train_model = MagicMock(return_value={"loss": 0.1})
        self.evaluate_model = MagicMock(return_value={"accuracy": 0.9})


def test_model_lifecycle_uses_store_and_logger():
    logger = MagicMock()
    store = MagicMock()
    lifecycle = ModelManager(logger, store)

    lifecycle.save("m", "path")
    lifecycle.load("path")

    logger.info.assert_any_call("Saving model to %s", "path")
    logger.info.assert_any_call("Loading model from %s", "path")
    store.save.assert_called_once_with("m", "path")
    store.load.assert_called_once_with("path")


def test_training_manager_runs_pipeline():
    framework = DummyFramework()
    data_service = MagicMock()
    data_service.fetch.return_value = "data"
    logger = MagicMock()

    orchestrator = TrainingManager(framework, data_service, logger)
    result = orchestrator.run({"layers": 2}, "query")

    data_service.fetch.assert_called_once_with("query")
    framework.create_model.assert_called_once_with({"layers": 2})
    framework.train_model.assert_called_once_with("model", "data")
    assert result == {"loss": 0.1}


def test_evaluation_manager_runs_evaluation():
    framework = DummyFramework()
    data_service = MagicMock()
    data_service.fetch.return_value = "test_data"
    logger = MagicMock()

    evaluator = EvaluationManager(framework, data_service, logger)
    metrics = evaluator.run("model", "query")

    data_service.fetch.assert_called_once_with("query")
    framework.evaluate_model.assert_called_once_with("model", "test_data")
    assert metrics == {"accuracy": 0.9}
