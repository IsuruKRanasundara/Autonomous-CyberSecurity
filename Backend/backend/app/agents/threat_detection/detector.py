"""Threat detection logic and alert generation."""

from typing import Any, Dict, List


class ThreatDetector:
	"""Detect threats from normalized security telemetry."""

	def detect(self, event: Dict[str, Any]) -> List[Dict[str, Any]]:
		"""Return generated alerts for a suspicious event."""
		alerts: List[Dict[str, Any]] = []
		if event.get("severity") in {"high", "critical"}:
			alerts.append({"type": "threat", "event": event})
		return alerts
