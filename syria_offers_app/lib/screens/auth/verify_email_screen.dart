import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/screens/auth/set_password_screen.dart';

class VerifyEmailScreen extends StatelessWidget {
  final String email;
  final String phone;
  final String fullName;

  const VerifyEmailScreen({
    super.key,
    required this.email,
    required this.phone,
    required this.fullName,
  });

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    final codeController = TextEditingController();

    return Scaffold(
      appBar: AppBar(title: Text(loc.verifyEmailTitle!)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.email, size: 80, color: Theme.of(context).primaryColor),
            const SizedBox(height: 24),
            Text('${loc.enterVerificationCodeSentTo!} $email',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 24),
            TextField(
              controller: codeController,
              keyboardType: TextInputType.number,
              maxLength: 6,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, letterSpacing: 8),
              decoration: const InputDecoration(
                hintText: '000000',
                counterText: '',
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () async {
                final api = Provider.of<ApiService>(context, listen: false);
                try {
                  await api.verifyEmail(email: email, code: codeController.text);
                  if (context.mounted) {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (_) => SetPasswordScreen(email: email),
                      ),
                    );
                  }
                } catch (e) {
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('${loc.invalidCode!}: $e')),
                    );
                  }
                }
              },
              child: Text(loc.verify!),
            ),
          ],
        ),
      ),
    );
  }
}