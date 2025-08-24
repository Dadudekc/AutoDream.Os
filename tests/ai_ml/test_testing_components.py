import json
import importlib.util
from pathlib import Path

# Load testing module without importing the full package to avoid optional deps
spec = importlib.util.spec_from_file_location(
    "testing", Path(__file__).resolve().parents[2] / "src" / "ai_ml" / "testing.py"
)
testing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(testing)

DatasetConfig = testing.DatasetConfig
DatasetHandler = testing.DatasetHandler
ModelEvaluator = testing.ModelEvaluator
ResultReporter = testing.ResultReporter
TestRunConfig = testing.TestRunConfig
ConfigurableTestRunner = testing.ConfigurableTestRunner


def simple_model(x):
    return x * 2


def test_dataset_handler_reproducible():
    config = DatasetConfig(seed=123)
    handler1 = DatasetHandler(config)
    handler2 = DatasetHandler(config)
    assert handler1.load() == handler2.load()


def test_model_evaluator_accuracy():
    data = [(1, 2), (2, 4), (3, 6)]
    evaluator = ModelEvaluator(simple_model)
    metrics = evaluator.evaluate(data)
    assert metrics["accuracy"] == 1.0


def test_result_reporter_output():
    reporter = ResultReporter()
    report = reporter.report({"accuracy": 1.0})
    parsed = json.loads(report)
    assert parsed["metrics"]["accuracy"] == 1.0


def test_configurable_test_runner_reproducible():
    config = TestRunConfig(dataset=DatasetConfig(seed=42), model=simple_model)
    runner1 = ConfigurableTestRunner(config)
    runner2 = ConfigurableTestRunner(config)
    result1 = runner1.run()
    result2 = runner2.run()
    assert result1["metrics"] == result2["metrics"]
