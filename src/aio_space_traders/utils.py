import asyncio
from collections import deque, namedtuple
import time


class AsyncRateLimit:
    def __init__(self, per_second_limit: int = 2, per_minute_limit: int = 30):
        self.per_second_limit: int = per_second_limit
        self.per_minute_limit: int = per_minute_limit
        self.second_requests: deque[float] = deque()
        self.minute_requests: deque[float] = deque()
        self._lock: asyncio.Lock = asyncio.Lock()

    def _purge_expired_timestamps(self, now: float):
        # Remove timestamps older than 1 second for the per-second limit
        while self.second_requests and now - self.second_requests[0] >= 1:
            self.second_requests.popleft()

        # Remove timestamps older than 60 seconds for the per-minute limit.
        while self.minute_requests and now - self.minute_requests[0] >= 60:
            self.minute_requests.popleft()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            self._purge_expired_timestamps(now)
            wait_time = 0

            # Check per-second limit
            if len(self.second_requests) >= self.per_second_limit:
                wait_time = max(wait_time, 1 - (now - self.second_requests[0]))

            # Check per-minute limit
            if len(self.minute_requests) >= self.per_minute_limit:
                wait_time = max(wait_time, 60 - (now - self.minute_requests[0]))
            
            print(wait_time)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
                now = time.monotonic()
                self._purge_expired_timestamps(now)

            self.second_requests.append(now)
            self.minute_requests.append(now)

