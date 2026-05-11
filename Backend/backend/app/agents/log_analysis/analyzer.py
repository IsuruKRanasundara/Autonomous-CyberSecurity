"""Log correlation and suspicious pattern detection."""

from typing import Any, Dict, List


class LogAnalyzer:
	"""Analyze normalized logs for suspicious behavior."""

	def analyze(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
		"""Return log findings."""
		findings: List[Dict[str, Any]] = []
		for log in logs:
			if log.get("severity") == "high":
				findings.append({"finding": "suspicious_pattern", "log": log})
		return findings
