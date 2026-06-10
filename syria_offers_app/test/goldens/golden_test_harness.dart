import 'dart:async';
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'package:syria_offers_app/models/category.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/services/favorites_service.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

// ===== Mock HTTP for google_fonts in tests =====
class _MockHttpClient implements HttpClient {
  @override
  Future<HttpClientRequest> getUrl(Uri url) async {
    return _MockHttpClientRequest();
  }

  @override
  Future<HttpClientRequest> openUrl(String method, Uri url) async {
    return _MockHttpClientRequest();
  }

  @override
  void close({bool force = false}) {}

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpClientRequest implements HttpClientRequest {
  @override
  Future<HttpClientResponse> close() async {
    return _MockHttpClientResponse();
  }

  @override
  HttpHeaders get headers => throw UnimplementedError();

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpClientResponse implements HttpClientResponse {
  @override
  int get statusCode => 200;

  @override
  HttpClientResponseCompressionState get compressionState =>
      HttpClientResponseCompressionState.notCompressed;

  @override
  StreamSubscription<Uint8List> listen(
    void Function(Uint8List event)? onData, {
    void Function()? onDone,
    Function? onError,
    bool? cancelOnError,
  }) {
    return Stream<Uint8List>.fromIterable([Uint8List(0)]).listen(
      onData,
      onDone: onDone,
      onError: onError,
      cancelOnError: cancelOnError,
    );
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _MockHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) => _MockHttpClient();
}

// ⭐ هنا أضفنا الدالة التي تعطل تحميل الخطوط من الإنترنت
Future<void> setupGoogleFonts() async {
  HttpOverrides.global = _MockHttpOverrides();
}

// ========== Fake Services ==========

class FakeApiService extends ApiService {
  FakeApiService({this.categories = const [], this.offers = const [], this.dashboard = const {}});

  final List<Category> categories;
  final List<Offer> offers;
  final Map<String, dynamic> dashboard;

  @override
  Future<List<Category>> getCategories() async => categories;
  @override
  Future<List<Offer>> getOffers({int? categoryId}) async => offers;
  @override
  Future<Map<String, dynamic>> getMerchantDashboard() async => dashboard;
}

class FakeAdminApiService extends AdminApiService {
  FakeAdminApiService({this.dashboard = const {}, this.categories = const [], this.offers = const [], this.bookings = const []});

  final Map<String, dynamic> dashboard;
  final List<Category> categories;
  final List<Offer> offers;
  final List<dynamic> bookings;

  @override
  Future<Map<String, dynamic>> getDashboard() async => dashboard;
  @override
  Future<List<Category>> getCategories() async => categories;
  @override
  Future<List<Offer>> getOffers() async => offers;
  @override
  Future<List<dynamic>> getBookings() async => bookings;
}

class FakeAuthService extends AuthService {
  @override
  Future<String?> getToken() async => 'fake-token';
  @override
  Future<void> logout() async {}
}

class FakeFavoritesService extends FavoritesService {
  final Set<int> _favorites = {};

  FakeFavoritesService({List<int> favorites = const []}) {
    _favorites.addAll(favorites);
  }

  @override
  Future<void> addFavorite(int offerId) async => _favorites.add(offerId);
  @override
  Future<void> removeFavorite(int offerId) async => _favorites.remove(offerId);
  @override
  Future<bool> isFavorite(int offerId) async => _favorites.contains(offerId);
  @override
  Future<List<int>> listFavorites() async => _favorites.toList();
}

// ========== Golden Helper ==========

Future<void> pumpGoldenWidget(
  WidgetTester tester, {
  required Widget child,
  Size size = const Size(390, 844),
}) async {
  await setupGoogleFonts();             // ⭐ استدعاء التعطيل أولاً
  await initializeDateFormatting('ar', null);
  await tester.binding.setSurfaceSize(size);
  await tester.pumpWidget(child);
  await tester.pumpAndSettle();
}

Widget wrapWithApp({
  required Widget home,
  List<dynamic> providers = const [],
}) {
  return MultiProvider(
    providers: [
      Provider<ApiService>(create: (_) => FakeApiService()),
      Provider<AdminApiService>(create: (_) => FakeAdminApiService()),
      Provider<AuthService>(create: (_) => FakeAuthService()),
      Provider<FavoritesService>(create: (_) => FakeFavoritesService()),
      ...providers,
    ],
    child: MaterialApp(
      debugShowCheckedModeBanner: false,
      locale: const Locale('ar'),
      supportedLocales: const [Locale('ar'), Locale('en')],
      localizationsDelegates: const [
        AppLocalizationsDelegate(),
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      theme: buildTestTheme(),
      home: home,
    ),
  );
}

ThemeData buildTestTheme() {
  const primaryBlue = Color(0xFF003580);
  const accentOrange = Color(0xFFFF5722);
  const bgGray = Color(0xFFF5F5F5);
  const textDark = Color(0xFF212121);

  return ThemeData(
    primaryColor: primaryBlue,
    scaffoldBackgroundColor: bgGray,
    cardColor: Colors.white,
    fontFamily: 'Roboto',
    textTheme: const TextTheme(
      bodyLarge: TextStyle(color: textDark, fontFamily: 'Roboto'),
      bodyMedium: TextStyle(color: textDark, fontFamily: 'Roboto'),
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
  );
}