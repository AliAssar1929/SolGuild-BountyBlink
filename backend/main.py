import datetime
import os
import uuid
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import settings
from models import init_db, SessionLocal, Task, Claim, Submission
from solana_service import solana_service
from verifier_service import verifier_service

app = FastAPI(title="BountyBlink API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class CreateTaskRequest(BaseModel):
    title: str
    instruction: str
    target_description: str
    latitude: float
    longitude: float
    reward_sol: float = 0.01
    poster_address: str

class ClaimTaskRequest(BaseModel):
    worker_address: str

class RefundTaskRequest(BaseModel):
    poster_address: str

# Seed Tasks Helper
def seed_demo_data(db: Session):
    existing = db.query(Task).count()
    if existing == 0:
        now = datetime.datetime.utcnow()
        expiry = now + datetime.timedelta(days=2)
        demo_tasks = [
            Task(
                id=str(uuid.uuid4()),
                title="Verify Alexanderplatz EV Charger",
                instruction="Check if the Allego fast-charger #3 screen is operational and connector is docked.",
                target_description="Green or active display on Allego station, intact CCS2 cable",
                latitude=52.5219,
                longitude=13.4132,
                reward_sol=0.01,
                poster_address="Agent_Sentinel_9X_DevnetKey",
                status="OPEN",
                fund_tx_sig="5KjX...DemoLockSig",
                created_at=now,
                expires_at=expiry
            ),
            Task(
                id=str(uuid.uuid4()),
                title="Bakery Opening Hours Board",
                instruction="Take a crisp photo of 'Bäckerei Siebert' chalkboard showing Sunday hours.",
                target_description="Chalkboard sign near entrance with legible opening hours",
                latitude=52.5401,
                longitude=13.4184,
                reward_sol=0.01,
                poster_address="Agent_Crawler_4B_DevnetKey",
                status="OPEN",
                fund_tx_sig="4WqP...DemoLockSig",
                created_at=now,
                expires_at=expiry
            ),
            Task(
                id=str(uuid.uuid4()),
                title="DHL Parcel Locker #108 Full Check",
                instruction="Photograph parcel locker status indicator (red/green capacity light).",
                target_description="Yellow DHL Packstation with clear view of interface screen",
                latitude=52.5163,
                longitude=13.3777,
                reward_sol=0.01,
                poster_address="Agent_Logistics_AI_DevnetKey",
                status="OPEN",
                fund_tx_sig="3RtL...DemoLockSig",
                created_at=now,
                expires_at=expiry
            )
        ]
        db.add_all(demo_tasks)
        db.commit()

# Ensure seed data exists
db_sess = SessionLocal()
seed_demo_data(db_sess)
db_sess.close()

# API Endpoints
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "escrow_pubkey": solana_service.pubkey_str,
        "escrow_balance_sol": solana_service.get_balance()
    }

