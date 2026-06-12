import 'package:flutter/material.dart';

class AppLocalizations {
  final Map<String, String> _strings;

  AppLocalizations(this._strings);

  String? get login => _strings['login'];
  String? get password => _strings['password'];
  String? get email => _strings['email'];
  String? get signIn => _strings['signIn'];
  String? get forgotPassword => _strings['forgotPassword'];
  String? get noAccount => _strings['noAccount'];
  String? get registerNow => _strings['registerNow'];
  String? get fullName => _strings['fullName'];
  String? get phone => _strings['phone'];
  String? get verifyCode => _strings['verifyCode'];
  String? get verify => _strings['verify'];
  String? get setPassword => _strings['setPassword'];
  String? get confirmPassword => _strings['confirmPassword'];
  String? get save => _strings['save'];
  String? get welcome => _strings['welcome'];
  String? get exploreOffers => _strings['exploreOffers'];
  String? get searchHint => _strings['searchHint'];
  String? get noOffers => _strings['noOffers'];
  String? get discover => _strings['discover'];
  String? get offers => _strings['offers'];
  String? get culturalSites => _strings['culturalSites'];
  String? get favorites => _strings['favorites'];
  String? get chat => _strings['chat'];
  String? get admin => _strings['admin'];
  String? get logout => _strings['logout'];
  String? get all => _strings['all'];
  String? get hotel => _strings['hotel'];
  String? get restaurant => _strings['restaurant'];
  String? get park => _strings['park'];
  String? get activity => _strings['activity'];
  String? get event => _strings['event'];
  String? get cinema => _strings['cinema'];
  String? get noPlaces => _strings['noPlaces'];
  String? get openInMaps => _strings['openInMaps'];
  String? get bookNow => _strings['bookNow'];
  String? get price => _strings['price'];
  String? get endDate => _strings['endDate'];
  String? get location => _strings['location'];
  String? get distance => _strings['distance'];
  String? get exportCalendar => _strings['exportCalendar'];
  String? get copyText => _strings['copyText'];
  String? get site => _strings['site'];
  String? get historicalOverview => _strings['historicalOverview'];
  String? get visitingHours => _strings['visitingHours'];
  String? get entryFee => _strings['entryFee'];
  String? get noFavorites => _strings['noFavorites'];
  String? get refresh => _strings['refresh'];
  String? get flashDeals => _strings['flashDeals'];
  String? get recommendedForYou => _strings['recommendedForYou'];

  // ═════════ NEUE CHAT‑SCHLÜSSEL ═════════
  String? get chatHint => _strings['chatHint'];
  String? get chatTitle => _strings['chatTitle'];
  String? get greetingMessage => _strings['greetingMessage'];
  String? get addedToCalendar => _strings['addedToCalendar'];
  String? get calendarFailed => _strings['calendarFailed'];
  String? get download => _strings['download'];

  // ═════════ AUTH‑SCHLÜSSEL ═════════
  String? get pleaseEnterPhone => _strings['pleaseEnterPhone'];
  String? get verificationCodeSent => _strings['verificationCodeSent'];
  String? get pleaseFillAllFields => _strings['pleaseFillAllFields'];
  String? get invalidOtp => _strings['invalidOtp'];
  String? get loginFailed => _strings['loginFailed'];
  String? get error => _strings['error'];
  String? get allOffersInOnePlace => _strings['allOffersInOnePlace'];
  String? get continueBtn => _strings['continueBtn'];
  String? get newAccount => _strings['newAccount'];
  String? get register => _strings['register'];
  String? get verificationCodeTitle => _strings['verificationCodeTitle'];
  String? get otpCode => _strings['otpCode'];
  String? get confirm => _strings['confirm'];
  String? get passwordMismatch => _strings['passwordMismatch'];
  String? get enterNewPassword => _strings['enterNewPassword'];
  String? get verifyEmailTitle => _strings['verifyEmailTitle'];
  String? get enterVerificationCodeSentTo =>
      _strings['enterVerificationCodeSentTo'];
  String? get invalidCode => _strings['invalidCode'];
  String? get failed => _strings['failed'];

