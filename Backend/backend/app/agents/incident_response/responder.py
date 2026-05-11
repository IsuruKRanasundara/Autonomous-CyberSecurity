"""Response execution logic for incident containment and triage."""

from typing import Any, Dict, List


class IncidentResponder:
	"""Apply response actions for an incident."""

	def respond(self, incident: Dict[str, Any]) -> List[Dict[str, Any]]:
		"""Return the response actions that would be executed."""
		return [{"incident_id": incident.get("id"), "action": "containment"}]
