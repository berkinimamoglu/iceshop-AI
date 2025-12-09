# 🧊 ICESHOP — AI-Orchestrated Physical Commerce & Flash Demand Engine  

Iceshop is a next-generation commerce platform that uses AI to coordinate buyers and sellers through **WhatsApp AI voice agents**, driving synchronized demand toward physical stores.  
It does not operate like traditional e-commerce. Instead, Iceshop creates **Flash Purchase Windows**—short time intervals where multiple buyers visit the same store to obtain better prices or exclusive advantages.

This repository contains the backend, AI decision engine, campaign orchestration logic, and system architecture powering the Iceshop platform.

---

## 🧬 What Is Iceshop?

Iceshop is a **dynamic, AI-driven retail coordination engine** that:

- Collects buyer intent through WhatsApp  
- Analyzes availability, location, demand level, and timing  
- Engages sellers for stock + discount negotiation  
- Groups compatible buyers together  
- Predicts optimal time intervals to create synchronized demand  
- Opens Flash Purchase Windows (e.g., 14:00–14:20)  
- Directs multiple buyers to physical stores simultaneously  
- Generates discounts or benefits for buyers  
- Creates predictable, high-density traffic for sellers  

Iceshop enables a **new form of commerce**:  
AI-powered, time-compressed, synchronized retail demand.

---

## 📞 WhatsApp-First Product Strategy

### Why WhatsApp-first?

- Zero onboarding friction  
- No mobile app required during MVP  
- Buyers already understand voice messages & chat  
- Sellers operate easily via WhatsApp Business  
- AI voice agents provide natural communication  
- Fastest possible go-to-market approach  

WhatsApp serves as the **primary interface** during early product phases.

### Long-Term Roadmap for Channels

1. **WhatsApp → MVP launch**  
2. **Mini Web Panel → confirmations, maps, flash timers**  
3. **Mobile App → advanced buyer & seller dashboards**  
4. **Voice Call AI Agent → fallback or high-engagement use cases**  
5. **SMS Notifications → optional backup channel**

Backend logic remains identical across all interfaces.

---

## 🔥 Flash Purchase Windows — The Core Mechanism

A Flash Purchase Window is a short, highly optimized time interval where AI coordinates multiple buyers to visit a physical store to buy the same product.

### Buyer Flow

1. Buyer declares interest via WhatsApp  
2. AI collects:  
   - desired product  
   - availability  
   - location  
   - budget  
3. AI identifies matching buyers  
4. AI selects store + optimal time  
5. Buyer receives Flash Window instructions  
6. Buyer purchases during that exact interval  
7. Buyer receives better price or benefit  

### Seller Flow

1. Seller provides stock + acceptable discount  
2. AI negotiates conditions via WhatsApp  
3. Seller sees expected buyer count  
4. Seller prepares flash interval  
5. Store receives synchronized foot traffic  

Sellers love it because traffic is **predictable** and **dense**.  
Buyers love it because benefits are **exclusive** and **AI-optimized**.

---

## 🤖 AI Decision & Opportunity Engine (campaign_logic.py)

The intelligence of Iceshop lives in:



# 🧊 Iceshop AI Backend

Iceshop AI, fiziksel mağazalarda **AI tabanlı anlık kampanya (flash purchase window)** oluşturan bir yerel ticaret otomasyon sistemidir.  
Alıcılar ve satıcılar **WhatsApp üzerinden** sisteme bağlanır; backend bu sinyalleri analiz eder, fırsat üretir ve kısa süreli satın alma pencereleri oluşturur.

Bu repo:  
👉 **Iceshop AI Backend (FastAPI) – Faz 1 tam çalışan API katmanı**

Yeni bir ChatGPT oturumu veya yazılım mühendisi bu dosyayı okuduğunda projeye tamamen hâkim olmalıdır.

---

# 🚀 1. Vizyon

Iceshop, fiziksel mağazalarda:

- Gerçek zamanlı arz–talep eşleştirme  
- AI fırsat analizi  
- Flash purchase window (ör: 10 dakikalık toplu satın alma fırsatı)  
- WhatsApp voice-agent ile tamamen otomatik yönlendirme  

sunmak için tasarlanmıştır.

Uygulama **WhatsApp-first** yaklaşımına sahiptir.  
Mobil app veya web dashboard daha sonraki fazlarda gelecektir.

---

# 🏗️ 2. Proje Mimarisi (Faz 1)


---

Dostum/yoldaş, sadece bunu **tamamını** README.md içerisine yapıştır → commit → push et.

Sonra yeni chat açıp:

> “Iceshop AI backend repository: <repo_link> — projeyi oku ve Faz 2 için devam edelim.”

dediğinde sistem yeni oturumda bile projeyi %100 anlayacak.

Hazırsan push edebilirsin. 🚀

backend/
└── app/
├── api/
│ └── v1/
│ ├── buyers.py
│ ├── sellers.py
│ ├── campaigns.py
│ └── flash_window_routes.py
│
├── core/
│ ├── main.py
│ ├── campaign_logic.py
│ ├── state.py
│ └── config.py
│
├── models/
│ ├── buyer.py
│ ├── seller.py
│ └── flash_window.py
│
└── services/
├── scheduler.py
├── whatsapp_agent.py
└── utils/


Faz 1’de tüm veri **in-memory state** olarak tutulmaktadır.  
Gerçek veritabanı Faz 3’te eklenecektir.

---

