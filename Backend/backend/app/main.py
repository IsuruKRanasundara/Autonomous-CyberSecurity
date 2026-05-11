"""Main application entry point for the backend service."""

from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path
from typing import Iterable


if __package__ in {None, ""}:
	sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


def _collect_routers() -> Iterable[object]:
	"""Import router modules lazily and return any defined routers."""
	from app.api.routes import agents, alerts, incidents, reports

	for module in (alerts, incidents, reports, agents):
		router = getattr(module, "router", None)
		if router is not None:
			yield router
		else:
			logger.debug("No router defined in %s", module.__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
	logger.info("Starting backend application")
	yield
	logger.info("Stopping backend application")


app = FastAPI(
	title="AI Multi-Agent SOC",
	description="Backend API for the autonomous cybersecurity SOC platform.",
	version="0.1.0",
	lifespan=lifespan,
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
	response = await call_next(request)
	logger.info(
		"%s %s -> %s",
		request.method,
		request.url.path,
		response.status_code,
	)
	return response


for router in _collect_routers():
	app.include_router(router)


@app.get("/health", tags=["system"])
async def health_check() -> JSONResponse:
	return JSONResponse({"status": "ok"})


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
