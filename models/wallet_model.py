from services.db_service import db
import uuid
from datetime import datetime

class Wallet(db.Model):
    __tablename__ = 'wallet'

    wallet_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)