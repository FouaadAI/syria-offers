import requests

import os
BASE = "http://localhost:8000/api/v1"
ADMIN = {"username": os.getenv("ADMIN_USERNAME", "admin"), "password": os.getenv("ADMIN_PASSWORD", "change-me-in-production")}

r = requests.post(f"{BASE}/admin/login", json=ADMIN)
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Kategorie-IDs holen (die Tabelle categories muss existieren)
r_cat = requests.get(f"{BASE}/categories/")   # öffentliche Kategorien
cats_data = r_cat.json()
cat_map = {c["name_en"]: c["id"] for c in cats_data}
# Falls die Kategorien nicht existieren, legen wir sie an (das passiert nur einmal)
needed = {
    "Hotels": ("فنادق", 1),
    "Restaurants": ("مطاعم", 2),
    "Museums": ("متاحف", 3),
    "Parks": ("منتزهات", 4),
    "Activities": ("أنشطة", 5),
    "Cultural Sites": ("معالم أثرية", 6),
    "Events": ("فعاليات", 7),
    "Cinema": ("سينما", 8),
}
for en_name, (ar_name, order) in needed.items():
    if en_name not in cat_map:
        resp = requests.post(f"{BASE}/admin/categories", json={
            "name_ar": ar_name, "name_en": en_name, "sort_order": order
        }, headers=headers)
        if resp.status_code == 201:
            cat_map[en_name] = resp.json()["id"]
        else:
            # Fallback: nochmal GET
            r_cat2 = requests.get(f"{BASE}/categories/")
            for c in r_cat2.json():
                if c["name_en"] == en_name:
                    cat_map[en_name] = c["id"]
print("Kategorien bereit.")

