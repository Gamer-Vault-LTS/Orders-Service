from services.db_service import db
import uuid
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    savings = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled', name='order_status'), default='pending')
    description = db.Column(db.JSON, nullable=True)
