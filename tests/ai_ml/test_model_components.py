from importlib import util
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[2] / "src" / "ai_ml"


def _load(name):
    spec = util.spec_from_file_location(name, ROOT / f"{name}.py")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


ModelLifecycle = _load("model_lifecycle").ModelLifecycle
TrainingOrchestrator = _load("training_orchestrator").TrainingOrchestrator
Evaluator = _load("evaluation").Evaluator


class DummyFramework:
    def __init__(self):
        self.create_model = MagicMock(return_value="model")
        self.train_model = MagicMock(return_value={"loss": 0.1})
        self.evaluate_model = MagicMock(return_value={"accuracy": 0.9})


def test_model_lifecycle_uses_store_and_logger():
    logger = MagicMock()
    store = MagicMock()
    lifecycle = ModelLifecycle(logger, store)

    lifecycle.save("m", "path")
    lifecycle.load("path")

    logger.info.assert_any_call("Saving model to %s", "path")
    logger.info.assert_any_call("Loading model from %s", "path")
    store.save.assert_called_once_with("m", "path")
    store.load.assert_called_once_with("path")


def test_training_orchestrator_runs_pipeline():
    framework = DummyFramework()
    data_service = MagicMock()
    data_service.fetch.return_value = "data"
    logger = MagicMock()

    orchestrator = TrainingOrchestrator(framework, data_service, logger)
    result = orchestrator.run({"layers": 2}, "query")

    data_service.fetch.assert_called_once_with("query")
    framework.create_model.assert_called_once_with({"layers": 2})
    framework.train_model.assert_called_once_with("model", "data")
    assert result == {"loss": 0.1}


def test_evaluator_runs_evaluation():
    framework = DummyFramework()
    data_service = MagicMock()
    data_service.fetch.return_value = "test_data"
    logger = MagicMock()

    evaluator = Evaluator(framework, data_service, logger)
    metrics = evaluator.run("model", "query")

    data_service.fetch.assert_called_once_with("query")
    framework.evaluate_model.assert_called_once_with("model", "test_data")
    assert metrics == {"accuracy": 0.9}
