"""Persistent memory storage for historical context."""

from typing import Any, Dict


class LongTermMemory:
	"""Store long-lived operational knowledge."""

	def __init__(self) -> None:
		self.store: Dict[str, Any] = {}

	def save(self, key: str, value: Any) -> None:
		self.store[key] = value

	def load(self, key: str, default: Any = None) -> Any:
		return self.store.get(key, default)
