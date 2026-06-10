import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/screens/admin/admin_dashboard_screen.dart';

class AdminLoginScreen extends StatelessWidget {
  final _userController = TextEditingController();
  final _passController = TextEditingController();

  AdminLoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(title: Text(loc.adminLoginTitle!)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _userController,
              decoration: InputDecoration(labelText: loc.username!),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _passController,
              obscureText: true,
              decoration: InputDecoration(labelText: loc.password!),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () async {
                final auth = Provider.of<AuthService>(context, listen: false);
                final ok = await auth.login(
                  _userController.text.trim(),
                  _passController.text.trim(),
                );
                if (ok) {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(
                        builder: (_) => const AdminDashboardScreen()),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text(loc.invalidCredentials!)),
                  );
                }
              },
              child: Text(loc.signIn!),
            ),
          ],
        ),
      ),
    );
  }
}
