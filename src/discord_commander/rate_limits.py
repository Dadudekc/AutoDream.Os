import asyncio
import time
from typing import Dict

class RateLimiter:
    def __init__(self, global_per_sec: int = 5, user_cooldown_sec: int = 2):
        self._sem = asyncio.Semaphore(global_per_sec)
        self._last: Dict[int, float] = {}
        self._cooldown = user_cooldown_sec

    async def acquire(self, user_id: int):
        await self._sem.acquire()
        now = time.monotonic()
        last = self._last.get(user_id, 0.0)
        if now - last < self._cooldown:
            await asyncio.sleep(self._cooldown - (now - last))
        self._last[user_id] = time.monotonic()

    def release(self):
        self._sem.release()
