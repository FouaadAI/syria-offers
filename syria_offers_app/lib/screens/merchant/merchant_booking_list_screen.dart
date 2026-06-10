import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/services/auth_service.dart';

class MerchantBookingListScreen extends StatefulWidget {
  const MerchantBookingListScreen({super.key});

  @override
  State<MerchantBookingListScreen> createState() =>
      _MerchantBookingListScreenState();
}

class _MerchantBookingListScreenState extends State<MerchantBookingListScreen> {
  late Future<List<dynamic>> _bookingsFuture;

  @override
  void initState() {
    super.initState();
    _loadBookings();
  }

  void _loadBookings() {
    _bookingsFuture =
        Provider.of<ApiService>(context, listen: false).getMyMerchantBookings();
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(
        title: Text(loc.merchantBookingsTitle!),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await Provider.of<AuthService>(context, listen: false).logout();
              if (context.mounted) {
                Navigator.pushReplacementNamed(context, '/home');
              }
            },
          ),
        ],
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _bookingsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('${loc.error}: ${snapshot.error}'));
          }
          final bookings = snapshot.data ?? [];
          if (bookings.isEmpty) {
            return Center(child: Text(loc.noBookingsYet!));
          }
          return ListView.builder(
            itemCount: bookings.length,
            itemBuilder: (context, index) {
              final b = bookings[index];
              return Card(
                margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                child: ListTile(
                  title: Text('${loc.bookingNumber} #${b['id']}'),
                  subtitle: Text(
                    '${loc.amount}: ${b['total_price']} ${loc.price} - ${loc.status}: ${b['status']}',
                  ),
                  trailing: Text(
                    b['booked_at'] != null
                        ? DateFormat('yyyy/MM/dd').format(
                            DateTime.parse(b['booked_at']),
                          )
                        : '',
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
