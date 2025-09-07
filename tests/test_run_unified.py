import pytest

from run_unified import main


@pytest.mark.parametrize(
    "mode,expected",
    [
        ("advanced-analysis", "Advanced analysis executed"),
        ("advanced-elimination", "Advanced elimination executed"),
        ("comprehensive", "Comprehensive analysis executed"),
        ("focused", "Focused analysis executed"),
        ("mass", "Mass elimination executed"),
    ],
)
def test_main_modes(
    mode: str, expected: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Ensure each mode triggers the correct handler."""
    main(["--mode", mode])
    captured = capsys.readouterr()
    assert captured.out.strip() == expected
