# implementation_plan.md — BountyBlink / SolGuild: Pan-European Expansion & Multi-Evidence Architecture

*Date: October 4, 2026 | Focus: European Guild Network | Stack: Vue 3 + FastAPI + SQLite + Gemini 3.1 Flash-Lite + Solana Devnet*  
*Roles: Backend Architect & Frontend Developer*

---

## 1. Executive Summary & Problem Analysis

### 1.1 Objectives
1. **European Guild Realignment**: Restrict geographic operational focus strictly to major populated European metropolitan centers (London, Paris, Berlin, Madrid, Rome, Amsterdam, Barcelona, Vienna), eliminating all legacy Asia/US references.
2. **Dense Realistic Quest Catalog**: Populate each of the 8 major European cities with at least 10 authentic, locally grounded quests (80+ quests total) adhering to real streets, landmarks, coordinates, and cultural realities.
3. **Three Canonical Guild Categories**:
   - **Civil Help**: Lost pets/belongings, wheelchair/elderly escort, safe ride companion / designated driver for vehicle, plant/home caretaking.
   - **Sensitive**: Subject surveillance/identification, object origin verification & intelligence sourcing, VIP security escort/bodyguarding. **Mandatory Protocol**: To claim a Sensitive bounty, claimants must submit both high-resolution photographic evidence AND a detailed investigation letter/intelligence report with verifiable source attribution.
   - **Commercial**: Product sourcing & UGC content creation, promotional storefront video/photoshoots, boutique inventory validation.
4. **AI Verifier Upgrade**: Switch verification engine to **Google Gemini 3.1 Flash-Lite** (`gemini-3.1-flash-lite`) using the verified API key (`AIzaSy...`). For Sensitive quests, the model performs dual-modal verification (evaluating the visual evidence and analyzing the written intelligence report for origin and source authenticity).
5. **Solana Devnet Settlement**: Confirm escrow balance (5.0 SOL live on Devnet at `JE922ncEr1G2bHrCCRpFDmT9q4y752aN4WxkPS4s1BDn`) and maintain zero-friction native SOL transfers.

---

## 2. Flaw Detection & Architectural Bottlenecks (Current State)

| # | Component | Current Implementation | Identified Flaw / Bottleneck | Architectural Solution |
|---|---|---|---|---|
| **F-01** | **Backend Models & DB Schema** | `Submission` table only stores `file_hash` and `image_path`. | Sensitive jobs require a full investigation letter and source citation. The database has no column to persist this report or audit it post-settlement. | Add `investigation_letter` (Text), `source_info` (Text), and `letter_file_path` (String) to `Submission` model; run automated migration script. |
| **F-02** | **Intake & Verification API** | `/api/tasks/{task_id}/submit` only accepts `photo: UploadFile`. | Form schema cannot receive written reports or source documents for Sensitive quests. | Update FastAPI endpoint with multipart form fields: `investigation_letter: Optional[str]`, `source_info: Optional[str]`, `letter_file: Optional[UploadFile]`. |
| **F-03** | **Gemini Vision Pipeline** | `verifier_service.py` evaluates single image against `instruction` and `target_desc`. | For Sensitive tasks, fraud or low-effort submissions can bypass verification if only a generic photo is uploaded without cross-examining the intelligence report. | Expand `verifier_service.py` to prompt Gemini 3.1 Flash-Lite with dual inputs (Image + Investigation Letter). Require minimum report depth, source attribution check, and visual consistency score. |
| **F-04** | **Quest Seeds & City Gating** | Database has only 8 tasks and includes Tokyo; location cards show Tokyo. | Geographic fragmentation; fails the "Europe only" and "10+ quests per major city" requirements. | Purge Tokyo seeds. Build comprehensive seed dictionary with 80+ geocoded quests across 8 major European hubs (10+ per city). |
| **F-05** | **Frontend Submission UX** | Mobile/desktop trigger is a raw file input (`<input type="file">`). | Claimants on Sensitive tasks have no input field to write or attach their investigation letter. | Implement a dedicated **Sensitive Intelligence Submission Modal** in Vue 3 with structured dossier inputs (Photo proof + Written investigation report + Intelligence source). |
| **F-06** | **Category UI & Issue Form** | `PostTaskForm.vue` has generic category selector. | Posters cannot configure specific Sensitive requirements (e.g. required intelligence fields), and category names are inconsistent (`Sensitive Task` vs `Sensitive`). | Standardize to `Civil Help`, `Sensitive`, `Commercial`. Add category helper cards and an explicit warning banner on `Sensitive` detailing the dual-evidence mandate. |
| **F-07** | **AI Model Target** | `config.py` and `.env` specify `gemini-2.5-flash`. | User explicitly directed to use `gemini-3.1-flash-lite`. | Update `.env` and `config.py` to `gemini-3.1-flash-lite`. |

