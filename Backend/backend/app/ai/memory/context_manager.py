"""Shared agent context management utilities."""

from typing import Any, Dict


class ContextManager:
	"""Combine short-term and long-term agent context."""

	def __init__(self) -> None:
		self.context: Dict[str, Any] = {}

	def merge(self, payload: Dict[str, Any]) -> Dict[str, Any]:
		self.context.update(payload)
		return self.context
