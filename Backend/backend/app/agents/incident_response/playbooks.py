"""Security response playbooks."""

from typing import Any, Dict, List


PLAYBOOKS: List[Dict[str, Any]] = [
	{"name": "credential_compromise", "steps": ["reset_password", "revoke_sessions"]},
	{"name": "malware_outbreak", "steps": ["isolate_host", "collect_artifacts"]},
]
