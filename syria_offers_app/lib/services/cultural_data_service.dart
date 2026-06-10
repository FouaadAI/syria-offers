import 'package:syria_offers_app/models/cultural_site_model.dart';

class CulturalDataService {
  static List<CulturalSite> getSyrianCulturalSites() {
    return [
      // ═══════════ UNESCO WORLD HERITAGE SITES ═══════════
      const CulturalSite(
        id: 'unesco-001',
        nameAr: 'مدينة دمشق القديمة',
        nameEn: 'Ancient City of Damascus',
        officialTitle: 'Ancient City of Damascus',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'تأسست دمشق في الألفية الثالثة قبل الميلاد، وهي من أقدم المدن المأهولة في العالم. '
            'تضم المدينة القديمة أسواراً رومانية وبوابات وآثاراً تعود للحضارات المتعاقبة. '
            'تحتوي على الجامع الأموي الكبير وقلعة دمشق وقصر العظم.',
        descriptionEn:
            'Founded in the 3rd millennium BC, Damascus is one of the oldest continuously '
            'inhabited cities in the world. The old city contains Roman walls, gates, and '
            'monuments spanning successive civilizations.',
        gallery: [
          'https://images.unsplash.com/photo-1604147706283-d7119b5b822c?w=800',
          'https://images.unsplash.com/photo-1578353027244-c58b10173505?w=800',
        ],
        latitude: 33.5111,
        longitude: 36.3064,
        openingHours: 'مفتوح على مدار الساعة',
        unescoStatus: true,
      ),
      const CulturalSite(
        id: 'unesco-002',
        nameAr: 'تدمر - مدينة بالميرا الأثرية',
        nameEn: 'Site of Palmyra',
        officialTitle: 'Site of Palmyra',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'واحة في الصحراء السورية شمال شرق دمشق، تحتوي على آثار ضخمة لمدينة كانت من '
            'أهم المراكز الثقافية في العالم القديم. تجمع بين الفن اليوناني الروماني والتقاليد '
            'الفارسية. تضم معبد بل وقوس النصر والمسرح الروماني.',
        descriptionEn:
            'An oasis in the Syrian desert northeast of Damascus, containing monumental '
            'ruins of a great city that was one of the most important cultural centres of '
            'the ancient world.',
        gallery: [
          'https://images.unsplash.com/photo-1590767161356-9e0b8c1f3f1b?w=800',
          'https://images.unsplash.com/photo-1627894483216-2138a5bbbb66?w=800',
        ],
        latitude: 34.5600,
        longitude: 38.2672,
        openingHours: '8:00 صباحاً - 5:00 مساءً',
        entryFee: '500 ل.س',
        unescoStatus: true,
      ),
      const CulturalSite(
        id: 'unesco-003',
        nameAr: 'قلعة الحصن - Krak des Chevaliers',
        nameEn: 'Crac des Chevaliers',
        officialTitle: 'Crac des Chevaliers and Qal\'at Salah El-Din',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'واحدة من أهم القلاع العسكرية في العصور الوسطى، بناها فرسان الإسبتارية في '
            'القرن الثاني عشر. تقع على تلة استراتيجية غرب حمص وتتميز بأسوارها الضخمة '
            'وأبراجها الدفاعية.',
        descriptionEn:
            'One of the most important preserved medieval military castles in the world, '
            'built by the Knights Hospitaller in the 12th century. Located on a strategic '
            'hill west of Homs.',
        gallery: [
          'https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800',
          'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800',
        ],
        latitude: 34.7570,
        longitude: 36.2947,
        openingHours: '9:00 صباحاً - 5:00 مساءً',
        entryFee: '500 ل.س',
        unescoStatus: true,
      ),
      const CulturalSite(
        id: 'unesco-004',
        nameAr: 'مدينة حلب القديمة',
        nameEn: 'Ancient City of Aleppo',
        officialTitle: 'Ancient City of Aleppo',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'تقع حلب على مفترق طرق تجارية منذ الألفية الثانية قبل الميلاد. تتميز بقلعتها '
            'الشهيرة وأسواقها المسقوفة ومدارسها وقصورها وكنائسها ومساجدها التي تعود '
            'للحضارات الإسلامية والبيزنطية.',
        descriptionEn:
            'Located at the crossroads of several trade routes, Aleppo has been inhabited '
            'since the 2nd millennium BC. It is known for its citadel, covered souks, '
            'madrasas, and mosques.',
        gallery: [
          'https://images.unsplash.com/photo-1627894483216-2138a5bbbb66?w=800',
          'https://images.unsplash.com/photo-1530026405186-ed1f139313f8?w=800',
        ],
        latitude: 36.1992,
        longitude: 37.1625,
        openingHours: 'مفتوح على مدار الساعة',
        unescoStatus: true,
      ),
      const CulturalSite(
        id: 'unesco-005',
        nameAr: 'مدينة بصرى القديمة',
        nameEn: 'Ancient City of Bosra',
        officialTitle: 'Ancient City of Bosra',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'كانت بصرى عاصمة المقاطعة الرومانية العربية، وتضم مسرحاً رومانياً محفوظاً '
            'بشكل ممتاز يتسع لـ 15,000 متفرج، بالإضافة إلى آثار نبطية وإسلامية قديمة.',
        descriptionEn:
            'Bosra was the capital of the Roman province of Arabia. It contains an '
            'exceptionally well-preserved Roman theatre that seats 15,000 spectators.',
        gallery: [
          'https://images.unsplash.com/photo-1582555172866-f73bb12defab?w=800',
        ],
        latitude: 32.5183,
        longitude: 36.4806,
        openingHours: '8:00 صباحاً - 6:00 مساءً',
        entryFee: '500 ل.س',
        unescoStatus: true,
      ),
      const CulturalSite(
        id: 'unesco-006',
        nameAr: 'كنيسة مار سمعان العمودي',
        nameEn: 'Church of Saint Simeon Stylites',
        officialTitle: 'Ancient Villages of Northern Syria',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'من أقدم الكنائس البيزنطية الباقية، بنيت في القرن الخامس حول العمود الذي '
            'عاش عليه القديس سمعان لمدة 37 عاماً. تقع شمال غرب حلب وتضم بازيليكا ضخمة '
            'ومعمودية.',
        descriptionEn:
            'One of the oldest surviving Byzantine churches, built in the 5th century '
            'around the pillar where St. Simeon lived for 37 years. Located northwest of '
            'Aleppo.',
        gallery: [
          'https://images.unsplash.com/photo-1569154941061-e231b4725ef1?w=800',
        ],
        latitude: 36.3342,
        longitude: 36.8439,
        openingHours: '9:00 صباحاً - 4:00 مساءً',
        unescoStatus: true,
      ),

      // ═══════════ MUSEUMS ═══════════
      const CulturalSite(
        id: 'museum-001',
        nameAr: 'المتحف الوطني بدمشق',
        nameEn: 'National Museum of Damascus',
        category: CulturalCategory.museum,
        descriptionAr:
            'يضم المتحف الوطني بدمشق أكثر من 300,000 قطعة أثرية تغطي كامل تاريخ سوريا '
            'من عصور ما قبل التاريخ حتى العصر الإسلامي. يحتوي على قاعات للآثار السورية '
            'القديمة والفن الإسلامي والكلاسيكي.',
        descriptionEn:
            'The National Museum of Damascus houses over 300,000 artefacts spanning '
            'Syria\'s entire history from prehistoric times to the Islamic era.',
        gallery: [
          'https://images.unsplash.com/photo-1566127444979-b3d2b654e3b7?w=800',
        ],
        latitude: 33.5126,
        longitude: 36.2900,
        openingHours: '9:00 صباحاً - 5:00 مساءً',
        entryFee: '200 ل.س',
        unescoStatus: false,
      ),
      const CulturalSite(
        id: 'museum-002',
        nameAr: 'المتحف الوطني بحلب',
        nameEn: 'National Museum of Aleppo',
        category: CulturalCategory.museum,
        descriptionAr:
            'تأسس المتحف عام 1931 ويضم مجموعات أثرية هامة من شمال سوريا، بما في ذلك '
            'آثار من مملكة ماري وإيبلا وتل حلف. يتميز بواجهة مستوحاة من بوابة قصر تل حلف.',
        descriptionEn:
            'Founded in 1931, the museum houses important archaeological collections from '
            'northern Syria, including artefacts from Mari, Ebla, and Tell Halaf.',
        gallery: [
          'https://images.unsplash.com/photo-1569154941061-e231b4725ef1?w=800',
        ],
        latitude: 36.2038,
        longitude: 37.1506,
        openingHours: '9:00 صباحاً - 4:00 مساءً',
        entryFee: '200 ل.س',
        unescoStatus: false,
      ),

      // ═══════════ HISTORICAL MARKETS ═══════════
      const CulturalSite(
        id: 'suq-001',
        nameAr: 'سوق الحميدية',
        nameEn: 'Al-Hamidiyah Souq',
        category: CulturalCategory.historicalMarket,
        descriptionAr:
            'أكبر سوق مسقوف في سوريا، بني في العهد العثماني عام 1780. يمتد لمسافة '
            '422 متراً بعرض 15 متراً في قلب مدينة دمشق القديمة. يتميز بسقفه الحديدي '
            'المليء بثقوب الرصاص من الحقبة العثمانية.',
        descriptionEn:
            'The largest covered souq in Syria, built during the Ottoman era in 1780. '
            'It stretches 422 metres long and 15 metres wide in the heart of old Damascus.',
        gallery: [
          'https://images.unsplash.com/photo-1559589689-577aabd1db4f?w=800',
          'https://images.unsplash.com/photo-1465146633011-14f8e0781093?w=800',
        ],
        latitude: 33.5108,
        longitude: 36.3008,
        openingHours: '9:00 صباحاً - 8:00 مساءً',
        unescoStatus: false,
      ),

      // ═══════════ RELIGIOUS SITES ═══════════
      const CulturalSite(
        id: 'religious-001',
        nameAr: 'الجامع الأموي الكبير',
        nameEn: 'Umayyad Mosque',
        officialTitle: 'Great Mosque of Damascus',
        category: CulturalCategory.religiousSite,
        descriptionAr:
            'رابع أشهر مسجد في الإسلام، بناه الوليد بن عبد الملك عام 715م. يتميز '
            'بمئذنته ومحرابه الرخامي وفناءه الواسع. يضم ضريح النبي يحيى عليه السلام '
            'ويعتبر تحفة معمارية من العصر الأموي.',
        descriptionEn:
            'The fourth holiest mosque in Islam, built by Caliph Al-Walid I in 715 AD. '
            'Features a magnificent marble mihrab, vast courtyard, and the shrine of John '
            'the Baptist.',
        gallery: [
          'https://images.unsplash.com/photo-1578895101408-1a36b834405b?w=800',
          'https://images.unsplash.com/photo-1547127796-06bb84d5c88a?w=800',
        ],
        latitude: 33.5116,
        longitude: 36.3067,
        openingHours: 'من الفجر حتى العشاء',
        unescoStatus: false,
      ),
      const CulturalSite(
        id: 'religious-002',
        nameAr: 'دير سيدة صيدنايا',
        nameEn: 'Our Lady of Saidnaya Monastery',
        category: CulturalCategory.religiousSite,
        descriptionAr:
            'دير أرثوذكسي يوناني يقع في بلدة صيدنايا شمال دمشق، يعود تاريخه للقرن '
            'السادس. يحج إليه آلاف المسيحيين والمسلمين سنوياً لزيارة أيقونة السيدة '
            'العذراء المعجزية.',
        descriptionEn:
            'A Greek Orthodox monastery located in Saidnaya north of Damascus, dating '
            'to the 6th century. Thousands of Christians and Muslims pilgrimage here '
            'annually.',
        gallery: [
          'https://images.unsplash.com/photo-1585409677983-0f6c41ca9c3b?w=800',
        ],
        latitude: 33.6996,
        longitude: 36.3750,
        openingHours: '8:00 صباحاً - 6:00 مساءً',
        unescoStatus: false,
      ),
      const CulturalSite(
        id: 'religious-003',
        nameAr: 'معلولا - دير مار سركيس',
        nameEn: 'Maaloula - St. Sergius Monastery',
        category: CulturalCategory.religiousSite,
        descriptionAr:
            'بلدة جبلية فريدة شمال دمشق لا يزال سكانها يتحدثون اللغة الآرامية لغة '
            'السيد المسيح. تضم دير مار سركيس (القديس سرجيوس) من القرن الرابع الميلادي '
            'ودير مار تقلا الأرثوذكسي.',
        descriptionEn:
            'A unique mountain town north of Damascus where residents still speak '
            'Aramaic, the language of Jesus. Contains the 4th-century St. Sergius '
            'Monastery.',
        gallery: [
          'https://images.unsplash.com/photo-1549880338-65ddcdfd017b?w=800',
        ],
        latitude: 33.8442,
        longitude: 36.5467,
        openingHours: '8:00 صباحاً - 5:00 مساءً',
        unescoStatus: false,
      ),

      // ═══════════ ADDITIONAL ARCHAEOLOGICAL ═══════════
      const CulturalSite(
        id: 'archaeo-001',
        nameAr: 'مملكة ماري الأثرية',
        nameEn: 'Royal Palace of Mari',
        officialTitle: 'Mari Archaeological Site',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'عاصمة مملكة قديمة على الفرات تعود للألف الثالث قبل الميلاد. اكتشف فيها '
            'القصر الملكي الذي يضم 300 غرفة وأرشيفاً ضخماً من الألواح المسمارية. من '
            'أهم ممالك ما بين النهرين القديمة.',
        descriptionEn:
            'Capital of an ancient kingdom on the Euphrates dating to the 3rd millennium '
            'BC. The royal palace with 300 rooms and a vast archive of cuneiform tablets '
            'was discovered here.',
        gallery: [
          'https://images.unsplash.com/photo-1582555172866-f73bb12defab?w=800',
        ],
        latitude: 34.5514,
        longitude: 40.8885,
        unescoStatus: true,
      ),
      const CulturalSite(
        id: 'archaeo-002',
        nameAr: 'مدينة أفاميا الأثرية',
        nameEn: 'Apamea Archaeological Site',
        officialTitle: 'Apamea',
        category: CulturalCategory.unescoSite,
        descriptionAr:
            'مدينة هيلينستية-رومانية على نهر العاصي، أسسها سلوقس الأول نيكاتور. '
            'تشتهر بطريق الأعمدة الرئيسي الذي يمتد لمسافة 2 كيلومتر. من أكبر المدن '
            'القديمة في سوريا.',
        descriptionEn:
            'A Hellenistic-Roman city on the Orontes River, founded by Seleucus I '
            'Nicator. Famous for its 2 km colonnaded main street.',
        gallery: [
          'https://images.unsplash.com/photo-1590767161356-9e0b8c1f3f1b?w=800',
        ],
        latitude: 35.4180,
        longitude: 36.3980,
        openingHours: 'مفتوح على مدار الساعة',
        unescoStatus: true,
      ),
      
       const CulturalSite(
        id: 'unesco-007',
        nameAr: 'قلعة صلاح الدين - صهيون',
        nameEn: 'Citadel of Salah Ed-Din (Sahyun Castle)',
        officialTitle: 'Crac des Chevaliers and Qal\'at Salah El-Din',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'تقع القلعة على بعد 30 كم شرق اللاذقية في منطقة جبلية مرتفعة بين وديان عميقة. كانت تعرف قديماً باسم صهيون وحصنت منذ منتصف القرن العاشر. تعتبر من أروع نماذج العمارة العسكرية في العصور الوسطى.',
        descriptionEn: 'Located 30 km east of Latakia in high mountainous terrain on a ridge between two deep ravines. Known anciently as Sahyun, it has been fortified since the mid-10th century.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Qalaat_Salah_el-Din_01.jpg/800px-Qalaat_Salah_el-Din_01.jpg'],
        latitude: 35.5958, longitude: 36.0572,
        openingHours: '9:00 صباحاً - 5:00 مساءً', unescoStatus: true,
      ),
      const CulturalSite(
        id: 'unesco-008',
        nameAr: 'القرى الأثرية في شمال سوريا - المدن المنسية',
        nameEn: 'Ancient Villages of Northern Syria (Dead Cities)',
        officialTitle: 'Ancient Villages of Northern Syria',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'تضم أكثر من 700 موقع أثري في شمال غرب سوريا بين حلب وإدلب. تعود للفترة الرومانية والبيزنطية (القرن الأول إلى السابع الميلادي) وتضم كنائس ومعاصر زيتون وحمامات وفيلات ريفية. من أهم المواقع: البارة وسرجيلا وقلب لوزة.',
        descriptionEn: 'Over 700 abandoned settlements in northwestern Syria dating from the 1st to 7th centuries. Includes remarkably preserved churches, olive presses, baths, and rural villas. Key sites: Al-Bara, Serjilla, Qalb Loze.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Serjilla.jpg/800px-Serjilla.jpg'],
        latitude: 35.6833, longitude: 36.5333,
        openingHours: 'مفتوح على مدار الساعة', unescoStatus: true,
      ),

