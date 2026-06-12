import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';
import 'package:syria_offers_app/screens/home_screen.dart';
import 'package:syria_offers_app/screens/merchant/merchant_dashboard_screen.dart';
import 'package:syria_offers_app/screens/merchant/merchant_add_offer_screen.dart';
import 'package:syria_offers_app/screens/favorites_screen.dart';
import 'package:syria_offers_app/screens/cultural_sites_screen.dart';
import 'package:syria_offers_app/screens/auth/login_screen.dart';
import 'package:syria_offers_app/screens/auth/forgot_password_screen.dart';
import 'package:syria_offers_app/screens/chat_screen.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: '.env');
  await initializeDateFormatting('ar', null);

  runApp(
    MultiProvider(
      providers: [
        Provider(create: (_) => ApiService()),
        Provider(create: (_) => AuthService()),
        Provider(create: (_) => AdminApiService()),
      ],
      child: const SyriaOffersApp(),
    ),
  );
}

class SyriaOffersApp extends StatelessWidget {
  const SyriaOffersApp({super.key});

  @override
  Widget build(BuildContext context) {
    const primaryBlue = Color(0xFF003580);
    const accentOrange = Color(0xFFFF5722);
    const bgGray = Color(0xFFF5F5F5);
    const textDark = Color(0xFF212121);

    final baseText = Theme.of(context).textTheme;
    final cairoText = GoogleFonts.cairoTextTheme(baseText)
        .apply(bodyColor: textDark, displayColor: textDark);
    final interText = GoogleFonts.interTextTheme(baseText)
        .apply(bodyColor: textDark, displayColor: textDark);

    return MaterialApp(
      title: 'Offria',
      debugShowCheckedModeBanner: false,
      localeResolutionCallback: (locale, supportedLocales) {
        if (locale == null) return const Locale('en');
        if (locale.languageCode == 'ar') return const Locale('ar');
        if (locale.languageCode == 'de') return const Locale('de');
        if (locale.languageCode == 'en') return const Locale('en');
        return const Locale('en');
      },
      supportedLocales: const [
        Locale('ar'),
        Locale('de'),
        Locale('en'),
      ],
      localizationsDelegates: const [
        AppLocalizationsDelegate(),
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      theme: ThemeData(
        primaryColor: primaryBlue,
        scaffoldBackgroundColor: bgGray,
        cardColor: Colors.white,
        textTheme: cairoText.copyWith(
          labelSmall: interText.labelSmall,
          labelMedium: interText.labelMedium,
          labelLarge: interText.labelLarge,
          bodySmall: interText.bodySmall,
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: Color(0xFFDFE3E8)),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: Color(0xFFDFE3E8)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: const BorderSide(color: primaryBlue, width: 1.5),
          ),
        ),
        cardTheme: CardThemeData(
          color: Colors.white,
          elevation: 3,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          margin: EdgeInsets.zero,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: primaryBlue,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
          ),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: primaryBlue,
          foregroundColor: Colors.white,
          centerTitle: true,
          elevation: 0,
        ),
        colorScheme: ColorScheme.fromSeed(
          seedColor: primaryBlue,
          primary: primaryBlue,
          secondary: accentOrange,
          surface: Colors.white,
          brightness: Brightness.light,
        ),
      ),
      home: const LoginScreen(),
      routes: {
        '/home': (context) => const HomeScreen(),
        '/favorites': (context) => const FavoritesScreen(),
        '/cultural': (context) => const CulturalSitesScreen(),
        '/login': (context) => const LoginScreen(),
        '/forgot-password': (context) => const ForgotPasswordScreen(),
        '/merchant-dashboard': (context) => const MerchantDashboardScreen(),
        '/merchant-add-offer': (context) => const MerchantAddOfferScreen(),
        '/chat': (context) => const ChatScreen(),
      },
    );
  }
}