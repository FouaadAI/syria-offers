# Modell-Registry – Syria Offers (Offria)

Dieses Dokument listet alle Datenmodelle im Flutter-Frontend und im FastAPI-Backend auf, inklusive ihrer Felder, Typen und einer kurzen Beschreibung.

---

## Inhalt

1. [Flutter-Modelle](#1-flutter-modelle)
2. [Backend-SQLAlchemy-Modelle](#2-backend-sqlalchemy-modelle)
3. [Backend-Pydantic-Schemas](#3-backend-pydantic-schemas)

---

## 1. Flutter-Modelle

### `Place` (`lib/models/place.dart`)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | `String` | Eindeutige ID des Ortes |
| `nameAr` | `String` | Name auf Arabisch |
| `nameEn` | `String` | Name auf Englisch |
| `officialTitle` | `String?` | Offizieller Titel (z. B. UNESCO) |
| `category` | `PlaceCategory` | Enum: hotel, restaurant, park, activity, event, cinema |
| `descriptionAr` | `String` | Beschreibung auf Arabisch |
| `descriptionEn` | `String` | Beschreibung auf Englisch |
| `galleryUrls` | `List<String>` | Bild-URLs |
| `galleryAssets` | `List<String>` | Lokale Asset-Pfade |
| `latitude` | `double` | Breitengrad |
| `longitude` | `double` | Längengrad |
| `openingHours` | `String?` | Öffnungszeiten |
| `phone` | `String?` | Telefonnummer |
| `website` | `String?` | Webseite |

**Hinweis:** Enthält die Extension `PlaceCategoryExtension` für lokalisierte Labels und Icons.

---

### `CulturalSite` (`lib/models/cultural_site_model.dart`)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | `String` | Eindeutige ID |
| `nameAr` | `String` | Name auf Arabisch |
| `nameEn` | `String` | Name auf Englisch |
| `officialTitle` | `String?` | Offizieller Titel |
| `category` | `CulturalCategory` | Enum: unescoSite, museum, historicalMarket, religiousSite |
| `descriptionAr` | `String` | Beschreibung auf Arabisch |
| `descriptionEn` | `String` | Beschreibung auf Englisch |
| `gallery` | `List<String>` | Bilder (URLs oder Assets) |
| `latitude` | `double` | Breitengrad |
| `longitude` | `double` | Längengrad |
| `openingHours` | `String?` | Öffnungszeiten |
| `entryFee` | `String?` | Eintrittspreis |
| `unescoStatus` | `bool` | UNESCO-Welterbe-Status |

---

### `Offer` (`lib/models/offer.dart`)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | `int` | Eindeutige ID |
| `titleAr` | `String` | Titel auf Arabisch |
| `titleEn` | `String` | Titel auf Englisch |
| `descriptionAr` | `String?` | Beschreibung auf Arabisch |
| `descriptionEn` | `String?` | Beschreibung auf Englisch |
| `originalPrice` | `double` | Originalpreis |
| `offerPrice` | `double` | Angebotspreis |
| `startDate` | `String?` | Startdatum (ISO-8601) |
| `endDate` | `String?` | Enddatum (ISO-8601) |
| `imageUrls` | `List<String>?` | Bild-URLs |
| `categoryId` | `int` | Verknüpfte Kategorie-ID |
| `isActive` | `bool` | Ist der Offer aktiv? |
| `isFlash` | `bool` | Flash-Deal? |
| `flashDiscountPercent` | `int?` | Rabatt-Prozentsatz |
| `approved` | `bool` | Admin-Genehmigung |
| `latitude` | `double?` | Breitengrad |
| `longitude` | `double?` | Längengrad |
| `locationNameAr` | `String?` | Ortsname (AR) |
| `locationNameEn` | `String?` | Ortsname (EN) |
| `purchaseTimestamp` | `DateTime?` | Kaufzeitpunkt |

**Methoden:** `fromJson`, `distanceTo`, `distanceText`, `isRefundable`, `getDisplayTitle`, `getDisplayLocation`

---

### `Category` (`lib/models/category.dart`)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | `int` | Eindeutige ID |
| `nameAr` | `String` | Name auf Arabisch |
| `nameEn` | `String` | Name auf Englisch |
| `iconUrl` | `String?` | Icon-URL |
| `sortOrder` | `int` | Sortierreihenfolge |

**Methoden:** `fromJson`

---

### `Booking` (`lib/models/booking.dart`)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `userName` | `String` | Name des Buchenden |
| `userPhone` | `String` | Telefonnummer |
| `bookedAt` | `DateTime` | Buchungszeitpunkt |
| `quantity` | `int` | Anzahl |
| `totalPrice` | `double` | Gesamtpreis |
| `offerId` | `int` | Verknüpfte Offer-ID |

---

## 2. Backend-SQLAlchemy-Modelle

### `User` (`backend/app/models/user.py`)

| Feld | Typ (DB) | Beschreibung |
|------|----------|--------------|
| `id` | `Integer, PK` | Eindeutige ID |
| `phone` | `String(20), unique` | Telefonnummer |
| `email` | `String(255), unique` | E-Mail (optional) |
| `full_name` | `String(255)` | Vollständiger Name |
| `hashed_password` | `String(255)` | Gehashter Passwort (optional für OTP-Flow) |
| `is_active` | `Boolean` | Konto aktiviert? |
| `verification_code` | `String(6)` | OTP-Code |
| `role` | `String(20)` | Rolle: customer, merchant, admin |
| `notification_settings` | `JSON` | Präferenzen für Benachrichtigungen |
| `created_at` | `DateTime` | Erstellungszeit |
| `updated_at` | `DateTime` | Letzte Aktualisierung |

---

### `Category` (`backend/app/models/offer.py`)

| Feld | Typ (DB) | Beschreibung |
|------|----------|--------------|
| `id` | `Integer, PK` | Eindeutige ID |
| `name_ar` | `String(255)` | Name auf Arabisch |
| `name_en` | `String(255)` | Name auf Englisch |
| `icon_url` | `String(500)` | Icon-URL |
| `sort_order` | `Integer` | Sortierreihenfolge |

**Relation:** `offers` → `Offer` (1:n)

---

### `Offer` (`backend/app/models/offer.py`)

| Feld | Typ (DB) | Beschreibung |
|------|----------|--------------|
| `id` | `Integer, PK` | Eindeutige ID |
| `title_ar` | `String(500)` | Titel auf Arabisch |
| `title_en` | `String(500)` | Titel auf Englisch |
| `description_ar` | `Text` | Beschreibung auf Arabisch |
| `description_en` | `Text` | Beschreibung auf Englisch |
| `original_price` | `Float` | Originalpreis |
| `offer_price` | `Float` | Angebotspreis |
| `start_date` | `DateTime` | Startdatum |
| `end_date` | `DateTime` | Enddatum |
| `is_active` | `Boolean` | Aktiv? |
| `image_urls` | `ARRAY(String)` | Bild-URLs |
| `latitude` | `Float` | Breitengrad |
| `longitude` | `Float` | Längengrad |
| `location_name_ar` | `String(500)` | Ortsname (AR) |
| `location_name_en` | `String(500)` | Ortsname (EN) |
| `max_bookings` | `Integer` | Maximale Buchungen |
| `current_bookings` | `Integer` | Aktuelle Buchungen |
| `category_id` | `Integer, FK` | Verknüpfte Kategorie |
| `is_flash` | `Boolean` | Flash-Deal? |
| `flash_discount_percent` | `Integer` | Rabatt-Prozentsatz |
| `merchant_id` | `Integer, FK` | Verknüpfter Händler |
| `approved` | `Boolean` | Admin-Genehmigung |
| `priority` | `Integer` | Priorität (0–10) |
| `view_count` | `Integer` | Anzahl Aufrufe |
| `image_quality_score` | `Integer` | Bildqualitäts-Score |
| `image_category_match` | `Boolean` | Bild-Kategorie-Übereinstimmung |
| `image_validation_message` | `Text` | Validierungsnachricht |
| `created_at` | `DateTime` | Erstellungszeit |
| `updated_at` | `DateTime` | Letzte Aktualisierung |

**Relationen:** `category` → `Category`, `merchant` → `Merchant`

---

### `Booking` (`backend/app/models/booking.py`)

| Feld | Typ (DB) | Beschreibung |
|------|----------|--------------|
| `id` | `Integer, PK` | Eindeutige ID |
| `user_id` | `Integer, FK` | Buchender Benutzer |
| `offer_id` | `Integer, FK` | Gebuchter Offer |
| `booked_at` | `DateTime` | Gewählter Termin |
| `quantity` | `Integer` | Anzahl |
| `total_price` | `Float` | Gesamtpreis |
| `status` | `Enum(BookingStatus)` | pending, confirmed, cancelled, refunded |
| `payment_id` | `String(500)` | Zahlungs-ID von externem Gateway |
| `payment_method` | `String(100)` | Zahlungsmethode |
| `created_at` | `DateTime` | Erstellungszeit |
| `updated_at` | `DateTime` | Letzte Aktualisierung |

**Relationen:** `user` → `User`, `offer` → `Offer`

---

### `Merchant` (`backend/app/models/merchant.py`)

| Feld | Typ (DB) | Beschreibung |
|------|----------|--------------|
| `id` | `Integer, PK` | Eindeutige ID |
| `user_id` | `Integer, FK, unique` | Verknüpfter Benutzer |
| `business_name` | `String(255)` | Firmenname |
| `business_type` | `Enum(BusinessType)` | restaurant, park, museum, cinema, activity, medical, other |
| `is_verified` | `Boolean` | Verifiziert? |
| `subscription_plan` | `Enum(SubscriptionPlan)` | free, premium |

**Relation:** `user` → `User`

---

### `TravelPlan` (`backend/app/models/travel_plan.py`)

| Feld | Typ (DB) | Beschreibung |
|------|----------|--------------|
| `id` | `Integer, PK` | Eindeutige ID |
| `user_id` | `Integer` | Verknüpfter Benutzer (optional, auch Gäste) |
| `preferences` | `JSON` | Interessen, Start-Stadt etc. |
| `days` | `Integer` | Anzahl der Tage |
| `plan_data` | `JSON` | Generierter Plan |
| `created_at` | `DateTime` | Erstellungszeit |

---

## 3. Backend-Pydantic-Schemas

### `CategoryBase / CategoryCreate / CategoryResponse` (`backend/app/schemas/category.py`)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `name_ar` | `str` | Name auf Arabisch |
| `name_en` | `str` | Name auf Englisch |
| `icon_url` | `str \| None` | Icon-URL |
| `sort_order` | `int` | Sortierreihenfolge |

`CategoryResponse` erweitert `CategoryBase` um `id: int`.

---

### `OfferBase / OfferCreate / OfferResponse` (`backend/app/schemas/offer.py`)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `title_ar` | `str` | Titel auf Arabisch |
| `title_en` | `str` | Titel auf Englisch |
| `description_ar` | `str \| None` | Beschreibung auf Arabisch |
| `description_en` | `str \| None` | Beschreibung auf Englisch |
| `original_price` | `float` | Originalpreis |
| `offer_price` | `float` | Angebotspreis |
| `start_date` | `datetime` | Startdatum |
| `end_date` | `datetime` | Enddatum |
| `image_urls` | `List[str] \| None` | Bild-URLs |
| `category_id` | `int` | Kategorie-ID |
| `is_flash` | `bool` | Flash-Deal? |
| `flash_discount_percent` | `int` | Rabatt-Prozentsatz |
| `latitude` | `float \| None` | Breitengrad |
| `longitude` | `float \| None` | Längengrad |
| `location_name_ar` | `str \| None` | Ortsname (AR) |
| `location_name_en` | `str \| None` | Ortsname (EN) |

`OfferResponse` erweitert `OfferBase` um:
- `id: int`
- `is_active: bool`
- `created_at: datetime`
- `image_quality_score: int \| None`
- `image_category_match: bool \| None`
- `image_validation_message: str \| None`

---

### `BookingCreate / BookingResponse` (`backend/app/schemas/booking.py`)

**BookingCreate**

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `user_name` | `str` | Name des Buchenden |
| `user_phone` | `str` | Telefonnummer |
| `offer_id` | `int` | Offer-ID |
| `booked_at` | `datetime` | Termin |
| `quantity` | `int` | Anzahl (Default: 1) |
| `total_price` | `float` | Gesamtpreis |

**BookingResponse**

Erweitert um `id`, `booking_code`, `status`, `created_at`.

---

### `TravelPlanRequest / TravelPlanResponse` (`backend/app/schemas/travel_plan.py`)

**TravelPlanRequest**

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `preferences` | `Dict[str, Any]` | Interessen, Start-Stadt etc. |
| `days` | `int` | Anzahl der Tage |

**Activity** (Nested)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `time` | `str` | Uhrzeit |
| `title` | `str` | Titel |
| `location` | `str` | Ort |
| `lat` | `float` | Breitengrad |
| `lng` | `float` | Längengrad |
| `description` | `str \| None` | Beschreibung |
| `offer_id` | `int \| None` | Verknüpfter Offer |

**DayPlan** (Nested)

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `day` | `int` | Tag-Nummer |
| `activities` | `List[Activity]` | Liste der Aktivitäten |

**TravelPlanResponse**

| Feld | Typ | Beschreibung |
|------|-----|--------------|
| `id` | `int` | Plan-ID |
| `plan` | `List[DayPlan]` | Tägliche Pläne |

---

## Zusammenfassung

| Projekt-Teil | Anzahl Modelle |
|--------------|----------------|
| Flutter (Dart) | 5 |
| Backend SQLAlchemy | 5 |
| Backend Pydantic | 4 Basis-Schemas + 6 abgeleitete |

Alle Modelle sind bidirektional zwischen Frontend und Backend abgestimmt, wobei die JSON-Serialisierung über Pydantic-Schemas (`from_attributes = True`) nahtlos erfolgt.