  // ═════════ ADMIN / MERCHANT / PAYMENT ═════════
  String? get adminLoginTitle => _strings['adminLoginTitle'];
  String? get username => _strings['username'];
  String? get invalidCredentials => _strings['invalidCredentials'];
  String? get addNewOffer => _strings['addNewOffer'];
  String? get titleAr => _strings['titleAr'];
  String? get titleEn => _strings['titleEn'];
  String? get originalPrice => _strings['originalPrice'];
  String? get offerPrice => _strings['offerPrice'];
  String? get category => _strings['category'];
  String? get required => _strings['required'];
  String? get selectCategory => _strings['selectCategory'];
  String? get description => _strings['description'];
  String? get descriptionOptional => _strings['descriptionOptional'];
  String? get offerStart => _strings['offerStart'];
  String? get offerEnd => _strings['offerEnd'];
  String? get flashOffer => _strings['flashOffer'];
  String? get discountPercent => _strings['discountPercent'];
  String? get selectImages => _strings['selectImages'];
  String? get adding => _strings['adding'];
  String? get addOffer => _strings['addOffer'];
  String? get pleaseSelectCategory => _strings['pleaseSelectCategory'];
  String? get offerAddedSuccess => _strings['offerAddedSuccess'];
  String? get manageBookings => _strings['manageBookings'];
  String? get booking => _strings['booking'];
  String? get amountLabel => _strings['amountLabel'];
  String? get statusLabel => _strings['statusLabel'];
  String? get statusChangedTo => _strings['statusChangedTo'];
  String? get cancel => _strings['cancel'];
  String? get refund => _strings['refund'];
  String? get manageOffers => _strings['manageOffers'];
  String? get failedToLoadOffers => _strings['failedToLoadOffers'];
  String? get confirmDelete => _strings['confirmDelete'];
  String? get confirmDeleteMessage => _strings['confirmDeleteMessage'];
  String? get no => _strings['no'];
  String? get yes => _strings['yes'];
  String? get approved => _strings['approved'];
  String? get notApproved => _strings['notApproved'];
  String? get myOffers => _strings['myOffers'];
  String? get noOffersYet => _strings['noOffersYet'];
  String? get approvedOffersCount => _strings['approvedOffersCount'];
  String? get pendingApproval => _strings['pendingApproval'];
  String? get pleaseFillAllFieldsAndCategory =>
      _strings['pleaseFillAllFieldsAndCategory'];
  String? get offerSentPendingApproval => _strings['offerSentPendingApproval'];
  String? get sending => _strings['sending'];
  String? get sendOffer => _strings['sendOffer'];
  String? get offerDeleted => _strings['offerDeleted'];
  String? get choosePaymentMethod => _strings['choosePaymentMethod'];
  String? get requiredAmount => _strings['requiredAmount'];
  String? get payAmount => _strings['payAmount'];
  String? get walletPhoneNumber => _strings['walletPhoneNumber'];
  String? get phoneHint => _strings['phoneHint'];
  String? get shamCash => _strings['shamCash'];
  String? get syriatelCash => _strings['syriatelCash'];
  String? get mtnCash => _strings['mtnCash'];
  String? get paymentFailed => _strings['paymentFailed'];
  String? get paymentSuccess => _strings['paymentSuccess'];
  String? get adminDashboardTitle => _strings['adminDashboardTitle'];
  String? get manageCategories => _strings['manageCategories'];
  String? get activeOffers => _strings['activeOffers'];
  String? get totalBookings => _strings['totalBookings'];
  String? get revenue => _strings['revenue'];
  String? get flashDealsShort => _strings['flashDealsShort'];
  String? get needsApproval => _strings['needsApproval'];
  String? get merchantDashboardTitle => _strings['merchantDashboardTitle'];
  String? get pending => _strings['pending'];
  String? get views => _strings['views'];
  String? get manageMyOffers => _strings['manageMyOffers'];
  String? get trackBookings => _strings['trackBookings'];
  String? get categoryListTitle => _strings['categoryListTitle'];
  String? get nameArabic => _strings['nameArabic'];
  String? get nameEnglish => _strings['nameEnglish'];
  String? get noOffersCurrently => _strings['noOffersCurrently'];
  String? get merchantBookingsTitle => _strings['merchantBookingsTitle'];
  String? get noBookingsYet => _strings['noBookingsYet'];
  String? get bookingNumber => _strings['bookingNumber'];
  String? get amount => _strings['amount'];
  String? get status => _strings['status'];
  String? get paymentSuccessTitle => _strings['paymentSuccessTitle'];
  String? get backToHome => _strings['backToHome'];

