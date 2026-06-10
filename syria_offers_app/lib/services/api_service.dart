import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:syria_offers_app/config.dart';
import 'package:syria_offers_app/models/category.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/services/auth_service.dart';

class ApiService {
  // Hilfsmethode für Authorization-Header
  Future<Map<String, String>> _authHeaders() async {
    final token = await AuthService().getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  // Bestehende Methoden (Kategorien, Angebote, etc.)
  Future<List<Category>> getCategories() async {
    final response =
        await http.get(Uri.parse('${AppConfig.baseUrl}/categories/'));
    if (response.statusCode == 200) {
      final List jsonList = json.decode(response.body);
      return jsonList.map((json) => Category.fromJson(json)).toList();
    } else {
      throw Exception('Kategorien konnten nicht geladen werden');
    }
  }

  Future<List<Offer>> getOffers({int? categoryId}) async {
    String url = '${AppConfig.baseUrl}/offers/';
    if (categoryId != null) {
      url += '?category_id=$categoryId';
    }
    final response = await http.get(Uri.parse(url));
    if (response.statusCode == 200) {
      final List jsonList = json.decode(response.body);
      return jsonList.map((json) => Offer.fromJson(json)).toList();
    } else {
      throw Exception('Angebote konnten nicht geladen werden');
    }
  }
  Future<Map<String, dynamic>> registerWithEmail({
    required String phone,
    required String email,
    required String fullName,
  }) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'phone': phone,
        'email': email,
        'full_name': fullName,
      }),
    );
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> verifyEmail({
    required String email,
    required String code,
  }) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/auth/verify'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'code': code,
      }),
    );
    return jsonDecode(response.body);
  }
  Future<List<Offer>> getFlashDeals() async {
    final response =
        await http.get(Uri.parse('${AppConfig.baseUrl}/flash-deals/'));
    if (response.statusCode == 200) {
      final List jsonList = json.decode(response.body);
      return jsonList.map((json) => Offer.fromJson(json)).toList();
    } else {
      return [];
    }
  }

  Future<List<Offer>> getRecommendations({required int userId}) async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/recommendations/$userId'),
    );
    if (response.statusCode == 200) {
      final List jsonList = json.decode(response.body);
      return jsonList.map((json) => Offer.fromJson(json)).toList();
    } else {
      return [];
    }
  }

  Future<Map<String, dynamic>> chatQuery(String query, {String sessionId = ''}) async {
    final uri = Uri.parse(
      '${AppConfig.baseUrl}/chatbot/?query=${Uri.encodeComponent(query)}&session_id=${Uri.encodeComponent(sessionId)}',
    );
    final response = await http.get(uri);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return {
        'reply': data['reply'] ?? '',
        'offers': data['offers'] ?? [],
        'plan_id': data['plan_id'],
        'session_id': data['session_id'] ?? '',
      };
    } else {
      throw Exception('Chatbot Fehler');
    }
  }

  Future<Map<String, dynamic>> createBooking({
    required String userName,
    required String userPhone,
    required int offerId,
    required String bookedAt,
    required int quantity,
    required double totalPrice,
  }) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/bookings/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_name': userName,
        'user_phone': userPhone,
        'offer_id': offerId,
        'booked_at': bookedAt,
        'quantity': quantity,
        'total_price': totalPrice,
      }),
    );
    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Buchung fehlgeschlagen');
    }
  }

  // ---------- NEUE MERCHANT-METHODEN ----------
  Future<Map<String, dynamic>> getMerchantDashboard() async {
    final headers = await _authHeaders();
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/merchant/dashboard'),
      headers: headers,
    );
    if (response.statusCode == 200) return jsonDecode(response.body);
    throw Exception('Dashboard konnte nicht geladen werden');
  }

  Future<List<Offer>> getMyMerchantOffers() async {
    final headers = await _authHeaders();
    headers['Cache-Control'] = 'no-cache';          // <-- أضف هذا
    final uri = Uri.parse('${AppConfig.baseUrl}/merchant/offers?nocache=${DateTime.now().millisecondsSinceEpoch}');
    final response = await http.get(uri, headers: headers);
    if (response.statusCode == 200) {
      final List list = jsonDecode(response.body);
      return list.map((json) => Offer.fromJson(json)).toList();
    }
    throw Exception('Angebote konnten nicht geladen werden');
  }

  Future<void> createMerchantOffer(Map<String, dynamic> data) async {
    final headers = await _authHeaders();
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/merchant/offers'),
      headers: headers,
      body: jsonEncode(data),
    );
    if (response.statusCode != 201) {
      throw Exception('Angebot konnte nicht erstellt werden');
    }
  }

  Future<void> deleteMyOffer(int offerId) async {
    final headers = await _authHeaders();
    final response = await http.delete(
      Uri.parse('${AppConfig.baseUrl}/merchant/offers/$offerId'),
      headers: headers,
    );
    if (response.statusCode != 200) {
      throw Exception('Löschen fehlgeschlagen');
    }
  }

  Future<List<dynamic>> getMyMerchantBookings() async {
    final headers = await _authHeaders();
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/merchant/bookings'),
      headers: headers,
    );
    if (response.statusCode == 200) return jsonDecode(response.body);
    throw Exception('Buchungen konnten nicht geladen werden');
  }

  // Plattformunabhängiger Upload
  Future<List<String>> uploadImages(List<File> files) async {
    // Web-Test: kein Upload möglich, geben leere Liste zurück
    if (files.isEmpty) return [];

    // Im Web: Multipart-Upload umgehen
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('${AppConfig.baseUrl}/uploads/images'),
      );
      for (final file in files) {
        request.files.add(await http.MultipartFile.fromPath('files', file.path));
      }
      final response = await http.Response.fromStream(await request.send());
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['images']);
      }
    } catch (e) {
      // Fehler ignorieren, leere Liste zurückgeben
    }
    return [];
  }
}