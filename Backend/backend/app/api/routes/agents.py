"""Agent status, workflow triggering, and monitoring APIs."""

from typing import Any, Dict, List

from fastapi import APIRouter


router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("", summary="List agents")
async def list_agents() -> List[Dict[str, Any]]:
	"""Return known agent statuses."""
	return []


@router.get("/{agent_name}/status", summary="Agent status")
async def agent_status(agent_name: str) -> Dict[str, Any]:
	"""Return status for a specific agent."""
	return {"agent": agent_name, "status": "unknown"}


@router.post("/{agent_name}/trigger", summary="Trigger workflow")
async def trigger_workflow(agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
	"""Trigger a workflow for a specific agent."""
	return {"agent": agent_name, "triggered": True, "payload": payload}


@router.get("/{agent_name}/monitor", summary="Monitor agent")
async def monitor_agent(agent_name: str) -> Dict[str, Any]:
	"""Return monitoring data for an agent."""
	return {"agent": agent_name, "monitoring": True}
