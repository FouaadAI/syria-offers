# Syria Offers / Offria – Vollständige Projektdokumentation

**Stand:** 10. Mai 2026  
**Zweck:** Dieses Dokument beschreibt die gesamte Code‑Architektur, alle Dateien, ihre Aufgaben und die zugrunde liegenden Design‑Entscheidungen. Es dient als Nachschlagewerk für zukünftige Erweiterungen, Wartung und Einarbeitung neuer Entwickler.

---

## Inhaltsverzeichnis

1. [Projektübersicht](#1-projektübersicht)
2. [Verzeichnisstruktur](#2-verzeichnisstruktur)
3. [Backend – Datei‑Referenz](#3-backend--datei-referenz)
   - [3.1 Hauptanwendung & Konfiguration](#31-hauptanwendung--konfiguration)
   - [3.2 Datenbank & Modelle](#32-datenbank--modelle)
   - [3.3 API‑Router](#33-api--router)
   - [3.4 Services](#34-services)
   - [3.5 Schemas (Pydantic)](#35-schemas-pydantic)
4. [Frontend – Datei‑Referenz](#4-frontend--datei-referenz)
   - [4.1 Haupteinstieg & Routing](#41-haupteinstieg--routing)
   - [4.2 Modelle](#42-modelle)
   - [4.3 Services](#43-services)
   - [4.4 Screens (Seiten)](#44-screens-seiten)
   - [4.5 Widgets (Wiederverwendbare Komponenten)](#45-widgets-wiederverwendbare-komponenten)
   - [4.6 Lokalisierung](#46-lokalisierung)
5. [Datenbank‑Design](#5-datenbank-design)
6. [API‑Endpunkte](#6-api-endpunkte)
7. [Entwicklungshinweise & Konventionen](#7-entwicklungshinweise--konventionen)
8. [Bekannte Probleme & Lösungen](#8-bekannte-probleme--lösungen)
9. [Zukünftige Erweiterungen](#9-zukünftige-erweiterungen)

---

## 1. Projektübersicht

**Syria Offers (Offria)** ist eine mobile Plattform (Android/iOS), die Touristen und Einheimischen hilft, Angebote und Sehenswürdigkeiten in Syrien zu entdecken, Reisen zu planen und Buchungen vorzunehmen. Die App unterstützt **Arabisch und Englisch** (umschaltbar nach Gerätesprache) und bietet einen KI‑gestützten Chatbot, der mit der Gemini‑API arbeitet.

**Technologie‑Stack:**

| Schicht | Technologie |
|---------|-------------|
| Frontend | Flutter 3.41 (Dart) |
| Backend  | FastAPI (Python 3.11) |
| Datenbank | PostgreSQL (über SQLAlchemy ORM) |
| Caching | Redis (für Rate Limiting) |
| KI | Google Gemini (2.5 Flash) |
| Deployment| Docker / Docker Compose |
| Migrationen| Alembic |

**Benutzerrollen:**
- **Gast** – kann Angebote und Services durchsuchen
- **Kunde** – kann Angebote buchen, Favoriten speichern, Chatbot nutzen
- **Händler (Merchant)** – kann Angebote erstellen und verwalten
- **Admin** – verwaltet Benutzer, Angebote, Kategorien und Buchungen

---

## 2. Verzeichnisstruktur
projekt_syr_offer/
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI‑App‑Initialisierung
│ │ ├── core/
│ │ │ ├── config.py # Umgebungsvariablen & Einstellungen
│ │ │ └── database.py # SQLAlchemy Engine & Session
│ │ ├── models/
│ │ │ ├── init.py
│ │ │ ├── user.py
│ │ │ ├── offer.py # Offer + Category
│ │ │ ├── booking.py
│ │ │ ├── merchant.py
│ │ │ └── travel_plan.py
│ │ ├── schemas/
│ │ │ ├── offer.py
│ │ │ ├── category.py
│ │ │ ├── booking.py
│ │ │ └── travel_plan.py
│ │ ├── api/v1/
│ │ │ ├── categories.py
│ │ │ ├── offers.py
│ │ │ ├── bookings.py
│ │ │ ├── auth.py
│ │ │ ├── admin.py
│ │ │ ├── merchant.py
│ │ │ ├── uploads.py
│ │ │ ├── payments.py
│ │ │ ├── flash_deals.py
│ │ │ ├── recommendations.py
│ │ │ ├── chatbot.py
│ │ │ └── travel_planner.py
│ │ └── services/
│ │ ├── payment.py
│ │ ├── recommender.py
│ │ ├── mail_service.py
│ │ ├── travel_planner.py # KI‑Logik (Gemini)
│ │ └── image_validation.py
│ ├── alembic/
│ │ ├── env.py
│ │ └── versions/
│ ├── alembic.ini
│ ├── requirements.txt
│ └── docker-compose.yml
│
└── syria_offers_app/ # Flutter‑Projekt
├── lib/
│ ├── main.dart
│ ├── config.dart
│ ├── models/
│ │ ├── category.dart
│ │ ├── offer.dart
│ │ ├── booking.dart
│ │ ├── place.dart
│ │ └── cultural_site_model.dart
│ ├── services/
│ │ ├── api_service.dart
│ │ ├── admin_api_service.dart
│ │ ├── auth_service.dart
│ │ ├── favorites_service.dart
│ │ ├── location_service.dart
│ │ ├── tourist_data_service.dart
│ │ └── cultural_data_service.dart
│ ├── screens/
│ │ ├── home_screen.dart
│ │ ├── discover_screen.dart
│ │ ├── place_detail_screen.dart
│ │ ├── offers_screen.dart
│ │ ├── offer_detail_screen.dart
│ │ ├── chat_screen.dart
│ │ ├── favorites_screen.dart
│ │ ├── cultural_sites_screen.dart
│ │ ├── cultural_site_detail_screen.dart
│ │ ├── booking_confirmation_screen.dart
│ │ ├── auth/
│ │ │ ├── login_screen.dart
│ │ │ ├── phone_login_screen.dart
│ │ │ ├── set_password_screen.dart
│ │ │ ├── verify_email_screen.dart
│ │ │ └── forgot_password_screen.dart
│ │ ├── admin/
│ │ │ ├── admin_login_screen.dart
│ │ │ ├── admin_dashboard_screen.dart
│ │ │ ├── category_list_screen.dart
│ │ │ ├── offer_list_screen.dart
│ │ │ ├── add_offer_screen.dart
│ │ │ └── booking_list_screen.dart
│ │ ├── merchant/
│ │ │ ├── merchant_dashboard_screen.dart
│ │ │ ├── merchant_offer_list_screen.dart
│ │ │ ├── merchant_add_offer_screen.dart
│ │ │ └── merchant_booking_list_screen.dart
│ │ └── payment/
│ │ ├── payment_screen.dart
│ │ └── payment_success_screen.dart
│ ├── widgets/
│ │ ├── offer_card.dart
│ │ ├── category_card.dart
│ │ └── flash_deal_card.dart
│ ├── localization/
│ │ └── app_localizations.dart
│ └── assets/
│ └── images/
├── android/app/src/main/
│ └── AndroidManifest.xml
├── ios/
├── pubspec.yaml
└── build/

---

## 3. Backend – Datei‑Referenz

### 3.1 Hauptanwendung & Konfiguration

#### `app/main.py`
- **Zweck:** Einstiegspunkt der FastAPI‑Anwendung.
- **Aufgaben:**
  - Initialisiert die Datenbank‑Engine (`create_all`).
  - Erstellt einen Gastbenutzer (`create_default_user`).
  - Registriert alle API‑Router unter `/api/v1/`.
  - Konfiguriert Middleware: CORS (alle Origins), `SlowAPI` (Rate Limiting, 100/Minute), `ForceNoCacheMiddleware` für GET‑Requests.
- **Warum so:** Zentraler Ort für alle globalen Einstellungen; durch `Base.metadata.create_all` wird die DB automatisch synchronisiert (Entwicklungsmodus).

#### `core/config.py`
- **Zweck:** Zentrale Konfiguration über `pydantic‑settings`.
- **Enthält:** `DATABASE_URL`, `SECRET_KEY`, `REDIS_URL`, `GEMINI_API_KEY`, SMTP‑Einstellungen für Brevo.
- **Warum so:** Trennung von Code und Konfiguration; Werte können per `.env`‑Datei oder Umgebungsvariablen überschrieben werden.

#### `core/database.py`
- **Zweck:** Erzeugt die SQLAlchemy‑Engine und Session‑Factory.
- **Warum so:** Wiederverwendbare Datenbankverbindung; `get_db`‑Generator wird als Dependency Injection in allen Routern genutzt.

---

### 3.2 Datenbank & Modelle

Alle Modelle erben von `Base` (declarative_base). Sie definieren die Tabellenstruktur und Beziehungen.

| Datei | Modell(e) | Wichtige Felder & Besonderheiten |
|-------|-----------|----------------------------------|
| `models/user.py` | `User` | `phone` (unique), `email`, `hashed_password`, `role` (customer/merchant/admin), `is_active` |
| `models/offer.py` | `Category`, `Offer` | `Category`: `name_ar`, `name_en`, `sort_order`; `Offer`: `title_ar/en`, `offer_price`, `latitude/longitude`, `category_id`, `approved`, `is_flash`, `image_urls` (ARRAY) |
| `models/booking.py` | `Booking`, `BookingStatus` | `Booking`: `user_id`, `offer_id`, `quantity`, `total_price`, `status` (Enum: pending/confirmed/cancelled/refunded) |
| `models/merchant.py` | `Merchant` | `user_id` (unique), `business_name`, `business_type`, `subscription_plan` |
| `models/travel_plan.py` | `TravelPlan` | `preferences` (JSON), `days`, `plan_data` (JSON), `created_at` |

**Warum so:** Die Modelle bilden die Geschäftslogik 1:1 ab. Fremdschlüssel und `relationship()` ermöglichen einfache Joins über SQLAlchemy.

---

### 3.3 API‑Router

Alle Router liegen unter `app/api/v1/` und werden in `main.py` registriert.

| Datei | Präfix | Haupt‑Endpunkte |
|-------|--------|-----------------|
| `categories.py` | `/categories` | GET `/` (alle Kategorien), POST `/` (neue anlegen) |
| `offers.py` | `/offers` | GET `/` (aktive Angebote, Filter nach `category_id`, `q`, `lat/lng`), POST `/` |
| `bookings.py` | `/bookings` | POST `/` (Buchung erstellen) |
| `auth.py` | `/auth` | `/login`, `/register`, `/verify`, `/set-password`, `/email-login`, `/forgot-password`, `/reset-password` |
| `admin.py` | `/admin` | `/login`, `/dashboard`, CRUD für Categories/Offers/Bookings, `/offers/{id}/approve` |
| `merchant.py` | `/merchant` | `/dashboard`, CRUD für eigene Offers, `/bookings` |
| `uploads.py` | `/uploads` | POST `/images` (MIME‑Validierung, 5 MB Limit, UUID‑Umbenennung) |
| `payments.py` | `/payments` | POST `/pay` (Strategy‑Pattern für ShamCash/MTN/Syriatel), POST `/refund` |
| `flash_deals.py`| `/flash-deals` | GET `/` |
| `recommendations.py` | `/recommendations` | GET `/{user_id}` (ML‑Empfehlungen) |
| `chatbot.py` | `/chatbot` | GET `/` (Gemini‑Chat mit `search_offers` und `plan_trip` Function Calling) |
| `travel_planner.py` | `/travel-planner` | POST `/generate`, GET `/{plan_id}/export-ics` |
| `reports.py` | `/reports` | GET `/daily` (Umsatz & Buchungen des Tages), GET `/top-offers` (meistgesehene Angebote) |

**Warum so:** REST‑Prinzipien; Admin‑ und Merchant‑Routen sind JWT‑geschützt (Bearer‑Token). Der Chatbot verwendet Gemini‑Function‑Calling, um die Absicht des Nutzers zu erkennen und entweder Angebote zu suchen oder einen Reiseplan zu generieren.

---

#### `api/v1/reports.py`
- **Zweck:** Berichts‑Endpunkte für Statistiken und Trends.
- **Endpunkte:**
  - `GET /reports/daily` – Liefert alle **bestätigten** Buchungen des aktuellen Tages (UTC) sowie die daraus resultierende **Gesamtumsatz**.
    - **Rückgabe:** `{ "date": "YYYY-MM-DD", "total_bookings": int, "total_revenue": float }`
  - `GET /reports/top-offers` – Listet die aktivsten, genehmigten Angebote nach **View‑Count** absteigend (default: 10 Stück).
    - **Rückgabe:** `[{ "id": int, "title": string, "views": int, "bookings": int }]`
- **Warum so:** Einfache SQLAlchemy‑Aggregationen (`func.sum`, `filter`, `count`) ohne externes BI‑Tool; direkt für Admin‑Dashboards nutzbar.

---

### 3.4 Services

#### `services/travel_planner.py`
- **Zweck:** Ruft Gemini auf, um einen strukturierten Reiseplan als JSON zu generieren.
- **Funktionen:** `build_context()` sammelt alle aktiven Angebote mit Koordinaten; `generate_travel_plan()` erstellt den Prompt und parst die JSON‑Antwort.
- **Parameter:** `lang` steuert die Ausgabesprache (ar/de/en).

#### `services/mail_service.py`
- **Zweck:** Sendet Verifizierungs‑ und Passwort‑Reset‑E‑Mails über Brevo SMTP.
- **Warum so:** Async‑SMTP mit `aiosmtplib`; HTML‑E‑Mails mit arabischem Text.

#### `services/recommender.py`
- **Zweck:** Bietet kollaboratives Filtern (NearestNeighbors) basierend auf Buchungen.
- **Fallback:** Wenn keine personalisierten Empfehlungen möglich sind, gibt der Service beliebte Angebote (Trending) zurück.

#### `services/payment.py`
- **Zweck:** Strategy‑Pattern für verschiedene lokale Zahlungsanbieter.
- **Enthält:** `PaymentProvider` (abstrakt), `ApiSyriaProvider` (Stub für ShamCash, MTN, Syriatel).

#### `services/image_validation.py`
- **Zweck:** Validiert hochgeladene Bilder mit Gemini Vision auf Kategorie‑Übereinstimmung.
- **Warum so:** Sicherstellung der Bildqualität; wird beim Erstellen eines Angebots automatisch aufgerufen.

---

### 3.5 Schemas (Pydantic)

| Datei | Klassen | Zweck |
|-------|---------|-------|
| `schemas/offer.py` | `OfferBase`, `OfferCreate`, `OfferResponse` | Request/Response‑Modelle für Angebote |
| `schemas/category.py` | `CategoryCreate`, `CategoryResponse` | Validierung für Kategorien |
| `schemas/booking.py` | `BookingCreate`, `BookingResponse` | Buchungsdaten validieren |
| `schemas/travel_plan.py` | `TravelPlanRequest`, `TravelPlanResponse` | Reiseplan‑Anfrage und -Antwort |

**Warum so:** Pydantic garantiert Typ‑Sicherheit und automatische Validierung für alle API‑Ein‑und -Ausgaben.

---

## 4. Frontend – Datei‑Referenz

### 4.1 Haupteinstieg & Routing

#### `lib/main.dart`
- **Zweck:** Initialisiert die App, definiert das Theme und die unterstützten Sprachen.
- **Wichtige Einstellungen:**
  - `localeResolutionCallback`: `ar` → Arabisch, `en` → Englisch, alles andere → Englisch.
  - `AppLocalizationsDelegate` wird registriert.
  - `Provider` für `ApiService`, `AuthService`, `AdminApiService`.
  - Routen: `/home`, `/cultural`, `/login`, `/chat`, `/merchant-dashboard` u.a.

#### `lib/config.dart`
- **Zweck:** Zentraler Ort für die Backend‑URL (`baseUrl`), die für API‑Aufrufe verwendet wird.

---

### 4.2 Modelle

| Datei | Klasse | Felder & Besonderheiten |
|-------|--------|--------------------------|
| `models/category.dart` | `Category` | `id`, `nameAr`, `nameEn`, `iconUrl`, `sortOrder`, `fromJson` |
| `models/offer.dart` | `Offer` | `id`, `titleAr/En`, `descriptionAr/En`, `offerPrice`, `latitude/longitude`, `distanceTo()`, `getDisplayTitle()`, `getDisplayLocation()` |
| `models/place.dart` | `Place`, `PlaceCategory` | `id`, `nameAr/En`, `category`, `galleryUrls`, `galleryAssets`, `latitude/longitude`, `getName()`, `getDescription()`, `getLabel()` |
| `models/cultural_site_model.dart` | `CulturalSite`, `CulturalCategory` | Ähnlich `Place`, zusätzlich `unescoStatus`, `openingHours` |
| `models/booking.dart` | `Booking` | `userName`, `userPhone`, `offerId`, `quantity`, `totalPrice` |

**Warum so:** Die Modelle spiegeln die Backend‑Schemata wider; `fromJson`‑Factory‑Methoden ermöglichen einfache Deserialisierung. Die Sprachumschaltung (`getDisplayTitle()` etc.) nutzt `Localizations.localeOf(context)`.

---

### 4.3 Services

| Datei | Klasse | Hauptmethoden |
|-------|--------|---------------|
| `services/api_service.dart` | `ApiService` | `getOffers()`, `getCategories()`, `chatQuery()`, `createBooking()`, `getFlashDeals()`, `getRecommendations()`, `uploadImages()` |
| `services/admin_api_service.dart` | `AdminApiService` | `getDashboard()`, `createOffer()`, `getBookings()`, `approveOffer()` |
| `services/auth_service.dart` | `AuthService` | `login()`, `getToken()`, `saveToken()`, `logout()` |
| `services/favorites_service.dart` | `FavoritesService` | `addFavorite()`, `removeFavorite()`, `listFavorites()` (nutzt SQLite) |
| `services/location_service.dart` | `LocationService` | `haversineDistanceKm()`, `sortOffersByDistance()` |
| `services/tourist_data_service.dart` | `TouristDataService` | `getAllPlaces()` – statische Liste aller touristischen Orte (Hotels, Restaurants, Parks, Events, etc.) |
| `services/cultural_data_service.dart` | `CulturalDataService` | `getSyrianCulturalSites()` – statische Liste von UNESCO‑Stätten, Museen, Märkten |

**Warum so:** Trennung von API‑Logik und UI; zentrale Verwaltung aller HTTP‑Aufrufe und Caching‑Strategien.

---

### 4.4 Screens (Seiten)

#### `screens/home_screen.dart`
- **Zweck:** Hauptbildschirm mit zwei Tabs (Discover / Offers).
- **Offer‑Tab:** Enthält Suchfeld, horizontale Kategorie‑Chips, Flash‑Deal‑Sektion, Empfehlungs‑Sektion (horizontal) und die vertikale Angebotsliste.
- **Discover‑Tab:** Zeigt den `DiscoverScreen` (touristische Services ohne Buchung).
- **Standort:** Die Benutzer‑ID wird aus dem JWT extrahiert (`_loadUserId`), um personalisierte Empfehlungen zu laden.

#### `screens/discover_screen.dart`
- **Zweck:** Zeigt alle Orte aus `TouristDataService` mit Filter‑Chips (Kategorien) und Entfernungsanzeige.
- **Sprachumschaltung:** Kategorienamen und Ortsnamen werden mehrsprachig über `AppLocalizations` und die Modell‑Methoden `getLabel(context)` / `getName(context)` dargestellt.

#### `screens/place_detail_screen.dart`
- **Zweck:** Detailansicht eines Ortes (Bildergalerie, Beschreibung, Öffnungszeiten, Karten‑Button).
- **Karte:** Öffnet `geo:`‑Link oder Google‑Maps‑Fallback.

#### `screens/offers_screen.dart`
- **Zweck:** Liste der Angebote für eine bestimmte Kategorie.
- **Sortierung:** Nutzt `LocationService` zur Distanzsortierung.

#### `screens/offer_detail_screen.dart`
- **Zweck:** Detailansicht eines buchbaren Angebots mit „Jetzt buchen“‑Button.
- **Buchungs‑Flow:** Öffnet ein Bottom‑Sheet für Name, Telefon, Datum, Personenzahl → `createBooking` → `BookingConfirmationScreen`.

#### `screens/booking_confirmation_screen.dart`
- **Zweck:** Erfolgsbestätigung nach einer erfolgreichen Buchung. Zeigt eine Zusammenfassung der Buchungsdetails und bietet Navigation zur Startseite oder zum Bezahlen.
- **Benötigte Parameter (alle `required`):**
  | Parameter | Typ | Beschreibung |
  |-----------|-----|--------------|
  | `bookingCode` | `String` | Vom Server generierter eindeutiger Buchungscode |
  | `userName` | `String` | Name des buchenden Nutzers |
  | `userPhone` | `String` | Telefonnummer des Nutzers |
  | `bookedAt` | `DateTime` | Zeitpunkt der Buchung |
  | `quantity` | `int` | Anzahl der gebuchten Plätze |
  | `totalPrice` | `double` | Gesamtsumme in SYP |
  | `bookingId` | `int` | Primärschlüssel der Buchung (vom Backend) für den Zahlungsflow |
- **UI‑Ablauf:**
  1. Großes Häkchen‑Icon (`Icons.check_circle`) und Dankesnachricht.
  2. **Info‑Card** mit allen Buchungsdaten (Name, Telefon, Datum, Anzahl, Preis) sowie dem hervorgehobenen `bookingCode`.
  3. **„العودة للرئيسية“** (Zurück zur Startseite) – `Navigator.pushNamedAndRemoveUntil(context, '/home', (route) => false)`
  4. **„ادفع الآن“** (Jetzt bezahlen) – Navigiert zu `PaymentScreen` und übergibt `bookingId` sowie `amount`.
- **Formatierung:** Währung wird mit `NumberFormat.currency(symbol: 'ل.س', locale: 'ar')` dargestellt; Datum via `DateFormat.yMMMd('ar')`.
- **Warum so:** Trennt Buchungsabschluss und Zahlung klar voneinander; der Nutzer erhält sofort visuelles Feedback und den Buchungscode, kann aber optional direkt zur Zahlung weitergeleitet werden.

#### `screens/chat_screen.dart`
- **Zweck:** KI‑Chatbot mit mehrzeiligem Eingabefeld (Enter = Zeilenumbruch, Senden nur per Button).
- **Sprachumschaltung:** Alle UI‑Texte (Titel, Hint, Buttons) über `AppLocalizations`.
- **Kalenderexport:** Lädt die ICS‑Datei herunter, speichert sie temporär und öffnet sie mit `open_filex`. System wählt automatisch die Kalender‑App aus.
- **Verlauf:** Sitzungs‑ID wird im State gehalten, um den Gesprächskontext zu bewahren.

#### `screens/favorites_screen.dart`
- **Zweck:** Zeigt favorisierte Angebote (gespeichert in lokaler SQLite‑DB).
- **Sprachumschaltung:** Angebotstitel und Währung werden je nach Gerätesprache angezeigt.

#### `screens/cultural_sites_screen.dart`
- **Zweck:** Liste kultureller Stätten (UNESCO, Museen, etc.) mit Filter‑Chips.
- **Sprachumschaltung:** Kategorien und Namen über die Modell‑Methoden `getLabel(context)` / `getName(context)`.

#### `screens/cultural_site_detail_screen.dart`
- **Zweck:** Detailansicht einer kulturellen Stätte (Bild, Beschreibung, Öffnungszeiten, Eintrittspreis, Karten‑Button).

#### `screens/auth/login_screen.dart`
- **Zweck:** E‑Mail‑Login mit Passwort‑Sichtbarkeits‑Toggle.
- **Sprachumschaltung:** Alle Labels über `AppLocalizations`.

#### `screens/auth/phone_login_screen.dart`
- **Zweck:** Registrierung per Telefonnummer + E‑Mail + Verifizierungscode.
- **Sprachumschaltung:** Derzeit nur arabische Texte (kann später lokalisiert werden).

#### `screens/admin/…` und `screens/merchant/…`
- **Zweck:** Admin‑ und Händler‑Dashboards für die Verwaltung von Angeboten, Kategorien und Buchungen.
- **Admin‑Login:** `admin` / `Syria2025!` (Hardcoded).

---

### 4.5 Widgets

| Datei | Widget | Zweck |
|-------|--------|-------|
| `widgets/offer_card.dart` | `OfferCard` | Karte für die Angebotsliste (Bild, Titel, Standort, Distanz, Preis) |
| `widgets/category_card.dart` | `CategoryCard` | Kategorie‑Kachel für die horizontale Liste |
| `widgets/flash_deal_card.dart` | `FlashDealCard` | Countdown‑Karte für Flash‑Angebote |

---

### 4.6 Lokalisierung

#### `localization/app_localizations.dart`
- **Zweck:** Mehrsprachige Textausgabe (Arabisch / Englisch).
- **Aufbau:** Klasse `AppLocalizations` mit Gettern für jeden Schlüssel; `AppLocalizationsDelegate` lädt die entsprechende Map (`_loadStrings`).
- **Verwendung:** `AppLocalizations.of(context)!.welcome` etc.
- **Warum so:** Keine externen `.arb`‑Dateien nötig; einfache Erweiterung durch Hinzufügen neuer Schlüssel in beiden Maps.

---

## 5. Datenbank‑Design

**Tabellen:**

| Tabelle | Spalten (Auswahl) | Besonderheiten |
|---------|-------------------|----------------|
| `users` | `id`, `phone`, `email`, `hashed_password`, `role`, `is_active` | Unique‑Constraints auf `phone` und `email` |
| `categories` | `id`, `name_ar`, `name_en`, `sort_order` | – |
| `offers` | `id`, `title_ar/en`, `offer_price`, `latitude/longitude`, `image_urls`, `approved`, `is_flash` | FK → `categories.id`, `merchants.id` |
| `merchants` | `id`, `user_id` (unique), `business_name`, `subscription_plan` | FK → `users.id` |
| `bookings` | `id`, `user_id`, `offer_id`, `booked_at`, `quantity`, `total_price`, `status` | FK → `users.id`, `offers.id` |
| `travel_plans` | `id`, `user_id`, `preferences` (JSON), `days`, `plan_data` (JSON) | Speichert generierte Reisepläne |

**Indizes** auf Primärschlüsseln, `category_id`, `merchant_id`, `user_id`.

---

## 6. API‑Endpunkte

Die vollständige Liste aller Endpunkte ist im Swagger unter `/docs` einsehbar. Hier die wichtigsten Kategorien:

| Kategorie | Endpunkte |
|-----------|-----------|
| **Auth** | `/auth/register`, `/auth/verify`, `/auth/email-login`, `/auth/set-password`, `/auth/forgot-password`, `/auth/reset-password` |
| **Offers** | `/offers/` (GET mit Filtern), `/offers/` (POST) |
| **Categories** | `/categories/` (GET, POST) |
| **Bookings** | `/bookings/` (POST) |
| **Admin** | `/admin/login`, `/admin/dashboard`, CRUD für Categories/Offers/Bookings, `/admin/offers/{id}/approve` |
| **Merchant** | `/merchant/dashboard`, CRUD für eigene Offers, `/merchant/bookings` |
| **Flash Deals** | `/flash-deals/` (GET) |
| **Recommendations** | `/recommendations/{user_id}` (GET) |
| **Chatbot** | `/chatbot/` (GET mit `query` und `session_id`) |
| **Travel Planner** | `/travel-planner/generate` (POST), `/travel-planner/{plan_id}/export-ics` (GET) |
| **Uploads** | `/uploads/images` (POST) |
| **Payments** | `/payments/pay`, `/payments/refund` |

---

## 7. Entwicklungshinweise & Konventionen

### Backend
- **Umgebungsvariablen:** Alle Secrets in `.env` (nicht im Repo).
- **Alembic:** Migrationen mit `alembic revision --autogenerate -m "message"` und `alembic upgrade head`.
- **Admin‑Benutzer:** `admin` / `Syria2025!` (nur für Entwicklung).
- **Bild‑Uploads:** Validierung mit `python-magic` (MIME) und Pillow (EXIF‑Entfernung).

### Frontend
- **Sprachumschaltung:** Immer `AppLocalizations.of(context)!` verwenden. Neue Texte in beiden Maps (Arabisch/Englisch) ergänzen.
- **API‑Aufrufe:** Über `ApiService` / `AdminApiService`; Token wird automatisch aus `AuthService` geholt.
- **Standort:** `Geolocator` für GPS; Distanzberechnung mit `LocationService.haversineDistanceKm()`.
- **Kalenderexport:** ICS‑Datei wird mit `http` heruntergeladen, in `getTemporaryDirectory()` gespeichert und mit `OpenFilex.open()` geöffnet.
- **Chat:** Sitzungs‑ID (`_sessionId`) wird über mehrere Nachrichten hinweg beibehalten.

---

## 8. Bekannte Probleme & Lösungen

| Problem | Lösung |
|---------|--------|
| **Pixel‑Overflow bei Formularen** | Alle Formular‑Screens in `SingleChildScrollView` wrappen (z.B. `login_screen.dart`). |
| **`canLaunchUrl` gibt `false` zurück** | `<queries>`‑Block im `AndroidManifest.xml` für `geo:`, `https:` und Maps‑Apps ergänzen. |
| **`AppLocalizations` nicht verfügbar in `initState`** | Initialisierung nach `didChangeDependencies` verschieben, Flag `_initialized` nutzen. |
| **ICS‑Datei wird von Google Kalender nicht akzeptiert** | `UID`, `DTSTAMP`, `DTEND` und Zeitzone (`timezone(timedelta(hours=3))`) hinzufügen. |
| **Chatbot antwortet auf Deutsch, obwohl Arabisch angefragt** | Sprache anhand der Anfragezeichen erkennen (`has_arabic`/`has_german`) und als `lang`‑Parameter an `generate_travel_plan()` und in den Antwort‑Texten verwenden. |

---

## 9. Zukünftige Erweiterungen

| Bereich | Mögliche Features |
|---------|-------------------|
| **Lokalisierung** | Weitere Sprachen hinzufügen (Türkisch, Französisch). |
| **Benachrichtigungen** | Push‑Benachrichtigungen für Flash‑Deals (FCM). |
| **Soziale Funktionen** | Reisepläne teilen, Bewertungen und Kommentare. |
| **Offline‑Modus** | Caching von Angeboten und Orten für den Offline‑Zugriff. |
| **Zahlungs‑Integration** | Echte API‑Anbindung für ShamCash, MTN Cash, Syriatel Cash. |
| **Standort‑basiertes Geo‑Fencing** | Automatische Benachrichtigung, wenn sich der Nutzer in der Nähe eines Angebots befindet. |
| **Kulturelle Stätten dynamisch laden** | Statt statischer Daten in `CulturalDataService` eine API‑Schnittstelle schaffen. |