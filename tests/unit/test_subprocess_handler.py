from src.utils.test_components import SubprocessHandler


def test_subprocess_handler_runs_echo():
    handler = SubprocessHandler()
    result = handler.run(["python", "-c", "print('hello')"])
    assert result["returncode"] == 0
    assert "hello" in result["stdout"]
