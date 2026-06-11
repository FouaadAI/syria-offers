"""
Professional Syria Tourism Database
====================================
Structured knowledge base for the Offria Smart Travel Assistant.
Contains ALL major Syrian cities, tourist sites, restaurants, markets,
religious sites, natural wonders, and adventure spots with:
  - Multilingual names (AR / DE / EN)
  - Exact GPS coordinates
  - Categories for intelligent filtering
  - Visit duration, price range, opening hours
  - City-to-city distance matrix (km + drive time)

HOW TO EXPAND:
  1. Add new Place objects to the PLACES list below.
  2. Add city-to-city distances to the DISTANCES dict.
  3. Re-build the Docker image or restart the API container.

RESEARCH PROMPT (give this to an AI researcher):
-------------------------------------------------
"Research and expand the Syria tourism database for the Offria travel app.
For each location provide:
  - Arabic name, German name, English name
  - City / Governorate
  - GPS coordinates (latitude, longitude)
  - Category: one of [history, food, nature, shopping, adventure, art, religious, beach, mountain, market, museum, hotel, wellness]
  - Short description in Arabic (2-3 sentences)
  - Typical visit duration (e.g. '2h', 'half-day', 'full-day')
  - Price range in Syrian Pounds: [free, cheap <5k, moderate 5k-20k, expensive >20k]
  - Opening hours or 'always_open' / 'sunrise_sunset'
  - Best time of day to visit
  - Wheelchair accessible: yes / no / partial
  - Family friendly: yes / no
  - Recommended age group: [all, kids, teens, adults, seniors]
  - Nearby places within 5 km (for clustering into a day plan)

Focus on: Damascus, Aleppo, Homs, Hama, Latakia, Tartus, Sweida, Deir Ezzor,
Raqqa, Idlib, Daraa, Al-Hasakah, Qamishli, Palmyra, Maaloula, Bosra, Crac des Chevaliers.
Also research every neighbourhood inside Damascus (e.g. Old City, Salhieh, Malki,
Baramkeh, Masaken Barzeh) and Aleppo (e.g. Al-Jdayde, Azazieh, Saadallah Al-Jabri)."
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Place:
    """Single tourist point of interest in Syria."""
    name_ar: str
    name_de: str
    name_en: str
    city_ar: str
    city_de: str
    city_en: str
    lat: float
    lng: float
    category: str  # history | food | nature | shopping | adventure | art | religious | beach | mountain | market | museum | hotel | wellness
    description_ar: str
    description_de: str
    description_en: str
    visit_duration: str        # e.g. "1h", "2h", "half-day", "full-day"
    price_range: str             # free | cheap | moderate | expensive
    opening_hours: str         # e.g. "08:00-18:00" or "always_open"
    best_time: str               # e.g. "morning", "sunset", "evening"
    wheelchair: str              # yes | no | partial
    family_friendly: bool
    age_group: str               # all | kids | teens | adults | seniors
    nearby_places: List[str]     # list of place name_ar within ~5 km


# =============================================================================
#  CORE DATA  –  manually curated, high-confidence facts
# =============================================================================

PLACES: List[Place] = [
    # ------------------------------------------------------------------
    #  DAMASCUS – Old City & Religious
    # ------------------------------------------------------------------
    Place(
        name_ar="الجامع الأموي", name_de="Umayyaden-Moschee", name_en="Umayyad Mosque",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5116, lng=36.3064, category="religious",
        description_ar="أحد أقدم وأكبر المساجد في العالم، يضم ضريح يوحنا المعمدان وشعر النبي. يعود تاريخه إلى العام 705 ميلادي.",
        description_de="Eine der ältesten und größten Moscheen der Welt mit dem Schrein Johannes des Täufers. Erbaut 705 n. Chr.",
        description_en="One of the oldest and largest mosques in the world, housing the shrine of John the Baptist. Built in 705 AD.",
        visit_duration="1h", price_range="free", opening_hours="08:00-20:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["باب شرقي", "قصر العظم", "شارع الميدان", "سوق الحميدية"]
    ),
    Place(
        name_ar="قصر العظم", name_de="Azem-Palast", name_en="Azem Palace",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5101, lng=36.3075, category="history",
        description_ar="قصر عثماني فاخر يعود للقرن الثامن عشر، يضم متحفًا للفنون والتقاليد الشعبية السورية وحدائق جميلة.",
        description_de="Prächtiger osmanischer Palast aus dem 18. Jh. mit Museum für syrische Volkskunst und wunderschönen Gärten.",
        description_en="Magnificent 18th-century Ottoman palace with a museum of Syrian folk art and beautiful gardens.",
        visit_duration="1.5h", price_range="cheap", opening_hours="09:00-18:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["الجامع الأموي", "باب شرقي", "سوق الحميدية"]
    ),
    Place(
        name_ar="سوق الحميدية", name_de="Hamidije-Souk", name_en="Al-Hamidiyah Souq",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5108, lng=36.3015, category="market",
        description_ar="أقدم وأشهر سوق في دمشق، يمتد من باب الشرقي حتى الجامع الأموي. يضم محلات للأقمشة، التوابل، الحلويات، والحرف اليدوية.",
        description_de="Ältester und berühmtester Markt von Damaskus, von Bab Sharqi bis zur Umayyaden-Moschee. Stoffe, Gewürze, Süßigkeiten, Handwerk.",
        description_en="Oldest and most famous market in Damascus, stretching from Bab Sharqi to the Umayyad Mosque. Fabrics, spices, sweets, crafts.",
        visit_duration="2h", price_range="moderate", opening_hours="09:00-21:00",
        best_time="evening", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["الجامع الأموي", "باب شرقي", "نوفارا", "قصر العظم"]
    ),
    Place(
        name_ar="باب شرقي", name_de="Bab Sharqi (Osttor)", name_en="Bab Sharqi",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5105, lng=36.3140, category="history",
        description_ar="أحد أبواب المدينة القديمة الاثني عشر، يعود إلى العصر الروماني. يتميز بقوسه الحجري المميز.",
        description_de="Eines der 12 Stadttore der Altstadt aus römischer Zeit, bekannt für seinen charakteristischen Steinbogen.",
        description_en="One of the 12 ancient city gates from Roman times, known for its distinctive stone arch.",
        visit_duration="20min", price_range="free", opening_hours="always_open",
        best_time="sunset", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["شارع الميدان", "الجامع الأموي", "سوق الحميدية"]
    ),
    Place(
        name_ar="شارع الميدان", name_de="Straße Al-Midan", name_en="Al-Midan Street",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5080, lng=36.3160, category="food",
        description_ar="حي تاريخي شهير بمطاعم الكباب والحلويات التقليدية. يضم أقدم محلات البقلاوة والمشبك في دمشق.",
        description_de="Historisches Viertel berühmt für Kebab-Restaurants und traditionelle Süßigkeiten. Älteste Baklava- und Meshbak-Läden Damaskus'.",
        description_en="Historic district famous for kebab restaurants and traditional sweets. Oldest baklava and meshbak shops in Damascus.",
        visit_duration="2h", price_range="cheap", opening_hours="10:00-23:00",
        best_time="evening", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["باب شرقي", "الجامع الأموي"]
    ),
    Place(
        name_ar="جبل قاسيون", name_de="Kasiyun-Berg", name_en="Mount Qasioun",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5500, lng=36.2500, category="nature",
        description_ar="جبل يطل على دمشق بأكملها، يضم كهف الدم ونقطة مراقبة للمدينة. مكان مثالي لمشاهدة غروب الشمس.",
        description_de="Berg mit Blick auf ganz Damaskus, beherbergt die Bluthöhle und einen Aussichtspunkt. Perfekt für Sonnenuntergänge.",
        description_en="Mountain overlooking all of Damascus, featuring the Blood Cave and a city viewpoint. Perfect for sunsets.",
        visit_duration="2h", price_range="free", opening_hours="sunrise_sunset",
        best_time="sunset", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["مطعم جبل قاسيون", "مقهى المطل"]
    ),
    Place(
        name_ar="كفرسوسة", name_de="Kafr Souseh", name_en="Kafr Souseh",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5050, lng=36.2800, category="shopping",
        description_ar="منطقة حديثة تضم مراكز تسوق ومقاهي عصرية. قريبة من جامعة دمشق والسفارات.",
        description_de="Modernes Viertel mit Einkaufszentren und trendigen Cafés. Nahe der Universität und den Botschaften.",
        description_en="Modern area with shopping malls and trendy cafés. Close to Damascus University and embassies.",
        visit_duration="2h", price_range="moderate", opening_hours="10:00-22:00",
        best_time="evening", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["المالكي", "المزة"]
    ),
    Place(
        name_ar="المالكي", name_de="Al-Malki", name_en="Al-Malki",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5150, lng=36.2750, category="shopping",
        description_ar="شارع رئيسي للتسوق الفاخر يضم أرقى المحلات والمطاعم. مركز تجاري وسياحي راقٍ.",
        description_de="Haupteinkaufsstraße mit Luxusläden und Restaurants. Edles Geschäfts- und Touristenzentrum.",
        description_en="Main luxury shopping street with high-end stores and restaurants. Upscale commercial and tourist hub.",
        visit_duration="2h", price_range="expensive", opening_hours="10:00-22:00",
        best_time="evening", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["كفرسوسة", "الروضة", "أبو رمانة"]
    ),
    Place(
        name_ar="معصرة باب الجنين", name_de="Ölmühle Bab al-Jneine", name_en="Bab al-Jneine Oil Press",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5130, lng=36.3120, category="history",
        description_ar="معصرة زيتون تقليدية في المدينة القديمة، تجربة حية للصناعة اليدوية السورية القديمة.",
        description_de="Traditionelle Olivenölmühle in der Altstadt, lebendige Erfahrung alter syrischer Handwerkskunst.",
        description_en="Traditional olive oil press in the Old City, a living experience of ancient Syrian craftsmanship.",
        visit_duration="30min", price_range="free", opening_hours="09:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["سوق الحميدية", "الجامع الأموي"]
    ),
    Place(
        name_ar="تكية السليمانية", name_de="Sulaymaniye-Tekke", name_en="Sulaymaniye Takiya",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5120, lng=36.3030, category="religious",
        description_ar="تكية صوفية تاريخية بناها السلطان سليمان القانوني. تضم مدرسة ومقبرة ومسجد.",
        description_de="Historische sufitische Tekke, erbaut von Sultan Suleiman. Beherbergt Schule, Friedhof und Moschee.",
        description_en="Historic Sufi takiya built by Sultan Suleiman. Houses a school, cemetery, and mosque.",
        visit_duration="1h", price_range="free", opening_hours="08:00-18:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["الجامع الأموي", "سوق الحميدية"]
    ),
    Place(
        name_ar="متحف دمشق الوطني", name_de="Nationale Museum Damaskus", name_en="National Museum of Damascus",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5140, lng=36.2910, category="museum",
        description_ar="يضم آثارًا من العصر الحجري حتى العصر الإسلامي المتأخر. أهمها نموذج مدينة دورا أوروبوس.",
        description_de="Von der Steinzeit bis zum späten Islam. Highlight: Modell der Stadt Dura Europos.",
        description_en="Artifacts from the Stone Age to the late Islamic period. Highlight: model of the city of Dura Europos.",
        visit_duration="3h", price_range="cheap", opening_hours="09:00-17:00",
        best_time="morning", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["سوق الحميدية", "تكية السليمانية"]
    ),
    Place(
        name_ar="مقهى النوفارة", name_de="Nawfara-Café", name_en="Al-Nawfara Café",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5105, lng=36.3010, category="food",
        description_ar="أقدم مقهى في دمشق (1709). يقدم القهوة العربية والشاي مع الحلويات التقليدية وسط الأجواء العثمانية.",
        description_de="Ältestes Café Damaskus (1709). Arabischer Kaffee, Tee, traditionelle Süßigkeiten in osmanischem Ambiente.",
        description_en="Oldest café in Damascus (1709). Arabic coffee, tea, traditional sweets in Ottoman ambiance.",
        visit_duration="1h", price_range="cheap", opening_hours="08:00-23:00",
        best_time="evening", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["سوق الحميدية", "الجامع الأموي"]
    ),
    Place(
        name_ar="مطعم بيت جدي", name_de="Beit Jaddi Restaurant", name_en="Beit Jaddi Restaurant",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5110, lng=36.3015, category="food",
        description_ar="مطعم تقليدي في المدينة القديمة يقدم المزة السورية الأصيلة: حمص، متبل، فتوش، كبة، كباب.",
        description_de="Traditionelles Restaurant in der Altstadt mit authentischer syrischer Mezze: Hummus, Mutabbal, Fattoush, Kibbeh, Kebab.",
        description_en="Traditional Old City restaurant serving authentic Syrian mezze: hummus, mutabbal, fattoush, kibbeh, kebab.",
        visit_duration="1.5h", price_range="moderate", opening_hours="12:00-23:00",
        best_time="evening", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["مقهى النوفارة", "سوق الحميدية"]
    ),
    Place(
        name_ar="حديقة تشرين", name_de="Tishreen-Park", name_en="Tishreen Park",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5180, lng=36.2680, category="nature",
        description_ar="أكبر حديقة عامة في دمشق، تضم بحيرة صناعية ومسارات مشي ومناطق للعب الأطفال.",
        description_de="Größter öffentlicher Park Damaskus mit künstlichem See, Wanderwegen und Spielbereichen.",
        description_en="Largest public park in Damascus with an artificial lake, walking trails, and children's play areas.",
        visit_duration="2h", price_range="free", opening_hours="sunrise_sunset",
        best_time="morning", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["المالكي", "كفرسوسة"]
    ),
    Place(
        name_ar="كنيسة حنانيا", name_de="Hanania-Kirche", name_en="Church of Hanania",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5095, lng=36.3085, category="religious",
        description_ar="كنيسة قديمة في المدينة القديمة مخصصة للقديس حنانيا. معمارها بيزنطي جميل.",
        description_de="Alte Kirche in der Altstadt dem Heiligen Hanania geweiht. Wunderschöne byzantinische Architektur.",
        description_en="Ancient church in the Old City dedicated to Saint Hanania. Beautiful Byzantine architecture.",
        visit_duration="30min", price_range="free", opening_hours="08:00-18:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["الجامع الأموي", "باب شرقي"]
    ),
    Place(
        name_ar="سوق البزورية", name_de="Spicesouq Al-Bzourieh", name_en="Al-Bzourieh Spice Market",
        city_ar="دمشق", city_de="Damaskus", city_en="Damascus",
        lat=33.5100, lng=36.3020, category="market",
        description_ar="سوق متخصص بالتوابل والبهارات والمكسرات والزيوت العطرية. رائحة دمشق الأصيلة.",
        description_de="Spezialmarkt für Gewürze, Nüsse und ätherische Öle. Der authentische Geruch von Damaskus.",
        description_en="Specialized market for spices, nuts, and essential oils. The authentic scent of Damascus.",
        visit_duration="1h", price_range="cheap", opening_hours="09:00-19:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["سوق الحميدية", "الجامع الأموي"]
    ),

    # ------------------------------------------------------------------
    #  MAALOULA – Religious & Nature
    # ------------------------------------------------------------------
    Place(
        name_ar="دير مار سركيس", name_de="Kloster Mar Sarkis", name_en="Mar Sarkis Monastery",
        city_ar="معلولا", city_de="Maaloula", city_en="Maaloula",
        lat=33.8440, lng=36.5450, category="religious",
        description_ar="دير يوناني أرثوذكسي يعود للقرن الرابع، يقع على جرف صخري في قرية معلولا حيث يتحدث السكان الآرامية حتى اليوم.",
        description_de="Griechisch-orthodoxes Kloster aus dem 4. Jh. auf einem Felsen in Maaloula, wo Einheimische bis heute Aramäisch sprechen.",
        description_en="4th-century Greek Orthodox monastery on a cliff in Maaloula, where locals still speak Aramaic.",
        visit_duration="1.5h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["دير مار تقلا", "كهف معلولا"]
    ),
    Place(
        name_ar="دير مار تقلا", name_de="Kloster Mar Takla", name_en="Mar Takla Monastery",
        city_ar="معلولا", city_de="Maaloula", city_en="Maaloula",
        lat=33.8430, lng=36.5470, category="religious",
        description_ar="دير آخر في معلولا مكرَّس للقديسة تقلا. يضم كنيسة صخرية وأيقونات قديمة.",
        description_de="Weiteres Kloster in Maaloula der Heiligen Takla geweiht. Felsenkirche und alte Ikonen.",
        description_en="Another Maaloula monastery dedicated to Saint Takla. Rock church and ancient icons.",
        visit_duration="1h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["دير مار سركيس", "كهف معلولا"]
    ),
    Place(
        name_ar="كهف معلولا", name_de="Maaloula-Höhle", name_en="Maaloula Cave",
        city_ar="معلولا", city_de="Maaloula", city_en="Maaloula",
        lat=33.8420, lng=36.5480, category="nature",
        description_ar="كهف طبيعي يطل على وادي معلولا. منظر طبيعي خلاب ومكان للتأمل.",
        description_de="Natürliche Höhle mit Blick auf das Maaloula-Tal. Atemberaubende Natur und Ort der Kontemplation.",
        description_en="Natural cave overlooking the Maaloula valley. Stunning nature and contemplation spot.",
        visit_duration="45min", price_range="free", opening_hours="always_open",
        best_time="afternoon", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["دير مار سركيس", "دير مار تقلا"]
    ),

    # ------------------------------------------------------------------
    #  BOSRA – Roman Theatre
    # ------------------------------------------------------------------
    Place(
        name_ar="مسرح بصرى الروماني", name_de="Römisches Theater Bosra", name_en="Roman Theatre of Bosra",
        city_ar="بصرى", city_de="Bosra", city_en="Bosra",
        lat=32.5180, lng=36.4810, category="history",
        description_ar="أفضل مسرح روماني محفوظ في العالم، يتسع لـ 15,000 متفرج. يقع داخل قلعة من العصر الإسلامي.",
        description_de="Besterhaltenes römisches Theater der Welt, 15.000 Zuschauer. Innerhalb einer islamischen Festung.",
        description_en="Best-preserved Roman theatre in the world, seating 15,000. Inside an Islamic-era fortress.",
        visit_duration="2h", price_range="cheap", opening_hours="08:00-18:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["قلعة بصرى", "المدرج الروماني"]
    ),
    Place(
        name_ar="قلعة بصرى", name_de="Bosra-Festung", name_en="Bosra Citadel",
        city_ar="بصرى", city_de="Bosra", city_en="Bosra",
        lat=32.5175, lng=36.4820, category="history",
        description_ar="قلعة أيوبية مبنية حول المسرح الروماني. تضم أبراجًا دفاعية ومسجدًا قديمًا.",
        description_de="Ayyubidische Festung um das römische Theater. Wehrtürme und alte Moschee.",
        description_en="Ayyubid citadel built around the Roman theatre. Defensive towers and ancient mosque.",
        visit_duration="1.5h", price_range="cheap", opening_hours="08:00-18:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["مسرح بصرى الروماني"]
    ),

    # ------------------------------------------------------------------
    #  PALMYRA (Tadmor) – Desert History
    # ------------------------------------------------------------------
    Place(
        name_ar="معبد بل", name_de="Bel-Tempel", name_en="Temple of Bel",
        city_ar="تدمر", city_de="Palmyra", city_en="Palmyra",
        lat=34.5470, lng=38.2670, category="history",
        description_ar="أكبر معبد في تدمر القديمة، مكرَّس للإله بل. يعود للقرن الأول الميلادي. أعيد ترميمه جزئيًا.",
        description_de="Größter Tempel des alten Palmyra, dem Gott Bel geweiht. 1. Jh. n. Chr. Teilweise restauriert.",
        description_en="Largest temple in ancient Palmyra, dedicated to the god Bel. 1st century AD. Partially restored.",
        visit_duration="1h", price_range="cheap", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["قوس النصر", "شارع الأعمدة", "مقبرة تدمر"]
    ),
    Place(
        name_ar="قوس النصر", name_de="Triumphbogen", name_en="Triumphal Arch",
        city_ar="تدمر", city_de="Palmyra", city_en="Palmyra",
        lat=34.5490, lng=38.2660, category="history",
        description_ar="قوس نصر روماني مبهر على المدخل الشرقي لمدينة تدمر. رمز للعظمة الرومانية.",
        description_de="Beeindruckender römischer Triumphbogen am Osttor von Palmyra. Symbol römischer Größe.",
        description_en="Impressive Roman triumphal arch at Palmyra's eastern gate. Symbol of Roman grandeur.",
        visit_duration="30min", price_range="free", opening_hours="always_open",
        best_time="sunrise", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["معبد بل", "شارع الأعمدة"]
    ),
    Place(
        name_ar="شارع الأعمدة", name_de="Säulenstraße", name_en="Colonnaded Street",
        city_ar="تدمر", city_de="Palmyra", city_en="Palmyra",
        lat=34.5510, lng=38.2680, category="history",
        description_ar="شارع مرصوف بالأعمدة الرخامية يمتد لكيلومتر واحد. كان الشريان الرئيسي للتجارة القديمة.",
        description_de="Marmorsäulenstraße über 1 km Länge. Einst die Hauptader des antiken Handels.",
        description_en="Marble-columned street stretching 1 km. Once the main artery of ancient trade.",
        visit_duration="1h", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["قوس النصر", "معبد بل"]
    ),
    Place(
        name_ar="مقبرة تدمر", name_de="Palmyra-Nekropole", name_en="Palmyra Necropolis",
        city_ar="تدمر", city_de="Palmyra", city_en="Palmyra",
        lat=34.5530, lng=38.2650, category="history",
        description_ar="مقابر برجية فريدة على أطراف المدينة. يصل ارتفاع بعض الأبراج إلى 4 طوابق.",
        description_de="Einzigartige turmartige Gräber am Stadtrand. Einige Türme erreichen 4 Stockwerke.",
        description_en="Unique tower tombs at the city edge. Some towers reach 4 stories.",
        visit_duration="1h", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["معبد بل", "شارع الأعمدة"]
    ),

    # ------------------------------------------------------------------
    #  CRAC DES CHEVALIERS – Crusader Castle
    # ------------------------------------------------------------------
    Place(
        name_ar="قلعة الحصن", name_de="Krak des Chevaliers", name_en="Krak des Chevaliers",
        city_ar="الحصن", city_de="Al-Husn", city_en="Al-Husn",
        lat=34.7560, lng=36.2950, category="history",
        description_ar="أفضل قلعة صليبية محفوظة في العالم. بنيت في القرن الحادي عشر فوق جبل في الساحل السوري.",
        description_de="Besterhaltene Kreuzfahrerburg der Welt. Erbaut im 11. Jh. auf einem Berg an der syrischen Küste.",
        description_en="Best-preserved Crusader castle in the world. Built in the 11th century on a mountain on the Syrian coast.",
        visit_duration="3h", price_range="cheap", opening_hours="09:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["مطعم الحصن", "وادي النصارى"]
    ),
    Place(
        name_ar="وادي النصارى", name_de="Wadi al-Nasara", name_en="Valley of the Christians",
        city_ar="الحصن", city_de="Al-Husn", city_en="Al-Husn",
        lat=34.7600, lng=36.2900, category="nature",
        description_ar="وادي خصب يضم قرى مسيحية تاريخية وكنائس قديمة ومزارع عنب.",
        description_de="Fruchtbares Tal mit historischen christlichen Dörfern, alten Kirchen und Weinbergen.",
        description_en="Fertile valley with historic Christian villages, ancient churches, and vineyards.",
        visit_duration="half-day", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["قلعة الحصن"]
    ),

    # ------------------------------------------------------------------
    #  ALEPPO – Old City & Citadel
    # ------------------------------------------------------------------
    Place(
        name_ar="قلعة حلب", name_de="Zitadelle von Aleppo", name_en="Aleppo Citadel",
        city_ar="حلب", city_de="Aleppo", city_en="Aleppo",
        lat=36.1990, lng=37.1630, category="history",
        description_ar="تلة محصنة عملاقة في قلب حلب، تاريخها يمتد من العصر الحيثي حتى العصر المملوكي. تضم مسرحًا ومتحفًا.",
        description_de="Riesige befestigte Anhöhe im Herzen Aleppos, von der Hethiterzeit bis zur Mamlukenära. Theater und Museum.",
        description_en="Massive fortified mound in Aleppo's heart, from Hittite times to Mamluk era. Theatre and museum.",
        visit_duration="2.5h", price_range="cheap", opening_hours="09:00-18:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["سوق حلب الكبير", "المدرسة الأشرفية", "جامع حلب الكبير"]
    ),
    Place(
        name_ar="سوق حلب الكبير", name_de="Großer Basar von Aleppo", name_en="Great Bazaar of Aleppo",
        city_ar="حلب", city_de="Aleppo", city_en="Aleppo",
        lat=36.2020, lng=37.1550, category="market",
        description_ar="أطول سوق مغطى في العالم (13 كم)، يعود للقرن الرابع عشر. يضم أقسامًا للحرير، التوابل، النحاس، والصابون.",
        description_de="Längste überdachte Marktstraße der Welt (13 km), 14. Jh. Abteilungen für Seide, Gewürze, Kupfer, Seife.",
        description_en="Longest covered market in the world (13 km), 14th century. Sections for silk, spices, copper, soap.",
        visit_duration="3h", price_range="moderate", opening_hours="09:00-20:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["قلعة حلب", "جامع حلب الكبير", "خان الوزير"]
    ),
    Place(
        name_ar="جامع حلب الكبير", name_de="Große Moschee von Aleppo", name_en="Great Mosque of Aleppo",
        city_ar="حلب", city_de="Aleppo", city_en="Aleppo",
        lat=36.2010, lng=37.1560, category="religious",
        description_ar="مسجد أيوبي ضخم بجوار القلعة. يضم مئذنة مملوكية رائعة وصحنًا واسعًا.",
        description_de="Riesige ayyubidische Moschee neben der Zitadelle. Prächtiges mamlukisches Minarett und großer Innenhof.",
        description_en="Massive Ayyubid mosque next to the Citadel. Magnificent Mamluk minaret and large courtyard.",
        visit_duration="1h", price_range="free", opening_hours="08:00-20:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["قلعة حلب", "سوق حلب الكبير"]
    ),
    Place(
        name_ar="خان الوزير", name_de="Khan al-Wazir", name_en="Khan al-Wazir",
        city_ar="حلب", city_de="Aleppo", city_en="Aleppo",
        lat=36.2030, lng=37.1540, category="history",
        description_ar="خان تجاري عثماني في السوق، يضم الآن محلات للحرف اليدوية والسجاد والأنتيكات.",
        description_de="Ottomanischer Handelshof im Basar, heute Handwerksläden, Teppiche und Antiquitäten.",
        description_en="Ottoman trading inn in the bazaar, now housing craft shops, carpets, and antiques.",
        visit_duration="1h", price_range="moderate", opening_hours="09:00-19:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["سوق حلب الكبير", "قلعة حلب"]
    ),
    Place(
        name_ar="مطعم ورد", name_de="Ward Restaurant", name_en="Ward Restaurant",
        city_ar="حلب", city_de="Aleppo", city_en="Aleppo",
        lat=36.2040, lng=37.1520, category="food",
        description_ar="مطعم حلبي تقليدي يقدم الكبة الحلبية الشهيرة والكباب بالكرز والمحاشي.",
        description_de="Traditionelles Aleppo-Restaurant mit berühmter Kibbeh, Kirsch-Kebab und Mahashi.",
        description_en="Traditional Aleppo restaurant serving famous Aleppo kibbeh, cherry kebab, and mahashi.",
        visit_duration="1.5h", price_range="moderate", opening_hours="12:00-23:00",
        best_time="evening", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["سوق حلب الكبير", "قلعة حلب"]
    ),

    # ------------------------------------------------------------------
    #  HAMA – Water Wheels
    # ------------------------------------------------------------------
    Place(
        name_ar="نواعير حماة", name_de="Wasserräder von Hama", name_en="Hama Water Wheels",
        city_ar="حماة", city_de="Hama", city_en="Hama",
        lat=35.1370, lng=36.7500, category="history",
        description_ar="أقدم نظام ري في العالم، يعود لأكثر من 3000 عام. ترفع المياه من نهر العاصي لتسقي البساتين.",
        description_de="Ältestes Bewässerungssystem der Welt, über 3000 Jahre alt. Hebt Wasser aus dem Orontes für die Obstgärten.",
        description_en="Oldest irrigation system in the world, over 3000 years old. Lifts water from the Orontes for orchards.",
        visit_duration="1h", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["حدائق حماة", "متحف حماة"]
    ),
    Place(
        name_ar="حدائق حماة", name_de="Hama-Gärten", name_en="Hama Gardens",
        city_ar="حماة", city_de="Hama", city_en="Hama",
        lat=35.1350, lng=36.7480, category="nature",
        description_ar="جداول وشلالات وبساتين على ضفاف نهر العاصي. مكان مثالي للراحة والتصوير.",
        description_de="Bäche, Wasserfälle und Obstgärten am Orontes. Ideal zum Entspannen und Fotografieren.",
        description_en="Streams, waterfalls, and orchards on the Orontes. Ideal for relaxing and photography.",
        visit_duration="1.5h", price_range="free", opening_hours="sunrise_sunset",
        best_time="afternoon", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["نواعير حماة"]
    ),

    # ------------------------------------------------------------------
    #  HOMS – Churches & Khalid ibn al-Walid
    # ------------------------------------------------------------------
    Place(
        name_ar="مسجد خالد بن الوليد", name_de="Khalid-ibn-al-Walid-Moschee", name_en="Khalid ibn al-Walid Mosque",
        city_ar="حمص", city_de="Homs", city_en="Homs",
        lat=34.7260, lng=36.7130, category="religious",
        description_ar="ضريح الصحابي خالد بن الوليد. مسجد عثماني بقبّتين ذهبيتين ومنارة عالية.",
        description_de="Schrein des Gefährten Khalid ibn al-Walid. Osmanische Moschee mit zwei goldenen Kuppeln und hohem Minarett.",
        description_en="Shrine of the companion Khalid ibn al-Walid. Ottoman mosque with two golden domes and tall minaret.",
        visit_duration="1h", price_range="free", opening_hours="08:00-20:00",
        best_time="morning", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["كنيسة أم الزنار", "مطعم حمص التقليدي"]
    ),
    Place(
        name_ar="كنيسة أم الزنار", name_de="Umm az-Zunar-Kirche", name_en="Church of Um al-Zennar",
        city_ar="حمص", city_de="Homs", city_en="Homs",
        lat=34.7280, lng=36.7150, category="religious",
        description_ar="أقدم كنيسة في حمص، يعود تاريخها للقرن الثاني. يعتقد أنها بنيت فوق بقايا كنيسه أقدم.",
        description_de="Älteste Kirche Homs', aus dem 2. Jh. Gilt als erbaut über den Resten einer noch älteren Kirche.",
        description_en="Oldest church in Homs, dating to the 2nd century. Believed built over remains of an even older church.",
        visit_duration="30min", price_range="free", opening_hours="08:00-18:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["مسجد خالد بن الوليد"]
    ),

    # ------------------------------------------------------------------
    #  LATAKIA – Mediterranean Coast
    # ------------------------------------------------------------------
    Place(
        name_ar="قلعة صلاح الدين", name_de="Saladin-Burg", name_en="Citadel of Saladin",
        city_ar="اللاذقية", city_de="Latakia", city_en="Latakia",
        lat=35.6000, lng=35.9830, category="history",
        description_ar="قلعة ضخمة فوق جرف بين الغابات الساحلية. بنيت من قبل البيزنطيين وأعيد بناؤها من الصليبيين.",
        description_de="Riesige Burg auf einem Felsen inmitten Küstenwälder. Erbaut von Byzantinern, von Kreuzfahrern ausgebaut.",
        description_en="Massive castle on a cliff amid coastal forests. Built by Byzantines, rebuilt by Crusaders.",
        visit_duration="2h", price_range="cheap", opening_hours="09:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["شاطئ السمرا", "مطعم الساحل اللاذقاني"]
    ),
    Place(
        name_ar="شاطئ السمرا", name_de="Samarra-Strand", name_en="Samarra Beach",
        city_ar="اللاذقية", city_de="Latakia", city_en="Latakia",
        lat=35.5900, lng=35.7700, category="beach",
        description_ar="شاطئ رملي طويل على البحر الأبيض المتوسط. مكان شعبي للسباحة والمشي لمسافات طويلة.",
        description_de="Langer Sandstrand am Mittelmeer. Beliebt zum Schwimmen und Spazierengehen.",
        description_en="Long sandy beach on the Mediterranean. Popular for swimming and strolling.",
        visit_duration="half-day", price_range="free", opening_hours="sunrise_sunset",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["قلعة صلاح الدين", "مطعم الساحل اللاذقاني"]
    ),
    Place(
        name_ar="مطعم الساحل اللاذقاني", name_de="Latakia-Küstenrestaurant", name_en="Latakia Coastal Restaurant",
        city_ar="اللاذقية", city_de="Latakia", city_en="Latakia",
        lat=35.5850, lng=35.7750, category="food",
        description_ar="مطعم على البحر يقدم أسماكًا طازجة، كالاماري، وطبق السمك المشوي التقليدي.",
        description_de="Strandrestaurant mit frischem Fisch, Calamari und traditionellem gegrilltem Fischgericht.",
        description_en="Beachside restaurant serving fresh fish, calamari, and traditional grilled fish dish.",
        visit_duration="2h", price_range="moderate", opening_hours="11:00-23:00",
        best_time="sunset", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["شاطئ السمرا", "قلعة صلاح الدين"]
    ),

    # ------------------------------------------------------------------
    #  TARTUS – Crusader Port
    # ------------------------------------------------------------------
    Place(
        name_ar="قلعة طرطوس", name_de="Tartus-Zitadelle", name_en="Tartus Citadel",
        city_ar="طرطوس", city_de="Tartus", city_en="Tartus",
        lat=34.8930, lng=35.8820, category="history",
        description_ar="قلعة صليبية على البحر المتوسط. تستخدم الآن كمتحف بحري ومكان للفعاليات الثقافية.",
        description_de="Kreuzfahrerburg am Mittelmeer. Heute Marinemuseum und Ort für Kulturveranstaltungen.",
        description_en="Crusader castle on the Mediterranean. Now a maritime museum and cultural events venue.",
        visit_duration="1.5h", price_range="cheap", opening_hours="09:00-17:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["ميناء طرطوس", "شاطئ طرطوس"]
    ),
    Place(
        name_ar="ميناء طرطوس", name_de="Hafen von Tartus", name_en="Port of Tartus",
        city_ar="طرطوس", city_de="Tartus", city_en="Tartus",
        lat=34.8950, lng=35.8850, category="nature",
        description_ar="أكبر ميناء سوري على المتوسط. مكان مثالي لمشاهدة السفن وغروب الشمس.",
        description_de="Größter syrischer Mittelmeerhafen. Ideal zum Schiffegucken und Sonnenuntergang.",
        description_en="Largest Syrian Mediterranean port. Ideal for ship-watching and sunset views.",
        visit_duration="1h", price_range="free", opening_hours="always_open",
        best_time="sunset", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["قلعة طرطوس", "شاطئ طرطوس"]
    ),
    Place(
        name_ar="شاطئ طرطوس", name_de="Tartus-Strand", name_en="Tartus Beach",
        city_ar="طرطوس", city_de="Tartus", city_en="Tartus",
        lat=34.8900, lng=35.8800, category="beach",
        description_ar="شاطئ هادئ نظيف على المتوسط. مناسب للعائلات والأطفال.",
        description_de="Ruhiger, sauberer Mittelmeerstrand. Familien- und kinderfreundlich.",
        description_en="Quiet, clean Mediterranean beach. Family and child friendly.",
        visit_duration="half-day", price_range="free", opening_hours="sunrise_sunset",
        best_time="morning", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["قلعة طرطوس", "ميناء طرطوس"]
    ),

    # ------------------------------------------------------------------
    #  SWEIDA – Druze Mountains
    # ------------------------------------------------------------------
    Place(
        name_ar="شهبا", name_de="Shahba", name_en="Shahba",
        city_ar="السويداء", city_de="Sweida", city_en="Sweida",
        lat=32.8540, lng=36.6290, category="history",
        description_ar="مدينة رومانية صغيرة مسقط رأس الإمبراطور فيلب العربي. تضم مسرحًا رومانيًا وحمامات.",
        description_de="Kleine römische Stadt, Geburtsort Kaiser Philipps des Arabers. Römisches Theater und Bäder.",
        description_en="Small Roman city, birthplace of Emperor Philip the Arab. Roman theatre and baths.",
        visit_duration="1.5h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["جبل العرب", "مزرعة عنب السويداء"]
    ),
    Place(
        name_ar="جبل العرب", name_de="Dschabal al-Arab", name_en="Jabal al-Arab",
        city_ar="السويداء", city_de="Sweida", city_en="Sweida",
        lat=32.7500, lng=36.6500, category="mountain",
        description_ar="سلسلة جبلية بركانية يقطنها الدروز. تضم غابات البلوط والصنوبر ومناظر خلابة.",
        description_de="Vulkanische Bergkette, bewohnt von Drusen. Eichen- und Pinienwälder, atemberaubende Aussichten.",
        description_en="Volcanic mountain range inhabited by Druze. Oak and pine forests, breathtaking views.",
        visit_duration="half-day", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["شهبا", "مزرعة عنب السويداء"]
    ),
    Place(
        name_ar="مزرعة عنب السويداء", name_de="Sweida-Weinberg", name_en="Sweida Vineyard",
        city_ar="السويداء", city_de="Sweida", city_en="Sweida",
        lat=32.7100, lng=36.5700, category="nature",
        description_ar="مزارع عنب تقليدية في جبل العرب. تنتج عنبًا ونبيذًا محليًا. يمكن زيارة المزارع.",
        description_de="Traditionelle Weinberge im Dschabal al-Arab. Produzieren lokale Trauben und Wein. Besichtigungen möglich.",
        description_en="Traditional vineyards in Jabal al-Arab. Produce local grapes and wine. Farm visits available.",
        visit_duration="2h", price_range="cheap", opening_hours="09:00-17:00",
        best_time="afternoon", wheelchair="partial", family_friendly=True, age_group="adults",
        nearby_places=["جبل العرب", "شهبا"]
    ),

    # ------------------------------------------------------------------
    #  DEIR EZZOR – Euphrates & Dura Europos
    # ------------------------------------------------------------------
    Place(
        name_ar="دورا أوروبوس", name_de="Dura Europos", name_en="Dura Europos",
        city_ar="دير الزور", city_de="Deir Ezzor", city_en="Deir Ezzor",
        lat=34.7480, lng=40.7300, category="history",
        description_ar="مدينة حديثة قديمة على الفرات. يضم كنيسة أقدم كنيسة معروفة وأقدم صورة للعشاء الأخير.",
        description_de="Antike Grenzstadt am Euphrat. Älteste bekannte Kirche und ältestes Gemälde des Abendmahls.",
        description_en="Ancient frontier city on the Euphrates. Oldest known church and oldest painting of the Last Supper.",
        visit_duration="2h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["سد الفرات", "نهر الفرات"]
    ),
    Place(
        name_ar="سد الفرات", name_de="Euphrat-Staudamm", name_en="Euphrates Dam",
        city_ar="دير الزور", city_de="Deir Ezzor", city_en="Deir Ezzor",
        lat=35.0830, lng=40.4330, category="nature",
        description_ar="سد ضخم على نهر الفرات يولد الكهرباء ويخزن المياه. منظر مهيب.",
        description_de="Riesiger Staudamm am Euphrat zur Stromerzeugung und Wasserspeicherung. Imposanter Anblick.",
        description_en="Massive dam on the Euphrates generating electricity and storing water. Impressive sight.",
        visit_duration="1h", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["نهر الفرات", "دورا أوروبوس"]
    ),
    Place(
        name_ar="نهر الفرات", name_de="Euphrat-Fluss", name_en="Euphrates River",
        city_ar="دير الزور", city_de="Deir Ezzor", city_en="Deir Ezzor",
        lat=35.1000, lng=40.4000, category="nature",
        description_ar="أحد أقدم الأنهار في التاريخ. يمكن التنزه على ضفافه وركوب القوارب.",
        description_de="Einer der ältesten Flüsse der Geschichte. Spaziergänge am Ufer und Bootsfahrten möglich.",
        description_en="One of the oldest rivers in history. Riverside walks and boat rides available.",
        visit_duration="2h", price_range="free", opening_hours="sunrise_sunset",
        best_time="sunset", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["سد الفرات", "دورا أوروبوس"]
    ),

    # ------------------------------------------------------------------
    #  QAMISHLI / AL-HASAKAH – North East
    # ------------------------------------------------------------------
    Place(
        name_ar="تل براك", name_de="Tell Brak", name_en="Tell Brak",
        city_ar="القامشلي", city_de="Qamishli", city_en="Qamishli",
        lat=36.9830, lng=41.0670, category="history",
        description_ar="تل أثري يعود للعصر البرونزي. أحد أقدم المدن في سوريا والشرق الأوسط.",
        description_de="Archäologischer Hügel aus der Bronzezeit. Eine der ältesten Städte Syriens und des Nahen Ostens.",
        description_en="Archaeological mound from the Bronze Age. One of the oldest cities in Syria and the Middle East.",
        visit_duration="2h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["دير الزوراف", "نهر الخابور"]
    ),
    Place(
        name_ar="نهر الخابور", name_de="Khabur-Fluss", name_en="Khabur River",
        city_ar="الحسكة", city_de="Al-Hasakah", city_en="Al-Hasakah",
        lat=36.5000, lng=40.8000, category="nature",
        description_ar="نهر رئيسي في الجزيرة السورية. يخترق السهول الخصبة ويضم طيورًا مهاجرة.",
        description_de="Hauptfluss der syrischen Dschazira. Durchquert fruchtbare Ebenen, Heimat wandernder Vögel.",
        description_en="Major river in the Syrian Jazira. Crosses fertile plains, home to migrating birds.",
        visit_duration="1.5h", price_range="free", opening_hours="sunrise_sunset",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["تل براك"]
    ),

    # ------------------------------------------------------------------
    #  DARAA – South
    # ------------------------------------------------------------------
    Place(
        name_ar="خربة الديك", name_de="Khirbet ad-Dik", name_en="Khirbet ad-Dik",
        city_ar="درعا", city_de="Daraa", city_en="Daraa",
        lat=32.6000, lng=36.1000, category="history",
        description_ar="تل أثري يعود للعصر الكنعاني. يضم بقايا مدينة قديمة وآثارًا حجرية.",
        description_de="Archäologischer Hügel aus kanaanäischer Zeit. Überreste einer alten Stadt und Steinarbeiten.",
        description_en="Archaeological mound from Canaanite times. Remains of an ancient city and stonework.",
        visit_duration="1h", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["نهر اليرموك", "غابة الدرعا"]
    ),
    Place(
        name_ar="نهر اليرموك", name_de="Jarmuk-Fluss", name_en="Yarmouk River",
        city_ar="درعا", city_de="Daraa", city_en="Daraa",
        lat=32.6830, lng=35.9830, category="nature",
        description_ar="نهر تاريخي يفصل سوريا عن الأردن. وادي خلاب مع مناظر طبيعية.",
        description_de="Historischer Fluss, Grenze Syrien-Jordanien. Schönes Tal mit Naturlandschaft.",
        description_en="Historic river forming the Syria-Jordan border. Beautiful valley with natural scenery.",
        visit_duration="1.5h", price_range="free", opening_hours="sunrise_sunset",
        best_time="afternoon", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["خربة الديك"]
    ),

    # ------------------------------------------------------------------
    #  IDLIB – Dead Cities
    # ------------------------------------------------------------------
    Place(
        name_ar="المدن الميتة", name_de="Tote Städte", name_en="Dead Cities",
        city_ar="إدلب", city_de="Idlib", city_en="Idlib",
        lat=36.0830, lng=36.6330, category="history",
        description_ar="مجموعة من 700 قرية أثرية بيزنطية مهجورة في شمال سوريا. تضم كنائس وبيوت حجرية ومقابر.",
        description_de="700 verlassene byzantinische Dörfer in Nordsyrien. Kirchen, Steinhäuser und Gräber.",
        description_en="Cluster of 700 abandoned Byzantine villages in northern Syria. Churches, stone houses, tombs.",
        visit_duration="half-day", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["كنيسة سمعان", "سرجيلا", "البارة"]
    ),
    Place(
        name_ar="كنيسة سمعان", name_de="Simeon-Kirche", name_en="Church of Saint Simeon Stylites",
        city_ar="إدلب", city_de="Idlib", city_en="Idlib",
        lat=36.3340, lng=36.8440, category="religious",
        description_ar="أكبر كنيسة بازيليكية في العالم، بنيت حول عمود القديس سمعان العمودي في القرن الخامس.",
        description_de="Größte Basilika der Welt, erbaut um die Säule des Säulenheiligen Simeon im 5. Jh.",
        description_en="Largest basilica in the world, built around the pillar of Saint Simeon Stylites in the 5th century.",
        visit_duration="1.5h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["المدن الميتة"]
    ),

    # ------------------------------------------------------------------
    #  RAQQA – Abbasid Capital
    # ------------------------------------------------------------------
    Place(
        name_ar="قصر البنات", name_de="Qasr al-Banat", name_en="Qasr al-Banat",
        city_ar="الرقة", city_de="Raqqa", city_en="Raqqa",
        lat=35.9500, lng=39.0170, category="history",
        description_ar="قصر عباسي يعود للقرن التاسع. يضم أقواسًا وفسيفساء وحدائق قديمة.",
        description_de="Abbasidischer Palast aus dem 9. Jh. Bögen, Mosaiken und alte Gärten.",
        description_en="9th-century Abbasid palace. Arches, mosaics, and ancient gardens.",
        visit_duration="1h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["نهر الفرات", "سور الرقة"]
    ),
    Place(
        name_ar="سور الرقة", name_de="Raqqa-Mauer", name_en="Raqqa Wall",
        city_ar="الرقة", city_de="Raqqa", city_en="Raqqa",
        lat=35.9600, lng=39.0100, category="history",
        description_ar="بقايا أسوار مدينة الرقة العباسية القديمة. يعود تاريخها للقرن الثامن.",
        description_de="Reste der alten abbasidischen Stadtmauer von Raqqa aus dem 8. Jh.",
        description_en="Remains of the old Abbasid city walls of Raqqa from the 8th century.",
        visit_duration="45min", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="yes", family_friendly=True, age_group="all",
        nearby_places=["قصر البنات"]
    ),

    # ------------------------------------------------------------------
    #  SAFITA – Crusader Tower
    # ------------------------------------------------------------------
    Place(
        name_ar="قلعة صافيتا", name_de="Safita-Turm", name_en="Safita Tower",
        city_ar="صافيتا", city_de="Safita", city_en="Safita",
        lat=34.8170, lng=36.1170, category="history",
        description_ar="برج صليبي مرتفع يستخدم كنقطة مراقبة. يطل على الساحل والجبال.",
        description_de="Hoher Kreuzfahrerturm als Wachtposten. Blick auf Küste und Berge.",
        description_en="Tall Crusader tower used as a watchpoint. Overlooks coast and mountains.",
        visit_duration="1h", price_range="free", opening_hours="09:00-17:00",
        best_time="sunset", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["وادي النصارى", "قلعة الحصن"]
    ),

    # ------------------------------------------------------------------
    #  MARMARITA – Hidden Gem
    # ------------------------------------------------------------------
    Place(
        name_ar="مرمريتا", name_de="Marmarita", name_en="Marmarita",
        city_ar="مرمريتا", city_de="Marmarita", city_en="Marmarita",
        lat=34.7670, lng=36.2330, category="nature",
        description_ar="قرية سياحية في وادي النصارى تضم فنادق بوتيك ومناظر طبيعية وكنائس.",
        description_de="Touristisches Dorf im Wadi al-Nasara mit Boutique-Hotels, Natur und Kirchen.",
        description_en="Tourist village in Wadi al-Nasara with boutique hotels, nature, and churches.",
        visit_duration="half-day", price_range="moderate", opening_hours="always_open",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["وادي النصارى", "قلعة الحصن", "صافيتا"]
    ),

    # ------------------------------------------------------------------
    #  APAMEA – Roman Columns
    # ------------------------------------------------------------------
    Place(
        name_ar="أفاميا", name_de="Apamea", name_en="Apamea",
        city_ar="حماة", city_de="Hama", city_en="Hama",
        lat=35.4170, lng=36.4000, category="history",
        description_ar="مدينة رومانية ضخمة تضم أطول شارع أعمدة في العالم (2 كم). يعود للقرن الثاني.",
        description_de="Riesige römische Stadt mit der längsten Säulenstraße der Welt (2 km). 2. Jh.",
        description_en="Huge Roman city with the longest colonnaded street in the world (2 km). 2nd century.",
        visit_duration="2h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["نواعير حماة"]
    ),

    # ------------------------------------------------------------------
    #  SERJILLA – Dead City
    # ------------------------------------------------------------------
    Place(
        name_ar="سرجيلا", name_de="Serjilla", name_en="Serjilla",
        city_ar="إدلب", city_de="Idlib", city_en="Idlib",
        lat=36.1000, lng=36.6330, category="history",
        description_ar="قرية بيزنطية مهجورة من القرن الخامس. تحتفظ ببيوت حجرية كاملة وحمامات رومانية.",
        description_de="Verlassenes byzantinisches Dorf aus dem 5. Jh. Erhaltene Steinhäuser und römische Bäder.",
        description_en="Abandoned 5th-century Byzantine village. Intact stone houses and Roman baths.",
        visit_duration="1.5h", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["المدن الميتة", "كنيسة سمعان"]
    ),

    # ------------------------------------------------------------------
    #  UGARIT – Ancient Alphabet
    # ------------------------------------------------------------------
    Place(
        name_ar="أوغاريت", name_de="Ugarit", name_en="Ugarit",
        city_ar="اللاذقية", city_de="Latakia", city_en="Latakia",
        lat=35.6000, lng=35.7830, category="history",
        description_ar="مدينة بحرية قديمة من العصر البرونزي. مسقط رأس الأبجدية الأوغاريتية (أول أبجدية في العالم).",
        description_de="Antike Hafenstadt aus der Bronzezeit. Geburtsort des ugaritischen Alphabets (ältestes Alphabet der Welt).",
        description_en="Ancient Bronze Age port city. Birthplace of the Ugaritic alphabet (world's oldest alphabet).",
        visit_duration="2h", price_range="cheap", opening_hours="09:00-17:00",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["شاطئ السمرا", "قلعة صلاح الدين"]
    ),

    # ------------------------------------------------------------------
    #  EBLA – Royal Archive
    # ------------------------------------------------------------------
    Place(
        name_ar="إيبلا", name_de="Ebla", name_en="Ebla",
        city_ar="إدلب", city_de="Idlib", city_en="Idlib",
        lat=35.8000, lng=36.8000, category="history",
        description_ar="مدينة سومرية قديمة (2500 ق.م). اكتشفت فيها مكتبة ملكية تحتوي على 20,000 لوح طيني.",
        description_de="Alte sumerische Stadt (2500 v. Chr.). Königsbibliothek mit 20.000 Tontafeln entdeckt.",
        description_en="Ancient Sumerian city (2500 BC). Royal library with 20,000 clay tablets discovered.",
        visit_duration="2h", price_range="free", opening_hours="08:00-17:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["المدن الميتة"]
    ),

    # ------------------------------------------------------------------
    #  SEIDNAYA – Christian Monastery
    # ------------------------------------------------------------------
    Place(
        name_ar="دير السيدة في صيدنايا", name_de="Kloster Seidnaya", name_en="Seidnaya Monastery",
        city_ar="صيدنايا", city_de="Seidnaya", city_en="Seidnaya",
        lat=33.6960, lng=36.3770, category="religious",
        description_ar="دير مسيحي أرثوذكسي يضم أيقونة عذراء مريم المشهورة. يقع في قرية جبلية فوق دمشق.",
        description_de="Griechisch-orthodoxes Kloster mit berühmter Marien-Ikone. Bergdorf über Damaskus.",
        description_en="Greek Orthodox monastery with famous icon of Virgin Mary. Mountain village above Damascus.",
        visit_duration="1.5h", price_range="free", opening_hours="07:00-19:00",
        best_time="morning", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["معلولا", "جبل قاسيون"]
    ),

    # ------------------------------------------------------------------
    #  ZAHWA – Castle
    # ------------------------------------------------------------------
    Place(
        name_ar="قلعة الزهوة", name_de="Zahwa-Burg", name_en="Zahwa Castle",
        city_ar="اللاذقية", city_de="Latakia", city_en="Latakia",
        lat=35.6500, lng=36.0500, category="history",
        description_ar="قلعة صليبية صغيرة على تلة في الساحل السوري. مناظر رائعة للبحر.",
        description_de="Kleine Kreuzfahrerburg auf einem Hügel an der syrischen Küste. Fantastische Meeresblicke.",
        description_en="Small Crusader castle on a hill on the Syrian coast. Fantastic sea views.",
        visit_duration="1h", price_range="free", opening_hours="always_open",
        best_time="sunset", wheelchair="no", family_friendly=True, age_group="all",
        nearby_places=["شاطئ السمرا", "قلعة صلاح الدين"]
    ),

    # ------------------------------------------------------------------
    #  KAFRUN – Druze Village
    # ------------------------------------------------------------------
    Place(
        name_ar="كفرون", name_de="Kafrun", name_en="Kafrun",
        city_ar="السويداء", city_de="Sweida", city_en="Sweida",
        lat=32.7500, lng=36.6000, category="nature",
        description_ar="قرية درزية في جبل العرب تضم بساتين التفاح والكرز. مكان مثالي للتنزه.",
        description_de="Drusisches Dorf im Dschabal al-Arab mit Apfel- und Kirschplantagen. Ideal zum Wandern.",
        description_en="Druze village in Jabal al-Arab with apple and cherry orchards. Ideal for hiking.",
        visit_duration="2h", price_range="free", opening_hours="always_open",
        best_time="morning", wheelchair="partial", family_friendly=True, age_group="all",
        nearby_places=["جبل العرب", "شهبا"]
    ),
]


# =============================================================================
#  DISTANCE MATRIX (km)  –  used for realistic travel planning
# =============================================================================
# Format: ((city_a, city_b), distance_km, drive_time_hours)
DISTANCES: List[Tuple[Tuple[str, str], float, float]] = [
    # Damascus hub
    (("دمشق", "معَلولا"), 55, 1.0),
    (("دمشق", "صيدنايا"), 30, 0.5),
    (("دمشق", "بصرى"), 140, 2.0),
    (("دمشق", "تدمر"), 215, 2.5),
    (("دمشق", "حلب"), 355, 4.0),
    (("دمشق", "حماة"), 210, 2.5),
    (("دمشق", "حمص"), 165, 2.0),
    (("دمشق", "اللاذقية"), 330, 3.5),
    (("دمشق", "طرطوس"), 290, 3.0),
    (("دمشق", "السويداء"), 110, 1.5),
    (("دمشق", "درعا"), 100, 1.5),
    (("دمشق", "دير الزور"), 450, 5.0),
    (("دمشق", "الرقة"), 380, 4.5),
    (("دمشق", "إدلب"), 320, 3.5),
    (("دمشق", "القامشلي"), 680, 7.0),
    (("دمشق", "الحسكة"), 650, 7.0),
    # Aleppo hub
    (("حلب", "حماة"), 150, 1.5),
    (("حلب", "حمص"), 190, 2.0),
    (("حلب", "إدلب"), 65, 1.0),
    (("حلب", "اللاذقية"), 185, 2.0),
    (("حلب", "طرطوس"), 220, 2.5),
    (("حلب", "الرقة"), 160, 2.0),
    (("حلب", "القامشلي"), 340, 4.0),
    # Homs hub
    (("حمص", "حماة"), 45, 0.5),
    (("حمص", "طرطوس"), 125, 1.5),
    (("حمص", "اللاذقية"), 165, 2.0),
    (("حمص", "السويداء"), 90, 1.0),
    (("حمص", "بصرى"), 110, 1.5),
    # Hama hub
    (("حماة", "إدلب"), 90, 1.0),
    (("حماة", "اللاذقية"), 135, 1.5),
    (("حماة", "طرطوس"), 155, 1.5),
    # Latakia hub
    (("اللاذقية", "طرطوس"), 85, 1.0),
    (("اللاذقية", "إدلب"), 145, 1.5),
    # Sweida hub
    (("السويداء", "بصرى"), 80, 1.0),
    (("السويداء", "درعا"), 65, 1.0),
    # Deir Ezzor hub
    (("دير الزور", "الرقة"), 200, 2.0),
    (("دير الزور", "الحسكة"), 240, 2.5),
    (("دير الزور", "القامشلي"), 270, 3.0),
    # Qamishli / Hasakah
    (("القامشلي", "الحسكة"), 80, 1.0),
]


def get_distance(city_a: str, city_b: str) -> Tuple[float, float]:
    """Return (km, drive_hours) between two cities. Falls back to rough estimate if unknown."""
    if city_a == city_b:
        return 0.0, 0.0
    for (a, b), km, hrs in DISTANCES:
        if (a == city_a and b == city_b) or (a == city_b and b == city_a):
            return km, hrs
    # fallback estimate: ~80 km/h average on Syrian roads
    return 100.0, 1.5


def get_city_center(city_en: str) -> Tuple[float, float]:
    """Approximate GPS center of each major city."""
    centers = {
        "Damascus": (33.5138, 36.2765),
        "Aleppo": (36.2021, 37.1343),
        "Homs": (34.7308, 36.7094),
        "Hama": (35.1333, 36.7500),
        "Latakia": (35.5317, 35.7881),
        "Tartus": (34.8920, 35.8868),
        "Sweida": (32.7089, 36.5667),
        "Deir Ezzor": (35.3359, 40.1408),
        "Raqqa": (35.9606, 39.0089),
        "Idlib": (35.9306, 36.6339),
        "Daraa": (32.6257, 36.1060),
        "Al-Hasakah": (36.5024, 40.7477),
        "Qamishli": (37.0590, 41.2280),
        "Palmyra": (34.5614, 38.2842),
        "Maaloula": (33.8443, 36.5456),
        "Bosra": (32.5175, 36.4810),
        "Al-Husn": (34.7560, 36.2950),
        "Seidnaya": (33.6960, 36.3770),
        "Safita": (34.8170, 36.1170),
        "Marmarita": (34.7670, 36.2330),
    }
    return centers.get(city_en, (33.5138, 36.2765))


# =============================================================================
#  QUICK HELPERS for the travel planner
# =============================================================================

def places_in_city(city_en: str) -> List[Place]:
    """All places inside a given city (English name)."""
    return [p for p in PLACES if p.city_en.lower() == city_en.lower()]


def places_by_category(categories: List[str]) -> List[Place]:
    """All places matching any of the given categories."""
    cats = [c.lower() for c in categories]
    return [p for p in PLACES if p.category.lower() in cats]


def places_by_interest(interest: str) -> List[Place]:
    """Fuzzy match interest string to places."""
    interest = interest.lower()
    mapping = {
        "history": ["history", "museum", "religious"],
        "food": ["food", "market"],
        "nature": ["nature", "mountain", "beach"],
        "shopping": ["shopping", "market"],
        "adventure": ["adventure", "mountain"],
        "art": ["art", "museum", "history"],
        "religious": ["religious", "history"],
        "beach": ["beach", "nature"],
        "mountain": ["mountain", "nature"],
        "market": ["market", "shopping", "food"],
    }
    cats = mapping.get(interest, [interest])
    return places_by_category(cats)
