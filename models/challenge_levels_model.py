from services.db_service import db
from sqlalchemy import Column, Integer, String, Numeric

class ChallengeLevels(db.Model):
    __tablename__ = 'challenge_levels'

    level_id = Column(Integer, primary_key=True)
    level_name = Column(String(50), nullable=False)
    min_transactions = Column(Integer, nullable=False)
    annual_interest = Column(Numeric(5,3), nullable=False)