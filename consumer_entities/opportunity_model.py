from sqlalchemy import Column, String, Float, Date, JSON
from .base_model import BaseModel

class Opportunity(BaseModel):
    __tablename__ = "opportunities"
    
    name = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    probability = Column(Float, nullable=False)
    expected_close_date = Column(Date, nullable=False)
    account_id = Column(String, nullable=False)
    owner_id = Column(String, nullable=False)
    meta_data = Column(JSON, nullable=True)
    
    def __repr__(self):
        return f"<Opportunity(name='{self.name}', stage='{self.stage}', amount={self.amount})>" 