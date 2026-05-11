"""ChromaDB integration wrapper."""

from typing import Any, Dict


class ChromaClient:
	"""Represent a ChromaDB client."""

	def __init__(self, collection_name: str = "security_incidents") -> None:
		self.collection_name = collection_name

	def upsert(self, item: Dict[str, Any]) -> None:
		return None
