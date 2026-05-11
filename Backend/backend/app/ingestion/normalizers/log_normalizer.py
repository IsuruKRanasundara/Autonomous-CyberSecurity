"""Normalize heterogeneous logs into a common schema."""

from typing import Any, Dict


class LogNormalizer:
	"""Convert raw log records into normalized events."""

	def normalize(self, log: Dict[str, Any]) -> Dict[str, Any]:
		return {"normalized": True, **log}
