# development_guide.md
# ICESHOP AI – Development Guide
## Technical Requirements, Architecture, Phased Delivery Plan (Engineering Spec)

> **Doc purpose:** This is the authoritative engineering specification for building Iceshop AI from its current state (Faz 2 – in-memory FastAPI MVP) into a production-grade, scalable, ethical, location-aware, real-time flash opportunity engine.

---

## 0) Glossary

- **Buyer (Alıcı):** End user who receives flash offers and can pre-commit / join.
- **Seller (Satıcı):** Local merchant who can publish products and accept flash windows.
- **Product (Ürün):** Seller-owned item/service with price and optional stock.
- **Pre-Commit (Ön Katılım):** Buyer’s intent signal before activation; not binding; used for clustering and minimum demand thresholds.
- **Flash Window (Fırsat Penceresi):** Short-lived opportunity window with a start/end time and status lifecycle.
- **Status Lifecycle:** `SCHEDULED -> ACTIVE -> EXPIRED` (plus optional `CANCELLED`).
- **Offer / Deal:** A specific price advantage proposal tied to a Product (or bundle).
- **Location:** Latitude/longitude + human-readable district/neighborhood; used for proximity filtering.
- **Campaign Logic / Engine:** Scoring and decision layer that decides when/what to offer.

---

## 1) Current State (Baseline – Faz 2)

### 1.1 Running Backend
- **Framework:** FastAPI
- **Entry:** `uvicorn app.main:app --reload`
- **Swagger:** `http://127.0.0.1:8000/docs`
- **Current storage:** In-memory singleton `state` (no DB yet)

### 1.2 Key Rule: Imports
- ✅ Always: `from app.<...> import ...`
- ❌ Never: `from backend.<...> import ...`
- Run uvicorn from `/backend` directory; otherwise `ModuleNotFoundError: app`.

### 1.3 Implemented Routers (expected)
- `/api/buyers/*`
- `/api/sellers/*`
- `/api/flash-windows/*` (new)
- `/api/whatsapp/*` (simulated)

### 1.4 In-Memory State
- Single `state` instance holds:
  - buyers, sellers, products, precommits, flash_windows
- This is MVP scaffolding; will migrate to DB + cache in Faz 6.

---

## 2) Product Vision → Engineering Translation

### 2.1 What we build
A **real-time, location-aware, pre-commit-driven flash opportunity engine** that:
- Observes buyer intent & proximity
- Observes seller supply & load
- Produces short-lived offers
- Requires/benefits from buyer pre-commit aggregation
- Activates only when minimum conditions are met (demand threshold, time, seller consent)
- Sends notifications (currently simulated; later WhatsApp/voice)

### 2.2 What we do NOT build (explicit non-goals)
- No “power grab” / manipulation layer
- No dark patterns, no forced nudging
- No personal profiling beyond product fit & proximity
- No discriminatory targeting based on sensitive attributes

---

## 3) Core Requirements (Functional)

### FR-1 Buyer Registration
- System can register and retrieve buyers
- Buyer has location, categories, price sensitivity
- Buyer is identified by stable `buyer_id` (string)

**Acceptance Criteria**
- POST `/api/buyers/register` stores buyer in `state.buyers`
- Duplicate buyer_id overwrites or rejects (choose consistent behavior; recommended: reject 409 unless explicitly “update” endpoint)

---

### FR-2 Seller Registration
- System can register and retrieve sellers
- Seller has location and category
- Seller owns products

**Acceptance Criteria**
- POST `/api/sellers/register` stores seller in `state.sellers`

---

### FR-3 Product Management (Seller Inventory/Menu)
- Seller can add products
- Seller can list products

**Acceptance Criteria**
- POST `/api/sellers/{seller_id}/products` creates product, stores in `state.products`, and links product_id into `seller.product_ids`
- GET `/api/sellers/{seller_id}/products` returns list of products for that seller

---

### FR-4 Pre-Commit via Messaging (Simulated WhatsApp)
- When buyer sends “katıl/join/evet” with `buyer_id`, `seller_id`, `proposed_window_id`, system creates a PreCommit.
- PreCommit is stored and later linked to a Flash Window.

**Acceptance Criteria**
- POST `/api/whatsapp/webhook` with metadata `{buyer_id, seller_id, proposed_window_id}` creates `state.precommits[pre_id]`
- Response includes `"action":"precommit_created"` and `precommit_id`

---

### FR-5 Flash Window Create + Read
- System can create and read flash windows
- Windows have lifecycle fields and participant lists

**Acceptance Criteria**
- POST `/api/flash-windows/create` stores window in `state.flash_windows`
- GET `/api/flash-windows/{window_id}` returns the stored object

---

### FR-6 Link PreCommits to Flash Window (Aggregation)
- System can link all seller-specific precommits to a flash window when scheduled/activated.

**Acceptance Criteria**
- POST `/api/flash-windows/link-precommits` returns linked_count > 0 if precommits exist

---

### FR-7 Activate Flash Window (Manual Scheduler Step)
- In MVP, activation is manual.
- In Faz 4, activation becomes scheduled/automatic.