---

## 3. Database Architecture & Schema Specification

### 3.1 Updated `tasks` Table (SQLite)
```sql
CREATE TABLE tasks (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(140) NOT NULL,
    category VARCHAR(50) NOT NULL,          -- 'Civil Help', 'Sensitive', 'Commercial'
    instruction TEXT NOT NULL,
    target_description TEXT NOT NULL,
    forbidden_description TEXT,
    place_name VARCHAR(120),
    full_address VARCHAR(255),
    city VARCHAR(80) NOT NULL,              -- London, Paris, Berlin, Madrid, Rome, Amsterdam, Barcelona, Vienna
    country VARCHAR(80) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    radius_meters INTEGER DEFAULT 150,
    photos_required INTEGER DEFAULT 1,
    finish_window_minutes INTEGER DEFAULT 15,
    reward_sol FLOAT DEFAULT 0.035,
    poster_address VARCHAR(44) NOT NULL,
    status VARCHAR(20) DEFAULT 'OPEN',      -- 'OPEN', 'CLAIMED', 'PAID', 'REJECTED', 'REFUNDED'
    reference_photo_url VARCHAR(255),
    fund_tx_sig VARCHAR(88),
    payout_tx_sig VARCHAR(88),
    refund_tx_sig VARCHAR(88),
    active_claim_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL
);
CREATE INDEX idx_tasks_city_category ON tasks(city, category);
CREATE INDEX idx_tasks_status ON tasks(status);
```

### 3.2 Updated `submissions` Table (SQLite)
```sql
CREATE TABLE submissions (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL,
    claim_id VARCHAR(36) NOT NULL,
    worker_address VARCHAR(44) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    investigation_letter TEXT,              -- Mandatory for 'Sensitive' category
    source_info TEXT,                       -- Source of intelligence/origin
    letter_file_path VARCHAR(255),          -- Optional uploaded report document
    submitted_lat FLOAT,
    submitted_lon FLOAT,
    location_source VARCHAR(20) DEFAULT 'DEVICE',
    distance_meters FLOAT,
    tier0_pass BOOLEAN DEFAULT 0,           -- Intake & hash duplicate check
    tier1_pass BOOLEAN DEFAULT 0,           -- Geofence tolerance check
    tier2_pass BOOLEAN DEFAULT 0,           -- Gemini 3.1 Flash-Lite evaluation
    vision_confidence FLOAT DEFAULT 0.0,
    vision_reason TEXT,
    final_status VARCHAR(20) DEFAULT 'REJECTED',
    tokens_used INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(task_id) REFERENCES tasks(id),
    FOREIGN KEY(claim_id) REFERENCES claims(id)
);
```

---

## 4. Backend System Architecture & API Contracts

### 4.1 REST Endpoints

#### 1. `POST /api/tasks/{task_id}/submit` (Multi-Evidence Intake)
- **Content-Type**: `multipart/form-data`
- **Fields**:
  - `worker_address`: `string` (Base58 public key)
  - `photo`: `UploadFile` (JPG/PNG photographic evidence)
  - `fixture_type`: `Optional[str]` (`"VALID"` | `"FAKE"`)
  - `browser_lat`: `Optional[float]`
  - `browser_lon`: `Optional[float]`
  - `investigation_letter`: `Optional[str]` (**Required if `task.category == 'Sensitive'`**)
  - `source_info`: `Optional[str]` (**Required if `task.category == 'Sensitive'`**)
  - `letter_file`: `Optional[UploadFile]` (Optional PDF/TXT document upload)

#### 2. `POST /api/demo/reset` (Reseed European Catalog)
- Purges database and executes transactional seeding of 80+ verified quests across the 8 European capitals with authentic coordinates.

---

## 5. Gemini 3.1 Flash-Lite Verifier Service Specification

### 5.1 Dual-Modal Verification Prompt Design
For **Sensitive** tasks, Gemini 3.1 Flash-Lite evaluates both the image and the written intelligence report:

