import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:syria_offers_app/config.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

class SetPasswordScreen extends StatefulWidget {
  final String email;
  const SetPasswordScreen({super.key, required this.email});

  @override
  State<SetPasswordScreen> createState() => _SetPasswordScreenState();
}

class _SetPasswordScreenState extends State<SetPasswordScreen> {
  final _passwordCtrl = TextEditingController();
  final _confirmCtrl = TextEditingController();
  bool _isLoading = false;
  bool _obscurePassword = true;
  bool _obscureConfirm = true;

  Future<void> _submit() async {
    final loc = AppLocalizations.of(context);
    if (_passwordCtrl.text.trim().isEmpty || _passwordCtrl.text != _confirmCtrl.text) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.passwordMismatch!)),
      );
      return;
    }

    setState(() => _isLoading = true);
    try {
      final setResponse = await http.post(
        Uri.parse('${AppConfig.baseUrl}/auth/set-password'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': widget.email,
          'password': _passwordCtrl.text.trim(),
        }),
      );
      if (setResponse.statusCode != 200) {
        final err = jsonDecode(setResponse.body)['detail'] ?? loc.failed!;
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(err)));
        setState(() => _isLoading = false);
        return;
      }

      final loginResponse = await http.post(
        Uri.parse('${AppConfig.baseUrl}/auth/email-login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': widget.email,
          'password': _passwordCtrl.text.trim(),
        }),
      );
      if (loginResponse.statusCode == 200) {
        final data = jsonDecode(loginResponse.body);
        await AuthService().saveToken(data['access_token']);
        final role = data['role'];
        if (!mounted) return;
        if (role == 'merchant') {
          Navigator.pushReplacementNamed(context, '/merchant-dashboard');
        } else {
          Navigator.pushReplacementNamed(context, '/home');
        }
      } else {
        if (mounted) Navigator.pushReplacementNamed(context, '/login');
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('${loc.error!}: $e')));
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(loc.setPassword!)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(loc.enterNewPassword!, style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 24),
            TextField(
              controller: _passwordCtrl,
              obscureText: _obscurePassword,
              decoration: InputDecoration(
                labelText: loc.password!,
                suffixIcon: IconButton(
                  icon: Icon(_obscurePassword ? Icons.visibility_off : Icons.visibility),
                  onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                ),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _confirmCtrl,
              obscureText: _obscureConfirm,
              decoration: InputDecoration(
                labelText: loc.confirmPassword!,
                suffixIcon: IconButton(
                  icon: Icon(_obscureConfirm ? Icons.visibility_off : Icons.visibility),
                  onPressed: () => setState(() => _obscureConfirm = !_obscureConfirm),
                ),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _submit,
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Text(loc.save!),
              ),
            ),
          ],
        ),
      ),
    );
  }
}