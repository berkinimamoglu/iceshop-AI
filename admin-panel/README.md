Bu README:
Sistemin vizyonunu,
Teknik mimarisini,
Akışları,
Veri modellerini,
Yapılacak fazları,
Entegrasyon planlarını,
Kod yapısını,
Scheduler ve Flash Window mantığını,
Pre-commit (ön katılım) tasarımını,
WhatsApp Voice Agent entegrasyonunu,
Orkestrasyon modelini
BAŞTAN SONA eksiksiz şekilde anlatacak.

ICESHOP AI – FULL TECHNICAL README (Zero-to-Master Explanation)
AI-Driven Local Commerce Orchestration Engine
Complete Backend Architecture, Logic & Development Roadmap
❄️ 1. WHAT IS ICESHOP AI? (HIGH-LEVEL OVERVIEW)
Iceshop AI, şehirdeki fiziksel dükkânlar ile mahalledeki alıcılar arasındaki arz–talep ilişkisini gerçek zamanlı yöneten, ihtiyaç anında 10 dakikalık Flash Purchase Window (mikro-kampanyalar) oluşturan ve tüm iletişimi WhatsApp Voice Agent üzerinden gerçekleştiren bir AI ticaret altyapısıdır.
Bunu bir “City Commerce Operating System” gibi düşünebilirsin:
Alıcılar WhatsApp üzerinden sisteme bağlanır
Satıcılar WhatsApp üzerinden stok, yoğunluk ve fırsat sinyalleri gönderir
Backend (bu repo) şehir içi talep + arz verilerini anlık izler
AI, fırsat gördüğünde 10 dakikalık Flash Window kampanyaları üretir
Alıcı “katıl” diyerek fırsatı kabul eder → pre-commit oluşur
Kampanya aktif olunca sistem satıcıya:
"Şu anda 3 kişi yolda, ortalama mesafe 350 m" gibi bilgiler gönderir
Sistem böylece boş kapasiteyi trafik ve gelire çevirir
Sıfırdan başlayan bir yazılımcı, aşağıdaki dokümantasyonla projenin tamamını anlayabilir.

2. CORE CONCEPTS (THE HEART OF THE SYSTEM)
Sistemin çalışmasını mümkün kılan ana kavramlar:
🔹 Buyer
Mahallede yaşayan ve WhatsApp üzerinden talep sinyalleri veren kişi.
Örn: “Kahve içmek istiyorum”, “Tost lazım”, “Market indirimi var mı?”
Buyer bilgileri:
Telefon / WhatsApp ID
Lokasyon (semt, mahalle, lat/lng)
Tercihler (kategori, fiyat seviyesi)
Pre-commit davranışları
🔹 Seller
Fiziksel dükkan (kahveci, lokanta, bakkal, kasap, kuaför, market, restoran).
Satıcı sinyalleri:
Yoğunluk (low/medium/high)
Stok (fazla / kritik / promosyon)
Fiyat aralıkları
Lokasyon

Demand & Supply Signals
Alıcı ve satıcı sürekli sinyal gönderir:
Demand signals (buyer):
“Latte istiyorum”
“Tost lazım”
“Uygun fiyatlı kahve arıyorum”
Supply signals (seller):
“Bu saat boşum”
“Yoğunluk düşük”
“Stok fazlası ürün var”
🔹 Flash Purchase Window (10-Dakikalık Fırsat Penceresi)
AI tarafından üretilen, 10 dakika süreli, lokasyon bazlı mikro kampanyadır.
Örnek:
Moda’daki M Coffee → 10 dk için latte %20 indirim
Beşiktaş Çarşı → 10 dk döner 89 TL
Bornova → 10 dk 1 alana 1 bedava waffle
Bu pencereler:
Belirli bir satıcıya bağlıdır
Belirli bir buyer cluster’a gönderilir
Start/End time içerir
Lokasyon & pre-commit verisine göre optimize edilir
🔹 Pre-Commit (Ön Katılım)
AI buyer’a teklif gönderir:
“Moda’da 10 dk latte %20 indirim açabilirim. Katılmak ister misin?”
Buyer “katıl” der →
→ Sistem bunu pre-commit olarak kaydeder.
Eğer kampanya gerçekten aktif olursa, satıcıya şu bilgi topluca iletilir:
“3 kişi kampanya başladığında geliyorum dedi.”
Bu sinyal:
Kampanya skorunu yükseltir
AI’nin kampanya açma kararını etkiler
Satıcıya operasyonel hazırlık sağlar
🔹 Real-Time Location Matching
Hem alıcı hem satıcı lokasyon verisi içerir.
Sistem:
Buyer → Seller mesafesini hesaplar
Yalnızca yürünebilir mesafedeki kişilere fırsat gönderir
Avantaj oranını mesafeye göre optimize eder

