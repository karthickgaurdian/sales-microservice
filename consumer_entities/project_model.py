from sqlalchemy import Column, String, Float, Date, Boolean, JSON
from .base_model import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"
    
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    manager_id = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    meta_data = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<Project(name='{self.name}', status='{self.status}', budget={self.budget})>" 