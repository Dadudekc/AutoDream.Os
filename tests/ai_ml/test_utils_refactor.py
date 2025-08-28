import importlib.util
import json
from pathlib import Path


def load_module(relative_path: str):
    spec = importlib.util.spec_from_file_location("mod", Path(relative_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

config = load_module("src/ai_ml/utils/config.py")
logging_utils = load_module("src/ai_ml/utils/logging_utils.py")
performance = load_module("src/ai_ml/utils/performance.py")

config_loader = config.config_loader
logger_setup = logging_utils.logger_setup
performance_monitor = performance.performance_monitor
JSONPerformanceDataStore = performance.JSONPerformanceDataStore


def test_config_loader_reads_file(tmp_path):
    cfg = {"a": 1}
    cfg_file = tmp_path / "cfg.json"
    cfg_file.write_text(json.dumps(cfg))
    result = config_loader(str(cfg_file))
    assert result == cfg


def test_logger_setup_creates_file(tmp_path):
    log_file = tmp_path / "app.log"
    logger = logger_setup(log_level="DEBUG", log_file=str(log_file))
    logger.debug("test")
    assert log_file.exists()


def test_performance_monitor_writes_data(tmp_path):
    store = JSONPerformanceDataStore(tmp_path / "perf.json")

    @performance_monitor(store=store)
    def add(a, b):
        return a + b

    assert add(1, 2) == 3
    data = json.loads((tmp_path / "perf.json").read_text())
    assert "add" in data["functions"]
