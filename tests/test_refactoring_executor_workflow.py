import json
import os
from pathlib import Path

from scripts.refactoring_executor import RefactoringExecutor


def test_extraction_and_import(tmp_path):
    compliance_file = tmp_path / "compliance.json"
    compliance_file.write_text(json.dumps({"violations": {}}))

    target_file = tmp_path / "sample.py"
    target_file.write_text("class Demo:\n    pass\n\n" "def helper():\n    return 1\n")

    os.chdir(tmp_path)
    executor = RefactoringExecutor(str(compliance_file))

    result = executor._extract_core_functionality(str(target_file))
    assert result["success"]

    module_path = tmp_path / "sample_extracted.py"
    assert module_path.exists()
    module_content = module_path.read_text()
    assert "class Demo" in module_content

    updated_content = target_file.read_text()
    assert "class Demo" not in updated_content
    assert "from sample_extracted import Demo" in updated_content
