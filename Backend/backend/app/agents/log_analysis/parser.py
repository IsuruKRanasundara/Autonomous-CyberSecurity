"""Parse raw logs and normalize formats."""

from typing import Any, Dict


class LogParser:
	"""Convert raw log payloads into a structured form."""

	def parse(self, raw_log: str) -> Dict[str, Any]:
		"""Parse a raw log line into a dictionary."""
		return {"raw": raw_log.strip(), "source": "unknown"}
