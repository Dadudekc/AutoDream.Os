import importlib.util
from pathlib import Path


def load(name, file):
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parents[2] / f"src/ai_ml/testing/{file}"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_run_tests(tmp_path):
    DatasetPreparer = load("dataset_preparation", "dataset_preparation.py").DatasetPreparer
    ModelEvaluator = load("model_evaluation", "model_evaluation.py").ModelEvaluator
    preparer = DatasetPreparer(tmp_path)
    preparer.generate_test_file("test_eval.py")
    evaluator = ModelEvaluator(project_path=tmp_path, test_dir=tmp_path)
    result = evaluator.run_tests()
    assert result["return_code"] == 0
    assert result.get("passed", 0) == 1
