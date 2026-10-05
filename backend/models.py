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
    category = Column(String(50), default="Infrastructure")
    instruction = Column(Text, nullable=False)
    target_description = Column(Text, nullable=False)
    forbidden_description = Column(Text, nullable=True) # what the photo must not show
    place_name = Column(String(120), nullable=True)
    full_address = Column(String(255), nullable=True)
    city = Column(String(80), default="Berlin")
    country = Column(String(80), default="Germany")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    radius_meters = Column(Integer, default=150)
    photos_required = Column(Integer, default=1)
    finish_window_minutes = Column(Integer, default=10)
    reward_sol = Column(Float, default=0.01)
    poster_address = Column(String(44), nullable=False)
    status = Column(String(20), default="OPEN", index=True) # OPEN, CLAIMED, PAID, REJECTED, REFUNDED
    reference_photo_url = Column(String(255), nullable=True)
    fund_tx_sig = Column(String(88), nullable=True)
    payout_tx_sig = Column(String(88), nullable=True)
    refund_tx_sig = Column(String(88), nullable=True)
    active_claim_id = Column(String(36), nullable=True)
    failed_attempts = Column(Integer, default=0)
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
    investigation_letter = Column(Text, nullable=True) # Full written report for Sensitive quests
    source_info = Column(Text, nullable=True) # Source attribution of gathered intelligence
    letter_file_path = Column(String(255), nullable=True) # Optional supporting document attachment path
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
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    address = Column(String(44), primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(150), nullable=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    email_verification_code = Column(String(6), nullable=True)
    email_code_expires_at = Column(DateTime, nullable=True)
    joined_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    tasks_posted = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    total_earned_sol = Column(Float, default=0.0)
    airdropped_gas = Column(Boolean, default=False)
    cluster = Column(String(20), default="devnet")

class VerificationCache(Base):
    __tablename__ = "verification_cache"

    cache_key = Column(String(64), primary_key=True, index=True) # sha256(image_hash + task_id)
    decision = Column(Boolean, nullable=False)
    confidence = Column(Float, nullable=False)
    reason = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuthNonce(Base):
    __tablename__ = "auth_nonces"

    address = Column(String(44), primary_key=True)
    nonce = Column(String(64), nullable=False)
    expires_at = Column(DateTime, nullable=False)

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