  // ═════════ MISSING LOCALIZATION KEYS ═════════
  String? get currencySymbol => _strings['currencySymbol'];
  String? get bookingDate => _strings['bookingDate'];
  String? get quantity => _strings['quantity'];
  String? get totalAmount => _strings['totalAmount'];
  String? get bookingCode => _strings['bookingCode'];
  String? get bookingConfirmed => _strings['bookingConfirmed'];
  String? get thankYouBookingConfirmed => _strings['thankYouBookingConfirmed'];
  String? get showLocation => _strings['showLocation'];
  String? get bookingInfo => _strings['bookingInfo'];
  String? get confirmBooking => _strings['confirmBooking'];
  String? get name => _strings['name'];
  String? get website => _strings['website'];
  String? get favoritesAdd => _strings['favoritesAdd'];
  String? get favoritesRemove => _strings['favoritesRemove'];
  String? get shareOfferTitle => _strings['shareOfferTitle'];
  String? get shareOfferBody => _strings['shareOfferBody'];
  String? get notAvailable => _strings['notAvailable'];
  String? get directions => _strings['directions'];
  String? get distanceMeters => _strings['distanceMeters'];
  String? get payNow => _strings['payNow'];
  String? get phoneRequired => _strings['phoneRequired'];
  String? get phoneTooShort => _strings['phoneTooShort'];
  String? get verificationFailed => _strings['verificationFailed'];

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }
}

class AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['ar', 'de', 'en'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) async {
    final strings = await _loadStrings(locale.languageCode);
    return AppLocalizations(strings);
  }

  @override
  bool shouldReload(covariant LocalizationsDelegate<AppLocalizations> old) =>
      false;

  static Future<Map<String, String>> _loadStrings(String languageCode) async {
    if (languageCode == 'ar') {
      return {
        'login': 'تسجيل الدخول',
        'password': 'كلمة المرور',
        'email': 'البريد الإلكتروني',
        'signIn': 'دخول',
        'forgotPassword': 'نسيت كلمة المرور؟',
        'noAccount': 'ليس لديك حساب؟',
        'registerNow': 'سجل الآن',
        'fullName': 'الاسم الكامل',
        'phone': 'رقم الهاتف',
        'verifyCode': 'رمز التحقق',
        'verify': 'تحقق',
        'setPassword': 'تعيين كلمة المرور',
        'confirmPassword': 'تأكيد كلمة المرور',
        'save': 'حفظ',
        'welcome': 'مرحباً بك',
        'exploreOffers': 'استكشف عروض سوريا',
        'searchHint': 'ابحث عن عروض أو مواقع',
        'noOffers': 'لا توجد عروض حالياً',
        'discover': 'اكتشف',
        'offers': 'عروض',
        'culturalSites': 'المعالم الثقافية',
        'favorites': 'المفضلة',
        'chat': 'المساعد الذكي',
        'admin': 'لوحة التحكم',
        'logout': 'تسجيل خروج',
        'all': 'الكل',
        'hotel': 'فنادق',
        'restaurant': 'مطاعم',
        'park': 'منتزهات',
        'activity': 'أنشطة',
        'event': 'فعاليات',
        'cinema': 'سينما',
        'noPlaces': 'لا توجد أماكن حالياً',
        'openInMaps': 'فتح في الخرائط',
        'bookNow': 'احجز الآن',
        'price': 'ل.س',
        'endDate': 'ينتهي العرض',
        'location': 'الموقع',
        'distance': 'كم',
        'exportCalendar': 'تصدير إلى التقويم',
        'copyText': 'تم نسخ النص',
        'site': 'موقع تراث عالمي - UNESCO',
        'historicalOverview': 'لمحة تاريخية',
        'visitingHours': 'أوقات الزيارة',
        'entryFee': 'رسوم الدخول',
        'noFavorites': 'لا توجد عروض في المفضلة',
        'refresh': 'تحديث',
        'flashDeals': 'عروض فلاشية',
        'recommendedForYou': 'اقترحنا لك',
        // Chat
        'chatHint': 'اسأل عن العروض أو خطط لرحلتك...',
        'chatTitle': 'المساعد الذكي',
        'greetingMessage':
            'مرحباً! أنا مساعدك الذكي. أخبرني عن اهتماماتك وسأخطط لك رحلة رائعة في سوريا! 🗺️✨',
        'addedToCalendar': '✅ تمت الإضافة إلى التقويم!',
        'calendarFailed': '⚠️ تعذر فتح التقويم. يمكنك تحميل الملف.',
        'download': 'تنزيل',
        // Auth
        'pleaseEnterPhone': 'يرجى إدخال رقم الهاتف',
        'verificationCodeSent': 'تم إرسال رمز التحقق',
        'pleaseFillAllFields': 'يرجى ملء جميع الحقول',
        'invalidOtp': 'رمز OTP غير صحيح',
        'loginFailed': 'فشل تسجيل الدخول',
        'error': 'خطأ',
        'allOffersInOnePlace': 'كـل العـروض بمكـان واحـد',
        'continueBtn': 'متابعة',
        'newAccount': 'حساب جديد',
        'register': 'تسجيل',
        'verificationCodeTitle': 'رمز التحقق',
        'otpCode': 'رمز OTP',
        'confirm': 'تأكيد',
        'passwordMismatch': 'كلمة المرور غير متطابقة',
        'enterNewPassword': 'أدخل كلمة مرور جديدة لحسابك',
        'verifyEmailTitle': 'التحقق من البريد الإلكتروني',
        'enterVerificationCodeSentTo': 'أدخل رمز التحقق المرسل إلى',
        'invalidCode': 'رمز غير صحيح',
        'failed': 'فشل',
        // Admin / Merchant / Payment
        'adminLoginTitle': 'تسجيل دخول الإدارة',
        'username': 'اسم المستخدم',
        'invalidCredentials': 'بيانات خاطئة',
        'addNewOffer': 'إضافة عرض جديد',
        'titleAr': 'العنوان العربي',
        'titleEn': 'العنوان الإنجليزي',
        'originalPrice': 'السعر الأصلي',
        'offerPrice': 'سعر العرض',
        'category': 'القسم',
        'required': 'مطلوب',
        'selectCategory': 'اختر قسماً',
        'description': 'الوصف',
        'descriptionOptional': 'الوصف (اختياري)',
        'offerStart': 'بداية العرض',
        'offerEnd': 'نهاية العرض',
        'flashOffer': 'عرض فلاشي',
        'discountPercent': 'نسبة الخصم %',
        'selectImages': 'اختيار صور',
        'adding': 'جارٍ الإضافة...',
        'addOffer': 'إضافة عرض',
        'pleaseSelectCategory': 'يرجى اختيار القسم',
        'offerAddedSuccess': 'تمت إضافة العرض بنجاح',
        'manageBookings': 'إدارة الحجوزات',
        'booking': 'حجز',
        'amountLabel': 'المبلغ',
        'statusLabel': 'الحالة',
        'statusChangedTo': 'تم تغيير الحالة إلى',
        'cancel': 'إلغاء',
        'refund': 'استرجاع',
        'manageOffers': 'إدارة العروض',
        'failedToLoadOffers': 'فشل تحميل العروض',
        'confirmDelete': 'تأكيد الحذف',
        'confirmDeleteMessage': 'هل تريد حذف',
        'no': 'لا',
        'yes': 'نعم',
        'approved': 'معتمد',
        'notApproved': 'غير معتمد',
        'myOffers': 'عروضي',
        'noOffersYet': 'لا توجد عروض بعد',
        'approvedOffersCount': 'لديك %count% عروض معتمدة',
        'pendingApproval': 'في انتظار الموافقة',
        'pleaseFillAllFieldsAndCategory': 'يرجى ملء جميع الحقول واختيار قسم',
        'offerSentPendingApproval': 'تم إرسال العرض وسيظهر بعد موافقة الإدارة',
        'sending': 'جارٍ الإرسال...',
        'sendOffer': 'إرسال العرض',
        'offerDeleted': 'تم حذف العرض',
        'choosePaymentMethod': 'اختيار وسيلة الدفع',
        'requiredAmount': 'المبلغ المطلوب',
        'payAmount': 'ادفع',
        'walletPhoneNumber': 'رقم الهاتف للمحفظة',
        'phoneHint': '09xxxxxxxx',
        'shamCash': 'شام كاش',
        'syriatelCash': 'سيرياتيل كاش',
        'mtnCash': 'MTN Cash',
        'paymentFailed': 'فشلت عملية الدفع',
        'paymentSuccess': 'تم الدفع بنجاح',
        'adminDashboardTitle': 'لوحة التحكم',
        'manageCategories': 'إدارة الأقسام',
        'activeOffers': 'العروض النشطة',
        'totalBookings': 'اجمالي الحجوزات',
        'revenue': 'الإيرادات',
        'flashDealsShort': 'عروض فلاشية',
        'needsApproval': 'تحتاج موافقة',
        'merchantDashboardTitle': 'لوحة تحكم التاجر',
        'pending': 'قيد الانتظار',
        'views': 'المشاهدات',
        'manageMyOffers': 'إدارة العروض',
        'trackBookings': 'متابعة الحجوزات',
        'categoryListTitle': 'إدارة الأقسام',
        'nameArabic': 'الاسم العربي',
        'nameEnglish': 'الاسم الإنجليزي',
        'noOffersCurrently': 'لا توجد عروض حالياً',
        'merchantBookingsTitle': 'حجوزات عروضي',
        'noBookingsYet': 'لا توجد حجوزات بعد',
        'bookingNumber': 'حجز',
        'amount': 'المبلغ',
        'status': 'الحالة',
        'paymentSuccessTitle': 'تم الدفع',
        'backToHome': 'العودة للرئيسية',
        // Missing keys added for hardcoded strings
        'currencySymbol': 'ل.س',
        'bookingDate': 'تاريخ الحجز',
        'quantity': 'العدد',
        'totalAmount': 'المبلغ الإجمالي',
        'bookingCode': 'رمز الحجز',
        'bookingConfirmed': 'تم الحجز بنجاح',
        'thankYouBookingConfirmed': 'شكراً لك! تم تأكيد حجزك',
        'showLocation': 'عرض الموقع',
        'bookingInfo': 'معلومات الحجز',
        'confirmBooking': 'تأكيد الحجز',
        'name': 'الاسم',
        'website': 'الموقع الإلكتروني',
        'favoritesAdd': 'إضافة إلى المفضلة',
        'favoritesRemove': 'إزالة من المفضلة',
        'shareOfferTitle': 'شوف هذا العرض الرائع على تطبيق Offria!',
        'shareOfferBody': 'حمل تطبيق Offria الآن واستكشف أفضل العروض! 🎁',
        'notAvailable': 'غير متوفر',
        'directions': 'الاتجاهات',
        'distanceMeters': 'م',
        'payNow': 'ادفع الآن',
        'phoneRequired': 'رقم الهاتف مطلوب',
        'phoneTooShort': 'يجب أن يحتوي رقم الهاتف على 10 أرقام على الأقل',
        'verificationFailed': 'فشل التحقق من الرمز',
      };
    }
    // Default Englisch (und Deutsch fällt auch hier rein)
    return {
      'login': 'Login',
      'password': 'Password',
      'email': 'Email',
      'signIn': 'Sign In',
      'forgotPassword': 'Forgot Password?',
      'noAccount': "Don't have an account?",
      'registerNow': 'Register Now',
      'fullName': 'Full Name',
      'phone': 'Phone',
      'verifyCode': 'Verification Code',
      'verify': 'Verify',
      'setPassword': 'Set Password',
      'confirmPassword': 'Confirm Password',
      'save': 'Save',
      'welcome': 'Welcome',
      'exploreOffers': 'Explore Syria Offers',
      'searchHint': 'Search offers or locations',
      'noOffers': 'No offers available',
      'discover': 'Discover',
      'offers': 'Offers',
      'culturalSites': 'Cultural Sites',
      'favorites': 'Favorites',
      'chat': 'Smart Assistant',
      'admin': 'Admin Panel',
      'logout': 'Logout',
      'all': 'All',
      'hotel': 'Hotels',
      'restaurant': 'Restaurants',
      'park': 'Parks',
      'activity': 'Activities',
      'event': 'Events',
      'cinema': 'Cinema',
      'noPlaces': 'No places found',
      'openInMaps': 'Open in Maps',
      'bookNow': 'Book Now',
      'price': 'SP',
      'endDate': 'Offer ends',
      'location': 'Location',
      'distance': 'km',
      'exportCalendar': 'Export to Calendar',
      'copyText': 'Text copied',
      'site': 'UNESCO World Heritage Site',
      'historicalOverview': 'Historical Overview',
      'visitingHours': 'Visiting Hours',
      'entryFee': 'Entry Fee',
      'noFavorites': 'No favorites yet',
      'refresh': 'Refresh',
      'flashDeals': 'Flash Deals',
      'recommendedForYou': 'Recommended for You',
      // Chat
      'chatHint': 'Ask for offers or plan your trip...',
      'chatTitle': 'Smart Assistant',
      'greetingMessage':
          'Hello! I am your smart assistant. Tell me about your interests and I will plan a wonderful trip for you in Syria! 🗺️✨',
      'addedToCalendar': '✅ Added to calendar!',
      'calendarFailed':
          '⚠️ Could not open calendar. You can download the file.',
      'download': 'Download',
      // Auth
      'pleaseEnterPhone': 'Please enter your phone number',
      'verificationCodeSent': 'Verification code sent',
      'pleaseFillAllFields': 'Please fill in all fields',
      'invalidOtp': 'Invalid OTP code',
      'loginFailed': 'Login failed',
      'error': 'Error',
      'allOffersInOnePlace': 'All offers in one place',
      'continueBtn': 'Continue',
      'newAccount': 'New Account',
      'register': 'Register',
      'verificationCodeTitle': 'Verification Code',
      'otpCode': 'OTP Code',
      'confirm': 'Confirm',
      'passwordMismatch': 'Passwords do not match',
      'enterNewPassword': 'Enter a new password for your account',
      'verifyEmailTitle': 'Verify Email',
      'enterVerificationCodeSentTo': 'Enter the verification code sent to',
      'invalidCode': 'Invalid code',
      'failed': 'Failed',
      // Admin / Merchant / Payment
      'adminLoginTitle': 'Admin Login',
      'username': 'Username',
      'invalidCredentials': 'Invalid credentials',
      'addNewOffer': 'Add New Offer',
      'titleAr': 'Title (Arabic)',
      'titleEn': 'Title (English)',
      'originalPrice': 'Original Price',
      'offerPrice': 'Offer Price',
      'category': 'Category',
      'required': 'Required',
      'selectCategory': 'Select a category',
      'description': 'Description',
      'descriptionOptional': 'Description (optional)',
      'offerStart': 'Offer Start',
      'offerEnd': 'Offer End',
      'flashOffer': 'Flash Offer',
      'discountPercent': 'Discount %',
      'selectImages': 'Select Images',
      'adding': 'Adding...',
      'addOffer': 'Add Offer',
      'pleaseSelectCategory': 'Please select a category',
      'offerAddedSuccess': 'Offer added successfully',
      'manageBookings': 'Manage Bookings',
      'booking': 'Booking',
      'amountLabel': 'Amount',
      'statusLabel': 'Status',
      'statusChangedTo': 'Status changed to',
      'cancel': 'Cancel',
      'refund': 'Refund',
      'manageOffers': 'Manage Offers',
      'failedToLoadOffers': 'Failed to load offers',
      'confirmDelete': 'Confirm Delete',
      'confirmDeleteMessage': 'Are you sure you want to delete',
      'no': 'No',
      'yes': 'Yes',
      'approved': 'Approved',
      'notApproved': 'Not approved',
      'myOffers': 'My Offers',
      'noOffersYet': 'No offers yet',
      'approvedOffersCount': 'You have %count% approved offers',
      'pendingApproval': 'Pending approval',
      'pleaseFillAllFieldsAndCategory':
          'Please fill all fields and select a category',
      'offerSentPendingApproval':
          'Offer submitted and will appear after admin approval',
      'sending': 'Sending...',
      'sendOffer': 'Send Offer',
      'offerDeleted': 'Offer deleted',
      'choosePaymentMethod': 'Choose Payment Method',
      'requiredAmount': 'Amount Due',
      'payAmount': 'Pay',
      'walletPhoneNumber': 'Wallet Phone Number',
      'phoneHint': '09xxxxxxxx',
      'shamCash': 'Sham Cash',
      'syriatelCash': 'Syriatel Cash',
      'mtnCash': 'MTN Cash',
      'paymentFailed': 'Payment failed',
      'paymentSuccess': 'Payment successful',
      'adminDashboardTitle': 'Admin Dashboard',
      'manageCategories': 'Manage Categories',
      'activeOffers': 'Active Offers',
      'totalBookings': 'Total Bookings',
      'revenue': 'Revenue',
      'flashDealsShort': 'Flash Deals',
      'needsApproval': 'Needs Approval',
      'merchantDashboardTitle': 'Merchant Dashboard',
      'pending': 'Pending',
      'views': 'Views',
      'manageMyOffers': 'Manage Offers',
      'trackBookings': 'Track Bookings',
      'categoryListTitle': 'Category Management',
      'nameArabic': 'Arabic Name',
      'nameEnglish': 'English Name',
      'noOffersCurrently': 'No offers currently',
      'merchantBookingsTitle': 'My Offer Bookings',
      'noBookingsYet': 'No bookings yet',
      'bookingNumber': 'Booking',
      'amount': 'Amount',
      'status': 'Status',
      'paymentSuccessTitle': 'Payment Successful',
      'backToHome': 'Back to Home',
      // Missing keys added for hardcoded strings
      'currencySymbol': 'SP',
      'bookingDate': 'Booking Date',
      'quantity': 'Quantity',
      'totalAmount': 'Total Amount',
      'bookingCode': 'Booking Code',
      'bookingConfirmed': 'Booking Confirmed',
      'thankYouBookingConfirmed': 'Thank you! Your booking has been confirmed.',
      'showLocation': 'Show Location',
      'bookingInfo': 'Booking Info',
      'confirmBooking': 'Confirm Booking',
      'name': 'Name',
      'website': 'Website',
      'favoritesAdd': 'Add to Favorites',
      'favoritesRemove': 'Remove from Favorites',
      'shareOfferTitle': 'Check out this amazing offer on Offria!',
      'shareOfferBody': 'Download the Offria app now and discover the best offers! 🎁',
      'notAvailable': 'Not available',
      'directions': 'Directions',
      'distanceMeters': 'm',
      'payNow': 'Pay Now',
      'phoneRequired': 'Phone number is required',
      'phoneTooShort': 'Phone number must be at least 10 digits',
      'verificationFailed': 'Verification failed',
    };
  }
}
