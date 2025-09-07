import importlib.util
from pathlib import Path


def load(name, file):
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parents[2] / f"src/ai_ml/testing/{file}"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_full_workflow(tmp_path):
    DatasetPreparer = load("dataset_preparation", "dataset_preparation.py").DatasetPreparer
    ModelEvaluator = load("model_evaluation", "model_evaluation.py").ModelEvaluator
    TestReporter = load("reporting", "reporting.py").TestReporter
    CleanupManager = load("cleanup", "cleanup.py").CleanupManager

    preparer = DatasetPreparer(tmp_path)
    test_file = preparer.generate_test_file("test_workflow.py")

    evaluator = ModelEvaluator(project_path=tmp_path, test_dir=tmp_path)
    result = evaluator.run_tests()

    reporter = TestReporter()
    summary = reporter.summarize([result])

    cleaner = CleanupManager()
    removed = cleaner.cleanup(preparer.generated_tests)

    assert summary["successful_runs"] == 1
    assert removed == 1
    assert not Path(test_file).exists()