```python
class SensitiveVerificationResult(BaseModel):
    is_authentic_onsite: bool
    matches_target_criteria: bool
    report_completeness_score: float  # 0 to 100
    source_credibility_score: float   # 0 to 100
    confidence_score: float           # Combined score
    detected_objects: list[str]
    report_assessment: str
    reason: str
```

**Verification Rule Engine**:
1. **Civil Help / Commercial**:
   - Validates physical photographic realism, on-site presence, and target match with threshold >= 80.0%.
2. **Sensitive Tasks**:
   - Rejects if `investigation_letter` is empty or < 50 characters.
   - Evaluates:
     a) Photographic confirmation of subject/object origin.
     b) Quality, detail, and internal coherence of the written letter.
     c) Explicit declaration of the information source.
   - Requires confidence_score >= 80.0% AND report_completeness_score >= 75.0%.

---

## 6. European Metropolis Distribution & Quest Inventory (80+ Quests)

| City | Country | Coordinates (Lat, Lon) | Quest Count | Core Quest Examples |
|---|---|---|---|---|
| **London** | United Kingdom | `51.5074, -0.1278` | **10+** | *Civil*: Safe night ride companion from Soho to Shoreditch; Lost velvet sketchbook in Camden Market.<br>*Sensitive*: Discreetly log license plate & delivery origin of black courier van in Mayfair; VIP close-escrow protection walk to Bank station.<br>*Commercial*: UGC promotional reel at Borough Market artisan bakery; Storefront display audit on Regent St. |
| **Paris** | France | `48.8566, 2.3522` | **10+** | *Civil*: Search for lost Siamese cat near Montmartre stairs; Assist elderly patron navigating Louvre carousel ramp.<br>*Sensitive*: Track origin serial numbers on vintage timepiece collection in Le Marais; Background check on gallery exhibition courier.<br>*Commercial*: Artisan perfume showcase photo at Palais-Royal; French pastry menu photoshoot in Belleville. |
| **Berlin** | Germany | `52.5200, 13.4050` | **10+** | *Civil*: Find lost calico cat 'Mika' at Boxhagener Platz; Wheelchair navigation at Warschauer Str. U-Bahn.<br>*Sensitive*: Document clandestine graffiti tagger identity along Spree riverbank; Security companion through Görlitzer Park at dusk.<br>*Commercial*: Independent vinyl shop promotional reel in Friedrichshain; Craft brewery taproom feature photo. |
| **Madrid** | Spain | `40.4168, -3.7038` | **10+** | *Civil*: Find lost golden retriever in El Retiro Park; Designated driver escort from Malasaña tapas tour.<br>*Sensitive*: Verify ownership lineage & physical provenance of antique bullfighting poster; Document suspicious courier meet at Atocha.<br>*Commercial*: Traditional churrería promotional photoshoot; Boutique leather shop showcase on Gran Vía. |
| **Rome** | Italy | `41.9028, 12.4964` | **10+** | *Civil*: Retrieve lost leather wallet near Trevi fountain steps; Plant watering & terrace safety check in Trastevere.<br>*Sensitive*: Document unauthorized street vendors operating near Colosseum arches; Source confirmation of Roman antique coin hoard.<br>*Commercial*: Espresso bar morning UGC reel in Campo de' Fiori; Artisan pasta workshop promotional shoot. |
| **Amsterdam** | Netherlands | `52.3676, 4.9041` | **10+** | *Civil*: Fish out lost house keys dropped near Prinsengracht canal bridge; Assist tourist on tandem bike repair near Jordaan.<br>*Sensitive*: Inspect maritime shipping registry plaque at Western Docklands; Security escort during late canal crossing.<br>*Commercial*: Botanical tulip boutique promotional reel; Vintage clothing storefront display audit in De Pijp. |
| **Barcelona** | Spain | `41.3879, 2.1699` | **10+** | *Civil*: Search for lost drone near Park Güell stone viaduct; Help grandmother with grocery haul up Gràcia stairs.<br>*Sensitive*: Verify authenticity & provenance of ceramic tile mosaic sample; Security escort near Gothic Quarter alleyways at midnight.<br>*Commercial*: Beachside tapas bar cocktail photoshoot; Skateboarding brand UGC video near MACBA plaza. |
| **Vienna** | Austria | `48.2082, 16.3738` | **10+** | *Civil*: Find lost violin bow case near Musikverein arcade; Wheelchair escort across cobblestone courtyard at Hofburg.<br>*Sensitive*: Verify provenance seal on rare classical manuscript in antique bookstore; Night surveillance of unauthorized courtyard access.<br>*Commercial*: Viennese coffeehouse Sachertorte promotional photo; Luxury porcelain boutique window display audit. |

