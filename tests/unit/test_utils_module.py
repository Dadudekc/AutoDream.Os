from src.testing.utils import run_command
import sys


def test_run_command_executes_python():
    rc, out, err = run_command([sys.executable, "-c", "print('hello')"])
    assert rc == 0
    assert out.strip() == "hello"
    assert err == ""
