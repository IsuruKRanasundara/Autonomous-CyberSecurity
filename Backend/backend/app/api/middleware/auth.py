"""JWT validation and role-based access helpers."""

from typing import Iterable, Optional

from fastapi import Header, HTTPException, status


def validate_jwt_token(authorization: Optional[str] = Header(default=None)) -> str:
	"""Validate a bearer token and return the token string.

	This scaffold keeps authentication logic in one place and can be
	replaced with a JWT library implementation later.
	"""
	if not authorization:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

	scheme, _, token = authorization.partition(" ")
	if scheme.lower() != "bearer" or not token:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

	return token


def require_roles(*allowed_roles: str):
	"""Create a role guard for protected endpoints."""
	allowed = set(role.lower() for role in allowed_roles)

	def dependency(user_roles: Optional[Iterable[str]] = None) -> None:
		roles = {role.lower() for role in (user_roles or [])}
		if allowed and not roles.intersection(allowed):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

	return dependency
