from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session

T = TypeVar('T')

class IRepository(Generic[T], ABC):
    @abstractmethod
    def create(self, db: Session, obj_in: dict) -> T:
        """Create a new record"""
        pass
    
    @abstractmethod
    def get(self, db: Session, id: int) -> Optional[T]:
        """Get a record by ID"""
        pass
    
    @abstractmethod
    def get_by_event_id(self, db: Session, event_id: str) -> Optional[T]:
        """Get a record by event ID"""
        pass
    
    @abstractmethod
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination"""
        pass
    
    @abstractmethod
    def update(self, db: Session, db_obj: T, obj_in: dict) -> T:
        """Update a record"""
        pass
    
    @abstractmethod
    def delete(self, db: Session, id: int) -> bool:
        """Delete a record"""
        pass 