"""Elasticsearch connection helpers."""

from typing import Any, Dict


class ElasticClient:
	"""Represent an Elasticsearch connection wrapper."""

	def __init__(self, host: str = "localhost", port: int = 9200) -> None:
		self.host = host
		self.port = port

	def ping(self) -> bool:
		return True
