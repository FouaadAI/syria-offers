import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:syria_offers_app/screens/payment/payment_screen.dart';

class BookingConfirmationScreen extends StatelessWidget {
  final String bookingCode;
  final String userName;
  final String userPhone;
  final DateTime bookedAt;
  final int quantity;
  final double totalPrice;
  final int bookingId; // ✅ جديد: مُعرف الحجز القادم من الخادم

  const BookingConfirmationScreen({
    super.key,
    required this.bookingCode,
    required this.userName,
    required this.userPhone,
    required this.bookedAt,
    required this.quantity,
    required this.totalPrice,
    required this.bookingId, // ✅ جديد
  });

  @override
  Widget build(BuildContext context) {
    final currencyFormat = NumberFormat.currency(
      symbol: 'ل.س',
      decimalDigits: 0,
      locale: 'ar',
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('تم الحجز بنجاح'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.check_circle, size: 100, color: Theme.of(context).colorScheme.secondary),
              const SizedBox(height: 24),
              const Text(
                'شكراً لك! تم تأكيد حجزك',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      _infoRow('الاسم', userName),
                      _infoRow('رقم الهاتف', userPhone),
                      _infoRow('تاريخ الحجز',
                          DateFormat.yMMMd('ar').format(bookedAt),),
                      _infoRow('العدد', quantity.toString()),
                      _infoRow('المبلغ الإجمالي',
                          currencyFormat.format(totalPrice),),
                      const SizedBox(height: 8),
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          'رمز الحجز: $bookingCode',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),
              // زر العودة للرئيسية (مُصلح)
              ElevatedButton(
                onPressed: () {
                  // يعود إلى الشاشة الرئيسية ويمسح كل ما قبلها
                  Navigator.pushNamedAndRemoveUntil(
                      context, '/home', (route) => false,);
                },
                child: const Text('العودة للرئيسية'),
              ),
              const SizedBox(height: 12),
              // زر الدفع (يستخدم bookingId الحقيقي)
              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => PaymentScreen(
                        bookingId: bookingId, // ✅ المُعرف الحقيقي
                        amount: totalPrice,
                      ),
                    ),
                  );
                },
                child: const Text('ادفع الآن'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _infoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
          Text(value),
        ],
      ),
    );
  }
}
