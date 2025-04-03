from datetime import datetime
from typing import Any
from sqlalchemy import Column, Integer, DateTime
from database.connection import Base

class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    def dict(self) -> dict[str, Any]:
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if getattr(self, column.name) is not None
        } 