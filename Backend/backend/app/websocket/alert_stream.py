"""Live alert streaming over websockets."""

from typing import Any, Dict

from app.websocket.socket_manager import SocketManager


socket_manager = SocketManager()


async def stream_alert(alert: Dict[str, Any]) -> None:
	"""Broadcast a live alert to connected clients."""
	return None