# Orte – die gleiche Liste wie in TouristDataService, aber ohne Preise (0)
places = [
    ("فندق رويال سميراميس", "Royal Semiramis Hotel", "أول فندق 5 نجوم في سوريا (1950).", "Syria's first 5-star hotel (1950).", 33.513, 36.278, "وسط المدينة", "City Centre", "Hotels"),
    ("فندق بيت زفران الساحر", "Beit Zafran Charm Hotel", "بوتيك في قلب دمشق القديمة.", "Boutique hotel in old Damascus.", 33.510, 36.292, "دمشق القديمة", "Old Damascus", "Hotels"),
    ("فندق بيت الولي", "Beit Al Wali Hotel", "بيت دمشقي من القرن 18.", "18th-century Damascene house.", 33.5096, 36.3058, "باب توما", "Bab Touma", "Hotels"),
    ("فندق شام بالاس", "Cham Palace Hotel", "5 نجوم، بولينغ، 5 مطاعم.", "5-star, bowling, 5 restaurants.", 33.5160, 36.2880, "وسط دمشق", "Central Damascus", "Hotels"),
    ("فندق ماندالون التراثي", "Mandaloune Heritage Hotel", "بوتيك رومانسي في حلب.", "Romantic boutique in Aleppo.", 36.200, 37.150, "حلب القديمة", "Old Aleppo", "Hotels"),
    ("منتجع أفاميا روتانا", "Afamia Rotana Resort", "4 مطاعم، شاطئ خاص، سبا.", "4 restaurants, private beach, spa.", 35.5215, 35.7814, "اللاذقية", "Latakia", "Hotels"),
    ("فندق لا ميرا", "La Mira Hotel", "7 طوابق على البحر.", "7-story hotel on the sea.", 35.525, 35.770, "اللاذقية", "Latakia", "Hotels"),
    ("منتجع هوليداي بيتش", "Holiday Beach Resort", "5 نجوم، شاطئ خاص.", "5-star, private beach.", 34.900, 35.870, "طرطوس", "Tartous", "Hotels"),
    ("منتجع مشتى الحلو", "Mashta al-Helou Resort", "منتجع جبلي 950م.", "Mountain resort 950m.", 34.8667, 36.2500, "مشتى الحلو", "Mashta al-Helou", "Hotels"),
    ("مطعم نارنج", "Naranj Restaurant", "أشهر مطاعم دمشق القديمة.", "Damascus' most famous restaurant.", 33.5108, 36.3032, "دمشق القديمة", "Old Damascus", "Restaurants"),
    ("مطعم توبل", "Tawabel Restaurant", "بوفيه فطور سميراميس.", "Breakfast buffet Semiramis.", 33.513, 36.278, "فندق سميراميس", "Semiramis Hotel", "Restaurants"),
    ("مطعم ماركو بولو", "Marco Polo Restaurant", "آسيوي فيوجن، عشاء فقط.", "Asian fusion, dinner only.", 33.513, 36.278, "فندق سميراميس", "Semiramis Hotel", "Restaurants"),
    ("رود هاوس ستيك هاوس", "Road House Steak House", "أفضل ستيك في دمشق.", "Damascus' best steak.", 33.540, 36.250, "دمر", "Dummar", "Restaurants"),
    ("برازيل غورمي", "Brazil Gourmet Pizzeria", "بيتزا نوتيلا الشهيرة.", "Famous Nutella pizza.", 33.520, 36.290, "وسط دمشق", "Central Damascus", "Restaurants"),
    ("مقهى د. فطاط", "Dr. Fattat", "فول وحمص 24 ساعة.", "24h foul & hummus.", 33.5133, 36.2945, "شمال القلعة", "North of Citadel", "Restaurants"),
    ("مطعم حارتنا", "Haretna Restaurant", "أجواء باب توما.", "Bab Touma vibe.", 33.5105, 36.3150, "باب توما", "Bab Touma", "Restaurants"),
    ("مطعم بيت جبري", "Beit Jabri Restaurant", "منزل دمشقي 1737.", "1737 Damascene house.", 33.5110, 36.3080, "دمشق القديمة", "Old Damascus", "Restaurants"),
    ("مثلجات بكداش", "Bakdash Ice Cream", "منذ 1895، آيس كريم المستكة.", "Since 1895, mastic ice cream.", 33.5108, 36.3008, "سوق الحميدية", "Al-Hamidiya Souq", "Restaurants"),
    ("مطعم غراند ستيشن", "Grand Station Restaurant", "إطلالة على قلعة حلب.", "Aleppo Citadel view.", 36.210, 37.140, "حلب", "Aleppo", "Restaurants"),
    ("غراند بلازا قرطبة", "Grand Plaza Qurtubah", "مشويات، كبسة، بيتزا.", "Grills, kabsa, pizza.", 36.205, 37.155, "حلب", "Aleppo", "Restaurants"),
    ("مطعم شنب", "Shanab Restaurant", "أشهر مطاعم حمص.", "Most famous in Homs.", 34.7333, 36.7167, "حمص", "Homs", "Restaurants"),
    ("مطعم مظاهر", "Mazaher Restaurant", "حجر بازلتي وخشب.", "Basalt stone & wood.", 34.730, 36.720, "حمص", "Homs", "Restaurants"),
    ("حلويات أبو اللبن", "Abu Al-Laban Sweets", "بشمانيه، فستق.", "Beshmeneh, pistachio.", 34.732, 36.718, "حمص", "Homs", "Restaurants"),
    ("مطعم المختار كفرام", "Al-Mukhtar Kafram", "غابة صنوبر ومشاوي.", "Forest restaurant.", 34.750, 36.650, "ظهر القصير", "Dhahr Al-Qaseer", "Restaurants"),
    ("حديقة تشرين", "Tishreen Park", "أكبر حديقة في دمشق.", "Largest park in Damascus.", 33.520, 36.270, "دمشق", "Damascus", "Parks"),
    ("محمية غابات الفرنلق", "Al-Furonlq Forest Reserve", "محمية طبيعية ساحلية.", "Coastal nature reserve.", 35.600, 36.000, "اللاذقية", "Latakia", "Parks"),
    ("بحيرة 16 تشرين", "Lake 16 Tishreen", "بحيرة جبلية خلابة.", "Stunning mountain lake.", 35.6554, 35.9476, "شرق اللاذقية", "East of Latakia", "Parks"),
    ("شاطئ وادي قنديل", "Wadi Qandil Beach", "رمال سوداء وغوص.", "Black sand beach.", 35.650, 35.850, "شمال اللاذقية", "North of Latakia", "Parks"),
    ("رأس البسيط", "Ras al-Basit Beach", "من أجمل شواطئ المتوسط.", "Mediterranean's finest.", 35.850, 35.917, "أقصى الشمال", "Far North", "Parks"),
    ("سوق الحميدية", "Al-Hamidiya Souq", "أكبر سوق مسقوف.", "Largest covered souq.", 33.5108, 36.3008, "دمشق القديمة", "Old Damascus", "Activities"),
    ("سوق البزورية", "Souk al-Bzourieh", "بهارات وعطارة.", "Spices & perfumery.", 33.511, 36.306, "دمشق القديمة", "Old Damascus", "Activities"),
    ("حمام نور الدين", "Hammam Nur al-Din", "حمام أيوبي 1169.", "Ayyubid bath 1169.", 33.5094, 36.3065, "دمشق القديمة", "Old Damascus", "Activities"),
    ("حمام البكري", "Hammam Al-Bakri", "أقدم حمام 1069.", "Oldest bath 1069.", 33.5108, 36.3150, "باب توما", "Bab Touma", "Activities"),
    ("ورشة صابون حلبي", "Aleppo Soap Workshop", "صابون الغار التقليدي.", "Traditional laurel soap.", 36.200, 37.155, "حلب", "Aleppo", "Activities"),
    ("جزيرة أرواد", "Arwad Island Boat Trip", "الجزيرة المأهولة الوحيدة.", "Syria's only inhabited island.", 34.855, 35.858, "طرطوس", "Tartous", "Activities"),
    ("تسلق جبال حميولي", "Kassab Himouli Hike", "مسار 2 كم، 950م.", "2 km trail, 950m.", 35.920, 35.980, "كسب", "Kassab", "Activities"),
    ("بولينغ شام بالاس", "Cham Palace Bowling", "صالة بولينغ حديثة.", "Modern bowling alley.", 33.5160, 36.2880, "فندق شام بالاس", "Cham Palace Hotel", "Activities"),
    ("سينما سيتي دمشق", "Cinema City Damascus", "سينما بشاشتين.", "Twin-screen cinema.", 33.510, 36.290, "دمشق", "Damascus", "Cinema"),
    ("سينما دمشق", "Cinema Dimashq", "4 قاعات، بار سوشي.", "4 screens, sushi bar.", 33.512, 36.288, "دمشق", "Damascus", "Cinema"),
    ("مهرجان إشراقات", "Ishraqat Festival", "فنون وتراث فبراير.", "Art & heritage Feb.", 33.512, 36.280, "دار الأوبرا", "Opera House", "Events"),
    ("مهرجان حمص التراثي", "Homs Heritage Festival", "احتفال ثقافي أبريل.", "Cultural celebration April.", 34.7333, 36.7167, "حمص", "Homs", "Events"),
    ("مهرجان أكيتو", "Akitu Festival", "رأس السنة الآشورية.", "Assyrian New Year.", 36.200, 37.150, "حلب", "Aleppo", "Events"),
    ("جولة رمضان الكبرى", "Grand Ramadan Tour", "8 أيام عبر سوريا.", "8 days across Syria.", 33.510, 36.300, "كل سوريا", "All Syria", "Events"),
    ("كرنفال مرمريتا", "Marmarita Carnival", "أزياء وموسيقى أغسطس.", "Costumes & music Aug.", 34.7833, 36.2833, "مرمريتا", "Marmarita", "Events"),
    ("معرض سوريا للسفر", "Syria Travel Show", "14-16 أبريل دمشق.", "April 14-16 Damascus.", 33.513, 36.280, "دمشق", "Damascus", "Events"),
    ("مهرجان وطن", "Watan Festival Tartous", "عروض وبازار مايو.", "Shows & bazaar May.", 34.890, 35.885, "طرطوس", "Tartous", "Events"),
]

for ar, en, desc_ar, desc_en, lat, lng, loc_ar, loc_en, cat in places:
    payload = {
        "title_ar": ar, "title_en": en,
        "description_ar": desc_ar, "description_en": desc_en,
        "original_price": 0, "offer_price": 0,
        "start_date": "2026-01-01T00:00:00Z", "end_date": "2026-12-31T23:59:59Z",
        "category_id": cat_map[cat],
        "latitude": lat, "longitude": lng,
        "location_name_ar": loc_ar, "location_name_en": loc_en,
        "image_urls": [],
        "is_flash": False, "flash_discount_percent": 0
    }
    resp = requests.post(f"{BASE}/admin/offers", json=payload, headers=headers)
    if resp.status_code == 201:
        print(f"✅ {ar}")
    else:
        print(f"❌ {ar}: {resp.text}")

print("\nImport abgeschlossen.")