# IceShop AI – AI-Driven Demand Aggregation Engine

IceShop AI, WhatsApp üzerinden çalışan bir **AI-orchestrated dinamik kampanya sistemi**dir.

Sistem üç farklı kampanya modelini destekler:

1. Buyer-driven campaigns  
2. Seller-driven campaigns  
3. AI-driven opportunity campaigns (unique differentiator)

---

## 🔥 Core Flow

### Buyer Conversation Engine
- `/buyers/create` → yeni buyer kaydı
- `/buyers/answer` → AI state machine + dynamic question routing
- AI → next_state, updated_data, reply
- Backend → buyer state memory
- n8n → WhatsApp response

### Campaign Engine
`api/campaigns.py` + `core/campaign_logic.py`:
- buyer_trigger()
- seller_create()
- ai_scan()

### AI Opportunity Engine
- latent demand clusters
- stock-pressure detection
- price elasticity analysis
- opportunity scoring
- seller → buyer → seller approval loop

---

## 🧠 Architecture

WhatsApp → n8n → FastAPI → AI → State Machine → Campaign Logic

Backend modüller:
- buyers.py
- campaigns.py
- state.py
- prompts.py
- campaign_logic.py

---

## 🚀 Deployment

VS Code → GitHub (main) → AWS Lightsail (git pull) → FastAPI → systemd  
n8n → public backend endpoint

---

## 📌 Notes for ChatGPT (Future Sessions)

- This repo contains **all project logic**.  
- The AI state machine is in `core/prompts.py` + `core/state.py`.  
- Campaign logic lives in `core/campaign_logic.py`.  
- `/buyers/answer` is the main AI interaction entrypoint.  
- AI should always return structured JSON.  
- n8n must never contain business logic.

---
