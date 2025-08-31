from constants_consolidation_system import ConstantDefinition, ConstantsConsolidator


def test_categorize_constant_management():
    consolidator = ConstantsConsolidator()
    const = ConstantDefinition(
        name="MAX_SPEED",
        value=42,
        file_path="src/manager/constants.py",
        line_number=1,
    )
    assert consolidator.categorize_constant(const) == "management"


def test_extract_constants(tmp_path):
    sample = tmp_path / "constants.py"
    sample.write_text("FOO = 1\nBAR = 'baz'\n")
    consolidator = ConstantsConsolidator()
    constants = consolidator.extract_constants_from_file(str(sample))
    names = {c.name for c in constants}
    assert {"FOO", "BAR"} <= names