3. HIGH-LEVEL ARCHITECTURE DIAGRAM
BUYER (WhatsApp)          SELLER (WhatsApp)
        │                          │
        ▼                          ▼
  VAPI Voice Agent  <───>  FastAPI Backend
        │                          │
        └───► Webhook Events       │
                (text/voice)       │
                                   │
       AI Campaign Engine <────────┘
                │
                ▼
      Flash Window Generator
                │
 ┌──────────────┼───────────────────┐
 │              │                   │
 ▼              ▼                   ▼
Location Match  Pre-Commit Store   Notification Engine
 │              │                   │
 ▼              ▼                   ▼
Active Buyer Set               WhatsApp Push Messages
Active Seller                  “3 kişi geliyor!”

4. BACKEND FOLDER STRUCTURE (TARGET DESIGN)
backend/
  app/
    main.py
    api/
      buyers.py
      sellers.py
      whatsapp.py
      campaigns.py
      flash_windows.py
    services/
      campaign_logic.py
      whatsapp_agent.py
      scheduler.py
      location_service.py
      precommit_manager.py
    core/
      state.py
      config.py
    models/
      buyer.py
      seller.py
      flash_window.py
      precommit.py
      location.py

admin-panel/
docker/
n8n/
❄️ 5. DATA MODELS (FULL DEFINITIONS)
🔹 Location
class Location(BaseModel):
    lat: float
    lng: float
    district: str
    neighborhood: str
🔹 Buyer
class Buyer(BaseModel):
    id: str
    phone_number: str
    name: str | None
    location: Location
    categories: list[str]
    price_sensitivity: str  # low / balanced / premium
🔹 Seller
class Seller(BaseModel):
    id: str
    phone_number: str
    name: str
    category: str
    location: Location
    density_status: str  # low / medium / high
    stock_status: str | None
🔹 PreCommit
class PreCommit(BaseModel):
    id: str
    buyer_id: str
    seller_id: str
    proposed_window_id: str
    timestamp: datetime
🔹 FlashWindow
class FlashWindow(BaseModel):
    id: str
    seller_id: str
    title: str
    description: str
    discount_percent: int | None
    static_price: float | None
    bundle_info: dict | None

    buyer_ids: list[str]          # hedeflenen kişiler
    pre_commit_ids: list[str]     # ön katılım verenler
    participant_ids: list[str]    # aktifken katılanlar

    start_time: datetime
    end_time: datetime
    status: Literal["SCHEDULED", "ACTIVE", "EXPIRED"]
❄️ 6. API ENDPOINTS (FULL LIST)
BUYER ROUTES
POST /api/buyers/register
POST /api/buyers/signal
GET  /api/buyers/{buyer_id}
SELLER ROUTES
POST /api/sellers/register
POST /api/sellers/signal
GET  /api/sellers/{seller_id}
CAMPAIGN ROUTES
POST /api/campaigns/scan
POST /api/campaigns/generate
FLASH WINDOW ROUTES
GET  /api/flash-windows/active
POST /api/flash-windows/create
WHATSAPP ROUTES
POST /api/whatsapp/webhook
POST /api/whatsapp/test-notification
❄️ 7. WHATSAPP INTEGRATION (VAPI)
Incoming messages → /api/whatsapp/webhook
Örneğin:
{
  "event_type": "message",
  "channel": "whatsapp",
  "from": "+9053xxxx",
  "text": "katıl",
  "metadata": {
    "buyer_id": "B123",
    "proposed_window_id": "P45"
  }
}
Backend:
“katıl” → pre-commit kaydı oluşturur
Outgoing messages (notifications)
whatsapp_agent.py üzerinden yapılır.
Örnek:
“Berkin, Moda’da latte 10 dk %20 indirim. Katılmak ister misin?”
❄️ 8. CAMPAIGN ENGINE (DETAILED LOGIC)
AI campaign motoru aşağıdaki bileşenlerden oluşur:
STEP 1 — Data Collection
Buyer demand signals
Seller supply signals
Location proximity
Pre-commit counts
STEP 2 — Opportunity Scoring
Her seller için skor hesaplanır:
score =
  w1 * active_demand_nearby +
  w2 * seller_density_score +
  w3 * precommit_count +
  w4 * product_category_match +
  w5 * buyer_to_seller_distance_score
