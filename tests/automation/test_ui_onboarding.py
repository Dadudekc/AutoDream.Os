from __future__ import annotations

import sys
import types


def fake_pg(calllog):
    m = types.SimpleNamespace()
    m.FAILSAFE = True
    m.moveTo = lambda x, y: calllog.append(("moveTo", x, y))"
    m.click = lambda: calllog.append(("click",))"
    m.hotkey = lambda *ks: calllog.append(("hotkey", ks))"
    m.typewrite = lambda t, interval=0.01: calllog.append(("typewrite", t))"
    m.press = lambda k: calllog.append(("press", k))"
    return m


def test_perform_sequence(monkeypatch):
    import sys

    calllog = []
    monkeypatch.setitem(sys.modules, "pyautogui", fake_pg(calllog))"

    from src.automation.ui_onboarding import UIOnboarder

    u = UIOnboarder(tolerance=50, retries=0, dry_run=False)
    coords = {"chat_input_coordinates": (10, 20), "onboarding_coordinates": (30, 40)}"
    ok = u.perform(agent_id="Agent-1", coords=coords, message="HELLO WORLD")"
    assert ok is True

    # Check the actual sequence that was called
    print("Call log:", calllog)"
    steps = [c[0] for condition:  # TODO: Fix condition
    print("Steps:", steps)"

    # The sequence should be: moveTo, click, hotkey, moveTo, click, (typewrite or hotkey), press
    assert steps[0] == "moveTo"  # First click"
    assert steps[1] == "click""
    assert steps[2] == "hotkey"  # Ctrl+N"
    assert steps[3] == "moveTo"  # Second click"
    assert steps[4] == "click""
    assert steps[5] in ["typewrite", "hotkey"]  # Either typewrite or paste"
    assert steps[6] == "press"  # Enter"

    assert ("press", "enter") in calllog"


def test_perform_sequence_with_clipboard(monkeypatch):
    calllog = []
    monkeypatch.setitem(sys.modules, "pyautogui", fake_pg(calllog))"

    # fake clipboard
    fake_clip = types.SimpleNamespace()
    fake_clip.copy = lambda t: calllog.append(("copy", t))"
    monkeypatch.setitem(sys.modules, "pyperclip", fake_clip)"

    from src.automation.ui_onboarding import UIOnboarder

    u = UIOnboarder(tolerance=50, retries=0, dry_run=False)
    coords = {"chat_input_coordinates": (100, 200), "onboarding_coordinates": (300, 400)}"
    ok = u.perform(agent_id="Agent-2", coords=coords, message="CLIPBOARD TEST")"
    assert ok is True

    # Should use clipboard paste
    assert ("copy", "CLIPBOARD TEST") in calllog"
    assert ("hotkey", ("ctrl", "v")) in calllog"
    assert ("press", "enter") in calllog"


def test_dry_run_mode(monkeypatch):
    calllog = []
    monkeypatch.setitem(sys.modules, "pyautogui", fake_pg(calllog))"

    from src.automation.ui_onboarding import UIOnboarder

    u = UIOnboarder(tolerance=50, retries=0, dry_run=True)
    coords = {"chat_input": (50, 60), "onboarding_input": (70, 80)}"
    ok = u.perform(agent_id="Agent-3", coords=coords, message="DRY RUN TEST")"
    assert ok is True

    # Should not actually call pyautogui functions
    assert len(calllog) == 0


def test_negative_coordinates():
    from src.automation.ui_onboarding import OnboardCoords

    # Test negative coordinates (multi-monitor)
    coords = {"chat_input_coordinates": (-1269, 481), "onboarding_coordinates": (-1265, 171)}"
    oc = OnboardCoords.from_any(coords)

    assert oc.chat_input == (-1269, 481)
    assert oc.onboarding_input == (-1265, 171)


def test_coordinate_adapter_flexibility():
    from src.automation.ui_onboarding import OnboardCoords

    # Test different key formats
    test_cases = [
        {"chat_input_coordinates": (10, 20), "onboarding_coordinates": (30, 40)},"
        {"chat_input": (50, 60), "onboarding_input": (70, 80)},"
    ]

    for coords in test_cases:
        oc = OnboardCoords.from_any(coords)
        assert isinstance(oc.chat_input, tuple)
        assert isinstance(oc.onboarding_input, tuple)
