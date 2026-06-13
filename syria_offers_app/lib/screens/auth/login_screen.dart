import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/screens/auth/phone_login_screen.dart';
import 'package:syria_offers_app/screens/admin/admin_dashboard_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

enum _LoginRole { user, merchant, admin }

class _LoginScreenState extends State<LoginScreen> {
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  bool _isLoading = false;
  bool _obscurePassword = true;
  _LoginRole _selectedRole = _LoginRole.user;

  Future<void> _login() async {
    final loc = AppLocalizations.of(context);
    final auth = Provider.of<AuthService>(context, listen: false);

    if (_selectedRole == _LoginRole.admin) {
      // ───────── Admin Login (Username + Password) ─────────
      if (_emailCtrl.text.trim().isEmpty || _passwordCtrl.text.isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(loc.pleaseFillAllFields!)),
        );
        return;
      }

      setState(() => _isLoading = true);
      final ok = await auth.loginAdmin(
        _emailCtrl.text.trim(),
        _passwordCtrl.text,
      );
      if (!mounted) return;
      setState(() => _isLoading = false);

      if (ok) {
        await Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => const AdminDashboardScreen()),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(loc.invalidCredentials!)),
        );
      }
      return;
    }

    // ───────── User / Merchant Login (Email + Password) ─────────
    if (_emailCtrl.text.trim().isEmpty || _passwordCtrl.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.pleaseFillAllFields!)),
      );
      return;
    }

    setState(() => _isLoading = true);
    final data = await auth.loginUser(
      _emailCtrl.text.trim(),
      _passwordCtrl.text,
    );
    if (!mounted) return;
    setState(() => _isLoading = false);

    if (data == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.loginFailed!)),
      );
      return;
    }

    final role = data['role'] as String? ?? 'customer';

    if (_selectedRole == _LoginRole.user && role != 'customer') {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.roleMismatch!)),
      );
      await auth.logout();
      return;
    }

    if (_selectedRole == _LoginRole.merchant && role != 'merchant') {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.roleMismatch!)),
      );
      await auth.logout();
      return;
    }

    if (_selectedRole == _LoginRole.user) {
      await Navigator.pushReplacementNamed(context, '/home');
    } else if (_selectedRole == _LoginRole.merchant) {
      await Navigator.pushReplacementNamed(context, '/merchant-dashboard');
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    final isAdmin = _selectedRole == _LoginRole.admin;
    return Scaffold(
      appBar: AppBar(title: Text(loc.login!)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset('assets/logo.png', height: 100),
            const SizedBox(height: 24),
            // ── Role selector ──
            Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: const Color(0xFFDFE3E8)),
              ),
              child: Row(
                children: [
                  _roleButton(loc.userLogin!, _LoginRole.user),
                  _roleButton(loc.merchantLogin!, _LoginRole.merchant),
                  _roleButton(loc.adminLogin!, _LoginRole.admin),
                ],
              ),
            ),
            const SizedBox(height: 24),
            TextField(
              controller: _emailCtrl,
              keyboardType: isAdmin ? TextInputType.text : TextInputType.emailAddress,
              decoration: InputDecoration(
                labelText: isAdmin ? loc.username : loc.email,
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _passwordCtrl,
              obscureText: _obscurePassword,
              decoration: InputDecoration(
                labelText: loc.password,
                suffixIcon: IconButton(
                  icon: Icon(
                    _obscurePassword ? Icons.visibility_off : Icons.visibility,
                  ),
                  onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                ),
              ),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _login,
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : Text(loc.signIn!),
              ),
            ),
            TextButton(
              onPressed: () => Navigator.pushNamed(context, '/forgot-password'),
              child: Text(loc.forgotPassword!),
            ),
            const SizedBox(height: 16),
            TextButton(
              onPressed: () async {
                await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const PhoneLoginScreen()),
                );
              },
              child: Text(loc.registerNow!),
            ),
          ],
        ),
      ),
    );
  }

  Widget _roleButton(String label, _LoginRole role) {
    final selected = _selectedRole == role;
    final theme = Theme.of(context);
    return Expanded(
      child: InkWell(
        onTap: () {
          setState(() {
            _selectedRole = role;
            _emailCtrl.clear();
            _passwordCtrl.clear();
          });
        },
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: selected ? theme.colorScheme.primary : Colors.transparent,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Text(
            label,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: selected ? Colors.white : theme.colorScheme.primary,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }
}