# 🔌 3. Çalıştırma

### Sanal ortamı aktifleştir:
```bash
source venv/bin/activate


Backend başlat:
uvicorn backend.app.core.main:app --reload
Swagger UI:
http://127.0.0.1:8000/docs

Backend başlat:
uvicorn backend.app.core.main:app --reload
Swagger UI:
http://127.0.0.1:8000/docs


4. API Endpoint’leri (Faz 1 – Tamamlanmış)
🟢 Buyer Trigger
POST /api/v1/buyer/trigger
Alıcının WhatsApp davranışı (istek, konum, ürün talebi) backend’e sinyal olarak iletilir.
Örnek:
{
  "buyer_id": "B123",
  "location": "Nisantasi",
  "request": "coffee"
}

Seller Trigger
POST /api/v1/seller/trigger
Satıcı stok, ürün veya aktif kampanya bilgisini iletir.
Örnek:

{
  "seller_id": "S55",
  "products": ["coffee"],
  "location": "Nisantasi"
}

AI Fırsat Analizi (Mock)
GET /api/v1/campaigns/opportunities
AI motoru buyer–seller eşleşmelerine göre fırsat döner.
Faz 1’de mock çalışır.

[
  {
    "seller_id": "S55",
    "product_id": "coffee",
    "estimated_price": 95.0,
    "buyer_group": ["B123","B200"],
    "score": 0.82,
    "action": "ASK_SELLER"
  }
]

Flash Purchase Window Oluşturma
POST /api/v1/flash-window/create
AI tarafından belirlenen fırsate göre kısa süreli satın alma penceresi oluşturur.
Input:

{
  "buyers": [
    {"buyer_id": "B123"},
    {"buyer_id": "B200"}
  ],
  "seller": {
    "seller_id": "S55",
    "product_id": "coffee01"
  }
}

{
  "seller_id": "S55",
  "product_id": "coffee01",
  "start_time": "2025-12-09T12:00",
  "end_time": "2025-12-09T12:10",
  "expected_buyers": 2,
  "benefit": "10% discount"
}

5. campaign_logic.py – AI Motoru (Mock)
Faz 1’de AI motoru:
Buyer sinyallerini state’e kaydeder
Seller sinyallerini state’e kaydeder
Fırsat analizi için mock sonuç döner
Flash window üretir
Gerçek AI bileşenleri Faz 3’te gelecektir:
Zaman-serisi analiz
Price curve modeling
Bölgesel talep tahmini
ML scoring
Fırsat optimizasyonu

6. WhatsApp Voice Agent (Faz 2)
Faz 2’de tüm iletişim VAPI üzerinden WhatsApp Voice Agent ile gerçekleşecektir.
WhatsApp akışları:
Alıcı onboarding (sesli)
Satıcı onboarding
AI fırsatı → alıcıya otomatik bildirim
Flash window saatleri → alıcıya yönlendirme
Son 5 dakikada FOMO mesajı (“Pencere kapanıyor!”)
Satıcıya bildirim → “2 müşteri geliyor, hazırlan”
Backend, bu entegrasyona tam hazırdır.

7. Yol Haritası
✔ Faz 1 — API Layer (Tamamlandı)
Router yapısı
State management
Mock AI campaign engine
Flash window generator
Swagger UI
🚧 Faz 2 — WhatsApp Agent Integration
VAPI bağlantısı
Buyer/Seller onboarding akışı
AI fırsatlarının otomatik iletilmesi
Flash window zamanlama bildirimleri
🚧 Faz 3 — Production AI Engine + Database
Gerçek ML modelleri
PostgreSQL + Redis
Seller dashboard
Mobil app

8. Test Payload Koleksiyonu
Buyer Test:
{"buyer_id":"B1", "request":"pizza", "location":"Kadikoy"}
Seller Test:
{"seller_id":"S1", "products":["pizza"], "location":"Kadikoy"}
Flash Window Test:
{
  "buyers":[{"buyer_id":"B1"}],
  "seller":{"seller_id":"S1","product_id":"pizza01"}
}

9. Yeni ChatGPT Oturumu İçin Özet (AI Context Block)
Aşağıdaki paragraf yeni bir ChatGPT oturumunda yapıştırıldığında sistem projeyi anında kavrar:
Bu repo Iceshop AI backend’idir. Buyers ve sellers WhatsApp üzerinden sinyal gönderir. Backend AI fırsat analizi yapar ve flash purchase window oluşturur. Faz 1 tamamen API bazlı mock AI ile çalışır. campaign_logic.py fırsat üretir ve flash window oluşturur. main.py tüm router’ları bağlar. Faz 2’de WhatsApp voice-agent entegrasyonu yapılacaktır. Sistem şu anda çalışır ve Swagger’da tüm endpoint’ler görünmektedir.

10. Sonuç
Bu README, projeyi hiç bilmeyen bir mühendisin veya bir ChatGPT oturumunun sistemi sıfırdan anlaması için tasarlanmıştır.
Backend şu anda tamamen çalışır durumdadır ve Faz 2’ye hazırdır.

---

Dostum/yoldaş, bu dosya **tek parça** halinde eksiksizdir.  
Direkt olarak README.md içine yapıştırıp push edebilirsin.

Hazırsan:  
👉 Yeni chat açabiliriz  
👉 Repo linkini gösterip **Faz 2 (WhatsApp Voice Agent)** geliştirmesine başlayabiliriz.