**Acceptance Criteria**
- POST `/api/flash-windows/activate` sets `status = ACTIVE`

---

### FR-8 Join Active Flash Window (Buyer Participation)
- Buyer can join an active flash window (again via simulated messaging)
- Participation is recorded in window participants

**Acceptance Criteria**
- POST `/api/whatsapp/webhook` with metadata `{buyer_id, flash_window_id}` adds buyer to `window.participant_ids`
- Response includes `"action":"joined_active_window"`

---

## 4) Non-Functional Requirements

### NFR-1 Performance
- In-memory MVP should handle:
  - 1000 buyers, 500 sellers, 5000 products
  - 100 flash windows active/day
  - 1–5 req/s local dev baseline

### NFR-2 Observability
- Structured logs (JSON preferred) for:
  - precommit created
  - window created/activated/expired
  - buyer joined
- Unique request IDs (later middleware)

### NFR-3 Correctness
- Idempotency rules defined for:
  - join window (same buyer re-join should not duplicate)
  - precommit (same buyer+seller+proposal should be de-duped OR versioned; choose and document)

### NFR-4 Security (later phases)
- Authentication/authorization (Faz 5/6)
- Rate limiting for webhook endpoints
- Input validation, strict schemas (Pydantic models)

### NFR-5 Ethics & Compliance
- Location data is sensitive: store minimal, allow deletion
- Avoid targeted discrimination or hidden scoring
- Provide explainability of why an offer exists (Faz 3/4)

---

## 5) Data Model Specification (Pydantic)

> File paths are indicative: `backend/app/models/*.py`

### 5.1 Location
- `lat: float`, `lng: float`
- `district: str | None`, `neighborhood: str | None`
- (Faz 3+) optionally `geohash: str`, `accuracy_m: int`

### 5.2 Buyer
Fields (MVP):
- `id: str`
- `phone_number: str`
- `name: str`
- `categories: list[str]`
- `price_sensitivity: str` (enum recommended: `low|balanced|high`)
- `location: Location`

(Faz 3+) add:
- `last_seen_at`
- `intent_history` (event sourced later)

### 5.3 Seller
Fields (MVP):
- `id: str`
- `phone_number: str`
- `name: str`
- `category: str`
- `location: Location`
- `density_status: str | None`
- `stock_status: str | None`
- `product_ids: list[str]`

(Faz 3+) add:
- `open_hours`
- `capacity_score`
- `current_queue_estimate`

### 5.4 Product
Fields (MVP):
- `id: str`
- `seller_id: str`
- `name: str`
- `description: str | None`
- `category: str | None`
- `price: float`
- `stock: int | None`
- `is_active: bool`

(Faz 3+) add:
- `cost_estimate` (optional)
- `margin_band` (optional)
- `demand_elasticity_estimate`

### 5.5 PreCommit
Fields (MVP):
- `id: str`
- `buyer_id: str`
- `seller_id: str`
- `proposed_window_id: str`
- `created_at: datetime`
- optional: `expires_at`

(Faz 3+) add:
- `product_preferences` (optional)
- `confidence` (0–1)

### 5.6 FlashWindow
Fields (MVP):
- `id: str`
- `seller_id: str`
- `title: str`
- `description: str`
- `start_time: datetime`
- `end_time: datetime`
- `status: str` (enum: SCHEDULED/ACTIVE/EXPIRED/CANCELLED)
- `product_id: str | None`
- `pre_commit_ids: list[str]`
- `participant_ids: list[str]`

(Faz 3+) add:
- `offer_type: percent|fixed|bundle`
- `offer_value: float`
- `min_participants: int`
- `max_participants: int | None`
- `activation_reason: dict` (explainability)

---

## 6) State Layer Spec (`app/core/state.py`)

### 6.1 Responsibilities
- Acts like an in-memory DB
- Ensures consistent linking:
  - Seller <-> Products
  - FlashWindow <-> PreCommits
  - FlashWindow <-> Participants

### 6.2 Required Methods (MVP)
- `add_buyer(buyer)`
- `get_buyer(id)`
- `add_seller(seller)`
- `get_seller(id)`
- `add_product(product)`
- `get_products_for_seller(seller_id)`
- `add_precommit(buyer_id, seller_id, proposed_window_id)`
- `link_precommits_to_window(window_id, seller_id)`
- `add_flash_window(window)`
- `get_flash_window(id)`
- `list_flash_windows_by_status(status)`
- `join_flash_window(buyer_id, window_id)` (idempotent: no duplicates)

### 6.3 Idempotency Rules (Recommended)
- join: if buyer already joined, no changes and return ok
- precommit: de-dupe by `(buyer_id, seller_id, proposed_window_id)` within a time window (e.g., 15 minutes)

---

## 7) API Contract Spec (Engineering)

> Base: `/api`

### 7.1 Buyers
- `POST /api/buyers/register` (body=Buyer)
  - 200: `{status:"ok", buyer_id}`
  - 409: `{status:"error", reason:"buyer_exists"}` (if implemented)

