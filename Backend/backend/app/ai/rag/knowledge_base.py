"""Threat intelligence knowledge base for RAG."""

from typing import Any, Dict, List


class KnowledgeBase:
	"""Store curated threat intelligence records."""

	def __init__(self) -> None:
		self.records: List[Dict[str, Any]] = []

	def add_record(self, record: Dict[str, Any]) -> None:
		self.records.append(record)
