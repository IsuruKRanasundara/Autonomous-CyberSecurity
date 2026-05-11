"""Temporary context memory for active workflows."""

from typing import Any, Dict


class ShortTermMemory:
	"""Store in-flight context for the current incident or agent run."""

	def __init__(self) -> None:
		self.store: Dict[str, Any] = {}

	def set(self, key: str, value: Any) -> None:
		self.store[key] = value

	def get(self, key: str, default: Any = None) -> Any:
		return self.store.get(key, default)
