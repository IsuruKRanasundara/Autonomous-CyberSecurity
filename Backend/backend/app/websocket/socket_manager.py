"""Real-time socket connections manager."""

from typing import Any, Dict, List


class SocketManager:
	"""Track active websocket connections."""

	def __init__(self) -> None:
		self.connections: List[Any] = []

	async def connect(self, websocket: Any) -> None:
		self.connections.append(websocket)

	def disconnect(self, websocket: Any) -> None:
		if websocket in self.connections:
			self.connections.remove(websocket)
