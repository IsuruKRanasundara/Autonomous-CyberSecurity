"""Request validation helpers."""

from typing import Any, Dict


def validate_payload(payload: Dict[str, Any]) -> bool:
	return isinstance(payload, dict)
