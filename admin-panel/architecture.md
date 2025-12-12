# architecture.md
# ICESHOP AI – System Architecture

## 1. Architectural Principles
- Event-driven, not request-driven
- State-first, logic-second
- Explicit lifecycle management
- AI as advisor, not dictator

---

## 2. High-Level Architecture

[ Buyer ]
|
| WhatsApp / App / API
v
[ Messaging Layer ]
|
v
[ FastAPI Backend ]
|
+--> State Engine (In-Memory / DB)
|
+--> Campaign Logic (AI / Rules)
|
+--> Scheduler



---

## 3. Component Breakdown

### 3.1 API Layer
- FastAPI routers
- Input validation via Pydantic
- Stateless request handling

### 3.2 State Layer
- Centralized state abstraction
- Responsible for consistency
- Acts as DB façade

### 3.3 Campaign Logic
- Scores demand
- Evaluates seller load
- Proposes offers
- Explains decisions

### 3.4 Scheduler
- Time-based activation
- Expiry handling
- Cleanup jobs

### 3.5 Messaging Layer
- WhatsApp (Faz 5)
- Voice agents (optional)
- Notification orchestration

---

## 4. Data Flow (Happy Path)

1. Buyer registers
2. Seller registers + products
3. Buyer sends intent (pre-commit)
4. State aggregates demand
5. Campaign logic evaluates opportunity
6. Flash window created
7. Window activated
8. Buyers join
9. Window expires

---

## 5. State vs DB (Future)

### Faz 2–3
- In-memory state
- Single process

### Faz 6+
- PostgreSQL (source of truth)
- Redis (active windows)
- Event log for analytics

---

## 6. Failure Handling

- Missing buyer/seller → reject
- Expired window → ignore join
- Messaging failure → retry + log
- Partial state updates → atomic operations (DB phase)

---

## 7. Scalability Strategy

- Horizontal API scaling
- Sticky cache for active windows
- Async workers for messaging
- Event sourcing optional for analytics

---

## 8. Security Architecture (Future)

- JWT for buyers/sellers
- API keys for integrations
- Role-based access (buyer/seller/admin)

---

## 9. Observability

- Structured logs
- Metrics (Prometheus)
- Traces (OpenTelemetry)
- Audit logs for decisions

---

## 10. Architectural Non-Goals

- No monolithic super-app
- No opaque black-box AI
- No centralized price control
