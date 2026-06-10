import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:syria_offers_app/config.dart';
import 'package:syria_offers_app/models/category.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'dart:io';
class AdminApiService {
  final AuthService _authService = AuthService();

  Future<Map<String, String>> _getHeaders() async {
    final token = await _authService.getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  // Dashboard
  Future<Map<String, dynamic>> getDashboard() async {
    final headers = await _getHeaders();
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/admin/dashboard'),
      headers: headers,
    );
    return jsonDecode(response.body);
  }

  // Categories
  Future<List<Category>> getCategories() async {
    final headers = await _getHeaders();
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/admin/categories'),
      headers: headers,
    );
    final List list = jsonDecode(response.body);
    return list.map((json) => Category.fromJson(json)).toList();
  }

  Future<void> createCategory(Map<String, dynamic> data) async {
    final headers = await _getHeaders();
    await http.post(
      Uri.parse('${AppConfig.baseUrl}/admin/categories'),
      headers: headers,
      body: jsonEncode(data),
    );
  }

  Future<void> deleteCategory(int id) async {
    final headers = await _getHeaders();
    await http.delete(
      Uri.parse('${AppConfig.baseUrl}/admin/categories/$id'),
      headers: headers,
    );
  }

  // Offers
  Future<List<Offer>> getOffers() async {
    final headers = await _getHeaders();
    headers['Cache-Control'] = 'no-cache';          // <-- أضف هذا
    final uri = Uri.parse('${AppConfig.baseUrl}/admin/offers?nocache=${DateTime.now().millisecondsSinceEpoch}');
    final response = await http.get(uri, headers: headers);
    final List list = jsonDecode(response.body);
    return list.map((json) => Offer.fromJson(json)).toList();
  }

  Future<void> createOffer(Map<String, dynamic> data) async {
    final headers = await _getHeaders();
    await http.post(
      Uri.parse('${AppConfig.baseUrl}/admin/offers'),
      headers: headers,
      body: jsonEncode(data),
    );
  }

  Future<void> updateOffer(int id, Map<String, dynamic> data) async {
    final headers = await _getHeaders();
    await http.put(
      Uri.parse('${AppConfig.baseUrl}/admin/offers/$id'),
      headers: headers,
      body: jsonEncode(data),
    );
  }

  Future<void> deleteOffer(int id) async {
    final headers = await _getHeaders();
    await http.delete(
      Uri.parse('${AppConfig.baseUrl}/admin/offers/$id'),
      headers: headers,
    );
  }

  // Bookings
  Future<List<dynamic>> getBookings() async {
    final headers = await _getHeaders();
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/admin/bookings'),
      headers: headers,
    );
    return jsonDecode(response.body);
  }

  Future<void> updateBookingStatus(int id, String status) async {
    final headers = await _getHeaders();
    await http.put(
      Uri.parse('${AppConfig.baseUrl}/admin/bookings/$id/status?status=$status'),
      headers: headers,
    );
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
  Future<void> approveOffer(int id) async {
    final headers = await _getHeaders();
    await http.put(
      Uri.parse('${AppConfig.baseUrl}/admin/offers/$id/approve'),
      headers: headers,
    );
  }  
}