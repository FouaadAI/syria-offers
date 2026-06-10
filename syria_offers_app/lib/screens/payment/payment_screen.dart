import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:syria_offers_app/config.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/screens/payment/payment_success_screen.dart';

class PaymentScreen extends StatelessWidget {
  final int bookingId;
  final double amount;

  const PaymentScreen({
    super.key,
    required this.bookingId,
    required this.amount,
  });

  void _processPayment(
      BuildContext context, String method, String phone) async {
    final loc = AppLocalizations.of(context);
    try {
      final response = await http.post(
        Uri.parse(
          '${AppConfig.baseUrl}/payments/pay?booking_id=$bookingId&amount=$amount&phone=$phone&method=$method',
        ),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['success'] == true) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(data['message'])),
          );
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => PaymentSuccessScreen(
                  message: data['message'] ?? loc.paymentSuccess!),
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(data['message'])),
          );
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(loc.paymentFailed!)),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('${loc.error}: $e')),
      );
    }
  }

  void _showPhoneDialog(BuildContext context, String method) {
    final loc = AppLocalizations.of(context);
    final phoneController = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(loc.walletPhoneNumber!),
        content: TextField(
          controller: phoneController,
          keyboardType: TextInputType.phone,
          decoration: InputDecoration(hintText: loc.phoneHint),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text(loc.cancel!),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(ctx);
              _processPayment(context, method, phoneController.text.trim());
            },
            child: Text(loc.confirm!),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(loc.choosePaymentMethod!)),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              '${loc.requiredAmount}: $amount ${loc.price}',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            _paymentMethodCard(
              context,
              loc.shamCash!,
              Icons.account_balance_wallet,
              'sham_cash',
            ),
            _paymentMethodCard(
              context,
              loc.mtnCash!,
              Icons.phone_android,
              'mtn_cash',
            ),
            _paymentMethodCard(
              context,
              loc.syriatelCash!,
              Icons.phone_iphone,
              'syriatel_cash',
            ),
          ],
        ),
      ),
    );
  }

  Widget _paymentMethodCard(
    BuildContext context,
    String title,
    IconData icon,
    String method,
  ) {
    final loc = AppLocalizations.of(context);
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: ListTile(
        leading: Icon(icon,
            color: Theme.of(context).colorScheme.secondary, size: 32),
        title: Text(title),
        subtitle: Text('${loc.payAmount} $amount ${loc.price}'),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: () => _showPhoneDialog(context, method),
      ),
    );
  }
}
