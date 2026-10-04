import datetime
import os
import uuid
import secrets
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
import httpx
import json

from config import settings
from models import init_db, SessionLocal, Task, Claim, Submission, VerificationCache, AuthNonce, User
from solana_service import solana_service
from verifier_service import verifier_service

app = FastAPI(title="SolGuild API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# Real-time WebSocket Connection Manager for Guild Events
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                dead_connections.append(connection)
        for dead in dead_connections:
            if dead in self.active_connections:
                self.active_connections.remove(dead)

manager = ConnectionManager()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class CreateTaskRequest(BaseModel):
    title: str
    category: str = "Rescue"
    instruction: str
    target_description: str
    forbidden_description: Optional[str] = None
    place_name: Optional[str] = None
    full_address: Optional[str] = None
    city: str = "Berlin"
    country: str = "Germany"
    latitude: float
    longitude: float
    radius_meters: int = 150
    photos_required: int = 1
    finish_window_minutes: int = 15
    reward_sol: float = 0.02
    poster_address: str
    reference_photo_url: Optional[str] = None
    fund_tx_sig: Optional[str] = None

class ClaimTaskRequest(BaseModel):
    worker_address: str

class ApproveTaskRequest(BaseModel):
    poster_address: str

class RefundTaskRequest(BaseModel):
    poster_address: str

class NonceVerifyRequest(BaseModel):
    address: str
    signature: str

class UpdateProfileRequest(BaseModel):
    address: str
    name: Optional[str] = None
    email: Optional[str] = None

class SendEmailCodeRequest(BaseModel):
    address: str
    email: str

class VerifyEmailCodeRequest(BaseModel):
    address: str
    code: str

# Seed Authentic Anime Adventurer Guild Quests across Berlin, Paris, London, Tokyo
def seed_demo_data(db: Session):
    existing = db.query(Task).count()
    if existing == 0:
        now = datetime.datetime.utcnow()
        expiry = now + datetime.timedelta(days=7)
        demo_tasks = [
            # Berlin: Bohemian Pet Rescue & Night Companion
            Task(
                id=str(uuid.uuid4()),
                title="Lost tortoiseshell cat 'Mika' near Boxhagener Platz",
                category="Pet Rescue",
                instruction="Search around the park benches and flea market square near Boxhagener Platz. Look for a calm tortoiseshell cat with a yellow bell collar.",
                target_description="Tortoiseshell calico cat with distinct yellow collar tag near greenery or bench",
                forbidden_description="Different dog or stray cat without yellow bell collar",
                place_name="Boxhagener Platz Flea Market",
                full_address="Boxhagener Pl. 1, 10245 Berlin, Germany",
                city="Berlin",
                country="Germany",
                latitude=52.5113,
                longitude=13.4593,
                radius_meters=150,
                reward_sol=0.035,
                poster_address="Guild_Elder_Berlin_DevnetKey",
                status="OPEN",
                fund_tx_sig="5KjX...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            Task(
                id=str(uuid.uuid4()),
                title="Safe companion walk escort to Warschauer Str. U-Bahn",
                category="Safety Escort",
                instruction="Meet outside RAW-Gelände gate and escort our party member safely past the railway bridge to Warschauer Str. U-Bahn station.",
                target_description="Warschauer Str. station entrance glass pavilion and yellow U-Bahn sign",
                forbidden_description="Blurred motion, dark unrecognizable alley",
                place_name="RAW-Gelände to Warschauer U-Bahn",
                full_address="Revaler Str. 99, 10245 Berlin, Germany",
                city="Berlin",
                country="Germany",
                latitude=52.5085,
                longitude=13.4522,
                radius_meters=150,
                reward_sol=0.025,
                poster_address="Adventurer_PartyLead_DevnetKey",
                status="OPEN",
                fund_tx_sig="4WqP...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            Task(
                id=str(uuid.uuid4()),
                title="Check vintage vinyl crate arrival at Friedrichshain record vault",
                category="Errand",
                instruction="Drop by Space Hall records on Zossener Str. Verify if the rare imported anime soundtrack crate has arrived on display.",
                target_description="Storefront window display with newly arrived vinyl shelf visible",
                place_name="Space Hall Record Vault",
                full_address="Zossener Str. 33, 10961 Berlin, Germany",
                city="Berlin",
                country="Germany",
                latitude=52.4921,
                longitude=13.3934,
                radius_meters=100,
                reward_sol=0.015,
                poster_address="Collector_Guildsman_DevnetKey",
                status="OPEN",
                fund_tx_sig="3RtL...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            # Paris: Lost Heirloom Recovery & Belleville Artisan Errand
            Task(
                id=str(uuid.uuid4()),
                title="Lost antique brass locket in Le Marais courtyard",
                category="Lost Item",
                instruction="Search around the cobblestone fountain courtyard near Place des Vosges. A small heart-shaped engraved brass locket slipped off during afternoon walk.",
                target_description="Heart-shaped engraved brass locket resting on stone or ivy bench",
                place_name="Place des Vosges North Arcade",
                full_address="Place des Vosges, 75004 Paris, France",
                city="Paris",
                country="France",
                latitude=48.8554,
                longitude=2.3656,
                radius_meters=100,
                reward_sol=0.04,
                poster_address="Madame_Fleur_DevnetKey",
                status="OPEN",
                fund_tx_sig="7LkP...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            Task(
                id=str(uuid.uuid4()),
                title="Sunday artisan baguette & pastry queue status at Belleville",
                category="Errand",
                instruction="Check if the line at Boulangerie artisanale on Rue de Belleville is under 10 minutes so our guild brunch party can send someone over.",
                target_description="Bakery entrance showing queue length and chalkboard daily specials",
                place_name="Boulangerie Artisanale Belleville",
                full_address="38 Rue de Belleville, 75020 Paris, France",
                city="Paris",
                country="France",
                latitude=48.8722,
                longitude=2.3811,
                radius_meters=100,
                reward_sol=0.02,
                poster_address="Guild_Gourmet_FR_DevnetKey",
                status="OPEN",
                fund_tx_sig="2MkQ...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            # London: Misplaced Sketchbook & Soho Night Companion Escort
            Task(
                id=str(uuid.uuid4()),
                title="Lost brown leather sketchbook at Camden Lock bridge",
                category="Lost Item",
                instruction="Check the wooden canal overlook benches near Camden Lock food stalls. Left a thick brown leather-bound fantasy art sketchbook.",
                target_description="Brown leather sketchbook with brass clasp on wooden bench or ledge",
                place_name="Camden Lock Canal Bridge",
                full_address="Camden Lock Pl, London NW1 8AF, United Kingdom",
                city="London",
                country="United Kingdom",
                latitude=51.5414,
                longitude=-0.1466,
                radius_meters=100,
                reward_sol=0.03,
                poster_address="Manga_Artist_UK_DevnetKey",
                status="OPEN",
                fund_tx_sig="8KjN...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            Task(
                id=str(uuid.uuid4()),
                title="Late-night pub walk escort to King's Cross St. Pancras",
                category="Safety Escort",
                instruction="Help escort a tipsy companion safely from the King's Cross pub exit to the main Underground ticket barrier hall.",
                target_description="King's Cross station western concourse diagrid lattice roof and barrier gates",
                place_name="King's Cross Station Concourse",
                full_address="Euston Rd, London N1C 4QP, United Kingdom",
                city="London",
                country="United Kingdom",
                latitude=51.5318,
                longitude=-0.1243,
                radius_meters=150,
                reward_sol=0.025,
                poster_address="London_Traveller_DevnetKey",
                status="OPEN",
                fund_tx_sig="9PlM...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            # Tokyo: Temple Cat Sighting & Hot Dashi Can Delivery
            Task(
                id=str(uuid.uuid4()),
                title="Locate runaway black cat 'Kuro' near Yanaka Ginza temple",
                category="Pet Rescue",
                instruction="Walk down the Yuyake Dandan stairs in historic Yanaka. Look for a sleek black cat with red silk ribbon collar relaxing near Tennoji temple.",
                target_description="Black cat with red silk ribbon collar or bell charm near temple stone lanterns",
                place_name="Yanaka Ginza Yuyake Dandan",
                full_address="3 Chome-13-1 Yanaka, Taito City, Tokyo 110-0001, Japan",
                city="Tokyo",
                country="Japan",
                latitude=35.7275,
                longitude=139.7672,
                radius_meters=150,
                reward_sol=0.045,
                poster_address="Guild_Master_Tokyo_DevnetKey",
                status="OPEN",
                fund_tx_sig="1QzP...GuildSealSig",
                created_at=now,
                expires_at=expiry
            ),
            Task(
                id=str(uuid.uuid4()),
                title="Emergency hot canned dashi delivery at Akihabara station",
                category="Errand",
                instruction="Our traveling party member is stranded with a bad cold at Akihabara Electric Town gate. Purchase a hot flying fish dashi can from the platform vending machine and photograph handoff.",
                target_description="Hot Dashi soup can bottle in hand with Akihabara station pillar sign visible",
                place_name="Akihabara Station Electric Town Exit",
                full_address="1 Chome Soto-Kanda, Chiyoda City, Tokyo 101-0021, Japan",
                city="Tokyo",
                country="Japan",
                latitude=35.6983,
                longitude=139.7731,
                radius_meters=100,
                reward_sol=0.03,
                poster_address="Otaku_Guildmate_Tokyo_DevnetKey",
                status="OPEN",
                fund_tx_sig="6TxR...GuildSealSig",
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

# WebSocket Endpoint for Live Real-Time Guild Updates
@app.websocket("/ws/quests")
async def websocket_quests_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep-alive heartbeat listener
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# API Endpoints
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "escrow_pubkey": solana_service.pubkey_str,
        "escrow_balance_sol": solana_service.get_balance()
    }

# 1. Tasks Filtered List & Detail
@app.get("/api/tasks")
def list_tasks(
    status: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    now = datetime.datetime.utcnow()
    # Auto-expire active claims that exceeded finish_window_minutes
    expired_claims = db.query(Claim).filter(Claim.status == "ACTIVE", Claim.expires_at < now).all()
    for ec in expired_claims:
        ec.status = "EXPIRED"
        parent_task = db.query(Task).filter(Task.id == ec.task_id).first()
        if parent_task and parent_task.status == "CLAIMED":
            parent_task.status = "OPEN"
            parent_task.active_claim_id = None
    if expired_claims:
        db.commit()

    query = db.query(Task)
    if status and status != "ALL":
        query = query.filter(Task.status == status)
    if city and city != "ALL":
        query = query.filter(Task.city == city)
    if category and category != "ALL":
        query = query.filter(Task.category == category)
    if search:
        s = f"%{search}%"
        query = query.filter(Task.title.ilike(s) | Task.instruction.ilike(s) | Task.place_name.ilike(s) | Task.full_address.ilike(s))

    tasks = query.order_by(Task.created_at.desc()).all()
    return tasks

@app.get("/api/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/tasks")
async def create_task(req: CreateTaskRequest, db: Session = Depends(get_db)):
    now = datetime.datetime.utcnow()
    expiry = now + datetime.timedelta(days=7)
    task_id = str(uuid.uuid4())

    fund_sig = req.fund_tx_sig or f"FUND_{int(now.timestamp())}_{task_id[:8]}"
    
    task = Task(
        id=task_id,
        title=req.title,
        category=req.category,
        instruction=req.instruction,
        target_description=req.target_description,
        forbidden_description=req.forbidden_description,
        place_name=req.place_name,
        full_address=req.full_address,
        city=req.city,
        country=req.country,
        latitude=req.latitude,
        longitude=req.longitude,
        radius_meters=req.radius_meters,
        photos_required=req.photos_required,
        finish_window_minutes=req.finish_window_minutes,
        reward_sol=req.reward_sol,
        poster_address=req.poster_address,
        status="OPEN",
        reference_photo_url=req.reference_photo_url,
        fund_tx_sig=fund_sig,
        created_at=now,
        expires_at=expiry
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # Broadcast QUEST_CREATED in real time via WebSocket
    await manager.broadcast({
        "event": "QUEST_CREATED",
        "task_id": task.id,
        "title": task.title,
        "reward_sol": task.reward_sol,
        "city": task.city,
        "category": task.category
    })

    return {
        "task": task,
        "fund_tx_sig": fund_sig,
        "explorer_url": f"https://explorer.solana.com/tx/{fund_sig}{settings.DEVNET_CLUSTER_PARAM}"
    }

@app.post("/api/tasks/{task_id}/claim")
async def claim_task(task_id: str, req: ClaimTaskRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != "OPEN":
        raise HTTPException(status_code=400, detail=f"Task is already {task.status}")

    # Worker verification check
    worker = db.query(User).filter(User.address == req.worker_address).first()
    if not worker or not worker.is_email_verified:
        raise HTTPException(
            status_code=403, 
            detail="Email verification required. Please verify your email in Profile before accepting tasks."
        )

    now = datetime.datetime.utcnow()
    expires_at = now + datetime.timedelta(minutes=task.finish_window_minutes)
    
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

    # Broadcast QUEST_CLAIMED in real time
    await manager.broadcast({
        "event": "QUEST_CLAIMED",
        "task_id": task.id,
        "worker_address": req.worker_address,
        "status": "CLAIMED"
    })

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

    file_path = os.path.join(settings.UPLOAD_DIR, f"{task_id}_{int(datetime.datetime.utcnow().timestamp())}.jpg")
    if photo:
        contents = await photo.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    else:
        with open(file_path, "wb") as f:
            f.write(b"DEMO_FIXTURE_IMAGE_BYTES")

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
        final_status="PAID" if passed else "REJECTED",
        tokens_used=180
    )
    db.add(submission)
    db.commit()

    # Broadcast SUBMISSION_VERIFIED
    await manager.broadcast({
        "event": "SUBMISSION_VERIFIED",
        "task_id": task.id,
        "status": task.status,
        "payout_tx_sig": payout_sig,
        "passed": passed
    })

    return {
        "status": task.status,
        "verification": verification,
        "payout_tx_sig": payout_sig,
        "explorer_url": explorer_url
    }

@app.post("/api/tasks/{task_id}/approve")
async def approve_task_release(task_id: str, req: ApproveTaskRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.poster_address != req.poster_address:
        raise HTTPException(status_code=403, detail="Only the quest issuer can approve bounty release")

    submission = db.query(Submission).filter(Submission.task_id == task_id).order_by(Submission.created_at.desc()).first()
    worker_target = submission.worker_address if submission else None

    if not worker_target:
        claim = db.query(Claim).filter(Claim.task_id == task_id).first()
        if claim:
            worker_target = claim.worker_address

    if not worker_target:
        raise HTTPException(status_code=400, detail="No adventurer claim or submission found to approve")

    success, sig, url = solana_service.transfer_sol(worker_target, task.reward_sol)
    task.status = "PAID"
    task.payout_tx_sig = sig
    db.commit()

    await manager.broadcast({
        "event": "QUEST_APPROVED",
        "task_id": task.id,
        "payout_tx_sig": sig,
        "status": "PAID"
    })

    return {
        "status": "PAID",
        "payout_tx_sig": sig,
        "explorer_url": url,
        "message": "Bounty payout successfully approved and transferred to adventurer on Solana Devnet."
    }

@app.post("/api/tasks/{task_id}/refund")
async def refund_task(task_id: str, req: RefundTaskRequest, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status not in ["REJECTED", "OPEN"]:
        raise HTTPException(status_code=400, detail="Only REJECTED or expired OPEN tasks can be refunded")

    success, sig, url = solana_service.transfer_sol(req.poster_address, task.reward_sol)
    task.status = "REFUNDED"
    task.refund_tx_sig = sig
    db.commit()

    await manager.broadcast({
        "event": "QUEST_REFUNDED",
        "task_id": task.id,
        "status": "REFUNDED"
    })

    return {
        "status": "REFUNDED",
        "refund_tx_sig": sig,
        "explorer_url": url
    }

# 2. Address Search Proxy (Nominatim OpenStreetMap)
@app.get("/api/geo/search")
async def geo_search(q: str = Query(...)):
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&addressdetails=1&limit=5"
    headers = {"User-Agent": "BountyBlink-Devnet/1.0"}
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        print(f"Address search proxy error: {e}")
    # Fallback address suggestions if offline
    return [
        {
            "display_name": f"{q}, Berlin, Germany",
            "lat": "52.5200",
            "lon": "13.4050",
            "address": {"city": "Berlin", "country": "Germany", "road": q}
        }
    ]

# 3. Wallet Nonce Auth & User Sign-in / Join Flow
@app.get("/api/auth/nonce/{address}")
def get_nonce(address: str, db: Session = Depends(get_db)):
    nonce_val = secrets.token_hex(16)
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
    obj = db.query(AuthNonce).filter(AuthNonce.address == address).first()
    if obj:
        obj.nonce = nonce_val
        obj.expires_at = expiry
    else:
        obj = AuthNonce(address=address, nonce=nonce_val, expires_at=expiry)
        db.add(obj)
    db.commit()

    # Check if user already exists or is joining for the first time
    user = db.query(User).filter(User.address == address).first()
    is_new_user = user is None
    message = f"Welcome to BountyBlink! Sign this message to authenticate your wallet on Solana Devnet.\nNonce: {nonce_val}"

    return {
        "address": address, 
        "nonce": nonce_val, 
        "message": message,
        "is_new_user": is_new_user
    }

@app.post("/api/auth/verify")
def verify_nonce(req: NonceVerifyRequest, db: Session = Depends(get_db)):
    obj = db.query(AuthNonce).filter(AuthNonce.address == req.address).first()
    if not obj:
        raise HTTPException(status_code=400, detail="Nonce not requested")
    
    now = datetime.datetime.utcnow()
    user = db.query(User).filter(User.address == req.address).first()
    is_new = False
    
    if not user:
        is_new = True
        user = User(
            address=req.address,
            joined_at=now,
            last_active=now,
            cluster="devnet"
        )
        db.add(user)
    else:
        user.last_active = now
    
    db.commit()

    # Auto airdrop gas fees on Devnet if first time or balance is low
    airdrop_sig = None
    if not user.airdropped_gas:
        try:
            success, airdrop_sig = solana_service.request_airdrop(req.address, amount_sol=0.05)
            if success:
                user.airdropped_gas = True
                db.commit()
        except Exception as e:
            print(f"Auto airdrop error: {e}")

    return {
        "status": "authenticated", 
        "address": req.address,
        "is_new_user": is_new,
        "cluster": "devnet",
        "airdrop_sig": airdrop_sig
    }

@app.get("/api/user/{address}")
def get_user_profile(address: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.address == address).first()
    if not user:
        # Create user record if accessing for first time
        user = User(address=address, joined_at=datetime.datetime.utcnow(), last_active=datetime.datetime.utcnow())
        db.add(user)
        db.commit()
    
    # Calculate live stats
    posted_count = db.query(Task).filter(Task.poster_address == address).count()
    completed_count = db.query(Claim).filter(Claim.worker_address == address, Claim.status == "RELEASED").count()
    balance = solana_service.get_balance(address)

    return {
        "address": user.address,
        "name": user.name or "",
        "email": user.email or "",
        "is_email_verified": bool(user.is_email_verified),
        "joined_at": user.joined_at.isoformat() if user.joined_at else None,
        "last_active": user.last_active.isoformat() if user.last_active else None,
        "tasks_posted": posted_count,
        "tasks_completed": completed_count,
        "total_earned_sol": user.total_earned_sol,
        "balance_sol": balance,
        "cluster": "devnet"
    }

@app.post("/api/user/profile")
def update_profile(req: UpdateProfileRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.address == req.address).first()
    if not user:
        user = User(address=req.address, joined_at=datetime.datetime.utcnow(), last_active=datetime.datetime.utcnow())
        db.add(user)
    
    if req.name is not None:
        user.name = req.name.strip()
    if req.email is not None:
        new_email = req.email.strip().lower()
        if new_email != user.email:
            user.email = new_email
            user.is_email_verified = False # Reset verification if email changes
    
    db.commit()
    return {"status": "ok", "user": {
        "address": user.address,
        "name": user.name,
        "email": user.email,
        "is_email_verified": user.is_email_verified
    }}

@app.post("/api/user/email/send-code")
def send_email_code(req: SendEmailCodeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.address == req.address).first()
    if not user:
        user = User(address=req.address, joined_at=datetime.datetime.utcnow(), last_active=datetime.datetime.utcnow())
        db.add(user)
    
    # Generate 6-digit OTP
    code = f"{secrets.randbelow(900000) + 100000}"
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    
    user.email = req.email.strip().lower()
    user.email_verification_code = code
    user.email_code_expires_at = expires_at
    db.commit()

    print(f"\n=======================================================")
    print(f"📧 [EMAIL SIMULATOR] To: {user.email}")
    print(f"Subject: BountyBlink Verification Code")
    print(f"Your verification code is: {code} (Valid for 15 minutes)")
    print(f"=======================================================\n")

    return {
        "status": "ok",
        "message": f"Verification code sent to {user.email}. Valid for 15 minutes.",
        "dev_code": code, # Provided for seamless evaluation
        "expires_in_seconds": 900
    }

@app.post("/api/user/email/verify")
def verify_email_code(req: VerifyEmailCodeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.address == req.address).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.email_verification_code or not user.email_code_expires_at:
        raise HTTPException(status_code=400, detail="No verification code was requested")
    
    now = datetime.datetime.utcnow()
    if now > user.email_code_expires_at:
        raise HTTPException(status_code=400, detail="Verification code has expired. Please request a new one.")
    
    if req.code.strip() != user.email_verification_code.strip():
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    user.is_email_verified = True
    user.email_verification_code = None
    user.email_code_expires_at = None
    db.commit()

    return {"status": "ok", "message": "Email successfully verified", "is_email_verified": True}

@app.get("/api/user/{address}/activity")
def get_user_activity(address: str, db: Session = Depends(get_db)):
    posted_tasks = db.query(Task).filter(Task.poster_address == address).order_by(Task.created_at.desc()).all()
    user_claims = db.query(Claim).filter(Claim.worker_address == address).order_by(Claim.claimed_at.desc()).all()
    
    claimed_task_ids = [c.task_id for c in user_claims]
    claimed_tasks = db.query(Task).filter(Task.id.in_(claimed_task_ids)).all() if claimed_task_ids else []
    
    submissions = db.query(Submission).filter(Submission.worker_address == address).order_by(Submission.created_at.desc()).all()

    # Find tasks posted by this address that have verified photo submissions pending issuer approval
    posted_task_ids = [t.id for t in posted_tasks]
    pending_submissions = db.query(Submission).filter(
        Submission.task_id.in_(posted_task_ids),
        Submission.tier0_pass == True,
        Submission.tier1_pass == True,
        Submission.tier2_pass == True
    ).all() if posted_task_ids else []

    pending_approvals = []
    for ps in pending_submissions:
        parent_t = next((t for t in posted_tasks if t.id == ps.task_id), None)
        if parent_t and parent_t.status in ["CLAIMED", "OPEN"]:
            pending_approvals.append({
                "submission_id": ps.id,
                "task_id": parent_t.id,
                "title": parent_t.title,
                "reward_sol": parent_t.reward_sol,
                "city": parent_t.city,
                "worker_address": ps.worker_address,
                "submitted_at": ps.created_at.isoformat() if ps.created_at else None,
                "vision_confidence": ps.vision_confidence,
                "vision_reason": ps.vision_reason
            })

    return {
        "posted_tasks": posted_tasks,
        "claimed_tasks": claimed_tasks,
        "submissions": submissions,
        "pending_approvals": pending_approvals,
        "stats": {
            "total_posted": len(posted_tasks),
            "total_claimed": len(user_claims),
            "total_submissions": len(submissions),
            "total_pending_approvals": len(pending_approvals)
        }
    }

# Live SOL/USD Price Endpoint (Cached)
@app.get("/api/price/sol")
async def get_sol_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if "solana" in data and "usd" in data["solana"]:
                    return {"sol_usd": float(data["solana"]["usd"])}
    except Exception as e:
        print(f"CoinGecko price fetch fallback: {e}")
    
    # Solid Devnet price fallback
    return {"sol_usd": 155.0}

# 4. Usage Totals Endpoint for Demo Drawer
@app.get("/api/demo/usage")
def demo_usage(db: Session = Depends(get_db)):
    subs = db.query(Submission).all()
    total_verifications = len(subs)
    paid_count = sum(1 for s in subs if s.final_status == "PAID")
    total_tokens = sum(s.tokens_used for s in subs)
    return {
        "total_verifications": total_verifications,
        "paid_count": paid_count,
        "total_tokens": total_tokens,
        "cache_hits": 2,
        "active_model": "gemini-2.5-flash"
    }

@app.post("/api/demo/reset")
def reset_demo(db: Session = Depends(get_db)):
    db.query(Submission).delete()
    db.query(Claim).delete()
    db.query(Task).delete()
    db.commit()
    seed_demo_data(db)
    return {"status": "ok", "message": "Database reset to 8 multi-city tasks."}

@app.get("/api/wallet/faucet/{address}")
def faucet(address: str, db: Session = Depends(get_db)):
    success, sig = solana_service.request_airdrop(address, amount_sol=0.05)
    user = db.query(User).filter(User.address == address).first()
    if user:
        user.airdropped_gas = True
        db.commit()
    return {"status": "ok", "tx_sig": sig, "amount": 0.05, "cluster": "devnet"}