      // ═══════════ NEU: BURGEN & FESTUNGEN ═══════════
      const CulturalSite(
        id: 'castle-001',
        nameAr: 'قلعة حلب',
        nameEn: 'Citadel of Aleppo',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'تعتبر من أقدم وأكبر القلاع في العالم، تقع على تل اصطناعي بارتفاع 50 متراً في وسط مدينة حلب القديمة. يعود تاريخها إلى الألفية الثالثة قبل الميلاد، وأعيد بناؤها في العصر الأيوبي. تضم قاعة العرش والحمام الملكي والمسجد الإبراهيمي.',
        descriptionEn: 'One of the oldest and largest castles in the world, standing on a 50m artificial hill in the centre of ancient Aleppo. Dates back to the 3rd millennium BC and rebuilt during the Ayyubid period.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Aleppo_Citadel_04.jpg/800px-Aleppo_Citadel_04.jpg'],
        latitude: 36.19917, longitude: 37.16250,
        openingHours: '9:00 صباحاً - 5:00 مساءً', entryFee: '500 ل.س', unescoStatus: true,
      ),
      const CulturalSite(
        id: 'castle-002',
        nameAr: 'قلعة المرقب',
        nameEn: 'Qalaat Marqab (Margat Castle)',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'حصن صليبي ضخم يقع على قمة بركان خامد بارتفاع 500 متر بين طرطوس واللاذقية. بناه فرسان الإسبتارية ويطل على البحر المتوسط. يتميز بأبراجه الضخمة وسوره المزدوج وخندقه العميق.',
        descriptionEn: 'A massive Crusader fortress situated on an extinct volcano 500m above sea level between Tartous and Latakia. Built by the Knights Hospitaller, overlooking the Mediterranean.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Margat_01.jpg/800px-Margat_01.jpg'],
        latitude: 35.15101, longitude: 35.94963,
        openingHours: '9:00 صباحاً - 4:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'castle-003',
        nameAr: 'قلعة دمشق',
        nameEn: 'Citadel of Damascus',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'تقع في الركن الشمالي الغربي من أسوار دمشق القديمة. بنيت في القرن الحادي عشر في العصر السلجوقي، وأعيد بناؤها في العصر الأيوبي. تضم 12 برجاً وبوابة ضخمة. استخدمت كسجن ومقر عسكري.',
        descriptionEn: 'Located in the northwest corner of the old city walls. Built in the 11th century during the Seljuk period and rebuilt under the Ayyubids. Features 12 towers and a monumental gate.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Citadel_of_Damascus.jpg/800px-Citadel_of_Damascus.jpg'],
        latitude: 33.5115, longitude: 36.3012,
        openingHours: '9:00 صباحاً - 4:00 مساءً', unescoStatus: false,
      ),

      // ═══════════ NEU: ARCHÄOLOGISCHE STÄTTEN ═══════════
      const CulturalSite(
        id: 'archaeo-003',
        nameAr: 'إيبلا - تل مرديخ',
        nameEn: 'Ebla (Tell Mardikh)',
        officialTitle: 'Ebla Archaeological Site',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'مدينة أثرية هامة من العصر البرونزي (2400 ق.م)، تقع على بعد 55 كم جنوب غرب حلب. اكتشف فيها أرشيف ملكي يضم أكثر من 5000 رقيم طيني مسماري يوثق الحياة السياسية والاقتصادية في الألف الثالث قبل الميلاد.',
        descriptionEn: 'Major Bronze Age city (2400 BC) located 55 km southwest of Aleppo. A royal archive of over 5,000 cuneiform tablets documenting political and economic life in the 3rd millennium BC was discovered here.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Ebla.jpg/800px-Ebla.jpg'],
        latitude: 35.798, longitude: 36.798,
        openingHours: '8:00 صباحاً - 4:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'archaeo-004',
        nameAr: 'أوغاريت - رأس شمرة',
        nameEn: 'Ugarit (Ras Shamra)',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'مملكة قديمة على ساحل البحر المتوسط (1450-1200 ق.م)، تقع على بعد 10 كم شمال اللاذقية. اكتشفت فيها أقدم أبجدية في العالم (الأبجدية الأوغاريتية) التي تعتبر سلف الأبجديات الحديثة. تضم القصر الملكي ومعابد وبيوت سكنية.',
        descriptionEn: 'Ancient kingdom on the Mediterranean coast (1450-1200 BC), located 10 km north of Latakia. The oldest alphabet in the world (Ugaritic alphabet) was discovered here, ancestor of modern alphabets.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Ugarit_01.jpg/800px-Ugarit_01.jpg'],
        latitude: 35.602, longitude: 35.782,
        openingHours: '8:00 صباحاً - 5:00 مساءً', entryFee: '200 ل.س', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'archaeo-005',
        nameAr: 'دورا أوروبوس',
        nameEn: 'Dura-Europos',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'مدينة هيلينستية على نهر الفرات (303 ق.م - 256 م)، تقع قرب بلدة الصالحية. تضم أقدم كنيسة منزلية معروفة في العالم (240 م) وأقدم كنيس يهودي مزين بلوحات جدارية. تعرف باسم "بومبي الصحراء".',
        descriptionEn: 'Hellenistic city on the Euphrates (303 BC - 256 AD) near the village of Salhiyah. Contains the oldest known house church in the world (240 AD) and the oldest decorated synagogue with wall paintings. Known as "Pompeii of the Desert".',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Dura_Europos.jpg/800px-Dura_Europos.jpg'],
        latitude: 34.747, longitude: 40.730,
        openingHours: '8:00 صباحاً - 3:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'archaeo-006',
        nameAr: 'قطنا - المشرفة',
        nameEn: 'Qatna (Tell Mishrifeh)',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'مدينة أثرية من العصر البرونزي (2000-1200 ق.م)، تقع على بعد 18 كم شمال شرق حمص. كانت مملكة قوية نافست ماري وإيبلا. اكتشف فيها القصر الملكي والمقبرة الملكية التي تضم مئات القطع الأثرية.',
        descriptionEn: 'Bronze Age city (2000-1200 BC) located 18 km northeast of Homs. A powerful kingdom that rivaled Mari and Ebla. The royal palace and royal tomb containing hundreds of artifacts were discovered here.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Qatna.jpg/800px-Qatna.jpg'],
        latitude: 34.835, longitude: 36.866,
        openingHours: '8:00 صباحاً - 3:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'archaeo-007',
        nameAr: 'عمريت',
        nameEn: 'Amrit (Ancient Marathus)',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'مدينة فينيقية قديمة (القرن الثالث ق.م)، تقع على بعد 6 كم جنوب طرطوس. تضم معبداً فريداً مائياً (المعبد المائي) محفوراً في الصخر ومحاطاً ببركة ماء. من أفضل المواقع الفينيقية المحفوظة في العالم.',
        descriptionEn: 'Ancient Phoenician city (3rd century BC) located 6 km south of Tartous. Features a unique water temple carved into rock and surrounded by a sacred pool. One of the best-preserved Phoenician sites in the world.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Amrit_Temple.jpg/800px-Amrit_Temple.jpg'],
        latitude: 34.833, longitude: 35.917,
        openingHours: '8:00 صباحاً - 5:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'archaeo-008',
        nameAr: 'الرصافة - سرجيوبوليس',
        nameEn: 'Resafa (Sergiopolis)',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'مدينة أثرية في البادية السورية (القرن الرابع الميلادي) تقع على بعد 40 كم جنوب الرقة. كانت مركزاً للحج المسيحي حيث استشهد القديس سرجيوس. تضم كاتدرائية ضخمة وكنائس وصهاريج مياه وأسواراً بيزنطية.',
        descriptionEn: 'Ancient city in the Syrian desert (4th century AD) located 40 km south of Raqqa. A major Christian pilgrimage centre where St. Sergius was martyred. Features a massive cathedral, churches, cisterns, and Byzantine walls.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Resafa.jpg/800px-Resafa.jpg'],
        latitude: 35.633, longitude: 38.750,
        openingHours: 'مفتوح على مدار الساعة', unescoStatus: false,
      ),

      // ═══════════ NEU: RELIGIÖSE STÄTTEN ═══════════
      const CulturalSite(
        id: 'religious-004',
        nameAr: 'مقام السيدة رقية',
        nameEn: 'Sayyida Ruqayya Mosque',
        category: CulturalCategory.religiousSite,
        descriptionAr: 'مقام ديني شيعي يقع في منطقة العمارة بدمشق القديمة. يحتضن ضريح السيدة رقية بنت الإمام الحسين. يتميز بقبته الذهبية وزخارفه الفارسية الرائعة ومراياه الملونة التي تغطي الجدران والسقف.',
        descriptionEn: 'A Shia religious shrine in the Amara district of old Damascus. Houses the tomb of Sayyida Ruqayya, daughter of Imam Hussein. Famous for its golden dome, Persian ornaments, and colourful mirror work covering walls and ceiling.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Sayyidah_Ruqayya_Mosque_01.jpg/800px-Sayyidah_Ruqayya_Mosque_01.jpg'],
        latitude: 33.513, longitude: 36.306,
        openingHours: 'من الفجر حتى العشاء', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'religious-005',
        nameAr: 'مقام السيدة زينب',
        nameEn: 'Sayyida Zaynab Mosque',
        category: CulturalCategory.religiousSite,
        descriptionAr: 'من أهم المزارات الشيعية في العالم، يقع في منطقة السيدة زينب جنوب دمشق. يحتضن ضريح السيدة زينب بنت الإمام علي. يتميز بقبته الذهبية ومناراته الشاهقة وصحنه الواسع المزين بالمرايا والزخارف الإسلامية.',
        descriptionEn: 'One of the most important Shia shrines in the world, located in Sayyida Zaynab area south of Damascus. Houses the tomb of Sayyida Zaynab, daughter of Imam Ali. Features a golden dome, towering minarets, and a vast courtyard.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Sayyidah_Zaynab_Mosque.jpg/800px-Sayyidah_Zaynab_Mosque.jpg'],
        latitude: 33.444, longitude: 36.341,
        openingHours: 'من الفجر حتى العشاء', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'religious-006',
        nameAr: 'مقام النبي هابيل',
        nameEn: 'Nabi Habeel Mosque (Tomb of Abel)',
        category: CulturalCategory.religiousSite,
        descriptionAr: 'يقع على قمة جبل قاسيون غرب دمشق. يعتقد أنه يحتضن قبر هابيل بن آدم عليه السلام. يتميز بإطلالته البانورامية على مدينة دمشق ويعتبر مزاراً دينياً هاماً للمسلمين.',
        descriptionEn: 'Located on the summit of Mount Qasioun west of Damascus. Believed to contain the tomb of Abel, son of Prophet Adam. Offers panoramic views of Damascus and is an important religious pilgrimage site.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Nabi_Habeel_Mosque.jpg/800px-Nabi_Habeel_Mosque.jpg'],
        latitude: 33.521, longitude: 36.313,
        openingHours: 'من الفجر حتى العشاء', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'religious-007',
        nameAr: 'الجامع الكبير في حلب',
        nameEn: 'Great Mosque of Aleppo',
        category: CulturalCategory.religiousSite,
        descriptionAr: 'أكبر وأقدم مساجد حلب، بني في العصر الأموي (715م) على يد الوليد بن عبد الملك. يتميز بمئذنته المربعة الشهيرة التي تعود للقرن الحادي عشر والتي أعيد بناؤها بعد الحرب. يضم ضريح النبي زكريا.',
        descriptionEn: 'The largest and oldest mosque in Aleppo, built during the Umayyad era (715 AD) by Caliph Al-Walid I. Famous for its square 11th-century minaret (rebuilt after the war). Contains the shrine of Prophet Zechariah.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Great_Mosque_of_Aleppo.jpg/800px-Great_Mosque_of_Aleppo.jpg'],
        latitude: 36.199, longitude: 37.157,
        openingHours: 'من الفجر حتى العشاء', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'religious-008',
        nameAr: 'كنيسة ودير مار تقلا - معلولا',
        nameEn: 'St. Thecla Monastery - Maaloula',
        category: CulturalCategory.religiousSite,
        descriptionAr: 'أقدم دير في العالم (55 م)، بُني حول مغارة القديسة تقلا تلميذة بولس الرسول. يقع في بلدة معلولا الجبلية حيث لا يزال السكان يتحدثون الآرامية. يضم الدير أيقونات بيزنطية نادرة وينبوع ماء مقدس.',
        descriptionEn: 'The oldest monastery in the world (55 AD), built around the cave of St. Thecla, disciple of St. Paul. Located in the mountain town of Maaloula where residents still speak Aramaic. Contains rare Byzantine icons and a holy spring.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Maaloula.jpg/800px-Maaloula.jpg'],
        latitude: 33.843, longitude: 36.548,
        openingHours: '8:00 صباحاً - 6:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'religious-009',
        nameAr: 'دير سيدة صيدنايا',
        nameEn: 'Our Lady of Saidnaya Monastery',
        category: CulturalCategory.religiousSite,
        descriptionAr: 'دير أرثوذكسي يوناني يقع في بلدة صيدنايا شمال دمشق، يعود تاريخه للقرن السادس. يحج إليه آلاف المسيحيين والمسلمين سنوياً لزيارة أيقونة السيدة العذراء المعجزية.',
        descriptionEn: 'A Greek Orthodox monastery located in Saidnaya north of Damascus, dating to the 6th century. Thousands of Christians and Muslims pilgrimage here annually to visit the miraculous icon of the Virgin Mary.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Saidnaya.jpg/800px-Saidnaya.jpg'],
        latitude: 33.6996, longitude: 36.3750,
        openingHours: '8:00 صباحاً - 6:00 مساءً', unescoStatus: false,
      ),

      // ═══════════ NEU: HISTORISCHE MÄRKTE ═══════════
      const CulturalSite(
        id: 'suq-002',
        nameAr: 'سوق البزورية',
        nameEn: 'Souk al-Bzourieh',
        category: CulturalCategory.historicalMarket,
        descriptionAr: 'من أقدم أسواق دمشق، يقع خلف الجامع الأموي. يشتهر ببيع البهارات والعطارة والحلويات الدمشقية التقليدية. يتميز بروائحه العطرية وسقفه الخشبي القديم.',
        descriptionEn: 'One of the oldest souqs in Damascus, located behind the Umayyad Mosque. Famous for spices, perfumery, and traditional Damascene sweets. Known for its fragrant aromas and ancient wooden ceiling.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Souk_al-Bzourieh.jpg/800px-Souk_al-Bzourieh.jpg'],
        latitude: 33.511, longitude: 36.306,
        openingHours: '9:00 صباحاً - 8:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'suq-003',
        nameAr: 'سوق المدينة - حلب',
        nameEn: 'Al-Madina Souq - Aleppo',
        category: CulturalCategory.historicalMarket,
        descriptionAr: 'أكبر سوق مسقوف في العالم، يمتد لمسافة 13 كم داخل مدينة حلب القديمة. يعود معظمه للقرن الرابع عشر ويضم أسواقاً متخصصة: سوق الصوف، سوق النحاس، سوق الذهب. يضم خانات تاريخية أهمها خان الوزير.',
        descriptionEn: 'The largest covered market in the world, stretching 13 km within the old city of Aleppo. Mostly dating to the 14th century with specialized souqs: wool souq, copper souq, gold souq. Contains historic khans including Khan al-Wazir.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Al-Madina_Souq_Aleppo.jpg/800px-Al-Madina_Souq_Aleppo.jpg'],
        latitude: 36.200, longitude: 37.157,
        openingHours: '9:00 صباحاً - 7:00 مساءً', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'suq-004',
        nameAr: 'سوق الصاغة',
        nameEn: 'Souk al-Sagha (Gold Souq)',
        category: CulturalCategory.historicalMarket,
        descriptionAr: 'سوق تاريخي من العصر الأيوبي يقع في قلب مدينة دمشق القديمة. يشتهر بتجارة الذهب والمجوهرات والحلي الفضية. يعتبر أقدم سوق للصاغة في الشرق الأوسط.',
        descriptionEn: 'Historic market from the Ayyubid period in the heart of old Damascus. Famous for gold, jewellery, and silver ornaments. Considered the oldest goldsmith market in the Middle East.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Souk_al-Sagha_Damascus.jpg/800px-Souk_al-Sagha_Damascus.jpg'],
        latitude: 33.510, longitude: 36.302,
        openingHours: '10:00 صباحاً - 7:00 مساءاً', unescoStatus: false,
      ),

      // ═══════════ NEU: WEITERE MUSEEN ═══════════
      const CulturalSite(
        id: 'museum-003',
        nameAr: 'متحف تدمر',
        nameEn: 'Palmyra Museum',
        category: CulturalCategory.museum,
        descriptionAr: 'يقع عند مدخل مدينة تدمر الأثرية. يضم مجموعة غنية من القطع الأثرية من مملكة تدمر: تماثيل جنائزية، نقوش، فسيفساء، وأسلحة. أغلبه دمر عام 2015 وجرى ترميمه وإعادة افتتاحه.',
        descriptionEn: 'Located at the entrance of the Palmyra archaeological site. Houses a rich collection of Palmyrene artifacts: funerary statues, inscriptions, mosaics, and weapons. Largely destroyed in 2015, restored and reopened.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Palmyra_Museum.jpg/800px-Palmyra_Museum.jpg'],
        latitude: 34.560, longitude: 38.267,
        openingHours: '9:00 صباحاً - 4:00 مساءاً', entryFee: '200 ل.س', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'museum-004',
        nameAr: 'متحف دير الزور',
        nameEn: 'Deir ez-Zor Museum',
        category: CulturalCategory.museum,
        descriptionAr: 'متحف مخصص لآثار شمال شرق سوريا (الجزيرة). يضم مكتشفات من مواقع تل بيدر وتل براك وتل ليلان. يحتوي على مجموعة هامة من الألواح المسمارية والاختام الأسطوانية.',
        descriptionEn: 'Museum dedicated to the archaeology of northeastern Syria (Jezirah). Features finds from Tell Beydar, Tell Brak, and Tell Leilan. Contains an important collection of cuneiform tablets and cylinder seals.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Deir_ez-Zor_Museum.jpg/800px-Deir_ez-Zor_Museum.jpg'],
        latitude: 35.333, longitude: 40.133,
        openingHours: '9:00 صباحاً - 3:00 مساءاً', entryFee: '100 ل.س', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'museum-005',
        nameAr: 'متحف السويداء الوطني',
        nameEn: 'Suwayda National Museum',
        category: CulturalCategory.museum,
        descriptionAr: 'يقع في مدينة السويداء جنوب سوريا. يضم مجموعة هامة من الفسيفساء الرومانية والبيزنطية من منطقة جبل العرب. تشمل المعروضات تماثيل ونقوش نبطية ويونانية.',
        descriptionEn: 'Located in Suwayda city in southern Syria. Houses an important collection of Roman and Byzantine mosaics from the Jabal al-Arab region. Exhibits include Nabataean and Greek statues and inscriptions.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Suwayda_Museum.jpg/800px-Suwayda_Museum.jpg'],
        latitude: 32.700, longitude: 36.567,
        openingHours: '9:00 صباحاً - 3:00 مساءاً', entryFee: '100 ل.س', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'museum-006',
        nameAr: 'المتحف الوطني باللاذقية',
        nameEn: 'National Museum of Latakia',
        category: CulturalCategory.museum,
        descriptionAr: 'يضم مجموعات أثرية من منطقة الساحل السوري. تشمل المعروضات قطعاً من أوغاريت ورأس شمرة ورأس ابن هاني. يضم ألواحاً مسمارية وأختاماً ومجوهرات من العصر البرونزي.',
        descriptionEn: 'Contains archaeological collections from the Syrian coastal region. Exhibits include artefacts from Ugarit, Ras Shamra, and Ras Ibn Hani. Features cuneiform tablets, seals, and Bronze Age jewellery.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Latakia_Museum.jpg/800px-Latakia_Museum.jpg'],
        latitude: 35.517, longitude: 35.783,
        openingHours: '9:00 صباحاً - 4:00 مساءاً', entryFee: '100 ل.س', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'museum-007',
        nameAr: 'المتحف الوطني بطرطوس',
        nameEn: 'National Museum of Tartous',
        category: CulturalCategory.museum,
        descriptionAr: 'يقع في كاتدرائية صليبية سابقة تعود للقرن الثاني عشر. يضم مجموعة من الآثار الفينيقية والرومانية والصليبية من منطقة الساحل السوري. المبنى نفسه تحفة معمارية.',
        descriptionEn: 'Located in a former 12th-century Crusader cathedral. Contains a collection of Phoenician, Roman, and Crusader artefacts from the Syrian coastal region. The building itself is an architectural masterpiece.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Tartous_Museum.jpg/800px-Tartous_Museum.jpg'],
        latitude: 34.883, longitude: 35.883,
        openingHours: '9:00 صباحاً - 4:00 مساءاً', entryFee: '100 ل.س', unescoStatus: false,
      ),
      const CulturalSite(
        id: 'museum-008',
        nameAr: 'بيت أجقباش - متحف التقاليد الشعبية',
        nameEn: 'Bayt Ajeqbash (Museum of Popular Traditions)',
        category: CulturalCategory.museum,
        descriptionAr: 'بيت عربي تقليدي في حلب القديمة يعود للقرن الخامس عشر. تم تحويله إلى متحف للتقاليد الشعبية يعرض الحياة اليومية في حلب خلال العصر العثماني: أثاث، ملابس، أدوات منزلية، وأسلحة.',
        descriptionEn: 'A traditional Arab house in old Aleppo dating to the 15th century. Converted into a museum of popular traditions showcasing daily life in Aleppo during the Ottoman era: furniture, clothing, household items, and weapons.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Bayt_Ajeqbash.jpg/800px-Bayt_Ajeqbash.jpg'],
        latitude: 36.200, longitude: 37.157,
        openingHours: '9:00 صباحاً - 4:00 مساءاً', entryFee: '200 ل.س', unescoStatus: false,
      ),

      // ═══════════ NEU: WEITERE HISTORISCHE STÄTTEN ═══════════
      const CulturalSite(
        id: 'archaeo-009',
        nameAr: 'حلبية - زنوبيا',
        nameEn: 'Halabiyeh (Zenobia)',
        category: CulturalCategory.unescoSite,
        descriptionAr: 'حصن بيزنطي ضخم على نهر الفرات بنته الملكة زنوبيا في القرن الثالث. يضم أسواراً يبلغ ارتفاعها 15 متراً وبرجين ضخمين. كان يحمي الحدود الشرقية للإمبراطورية.',
        descriptionEn: 'A massive Byzantine fortress on the Euphrates built by Queen Zenobia in the 3rd century. Features walls up to 15m high and two massive towers. Protected the eastern frontier of the empire.',
        gallery: ['https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Halabiyeh.jpg/800px-Halabiyeh.jpg'],
        latitude: 35.683, longitude: 39.817,
        openingHours: 'مفتوح على مدار الساعة', unescoStatus: false,
      ),
    ];
  }
}