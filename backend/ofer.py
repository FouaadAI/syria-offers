import requests
import os

BASE = "http://localhost:8000/api/v1"
ADMIN = {"username": os.getenv("ADMIN_USERNAME", "admin"), "password": os.getenv("ADMIN_PASSWORD", "change-me-in-production")}

r = requests.post(f"{BASE}/admin/login", json=ADMIN)
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# ---------- Kategorien ----------
cats = [
    ("فنادق", "Hotels", 1), ("مطاعم", "Restaurants", 2), ("متاحف", "Museums", 3),
    ("منتزهات", "Parks", 4), ("أنشطة", "Activities", 5), ("معالم أثرية", "Cultural Sites", 6),
    ("فعاليات", "Events", 7), ("سينما", "Cinema", 8),
]
cat_ids = {}
for name_ar, name_en, order in cats:
    r = requests.post(f"{BASE}/admin/categories", json={
        "name_ar": name_ar, "name_en": name_en, "sort_order": order
    }, headers=headers)
    if r.status_code == 201:
        cat_ids[name_en] = r.json()["id"]
        print(f"✅ Kategorie: {name_ar} (ID={cat_ids[name_en]})")
    else:
        r_get = requests.get(f"{BASE}/admin/categories", headers=headers)
        for c in r_get.json():
            if c["name_en"] == name_en:
                cat_ids[name_en] = c["id"]
                print(f"ℹ️  Kategorie existiert: {name_ar} (ID={cat_ids[name_en]})")

# ---------- Hilfsfunktion ----------
def add_offer(title_ar, title_en, desc_ar, desc_en, orig, offer,
              lat, lng, loc_ar, loc_en, cat_key, img_urls, is_flash=False, flash_pct=0):
    payload = {
        "title_ar": title_ar, "title_en": title_en,
        "description_ar": desc_ar, "description_en": desc_en,
        "original_price": orig, "offer_price": offer,
        "start_date": "2026-01-01T00:00:00Z", "end_date": "2026-12-31T23:59:59Z",
        "category_id": cat_ids[cat_key],
        "latitude": lat, "longitude": lng,
        "location_name_ar": loc_ar, "location_name_en": loc_en,
        "image_urls": img_urls,
        "is_flash": is_flash, "flash_discount_percent": flash_pct
    }
    r = requests.post(f"{BASE}/admin/offers", json=payload, headers=headers)
    if r.status_code == 201:
        print(f"  ✅ {title_ar}")
    else:
        print(f"  ❌ {title_ar}: {r.text}")

# ===================== DAMASKUS =====================
add_offer("فندق رويال سميراميس", "Royal Semiramis Hotel",
    "أول فندق 5 نجوم في سوريا (1950). مسبح على السطح، مطعم توبل، مطعم ماركو بولو.",
    "Syria's first 5-star hotel (1950). Rooftop pool, Tawabel & Marco Polo restaurants.",
    560, 460, 33.5130, 36.2780, "وسط المدينة", "City Centre", "Hotels",
    ["https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800"])

add_offer("فندق بيت زفران الساحر", "Beit Zafran Charm Hotel",
    "فندق بوتيك ساحر في قلب دمشق القديمة. تديره وكالة نوافير للسفر.",
    "Charming boutique hotel in the heart of old Damascus, operated by Nawafir Travel.",
    280, 220, 33.5100, 36.2920, "دمشق القديمة", "Old Damascus", "Hotels",
    ["https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800"])

