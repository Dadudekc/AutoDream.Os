# src/utils/confirm.py
import os

def confirm(prompt: str) -> bool:
    # Non-interactive override for automation
    if os.getenv("NONINTERACTIVE_YES", "").lower() in {"1", "true", "yes"}:
        return True
    try:
        ans = input(f"{prompt} [y/N]: ").strip().lower()
        return ans in {"y", "yes"}
    except EOFError:
        return False
