"""Interactive coordinate capture utilities."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .coordinate_repository import CoordinateRepository


class CoordinateCapture:
    """Capture screen coordinates for agents using pynput."""

    def __init__(self, repository: CoordinateRepository) -> None:
        self.repository = repository

    def interactive_coordinate_capture(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        try:  # pragma: no cover - interactive
            from pynput import mouse
        except ImportError:
            return {"error": "Install pynput: pip install pynput"}

        print("Hover over ONBOARDING location and press ENTER...")
        captured: List[List[int]] = []
        current = [0, 0]

        def on_move(x: int, y: int) -> None:
            current[0], current[1] = x, y

        def on_click(x: int, y: int, button, pressed):
            if pressed and button == mouse.Button.left:
                captured.append([x, y])
                if len(captured) == 1:
                    print("Hover over CHAT location and press ENTER...")
                elif len(captured) == 2:
                    return False

        listener = mouse.Listener(on_move=on_move, on_click=on_click)
        listener.start()

        try:  # pragma: no cover - interactive
            while len(captured) < 2:
                input()
                captured.append(current.copy())
                if len(captured) == 1:
                    print(f"Onboarding: {current}")
                elif len(captured) == 2:
                    print(f"Chat: {current}")
        finally:
            listener.stop()

        if len(captured) != 2:
            return {"error": "Capture cancelled"}

        onboarding, chat = captured
        if agent_id:
            return self.repository.update_agent_coordinates(agent_id, onboarding, chat)
        return self.repository.update_all_agents_coordinates(onboarding, chat)

    def capture_onboarding_only(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        try:  # pragma: no cover - interactive
            from pynput import mouse
        except ImportError:
            return {"error": "Install pynput: pip install pynput"}

        print("Hover over ONBOARDING location and press ENTER...")
        current = [0, 0]

        def on_move(x: int, y: int) -> None:
            current[0], current[1] = x, y

        listener = mouse.Listener(on_move=on_move)
        listener.start()
        try:  # pragma: no cover - interactive
            input()
            if agent_id:
                return self.repository.update_onboarding_coordinates(agent_id, current.copy())
            return self.repository.update_all_onboarding_coordinates(current.copy())
        finally:
            listener.stop()

    def capture_chat_only(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        try:  # pragma: no cover - interactive
            from pynput import mouse
        except ImportError:
            return {"error": "Install pynput: pip install pynput"}

        print("Hover over CHAT location and press ENTER...")
        current = [0, 0]

        def on_move(x: int, y: int) -> None:
            current[0], current[1] = x, y

        listener = mouse.Listener(on_move=on_move)
        listener.start()
        try:  # pragma: no cover - interactive
            input()
            if agent_id:
                return self.repository.update_chat_coordinates(agent_id, current.copy())
            return self.repository.update_all_chat_coordinates(current.copy())
        finally:
            listener.stop()