---

## 7. Frontend User Experience & Component Enhancements

### 7.1 Category Reclassification & Disclosures
- **`PostTaskForm.vue`**:
  - Update category options to: `['Civil Help', 'Sensitive', 'Commercial']`.
  - Add contextual description cards for each category.
  - When **Sensitive** is selected:
    - Display an amber/gold institutional badge:
      > **"Sensitive Protocol Required: Claimants must provide both physical photo evidence AND a formal investigation letter with intelligence source attribution."**
    - Enable custom requirement fields for the letter criteria.

### 7.2 Dedicated Sensitive Intelligence Submission Modal
- In `App.vue`:
  - When a user claims an `OPEN` task, status transitions to `CLAIMED`.
  - If `category === 'Civil Help'` or `'Commercial'`: Clicking action triggers direct camera/photo picker.
  - If `category === 'Sensitive'`: Clicking action opens the **Sensitive Investigation Dossier Modal**:
    - **Section 1: Photographic Proof**: File uploader with preview for target subject or origin.
    - **Section 2: Investigation Letter**: High-contrast, formatted textarea with minimum word counter (origin details, observations, timestamped findings).
    - **Section 3: Intelligence Source**: Text input specifying the source (e.g. *Witness statement, municipal public registry, physical inspection, direct observation*).
    - **Section 4: Optional Attachment**: Supporting PDF/TXT report document upload.
    - Submit button with spinner triggering `/api/tasks/{task_id}/submit`.

### 7.3 City Filter Bar & Map Sync
- **`TaskFilters.vue` & `LocationPermissionCard.vue`**:
  - Replace cities list with: `['London', 'Paris', 'Berlin', 'Madrid', 'Rome', 'Amsterdam', 'Barcelona', 'Vienna']`.
- **`MapCanvas.vue`**:
  - Add smooth fly-to centering when the user switches European cities.

---

## 8. Step-by-Step Implementation Roadmap

1. **Step 1: Configuration & Environment**
   - Update `backend/config.py` and `backend/.env` with `GEMINI_MODEL=gemini-3.1-flash-lite`.

2. **Step 2: Database Models & Migration**
   - Update `Submission` in `backend/models.py` with `investigation_letter`, `source_info`, and `letter_file_path`.
   - Run safe database migration script to alter existing SQLite database without data loss.

3. **Step 3: Verifier Service Dual-Modal Engine**
   - Update `backend/verifier_service.py` to support `gemini-3.1-flash-lite`.
   - Implement dual-modal evaluation prompt and strict validation logic for `Sensitive` submissions.

4. **Step 4: Seed Data Overhaul (80+ European Quests)**
   - Construct complete, authentic seed dataset of 80+ quests across London, Paris, Berlin, Madrid, Rome, Amsterdam, Barcelona, Vienna.
   - Update `seed_demo_data` in `backend/main.py`.

5. **Step 5: Backend Endpoint Enhancements**
   - Update `/api/tasks/{task_id}/submit` to parse multipart form fields for investigation letters and source info.

6. **Step 6: Frontend UI Component Updates**
   - Update `TaskFilters.vue` and `LocationPermissionCard.vue` with 8 European cities and 3 categories.
   - Update `PostTaskForm.vue` with category definitions and sensitive job disclosures.
   - Implement the **Sensitive Dossier Submission Modal** in `App.vue` and integrate with `/api/tasks/{task_id}/submit`.
   - Update `DemoToolsDrawer.vue` to supply realistic mock investigation letters when testing Sensitive tasks with one tap.

7. **Step 7: Verification & Testing**
   - Test `Civil Help` photo submission & payout.
   - Test `Sensitive` photo + investigation letter submission & Gemini 3.1 Flash-Lite dual verification.
   - Verify on-chain Devnet settlement from the funded 5.0 SOL escrow vault.

---

## 9. Constraints, Risks & Assumptions

1. **Escrow Solvency**: The backend Escrow Vault (`JE922nc...`) is confirmed funded with **5.0 SOL**, which guarantees headroom for at least 100+ on-chain payouts of 0.035–0.05 SOL each.
2. **Devnet RPC Availability**: Standard public RPC (`api.devnet.solana.com`) with local fallback simulation ensures uninterrupted judging even during Devnet congestion.
3. **Gemini 3.1 Flash-Lite Quotas**: Verified active on your API key; latency is low (<1.5s), ensuring rapid verification stepper feedback.
