import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    instruction = Column(Text, nullable=False)
    target_description = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_meters = Column(Integer, default=150)
    reward_sol = Column(Float, default=0.01)
    poster_address = Column(String(44), nullable=False)
    status = Column(String(20), default="OPEN", index=True) # OPEN, CLAIMED, PAID, REJECTED, REFUNDED
    fund_tx_sig = Column(String(88), nullable=True)
    payout_tx_sig = Column(String(88), nullable=True)
    refund_tx_sig = Column(String(88), nullable=True)
    active_claim_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

class Claim(Base):
    __tablename__ = "claims"

    id = Column(String(36), primary_key=True, index=True)
    task_id = Column(String(36), nullable=False, index=True)
    worker_address = Column(String(44), nullable=False)
    claimed_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    status = Column(String(20), default="ACTIVE") # ACTIVE, SUBMITTED, EXPIRED, RELEASED

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, index=True)
    task_id = Column(String(36), nullable=False, index=True)
    claim_id = Column(String(36), nullable=False)
    worker_address = Column(String(44), nullable=False)
    file_hash = Column(String(64), nullable=False, index=True)
    image_path = Column(String(255), nullable=False)
    submitted_lat = Column(Float, nullable=True)
    submitted_lon = Column(Float, nullable=True)
    location_source = Column(String(20), default="DEVICE") # EXIF, DEVICE, FIXTURE
    distance_meters = Column(Float, nullable=True)
    tier0_pass = Column(Boolean, default=False)
    tier1_pass = Column(Boolean, default=False)
    tier2_pass = Column(Boolean, default=False)
    vision_confidence = Column(Float, default=0.0)
    vision_reason = Column(Text, nullable=True)
    final_status = Column(String(20), default="REJECTED") # PAID, REJECTED
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
