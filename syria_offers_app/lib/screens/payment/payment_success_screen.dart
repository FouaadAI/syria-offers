import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

class PaymentSuccessScreen extends StatelessWidget {
  final String message;

  const PaymentSuccessScreen({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(title: Text(loc.paymentSuccessTitle!)),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SizedBox(
                width: 220,
                height: 220,
                child: Lottie.network(
                  'https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json',
                  repeat: false,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                message,
                textAlign: TextAlign.center,
                style:
                    const TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: () =>
                    Navigator.popUntil(context, (route) => route.isFirst),
                icon: const Icon(Icons.home),
                label: Text(loc.backToHome!),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