add_offer("فندق بيت الولي", "Beit Al Wali Hotel",
    "فندق من القرن الثامن عشر في قلب دمشق القديمة. فخامة تقليدية وأجواء ترحيبية.",
    "18th-century Damascene house hotel. Traditional luxury and welcoming atmosphere.",
    320, 260, 33.5096, 36.3058, "دمشق القديمة - باب توما", "Old Damascus - Bab Touma", "Hotels",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

add_offer("مطعم نارنج", "Naranj Restaurant",
    "أشهر مطاعم دمشق في المدينة القديمة. أطباق سورية أصيلة، أجواء فاخرة.",
    "Damascus' most famous restaurant in the Old City. Authentic Syrian cuisine.",
    80, 65, 33.5108, 36.3032, "دمشق القديمة", "Old Damascus", "Restaurants",
    ["https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800"])

add_offer("مطعم توبل - الفطور الدمشقي", "Tawabel Restaurant - Damascene Breakfast",
    "بوفيه فطور في الطابق السابع من فندق رويال سميراميس. أطباق سورية تقليدية.",
    "Breakfast buffet on the 7th floor of Royal Semiramis. Traditional Syrian dishes.",
    45, 35, 33.5130, 36.2780, "فندق رويال سميراميس - الطابق 7", "Royal Semiramis Hotel - 7th Floor", "Restaurants",
    ["https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=800"], True, 22)

add_offer("مطعم ماركو بولو", "Marco Polo Restaurant",
    "المطعم الوحيد في سوريا المتخصص بالمطبخ الآسيوي المدمج. يفتح للعشاء فقط.",
    "Syria's only Asian fusion restaurant. Dinner only. A unique culinary experience.",
    95, 75, 33.5130, 36.2780, "فندق رويال سميراميس", "Royal Semiramis Hotel", "Restaurants",
    ["https://images.unsplash.com/photo-1553621042-f6e147245754?w=800"], True, 21)

add_offer("رود هاوس ستيك هاوس", "Road House Steak House",
    "من أفضل مطاعم اللحوم في دمشق. حصص كبيرة، تشكيلة واسعة من الستيك.",
    "One of Damascus' best steakhouses. Generous portions, large steak selection.",
    70, 55, 33.5400, 36.2500, "دمر", "Dummar", "Restaurants",
    ["https://images.unsplash.com/photo-1558030006-450675393462?w=800"])

add_offer("برازيل غورمي بيتزا آند غريل", "Brazil Gourmet Pizzeria & Grill",
    "بيتزا نوتيلا الشهيرة. مطعم متميز مناسب للمناسبات العائلية. تقييم 4.4★.",
    "Home of the famous Nutella pizza. Upscale dining for family occasions. 4.4★ rating.",
    65, 50, 33.5200, 36.2900, "وسط دمشق", "Central Damascus", "Restaurants",
    ["https://images.unsplash.com/photo-1513104890138-7c749659a591?w=800"])

add_offer("مقهى الدكتور فطاط", "Dr. Fattat",
    "مؤسسة دمشقية أسطورية تقدم فطور الفول والحمص على مدار الساعة. أجواء شعبية أصيلة.",
    "Legendary Damascus institution serving foul and hummus breakfast day and night.",
    20, 15, 33.5133, 36.2945, "شمال قلعة دمشق", "North of Damascus Citadel", "Restaurants",
    ["https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800"])

add_offer("المتحف الوطني بدمشق", "National Museum of Damascus",
    "أكبر وأقدم متحف في سوريا (تأسس 1919). مكتشفات ماري وإيبلا وأوغاريت.",
    "Syria's largest and oldest museum (founded 1919). Mari, Ebla, Ugarit discoveries.",
    100, 100, 33.5125, 36.2900, "شارع شكري القوتلي", "Shukri al-Quwatli Street", "Museums",
    ["https://images.unsplash.com/photo-1582555172866-f73bb12defab?w=800"])

add_offer("متحف البيت الشامي", "Al-Bayt al-Shami Museum",
    "متحف تاريخي لدمشق في بيت شامي تقليدي. يعرض الحياة اليومية والتقاليد الدمشقية.",
    "Historical museum of Damascus in a traditional Damascene house.",
    50, 50, 33.5100, 36.3050, "دمشق القديمة", "Old Damascus", "Museums",
    ["https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800"])

add_offer("حديقة تشرين", "Tishreen Park",
    "أكبر حديقة في دمشق (71 فدان). مسارات مشي، ملاعب أطفال، نوافير، مناطق شواء.",
    "Largest park in Damascus (71 acres). Walking paths, playgrounds, water features.",
    0, 0, 33.5200, 36.2700, "دمشق - حي تشرين", "Damascus - Tishreen District", "Parks",
    ["https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800"])

add_offer("سوق الحميدية", "Al-Hamidiya Souq",
    "أكبر سوق مسقوف في سوريا من العصر العثماني (1780). أقمشة، تحف، عطور، حلويات، ذهب.",
    "Syria's largest covered market from Ottoman era (1780). Fabrics, antiques, gold.",
    0, 0, 33.5108, 36.3008, "دمشق القديمة", "Old Damascus", "Activities",
    ["https://images.unsplash.com/photo-1559589689-577aabd1db4f?w=800"])

add_offer("سوق البزورية", "Souk al-Bzourieh",
    "من أقدم أسواق دمشق خلف الجامع الأموي. بهارات وعطارة وحلويات دمشقية تقليدية.",
    "One of Damascus' oldest souqs behind the Umayyad Mosque. Spices, traditional sweets.",
    0, 0, 33.5110, 36.3060, "دمشق القديمة", "Old Damascus", "Activities",
    ["https://images.unsplash.com/photo-1465146633011-14f8e0781093?w=800"])

add_offer("قلعة دمشق", "Citadel of Damascus",
    "حصن من العصرين السلجوقي والأيوبي (القرن 11-13). 12 برجاً وبوابة ضخمة. موقع تراث عالمي.",
    "Fortress from Seljuk & Ayyubid eras. 12 towers, monumental gate. UNESCO World Heritage.",
    50, 50, 33.5117, 36.3019, "دمشق القديمة", "Old Damascus", "Cultural Sites",
    ["https://images.unsplash.com/photo-1590767161356-9e0b8c1f3f1b?w=800"])

add_offer("الجامع الأموي الكبير", "Umayyad Mosque",
    "تحفة معمارية من القرن الثامن الميلادي. رابع أشهر مسجد في الإسلام. ضريح النبي يحيى.",
    "8th-century architectural masterpiece. Fourth holiest mosque in Islam.",
    100, 100, 33.5116, 36.3067, "دمشق القديمة", "Old Damascus", "Cultural Sites",
    ["https://images.unsplash.com/photo-1578895101408-1a36b834405b?w=800"])

add_offer("دمشق القديمة - جولة تراثية", "Old Damascus Heritage Walk",
    "أقدم عاصمة مأهولة في العالم (منذ 635 ق.م). أزقة ضيقة، أسواق نابضة، معالم أثرية.",
    "Oldest continuously inhabited capital (since 635 BC). Narrow alleys, bustling souks.",
    0, 0, 33.5100, 36.3000, "دمشق القديمة", "Old Damascus", "Cultural Sites",
    ["https://images.unsplash.com/photo-1604147706283-d7119b5b822c?w=800"])

add_offer("حمام نور الدين", "Hammam Nur al-Din",
    "حمام تاريخي من العصر الأيوبي (1169). قباب وقاعات رخامية. تجربة حمام سوري أصيل.",
    "Historic bathhouse from the Ayyubid era (1169). Domes and marble halls.",
    30, 25, 33.5094, 36.3065, "دمشق القديمة", "Old Damascus", "Activities",
    ["https://images.unsplash.com/photo-1540555700478-4be289fbeca6?w=800"])

add_offer("حمام البكري", "Hammam Al-Bakri",
    "أقدم حمام عام في دمشق (1069). في حي باب توما. هندسة معمارية مملوكية رائعة.",
    "Oldest public bath in Damascus (1069). In Bab Touma neighborhood.",
    25, 20, 33.5108, 36.3150, "باب توما", "Bab Touma", "Activities",
    ["https://images.unsplash.com/photo-1560185007-5f0bb1866cab?w=800"])

# ===================== MAALOULA & SAIDNAYA =====================
add_offer("دير مار تقلا - معلولا", "St. Thecla Monastery - Maaloula",
    "أقدم دير في العالم (55 م). في بلدة معلولا الجبلية حيث يتحدث السكان الآرامية.",
    "World's oldest monastery (55 AD). In Maaloula where residents speak Aramaic.",
    30, 30, 33.8442, 36.5467, "معلولا", "Maaloula", "Cultural Sites",
    ["https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=800"])

add_offer("دير سيدة صيدنايا", "Our Lady of Saidnaya Monastery",
    "دير أرثوذكسي يوناني من القرن السادس. يحج إليه آلاف المسيحيين والمسلمين سنوياً.",
    "6th-century Greek Orthodox monastery. Thousands pilgrimage here annually.",
    25, 25, 33.6996, 36.3750, "صيدنايا", "Saidnaya", "Cultural Sites",
    ["https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=800"])

# ===================== ALEPPO =====================
add_offer("فندق ماندالون التراثي", "Mandaloune Heritage Hotel",
    "فندق بوتيك رومانسي مع مطعمين: الطلية والقناطر. بار مقبب، تجربة فريدة في حلب.",
    "Romantic boutique hotel with 2 restaurants. Vaulted bar, unique Aleppo experience.",
    350, 280, 36.2000, 37.1500, "حلب القديمة", "Old Aleppo", "Hotels",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

add_offer("مطعم غراند ستيشن", "Grand Station Restaurant",
    "مطعم عصري في حلب. أكل أصيل، خدمة فاخرة مع إطلالة مذهلة على القلعة.",
    "Modern restaurant in Aleppo. Authentic food, luxury service with citadel view.",
    60, 45, 36.2100, 37.1400, "مقابل قلعة حلب", "Opposite Aleppo Citadel", "Restaurants",
    ["https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800"], True, 25)

add_offer("قلعة حلب", "Citadel of Aleppo",
    "إحدى أقدم وأكبر القلاع في العالم. تل بارتفاع 50م. بانوراما 360°. تقييم 4.80★.",
    "One of the oldest & largest castles in the world. 50m hill. 4.80★ rating.",
    100, 100, 36.1992, 37.1625, "وسط حلب", "Central Aleppo", "Cultural Sites",
    ["https://images.unsplash.com/photo-1627894483216-2138a5bbbb66?w=800"])

add_offer("المتحف الوطني بحلب", "National Museum of Aleppo",
    "مجموعة أثرية هامة من شمال غرب سوريا. قطع من ممالك قديمة وحقب إسلامية.",
    "Important archaeological collection from northwest Syria.",
    50, 50, 36.2038, 37.1506, "حلب", "Aleppo", "Museums",
    ["https://images.unsplash.com/photo-1569154941061-e231b4725ef1?w=800"])

add_offer("سوق المدينة - حلب", "Al-Madina Souq - Aleppo",
    "أكبر سوق مسقوف في العالم (13 كم). أسواق متخصصة: الصياغ، النحاسين، الصوف.",
    "World's largest covered market (13 km). Specialized souqs: jewelry, copper, wool.",
    0, 0, 36.2000, 37.1570, "حلب القديمة", "Old Aleppo", "Activities",
    ["https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=800"])

add_offer("حمام يلبغا", "Hammam Yalbugha",
    "حمام مملوكي من عام 1491 بجوار قلعة حلب. بناه أمير حلب سيف الدين يلبغا الناصري.",
    "Mamluk bathhouse from 1491 next to Aleppo Citadel. Built by Emir Yalbugha.",
    20, 15, 36.1975, 37.1636, "بجوار قلعة حلب", "Next to Aleppo Citadel", "Activities",
    ["https://images.unsplash.com/photo-1540555700478-4be289fbeca6?w=800"])

# ===================== HOMS & KRAK =====================
add_offer("مطعم شنب", "Shanab Restaurant",
    "أشهر مطاعم حمص التقليدية قرب القلعة. أطباق لبنانية أصيلة: مشاوي، مقبلات.",
    "Most recommended traditional Homs restaurant near the Citadel.",
    55, 42, 34.7333, 36.7167, "قرب قلعة حمص", "Near Homs Citadel", "Restaurants",
    ["https://images.unsplash.com/photo-1544025162-d76694265947?w=800"], True, 24)

add_offer("مطعم مظاهر", "Mazaher Restaurant",
    "في حي الحميدية التاريخي. عمارة الحجر البازلتي والخشب المزخرف. مشاوي ومقبلات شرقية.",
    "In historic Al-Hamidiya district. Basalt stone architecture, ornate wood details.",
    50, 38, 34.7300, 36.7200, "حي الحميدية", "Al-Hamidiya District", "Restaurants",
    ["https://images.unsplash.com/photo-1559329007-40df8a9345d8?w=800"])

add_offer("حلويات أبو اللبن", "Abu Al-Laban Sweets",
    "أشهر محل حلويات في حمص. بشمانيه، حلويات غنية بالفستق، كنافة.",
    "Most famous sweets shop in Homs. Beshmeneh, pistachio-rich desserts.",
    20, 15, 34.7320, 36.7180, "وسط حمص", "Central Homs", "Restaurants",
    ["https://images.unsplash.com/photo-1551024506-0bccd828d307?w=800"])

add_offer("قلعة الحصن - Krak des Chevaliers", "Krak des Chevaliers",
    "أهم قلاع الفرسان الصليبيين وأكثرها حفظاً في العالم. موقع تراث عالمي.",
    "The most important and best-preserved Crusader castle in the world. UNESCO site.",
    100, 100, 34.7567, 36.2947, "غرب حمص", "West of Homs", "Cultural Sites",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

add_offer("مطعم المختار كفرام", "Al-Mukhtar Kafram",
    "مطعم في غابة ظهر القصير بين الصنوبر والكستناء. مشاوي، مزة كبيرة، تجربة ريفية.",
    "Forest restaurant among pines & chestnuts. Grilled meats, generous mezze.",
    45, 35, 34.7500, 36.6500, "ظهر القصير", "Dhahr Al-Qaseer", "Restaurants",
    ["https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800"])

# ===================== LATAKIA & KÜSTE =====================
add_offer("منتجع أفاميا روتانا", "Afamia Rotana Resort",
    "4 مطاعم، 2 مسابح خارجية، مسبح أطفال، شاطئ خاص، 24h خدمة غرف، سبا.",
    "4 restaurants, 2 outdoor pools, children's pool, private beach, 24h room service.",
    380, 300, 35.5215, 35.7814, "الشاطئ الأزرق - اللاذقية", "Blue Beach - Latakia", "Hotels",
    ["https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800"], True, 21)

add_offer("منتجع بلو بيتش", "Blue Beach Resort",
    "منتجع فاخر على شاطئ المتوسط. مسابح، شاطئ خاص، أنشطة مائية، برامج ترفيهية.",
    "Luxury Mediterranean beach resort. Pools, private beach, water activities.",
    120, 90, 35.5300, 35.7700, "شمال اللاذقية", "North of Latakia", "Parks",
    ["https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800"], True, 25)

add_offer("محمية غابات الفرنلق", "Al-Furonlq Forest Reserve",
    "محمية طبيعية ساحلية غنية بالتنوع البيولوجي. تخييم، مسارات، هواء نقي.",
    "Coastal nature reserve rich in biodiversity. Camping, trails, fresh air.",
    50, 50, 35.6000, 36.0000, "ريف اللاذقية", "Latakia Countryside", "Parks",
    ["https://images.unsplash.com/photo-1448375240586-882707db888b?w=800"])

add_offer("بحيرة 16 تشرين", "Lake 16 Tishreen",
    "بحيرة خلابة تحيط بها الجبال والغابات. جزر صغيرة، أشجار صنوبر وبلوط.",
    "Stunning lake surrounded by mountains and forests. Small islands, pine and oak trees.",
    30, 30, 35.6554, 35.9476, "شرق اللاذقية", "East of Latakia", "Parks",
    ["https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800"])

add_offer("قلعة صلاح الدين - صهيون", "Citadel of Salah Ed-Din",
    "حصن بيزنطي-صليبي مذهل على حافة جبلية بين واديين. موقع تراث عالمي.",
    "Stunning Byzantine-Crusader fortress on a ridge between two ravines. UNESCO site.",
    100, 100, 35.5958, 36.0572, "30 كم شرق اللاذقية", "30 km east of Latakia", "Cultural Sites",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

add_offer("المتحف الوطني باللاذقية", "National Museum of Latakia",
    "مجموعات أثرية من الساحل السوري. قطع من أوغاريت ورأس شمرة.",
    "Archaeological collections from the Syrian coast. Ugarit and Ras Shamra artifacts.",
    50, 50, 35.5170, 35.7830, "اللاذقية", "Latakia", "Museums",
    ["https://images.unsplash.com/photo-1582555172866-f73bb12defab?w=800"])

# ===================== TARTUS & KÜSTE =====================
add_offer("المتحف الوطني بطرطوس", "National Museum of Tartous",
    "في كاتدرائية صليبية سابقة من القرن 12. آثار فينيقية ورومانية وصليبية.",
    "In a former 12th-century Crusader cathedral. Phoenician, Roman, Crusader artifacts.",
    50, 50, 34.8830, 35.8830, "طرطوس", "Tartous", "Museums",
    ["https://images.unsplash.com/photo-1582555172866-f73bb12defab?w=800"])

add_offer("قلعة المرقب", "Qalaat Marqab (Margat Castle)",
    "حصن صليبي ضخم على قمة بركان خامد بارتفاع 500م. 14 برجاً دفاعياً.",
    "Massive Crusader fortress on extinct volcano (500m). 14 defensive towers.",
    80, 80, 35.1511, 35.9492, "بين طرطوس واللاذقية", "Between Tartous and Latakia", "Cultural Sites",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

add_offer("معبد عمريت المائي", "Amrit Water Temple",
    "معبد فينيقي فريد من القرن الثالث ق.م محفور في الصخر ومحاط ببركة مقدسة.",
    "Unique Phoenician water temple (3rd c. BC) carved into rock, sacred pool.",
    60, 60, 34.8330, 35.9170, "جنوب طرطوس", "South of Tartous", "Cultural Sites",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

# ===================== PALMYRA =====================
add_offer("مدينة تدمر الأثرية", "Palmyra (Tadmor)",
    "جوهرة الصحراء السورية الأسطورية. معبد بعل، قوس النصر، المسرح القديم.",
    "Syria's legendary desert jewel. Temple of Bel, Arch of Triumph, ancient theater.",
    100, 100, 34.5560, 38.2810, "تدمر - البادية السورية", "Palmyra - Syrian Desert", "Cultural Sites",
    ["https://images.unsplash.com/photo-1590767161356-9e0b8c1f3f1b?w=800"])

# ===================== BOSRA =====================
add_offer("مدينة بصرى الأثرية", "Bosra Archaeological Site",
    "أفضل مسرح روماني محفوظ في العالم (17000 متفرج). بازلت أسود.",
    "Best preserved Roman theater in the world (17,000 seats). Black basalt.",
    100, 100, 32.5178, 36.4817, "بصرى - جنوب سوريا", "Bosra - Southern Syria", "Cultural Sites",
    ["https://images.unsplash.com/photo-1582555172866-f73bb12defab?w=800"])

# ===================== ARCHÄOLOGISCHE STÄTTEN =====================
add_offer("مدينة أفاميا الأثرية", "Apamea Archaeological Site",
    "مدينة هيلينستية-رومانية. طريق الأعمدة الرئيسي يمتد 2 كم.",
    "Hellenistic-Roman city. Great Colonnade stretches 2 km.",
    70, 70, 35.4180, 36.3980, "شمال غرب حماة", "Northwest of Hama", "Cultural Sites",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

add_offer("أوغاريت - رأس شمرة", "Ugarit (Ras Shamra)",
    "مملكة قديمة على ساحل المتوسط (1450-1200 ق.م). أقدم أبجدية في العالم.",
    "Ancient kingdom on the Mediterranean coast (1450-1200 BC). World's oldest alphabet.",
    60, 60, 35.6020, 35.7820, "شمال اللاذقية", "North of Latakia", "Cultural Sites",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

add_offer("نواعير حماة", "Norias of Hama",
    "نواعير خشبية عملاقة من القرن 13 على نهر العاصي. من أكبر النواعير في العالم.",
    "Giant wooden water wheels from 13th c. on the Orontes River.",
    0, 0, 35.1333, 36.7500, "حماة - نهر العاصي", "Hama - Orontes River", "Cultural Sites",
    ["https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800"])

# ===================== FESTIVALS =====================
def add_festival(title_ar, title_en, desc_ar, desc_en, orig, offer,
                 lat, lng, loc_ar, loc_en, start_dt, end_dt, img_urls):
    payload = {
        "title_ar": title_ar, "title_en": title_en,
        "description_ar": desc_ar, "description_en": desc_en,
        "original_price": orig, "offer_price": offer,
        "start_date": start_dt + "T00:00:00Z", "end_date": end_dt + "T23:59:59Z",
        "category_id": cat_ids["Events"],
        "latitude": lat, "longitude": lng,
        "location_name_ar": loc_ar, "location_name_en": loc_en,
        "image_urls": img_urls,
        "is_flash": False, "flash_discount_percent": 0
    }
    r = requests.post(f"{BASE}/admin/offers", json=payload, headers=headers)
    if r.status_code == 201:
        print(f"  ✅ {title_ar}")
    else:
        print(f"  ❌ {title_ar}: {r.text}")

add_festival("مهرجان إشراقات - دار الأوبرا", "Ishraqat Festival – Opera House",
    "معرض فنون جميلة، معرض تراث، مناطق تفاعلية. فبراير 2026.",
    "Fine art exhibition, heritage exhibition, interactive zones. February 2026.",
    30, 30, 33.5120, 36.2800, "دار الأوبرا - دمشق", "Opera House - Damascus",
    "2026-02-08", "2026-02-12",
    ["https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800"])

add_festival("مهرجان حمص التراثي", "Homs Heritage Festival",
    "احتفال بعودة الحياة الثقافية. شارع رئيسي في حمص، أبريل 2026.",
    "Celebration of cultural revival. Main street, Homs, April 2026.",
    0, 0, 34.7333, 36.7167, "حمص - الشارع الرئيسي", "Homs - Main Street",
    "2026-04-15", "2026-04-16",
    ["https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800"])

add_festival("مهرجان أكيتو - رأس السنة الآشورية", "Akitu Festival",
    "احتفال برأس السنة الآشورية-السريانية 6776. عروض ثقافية ورقصات تقليدية.",
    "Assyrian-Syriac New Year 6776 celebration. Cultural performances & dances.",
    20, 20, 36.2000, 37.1500, "حلب", "Aleppo",
    "2026-04-04", "2026-04-04",
    ["https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800"])

add_festival("جولة رمضان الكبرى", "Grand Ramadan Tour - 8 Days",
    "8 أيام: دمشق، معلولا، حمص، حلب، تدمر، قلعة الحصن، بصرى. تجربة عمر.",
    "8 days: Damascus, Maaloula, Homs, Aleppo, Palmyra, Krak, Bosra. Lifetime experience.",
    2800, 2200, 33.5100, 36.3000, "جولة سوريا الكبرى", "Grand Syria Tour",
    "2026-02-20", "2026-03-20",
    ["https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800"])

print("\n🎉 ALLE ANGEBOTE ERFOLGREICH EINGEFÜGT!")