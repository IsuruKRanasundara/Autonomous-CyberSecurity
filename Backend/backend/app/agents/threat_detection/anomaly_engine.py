"""ML anomaly detection and pattern recognition utilities."""

from typing import Any, Dict


class AnomalyEngine:
	"""Score events for anomalies using lightweight heuristics."""

	def score(self, event: Dict[str, Any]) -> float:
		"""Return a normalized anomaly score."""
		score = 0.0
		if event.get("failed_logins", 0) > 5:
			score += 0.6
		if event.get("ip_reputation") == "bad":
			score += 0.4
		return min(score, 1.0)
