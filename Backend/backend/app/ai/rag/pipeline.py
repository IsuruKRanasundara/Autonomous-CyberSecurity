"""Full retrieval-augmented generation workflow."""

from typing import Any, Dict

from app.ai.rag.knowledge_base import KnowledgeBase
from app.ai.rag.retriever import Retriever


class RAGPipeline:
	"""Combine retrieval and generation for context-aware responses."""

	def __init__(self) -> None:
		self.retriever = Retriever()
		self.knowledge_base = KnowledgeBase()

	def run(self, query: str) -> Dict[str, Any]:
		"""Run the RAG pipeline for a query."""
		return {"query": query, "context": self.retriever.retrieve(query)}
