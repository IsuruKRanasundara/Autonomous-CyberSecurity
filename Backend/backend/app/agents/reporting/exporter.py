"""PDF, CSV, and JSON exporting utilities."""

from typing import Any, Dict


class ReportExporter:
	"""Export reports to common formats."""

	def export(self, report: Dict[str, Any], format: str = "json") -> Dict[str, Any]:
		"""Return an export payload for the requested format."""
		return {"format": format, "report": report}