@app.get("/api/tasks")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return tasks

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/tasks")
def create_task(req: CreateTaskRequest, db: Session = Depends(get_db)):
    now = datetime.datetime.utcnow()
    expiry = now + datetime.timedelta(days=2)
    task_id = str(uuid.uuid4())

    # Simulate / execute funding transaction from poster to escrow
    mock_fund_sig = f"FUND_{int(now.timestamp())}_{task_id[:8]}"
    
    task = Task(
        id=task_id,
        title=req.title,
        instruction=req.instruction,
        target_description=req.target_description,
        latitude=req.latitude,
        longitude=req.longitude,
        reward_sol=req.reward_sol,
        poster_address=req.poster_address,
        status="OPEN",
        fund_tx_sig=mock_fund_sig,
        created_at=now,
        expires_at=expiry
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return {
        "task": task,
        "fund_tx_sig": mock_fund_sig,
        "explorer_url": f"https://explorer.solana.com/tx/{mock_fund_sig}{settings.DEVNET_CLUSTER_PARAM}"
    }

@app.post("/api/tasks/{task_id}/claim")
def claim_task(task_id: str, req: ClaimTaskRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "OPEN":
        raise HTTPException(status_code=400, detail=f"Task is already {task.status}")

    now = datetime.datetime.utcnow()
    expires_at = now + datetime.timedelta(minutes=settings.CLAIM_TIMEOUT_MINUTES)
    
    claim = Claim(
        id=str(uuid.uuid4()),
        task_id=task.id,
        worker_address=req.worker_address,
        claimed_at=now,
        expires_at=expires_at,
        status="ACTIVE"
    )
    task.status = "CLAIMED"
    task.active_claim_id = claim.id
    db.add(claim)
    db.commit()
    return {"claim": claim, "task": task}

@app.post("/api/tasks/{task_id}/submit")
async def submit_evidence(
    task_id: str,
    worker_address: str = Form(...),
    fixture_type: Optional[str] = Form(None),
    browser_lat: Optional[float] = Form(None),
    browser_lon: Optional[float] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "CLAIMED":
        raise HTTPException(status_code=400, detail="Task must be in CLAIMED state to submit evidence")

    # Store photo or handle fixture
    file_path = os.path.join(settings.UPLOAD_DIR, f"{task_id}_{int(datetime.datetime.utcnow().timestamp())}.jpg")
    if photo:
        contents = await photo.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    else:
        # Default placeholder bytes if test button was tapped
        with open(file_path, "wb") as f:
            f.write(b"DEMO_IMAGE_BYTES_PLACEHOLDER")

    # Run verification pipeline
    verification = verifier_service.verify_submission(
        task_instruction=task.instruction,
        task_target_desc=task.target_description,
        task_lat=task.latitude,
        task_lon=task.longitude,
        file_path=file_path,
        device_lat=browser_lat,
        device_lon=browser_lon,
        fixture_type=fixture_type
    )

    passed = verification["tier0_pass"] and verification["tier1_pass"] and verification["tier2_pass"]
    payout_sig = None
    explorer_url = None

    if passed:
        # Trigger on-chain Devnet settlement transfer to worker!
        success, sig, url = solana_service.transfer_sol(worker_address, task.reward_sol)
        payout_sig = sig
        explorer_url = url
        task.status = "PAID"
        task.payout_tx_sig = payout_sig
    else:
        task.status = "REJECTED"

    submission = Submission(
        id=str(uuid.uuid4()),
        task_id=task.id,
        claim_id=task.active_claim_id or "claim_fixture",
        worker_address=worker_address,
        file_hash=verification["file_hash"],
        image_path=file_path,
        submitted_lat=browser_lat,
        submitted_lon=browser_lon,
        distance_meters=verification["distance_meters"],
        tier0_pass=verification["tier0_pass"],
        tier1_pass=verification["tier1_pass"],
        tier2_pass=verification["tier2_pass"],
        vision_confidence=verification["confidence"],
        vision_reason=verification["reason"],
        final_status="PAID" if passed else "REJECTED"
    )
    db.add(submission)
    db.commit()

    return {
        "status": task.status,
        "verification": verification,
        "payout_tx_sig": payout_sig,
        "explorer_url": explorer_url
    }

@app.post("/api/tasks/{task_id}/refund")
def refund_task(task_id: str, req: RefundTaskRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status not in ["REJECTED", "OPEN"]:
        raise HTTPException(status_code=400, detail="Only REJECTED or expired OPEN tasks can be refunded")

    success, sig, url = solana_service.transfer_sol(req.poster_address, task.reward_sol)
    task.status = "REFUNDED"
    task.refund_tx_sig = sig
    db.commit()

    return {
        "status": "REFUNDED",
        "refund_tx_sig": sig,
        "explorer_url": url
    }

@app.post("/api/demo/reset")
def reset_demo(db: Session = Depends(get_db)):
    db.query(Submission).delete()
    db.query(Claim).delete()
    db.query(Task).delete()
    db.commit()
    seed_demo_data(db)
    return {"status": "ok", "message": "Database reset to initial demo tasks."}

@app.get("/api/wallet/faucet/{address}")
def faucet(address: str):
    success, sig = solana_service.request_airdrop(address, amount_sol=0.05)
    return {"status": "ok", "tx_sig": sig, "amount": 0.05}
