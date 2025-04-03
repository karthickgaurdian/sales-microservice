from typing import Dict, Any, Type, Callable
from sqlalchemy.orm import Session
from .interfaces.i_processing_service import IProcessingService
from ..consumer_repository.opportunity_repository import OpportunityRepository
from ..consumer_repository.project_repository import ProjectRepository
from ..consumer_entities.opportunity_model import Opportunity
from ..consumer_entities.project_model import Project
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class ProcessingService(IProcessingService):
    def __init__(self):
        self.processors: Dict[str, Callable] = {}
        self.repositories: Dict[str, Any] = {
            "Opportunity": OpportunityRepository(),
            "Project": ProjectRepository()
        }
        self._register_default_processors()
    
    def _register_default_processors(self):
        """Register default processors for known object types"""
        self.register_processor("Opportunity", self._process_opportunity)
        self.register_processor("Project", self._process_project)
    
    async def process_message(self, message: Dict[str, Any], db: Session) -> None:
        """Process a message and store it in the database"""
        try:
            object_type = message.get("object_type")
            if not object_type:
                logger.error("Message missing object_type")
                return
            
            processor = self.get_processor(object_type)
            if not processor:
                logger.error(f"No processor found for object_type: {object_type}")
                return
            
            await processor(message, db)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def get_processor(self, object_type: str) -> Callable:
        """Get the appropriate processor for the object type"""
        return self.processors.get(object_type)
    
    def register_processor(self, object_type: str, processor: Callable) -> None:
        """Register a new processor for an object type"""
        self.processors[object_type] = processor
    
    async def _process_opportunity(self, message: Dict[str, Any], db: Session) -> None:
        """Process an opportunity message"""
        try:
            repository = self.repositories["Opportunity"]
            opportunity_data = {
                "event_id": message.get("event_id", Opportunity.generate_event_id()),
                "name": message.get("name"),
                "stage": message.get("stage"),
                "amount": message.get("amount"),
                "probability": message.get("probability"),
                "expected_close_date": message.get("expected_close_date"),
                "account_id": message.get("account_id"),
                "owner_id": message.get("owner_id"),
                "metadata": message.get("metadata")
            }
            
            existing = repository.get_by_event_id(db, opportunity_data["event_id"])
            if existing:
                repository.update(db, existing, opportunity_data)
            else:
                repository.create(db, opportunity_data)
                
            logger.info(f"Successfully processed opportunity: {opportunity_data['event_id']}")
            
        except Exception as e:
            logger.error(f"Error processing opportunity: {str(e)}")
            raise
    
    async def _process_project(self, message: Dict[str, Any], db: Session) -> None:
        """Process a project message"""
        try:
            repository = self.repositories["Project"]
            project_data = {
                "event_id": message.get("event_id", Project.generate_event_id()),
                "name": message.get("name"),
                "status": message.get("status"),
                "start_date": message.get("start_date"),
                "end_date": message.get("end_date"),
                "budget": message.get("budget"),
                "is_active": message.get("is_active", True),
                "manager_id": message.get("manager_id"),
                "client_id": message.get("client_id"),
                "metadata": message.get("metadata")
            }
            
            existing = repository.get_by_event_id(db, project_data["event_id"])
            if existing:
                repository.update(db, existing, project_data)
            else:
                repository.create(db, project_data)
                
            logger.info(f"Successfully processed project: {project_data['event_id']}")
            
        except Exception as e:
            logger.error(f"Error processing project: {str(e)}")
            raise 