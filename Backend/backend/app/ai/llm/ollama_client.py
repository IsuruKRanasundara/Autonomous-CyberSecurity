"""Local LLM integration for Ollama-backed models."""

from typing import Any, Dict


class OllamaClient:
	"""Wrap prompt execution against a local Ollama model."""

	def execute_prompt(self, prompt: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
		"""Return a stubbed local LLM response payload."""
		return {"provider": "ollama", "prompt": prompt, "context": context or {}}
