"""Workflow manager for incident states and agent execution pipelines."""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class WorkflowState:
	"""Track incident workflow state."""

	workflow_id: str
	status: str = "created"
	steps: List[Dict[str, Any]] = field(default_factory=list)


class WorkflowManager:
	"""Manage execution pipelines for incident response workflows."""

	def __init__(self) -> None:
		self.workflows: Dict[str, WorkflowState] = {}

	def create_workflow(self, workflow_id: str) -> WorkflowState:
		state = WorkflowState(workflow_id=workflow_id)
		self.workflows[workflow_id] = state
		return state

	def update_status(self, workflow_id: str, status: str) -> WorkflowState:
		workflow = self.workflows[workflow_id]
		workflow.status = status
		return workflow
