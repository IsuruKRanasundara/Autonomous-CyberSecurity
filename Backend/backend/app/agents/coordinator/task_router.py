"""Task routing logic for assigning work to the correct agents."""

from collections import deque
from typing import Any, Deque, Dict, Optional


class TaskRouter:
	"""Route and queue tasks for agent execution."""

	def __init__(self) -> None:
		self.queue: Deque[Dict[str, Any]] = deque()

	def route(self, task: Dict[str, Any]) -> str:
		"""Return the target agent for a task."""
		task_type = str(task.get("type", "general")).lower()
		if "malware" in task_type:
			return "malware_analysis"
		if "incident" in task_type:
			return "incident_response"
		if "log" in task_type:
			return "log_analysis"
		return "threat_detection"

	def enqueue(self, task: Dict[str, Any]) -> None:
		"""Add a task to the internal queue."""
		self.queue.append(task)

	def dequeue(self) -> Optional[Dict[str, Any]]:
		"""Remove and return the next queued task."""
		return self.queue.popleft() if self.queue else None
