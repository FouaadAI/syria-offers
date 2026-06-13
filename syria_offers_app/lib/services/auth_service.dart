import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:syria_offers_app/config.dart';

class AuthService {
  static const String _tokenKey = 'access_token';

  // ───────── Benutzer / Händler (E-Mail) ─────────
  Future<Map<String, dynamic>?> loginUser(String email, String password) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/auth/email-login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await saveToken(data['access_token']);
      return data;
    }
    return null;
  }

  // ───────── Admin (Benutzername / Passwort) ─────────
  Future<bool> loginAdmin(String username, String password) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/admin/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await saveToken(data['access_token']);
      return true;
    }
    return false;
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_tokenKey);
  }

  Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_tokenKey, token);
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tokenKey);
  }

  Future<int> getUserId() async {
    final token = await getToken();
    if (token == null) return 1; // Gast
    try {
      final parts = token.split('.');
      final payload = json.decode(utf8.decode(base64Url.decode(base64.normalize(parts[1]))));
      return int.tryParse(payload['sub']) ?? 1;
    } catch (_) {
      return 1;
    }
  }
}
