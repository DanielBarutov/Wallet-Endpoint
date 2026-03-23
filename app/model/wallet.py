from app.model.base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
import uuid

class Wallet(Base):
    __tablename__ = "wallet"
    id = Column(Integer, primary_key=True)
    wallet_uuid = Column(String, unique=True, default=str(uuid.uuid4()))
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())