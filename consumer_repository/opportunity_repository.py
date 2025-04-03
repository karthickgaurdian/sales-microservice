from typing import Optional, List
from sqlalchemy.orm import Session
from consumer_repository.interfaces.i_repository import IRepository
from consumer_entities.opportunity_model import Opportunity
from consumer_utils.logger import setup_logger

logger = setup_logger(__name__)

class OpportunityRepository(IRepository[Opportunity]):
    def __init__(self, db: Session):
        self.db = db
        logger.info("Initialized OpportunityRepository")

    async def process_message(self, data: dict) -> None:
        """Process an opportunity message"""
        try:
            logger.info(f"Processing opportunity message: {data.get('name', 'Unknown')}")
            
            # Extract opportunity data
            opportunity_data = {
                "event_id": data.get("event_id"),
                "name": data.get("name"),
                "stage": data.get("stage"),
                "amount": data.get("amount"),
                "probability": data.get("probability"),
                "expected_close_date": data.get("expected_close_date"),
                "account_id": data.get("account_id"),
                "owner_id": data.get("owner_id"),
                "meta_data": data.get("meta_data")
            }
            
            # Check if opportunity exists by event_id
            existing = self.get_by_event_id(self.db, opportunity_data["event_id"])
            
            if existing:
                logger.info(f"Updating existing opportunity with event_id: {opportunity_data['event_id']}")
                self.update(self.db, existing, opportunity_data)
            else:
                logger.info(f"Creating new opportunity with event_id: {opportunity_data['event_id']}")
                self.create(self.db, opportunity_data)
                
        except Exception as e:
            logger.error(f"Error processing opportunity message: {str(e)}")
            raise

    def create(self, db: Session, obj_in: dict) -> Opportunity:
        logger.info(f"Creating new opportunity: {obj_in.get('name', 'Unknown')}")
        db_obj = Opportunity(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Successfully created opportunity with ID: {db_obj.id}")
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Opportunity]:
        logger.info(f"Fetching opportunity with ID: {id}")
        return db.query(Opportunity).filter(Opportunity.id == id).first()
    
    def get_by_event_id(self, db: Session, event_id: str) -> Optional[Opportunity]:
        logger.info(f"Fetching opportunity with event_id: {event_id}")
        return db.query(Opportunity).filter(Opportunity.event_id == event_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Opportunity]:
        logger.info(f"Fetching all opportunities with skip={skip}, limit={limit}")
        return db.query(Opportunity).offset(skip).limit(limit).all()
    
    def update(self, db: Session, db_obj: Opportunity, obj_in: dict) -> Opportunity:
        logger.info(f"Updating opportunity with ID: {db_obj.id}")
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Successfully updated opportunity with ID: {db_obj.id}")
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        logger.info(f"Attempting to delete opportunity with ID: {id}")
        obj = db.query(Opportunity).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            logger.info(f"Successfully deleted opportunity with ID: {id}")
            return True
        logger.warning(f"Opportunity with ID: {id} not found for deletion")
        return False 