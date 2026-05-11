"""API request limiting and abuse prevention helpers."""

from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Deque, Dict

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
	"""Simple per-client rate limiter for API abuse prevention."""

	def __init__(self, max_requests: int = 100, window_seconds: int = 60):
		self.max_requests = max_requests
		self.window = timedelta(seconds=window_seconds)
		self._requests: Dict[str, Deque[datetime]] = defaultdict(deque)

	def check(self, request: Request) -> None:
		"""Raise if the request exceeds the allowed rate."""
		client = request.client.host if request.client else "anonymous"
		now = datetime.utcnow()
		queue = self._requests[client]

		while queue and now - queue[0] > self.window:
			queue.popleft()

		if len(queue) >= self.max_requests:
			raise HTTPException(
				status_code=status.HTTP_429_TOO_MANY_REQUESTS,
				detail="Rate limit exceeded",
			)

		queue.append(now)


rate_limiter = InMemoryRateLimiter()
