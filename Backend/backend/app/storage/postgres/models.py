"""Database models and ORM schemas."""

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.config.database import Base


class Incident(Base):
	__tablename__ = "incidents"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False)
	description = Column(Text, nullable=True)
	status = Column(String(50), default="open")
	created_at = Column(DateTime(timezone=True), server_default=func.now())