STEP 3 — If score > threshold → Create Flash Window
Flash window oluşturulur:
Title / description
Advantage (% indirim, fixed price, bundle)
Start/End time
Eligible buyers (lokasyon bazlı)
STEP 4 — Scheduler Activates the Window
start_time geldiğinde:
Window → "ACTIVE"
Satıcıya toplu pre-commit bildirimi gönderilir
Buyer’lara pencere açıldığı duyurulur
STEP 5 — When expired → state cleanup & analytics
❄️ 9. LOCATION ENGINE (DETAILED)
Mesafe hesabı:
distance = haversine(buyer.location, seller.location)
if distance < 1.0 km:
    eligible = True
Avantaj oranı mesafeyle optimize edilebilir:
if distance < 300m → %15 indirim
if distance < 600m → %20
if distance < 900m → %30
❄️ 10. PRE-COMMIT ENGINE (DETAILED)
Buyer bir teklifi kabul edince:
precommit = PreCommit(
    id=uuid4(),
    buyer_id="B123",
    seller_id="S12",
    proposed_window_id="P45"
)
Flash window açılırsa:
Aynı seller + proposed_window_id ile eşleşen tüm pre-commit’ler toplanır
Satıcıya bildirilir:
“3 kişi bu pencereye ön katılım verdi.”
❄️ 11. FLASH WINDOW LIFECYCLE (FULL)
SCHEDULED → ACTIVE → EXPIRED
SCHEDULED
Bekleme aşaması
Pre-commit listesi toplanır
ACTIVE
Scheduler tetikler
Satıcıya toplu bildirim gider
Buyer’lara fırsat duyurulur
Participant listesi büyür
EXPIRED
Sistem kapatır
Analytics & learning eklenir
❄️ 12. SYSTEM ROADMAP (FAZLAR)
✅ FAZ 1 — Backend Fundamentals
Tamamlandı.
🚧 FAZ 2 — WhatsApp + Location + Pre-Commit
Devam ediyor.
🔮 FAZ 3 — Production
PostgreSQL DB
ML Learning Engine
Admin Dashboard
Advanced Campaign Pricing
B2B Integrations
❄️ 13. LOCAL DEVELOPMENT SETUP
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
Swagger UI:
http://localhost:8000/docs
❄️ 14. BUSINESS MODEL (HOW ICESHOP MAKES MONEY)
Micro-traffic fee → dükkâna yönlendirilen her müşteri için küçük ücret
Seller Boost → daha fazla görünürlük isteyen satıcılar
AI Optimization Subscription → premium satıcı planı
Manual Flash Window Fee → satıcı kendi penceresini açarsa
Buyer Premium → özel fırsatları önce alma
B2B / Municipality Deals
❄️ 15. FINAL NOTE FOR DEVELOPERS
Bu README, Iceshop AI backend’ine yeni başlayan her yazılımcının:
Sistemin vizyonunu,
Mimarisini,
Veri modellerini,
Servisler arası ilişkiyi,
Kampanya mantığını,
WhatsApp entegrasyonunu,
Lokasyon & pre-commit motorunu,
Kodun genişletilmesi gereken noktalarını
tek bir dokümanda tam olarak anlaması için hazırlanmıştır.
Tüm kod modülleri bu mimariye göre yapılandırılmalıdır.


