"""Unit tests for validator submodules."""

from src.utils.validators import DataValidators, FormatValidators, ValueValidators


def test_format_validators_email_and_url():
    assert FormatValidators.is_valid_email("test@example.com")
    assert not FormatValidators.is_valid_email("bad-email")
    assert FormatValidators.is_valid_url("https://example.com")
    assert not FormatValidators.is_valid_url("not-a-url")


def test_data_validators_required_and_json():
    data = {"name": "Alice"}
    errors = DataValidators.validate_required_fields(data, ["name", "age"])
    assert "age" in errors
    assert DataValidators.validate_json_string("{}")
    assert not DataValidators.validate_json_string("{bad json}")


def test_value_validators_length_and_range():
    assert ValueValidators.validate_string_length("abc", 1, 5)
    assert not ValueValidators.validate_string_length("", 1, 5)
    assert ValueValidators.validate_numeric_range(5, 0, 10)
    assert not ValueValidators.validate_numeric_range(15, 0, 10)
