from typing import Optional, List
from sqlalchemy.orm import Session
from consumer_repository.interfaces.i_repository import IRepository
from consumer_entities.project_model import Project
from consumer_utils.logger import setup_logger

logger = setup_logger(__name__)

class ProjectRepository(IRepository[Project]):
    def __init__(self, db: Session):
        self.db = db
        logger.info("Initialized ProjectRepository")

    async def process_message(self, data: dict) -> None:
        """Process a project message"""
        try:
            logger.info(f"Processing project message: {data.get('name', 'Unknown')}")
            
            # Extract project data
            project_data = {
                "event_id": data.get("event_id"),
                "name": data.get("name"),
                "status": data.get("status"),
                "start_date": data.get("start_date"),
                "end_date": data.get("end_date"),
                "budget": data.get("budget"),
                "account_id": data.get("account_id"),
                "owner_id": data.get("owner_id"),
                "meta_data": data.get("meta_data")
            }
            
            # Check if project exists by event_id
            existing = self.get_by_event_id(self.db, project_data["event_id"])
            
            if existing:
                logger.info(f"Updating existing project with event_id: {project_data['event_id']}")
                self.update(self.db, existing, project_data)
            else:
                logger.info(f"Creating new project with event_id: {project_data['event_id']}")
                self.create(self.db, project_data)
                
        except Exception as e:
            logger.error(f"Error processing project message: {str(e)}")
            raise

    def create(self, db: Session, obj_in: dict) -> Project:
        logger.info(f"Creating new project: {obj_in.get('name', 'Unknown')}")
        db_obj = Project(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Successfully created project with ID: {db_obj.id}")
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Project]:
        logger.info(f"Fetching project with ID: {id}")
        return db.query(Project).filter(Project.id == id).first()
    
    def get_by_event_id(self, db: Session, event_id: str) -> Optional[Project]:
        logger.info(f"Fetching project with event_id: {event_id}")
        return db.query(Project).filter(Project.event_id == event_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
        logger.info(f"Fetching all projects with skip={skip}, limit={limit}")
        return db.query(Project).offset(skip).limit(limit).all()
    
    def update(self, db: Session, db_obj: Project, obj_in: dict) -> Project:
        logger.info(f"Updating project with ID: {db_obj.id}")
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info(f"Successfully updated project with ID: {db_obj.id}")
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        logger.info(f"Attempting to delete project with ID: {id}")
        obj = db.query(Project).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            logger.info(f"Successfully deleted project with ID: {id}")
            return True
        logger.warning(f"Project with ID: {id} not found for deletion")
        return False 