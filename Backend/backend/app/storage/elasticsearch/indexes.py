"""Elasticsearch index creation and mappings."""

from typing import Any, Dict


INDEX_MAPPINGS: Dict[str, Dict[str, Any]] = {
	"alerts": {"properties": {"severity": {"type": "keyword"}}},
	"incidents": {"properties": {"status": {"type": "keyword"}}},
}


def create_indexes() -> Dict[str, Dict[str, Any]]:
	return INDEX_MAPPINGS
