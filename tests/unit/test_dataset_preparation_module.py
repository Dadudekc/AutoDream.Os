import importlib.util
from pathlib import Path


def load_dataset_preparer():
    spec = importlib.util.spec_from_file_location(
        "dataset_preparation", Path(__file__).resolve().parents[2] / "src/ai_ml/testing/dataset_preparation.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.DatasetPreparer


def test_generate_and_discover(tmp_path):
    DatasetPreparer = load_dataset_preparer()
    preparer = DatasetPreparer(tmp_path)
    created = preparer.generate_test_file("test_sample.py")
    assert Path(created).exists()
    discovered = preparer.discover_tests()
    assert created in discovered