### 7.2 Sellers
- `POST /api/sellers/register` (body=Seller)
- `GET /api/sellers/{seller_id}`
- `POST /api/sellers/{seller_id}/products` (body: {name, category, price, stock})
- `GET /api/sellers/{seller_id}/products`

### 7.3 Flash Windows
- `POST /api/flash-windows/create` (body=FlashWindow)
- `GET /api/flash-windows/{window_id}`
- `GET /api/flash-windows/active/all`
- `POST /api/flash-windows/link-precommits` (body: {flash_window_id, seller_id})
- `POST /api/flash-windows/activate` (body: {flash_window_id})

### 7.4 WhatsApp (Simulated)
- `POST /api/whatsapp/webhook`
  - If `metadata.flash_window_id` exists and text indicates join:
    - join active window
  - Else if `buyer_id + seller_id + proposed_window_id` exists:
    - create precommit
  - Else: ignored

**Recommended Response Schema**
- `{status:"ok", action:"precommit_created", precommit_id}`
- `{status:"ok", action:"joined_active_window"}`
- `{status:"ignored", reason:"unsupported_message"}`

---

## 8) End-to-End Test Plan (E2E)

### 8.1 Pre-conditions
- Backend running from `/backend`
- Swagger accessible
- In-memory state is empty (fresh server start)

### 8.2 E2E Scenario A (Happy Path)
1) Register seller `seller_mcoffee`
2) Add product `Latte`
3) Register buyer `buyer_berkin`
4) POST `/api/whatsapp/webhook` with precommit metadata → expect `precommit_created`
5) Create flash window `fw_mcoffee_latte` (SCHEDULED)
6) Link precommits to window → expect `linked_count >= 1`
7) Activate window → expect status ACTIVE
8) POST `/api/whatsapp/webhook` with `{flash_window_id}` → expect `joined_active_window`
9) GET window → participants includes buyer

**Acceptance Criteria**
- Window contains `pre_commit_ids` and `participant_ids`
- No duplicate buyer participant entries

### 8.3 Negative Scenarios (Devil’s Advocate / Failure)
- Missing buyer_id: webhook should be ignored (no precommit)
- Join non-existent window: return 404 or ignored (define behavior)
- Link precommits with wrong seller_id: linked_count=0
- Activate non-existent window: 404
- Create window with end_time < start_time: 422 validation error

---

## 9) Phased Delivery Plan (Engineering Roadmap)

### FAZ 2 (Current) – In-Memory MVP
**Goal:** Validate core lifecycle end-to-end with minimal components.
- In-memory state
- Basic CRUD and linking
- Manual activation
- Simulated messaging

**Done Criteria**
- E2E Scenario A passes consistently in Swagger

---

### FAZ 3 – Intelligence Layer (Scoring & Decision)
**Goal:** Decide “when/what/how” to offer.

#### Deliverables
- **Proximity Scoring**
  - Compute buyer-seller distance (Haversine)
  - Filter within radius (e.g., 1–2 km adjustable)
- **Demand Clustering**
  - Count precommits per seller per window proposal
  - Identify spikes by category and time
- **Seller Load / Density Scoring**
  - seller density_status / queue estimate affects discount recommendation
- **Offer Generator**
  - choose product_id
  - propose offer type/value
  - compute min_participants threshold
- **Explainability**
  - store `activation_reason` dict on FlashWindow

#### Acceptance Criteria
- Given precommits and seller density, engine produces consistent offer proposal
- Explainability present for each generated window

---

### FAZ 4 – Scheduling & Automation
**Goal:** Make activation/expiry automatic.

#### Deliverables
- Scheduler (APScheduler/Celery beat)
- Auto transition:
  - SCHEDULED -> ACTIVE at start_time if threshold satisfied
  - ACTIVE -> EXPIRED at end_time
- Cleanup expired precommits
- System metrics: active windows count

#### Acceptance Criteria
- No manual activation needed
- Windows expire automatically and cannot be joined after expiry (enforced)

---

### FAZ 5 – Communication Layer (WhatsApp / Voice)
**Goal:** Real user messaging & seller notification.

#### Deliverables
- WhatsApp provider integration (or Twilio/Meta)
- Outbound templates:
  - Buyer offer
  - Buyer confirmation
  - Seller aggregated precommit notification (“X kişi geliyor”)
- Voice agent integration (optional) with VAPI
- Localization TR/EN

#### Acceptance Criteria
- A real buyer can opt-in and receive a real message
- Seller receives aggregated precommit count before activation

---

### FAZ 6 – Persistence & Scale
**Goal:** Production-grade data durability and scalability.

#### Deliverables
- PostgreSQL schema for buyers/sellers/products/precommits/windows
- Redis cache for active windows
- Migrations (Alembic)
- Event logging table (event sourcing optional)
- Auth (JWT / API keys)
- Rate limiting
- Observability (OpenTelemetry optional)

#### Acceptance Criteria
- Server restarts do not lose data
- Active windows served from cache with DB fallback

---

## 10) Dev Environment Guide

### 10.1 Run
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
