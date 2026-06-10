import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import 'dart:convert';
import 'package:syria_offers_app/config.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/screens/auth/verify_email_screen.dart';
import 'package:syria_offers_app/screens/auth/set_password_screen.dart';

class PhoneLoginScreen extends StatefulWidget {
  const PhoneLoginScreen({super.key});

  @override
  State<PhoneLoginScreen> createState() => _PhoneLoginScreenState();
}

class _PhoneLoginScreenState extends State<PhoneLoginScreen> {
  final _phoneController = TextEditingController();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _otpController = TextEditingController();

  bool _isLoading = false;
  bool _needsName = false;
  bool _isOtpSent = false;
  String? _registeredEmail;

  Future<void> _checkPhone() async {
    final loc = AppLocalizations.of(context);
    final phone = _phoneController.text.trim();
    if (phone.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.pleaseEnterPhone!)),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final loginResponse = await http.post(
        Uri.parse('${AppConfig.baseUrl}/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'phone': phone}),
      );

      if (loginResponse.statusCode == 200) {
        setState(() {
          _isOtpSent = true;
          _needsName = false;
          _isLoading = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(loc.verificationCodeSent!)),
        );
        return;
      }
    } catch (_) {}

    setState(() {
      _needsName = true;
      _isLoading = false;
    });
  }

  Future<void> _register() async {
    final loc = AppLocalizations.of(context);
    if (_nameController.text.trim().isEmpty || _emailController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.pleaseFillAllFields!)),
      );
      return;
    }

    setState(() => _isLoading = true);
    try {
      final api = Provider.of<ApiService>(context, listen: false);
      await api.registerWithEmail(
        phone: _phoneController.text.trim(),
        email: _emailController.text.trim(),
        fullName: _nameController.text.trim(),
      );

      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => VerifyEmailScreen(
              email: _emailController.text.trim(),
              phone: _phoneController.text.trim(),
              fullName: _nameController.text.trim(),
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('${loc.failed!}: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _verifyOtpAndLogin() async {
    final loc = AppLocalizations.of(context);
    if (_otpController.text.trim() != '123456') {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.invalidOtp!)),
      );
      return;
    }

    setState(() => _isLoading = true);
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/auth/login'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'phone': _phoneController.text.trim()}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final token = data['access_token'];
        final role = data['role'];

        await AuthService().saveToken(token);

        if (!mounted) return;
        if (role == 'merchant') {
          Navigator.pushReplacementNamed(context, '/merchant-dashboard');
        } else {
          _registeredEmail = _emailController.text.trim();
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => SetPasswordScreen(email: _registeredEmail!),
            ),
          );
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(loc.loginFailed!)),
        );
        setState(() => _isLoading = false);
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('${loc.error!}: $e')),
      );
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(loc.login!)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: _isOtpSent
            ? _buildOtpForm(loc)
            : (_needsName ? _buildRegisterForm(loc) : _buildPhoneOnlyForm(loc)),
      ),
    );
  }

  Widget _buildPhoneOnlyForm(AppLocalizations loc) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          children: [
            Image.asset(
              'assets/logo.png',
              height: 120,
            ),
            const SizedBox(height: 32),
            Text(loc.allOffersInOnePlace!,
              style: const TextStyle(fontSize: 16, color: Colors.grey),
            ),
            const SizedBox(height: 48),
            TextField(
              controller: _phoneController,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(
                labelText: loc.phone!,
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _checkPhone,
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Text(loc.continueBtn!),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRegisterForm(AppLocalizations loc) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(loc.newAccount!, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            TextField(
              controller: _nameController,
              decoration: InputDecoration(
                labelText: loc.fullName!,
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _phoneController,
              keyboardType: TextInputType.phone,
              enabled: false,
              decoration: InputDecoration(
                labelText: loc.phone!,
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _emailController,
              keyboardType: TextInputType.emailAddress,
              decoration: InputDecoration(
                labelText: loc.email!,
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _register,
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Text(loc.register!),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOtpForm(AppLocalizations loc) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(loc.verificationCodeTitle!, style: const TextStyle(fontSize: 20)),
            const SizedBox(height: 20),
            TextField(
              controller: _otpController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                labelText: loc.otpCode!,
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _isLoading ? null : _verifyOtpAndLogin,
              child: _isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : Text(loc.confirm!),
            ),
          ],
        ),
      ),
    );
  }
}