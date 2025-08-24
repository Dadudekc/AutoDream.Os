from src.services.coordinator import CoordinationStrategy


def test_choose_queue_for_short_message():
    strategy = CoordinationStrategy(threshold=5)
    assert strategy.choose("hi") == "queue"


def test_choose_pyautogui_for_long_message():
    strategy = CoordinationStrategy(threshold=5)
    assert strategy.choose("hello world") == "pyautogui"
