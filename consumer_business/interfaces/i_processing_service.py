from abc import ABC, abstractmethod
from typing import Dict, Any
from sqlalchemy.orm import Session

class IProcessingService(ABC):
    @abstractmethod
    async def process_message(self, message: Dict[str, Any], db: Session) -> None:
        """Process a message and store it in the database"""
        pass
    
    @abstractmethod
    def get_processor(self, object_type: str):
        """Get the appropriate processor for the object type"""
        pass
    
    @abstractmethod
    def register_processor(self, object_type: str, processor):
        """Register a new processor for an object type"""
        pass 