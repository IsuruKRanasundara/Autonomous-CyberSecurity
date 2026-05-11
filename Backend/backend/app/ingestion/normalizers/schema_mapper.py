"""Event schema mapping utilities."""

from typing import Any, Dict


SCHEMA_MAP = {
	"timestamp": "event_time",
	"source_ip": "src_ip",
	"destination_ip": "dest_ip",
}


def map_schema(event: Dict[str, Any]) -> Dict[str, Any]:
	"""Map event keys to the internal schema."""
	mapped = {}
	for key, value in event.items():
		mapped[SCHEMA_MAP.get(key, key)] = value
	return mapped
