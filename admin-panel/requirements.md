# requirements.md
# ICESHOP AI – Product & Engineering Requirements

## 1. Purpose
This document defines the functional and non-functional requirements of Iceshop AI.
It serves as the single source of truth for product, engineering, and AI decision-making.

---

## 2. Product Objective
Enable local, real-time, consent-based commerce by dynamically matching buyer intent with seller supply through short-lived flash opportunity windows.

---

## 3. Stakeholders
- Buyers (end users)
- Sellers (local merchants)
- Platform operator (Iceshop)
- Future partners (cities, malls, brands)

---

## 4. User Personas

### Buyer Persona
- Urban, mobile-first
- Price-aware but time-sensitive
- Wants nearby, immediate opportunities
- Opt-in behavior (no spam tolerance)

### Seller Persona
- Local SME
- Limited marketing budget
- Wants predictable demand
- Accepts discounts only when demand is guaranteed

---

## 5. User Stories (Core)

### Buyer Stories
- As a buyer, I want to receive relevant nearby offers
- As a buyer, I want to pre-commit without obligation
- As a buyer, I want to join an active offer instantly
- As a buyer, I want transparency on why I received an offer

### Seller Stories
- As a seller, I want to see aggregated demand before offering discounts
- As a seller, I want to control timing and capacity
- As a seller, I want only relevant buyers to be notified

---

## 6. Functional Requirements

### FR-01 Buyer Registration
- Buyers must be uniquely identifiable
- Buyers must have location and category interests

### FR-02 Seller Registration
- Sellers must be uniquely identifiable
- Sellers must define category and location

### FR-03 Product Management
- Sellers can add/update/remove products
- Products have price and optional stock

### FR-04 Pre-Commit
- Buyers can signal intent before activation
- Pre-commit is non-binding
- Pre-commit expires automatically after a defined TTL

### FR-05 Flash Window Lifecycle
- Create (scheduled)
- Activate (manual or automatic)
- Accept participants
- Expire

### FR-06 Participation
- Buyers can join active windows once
- No duplicate participation

---

## 7. Non-Functional Requirements

### Performance
- Low latency (<200ms for core endpoints)
- Burst tolerance during activation windows

### Reliability
- No data loss in Faz 6+
- Graceful degradation if messaging fails

### Security
- Authentication (Faz 5+)
- Rate limiting on messaging endpoints

### Privacy
- Location data minimized
- Buyer can opt-out and delete data

---

## 8. Metrics & KPIs

- Pre-commit to activation ratio
- Activation to participation ratio
- Seller conversion rate
- Buyer repeat participation
- Average window fill time

---

## 9. Out of Scope (Explicit)
- Global marketplace aggregation
- Dynamic bidding wars
- User credit scoring
- Ad-based targeting

---

## 10. Success Criteria
The product is successful when:
- Sellers voluntarily create recurring flash windows
- Buyers actively pre-commit and join
- Discounts are demand-driven, not forced
