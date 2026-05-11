"""Common helper functions."""

from typing import Any


def safe_get(mapping: dict[str, Any], key: str, default: Any = None) -> Any:
	return mapping.get(key, default)
