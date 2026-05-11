"""Report generation and export APIs."""

from typing import Any, Dict

from fastapi import APIRouter, Query


router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate", summary="Generate report")
async def generate_report(payload: Dict[str, Any]) -> Dict[str, Any]:
	"""Generate a report from the provided input."""
	return {"message": "report generated", "data": payload}


@router.get("/export", summary="Export report")
async def export_report(
	report_id: str = Query(...),
	format: str = Query(default="json"),
) -> Dict[str, Any]:
	"""Export a report in the requested format."""
	return {"report_id": report_id, "format": format}
