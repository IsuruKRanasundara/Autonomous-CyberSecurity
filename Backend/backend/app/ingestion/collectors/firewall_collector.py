"""Firewall log ingestion collector."""

from typing import Any, Dict, List


class FirewallCollector:
	"""Collect firewall logs from upstream sources."""

	def collect(self) -> List[Dict[str, Any]]:
		return []
