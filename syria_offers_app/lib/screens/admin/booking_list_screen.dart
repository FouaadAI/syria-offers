import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';

class BookingListScreen extends StatelessWidget {
  const BookingListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(title: Text(loc.manageBookings!)),
      body: FutureBuilder<List<dynamic>>(
        future:
            Provider.of<AdminApiService>(context, listen: false).getBookings(),
        builder: (context, snapshot) {
          if (!snapshot.hasData)
            return const Center(child: CircularProgressIndicator());
          return ListView.builder(
            itemCount: snapshot.data!.length,
            itemBuilder: (context, index) {
              final b = snapshot.data![index];
              return ListTile(
                title: Text('${loc.booking} #${b['id']}'),
                subtitle: Text(
                    '${loc.amountLabel}: ${b['total_price']} | ${loc.statusLabel}: ${b['status']}'),
                trailing: PopupMenuButton<String>(
                  onSelected: (status) async {
                    await Provider.of<AdminApiService>(context, listen: false)
                        .updateBookingStatus(b['id'], status);
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                        content: Text('${loc.statusChangedTo} $status')));
                    // Refresh is automatic as FutureBuilder will rebuild on setState, but we need to force refresh
                    // we’ll use a simple workaround: Navigator.pushReplacement
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                          builder: (_) => const BookingListScreen()),
                    );
                  },
                  itemBuilder: (_) => [
                    PopupMenuItem(
                        value: 'confirmed', child: Text(loc.confirm!)),
                    PopupMenuItem(value: 'cancelled', child: Text(loc.cancel!)),
                    PopupMenuItem(value: 'refunded', child: Text(loc.refund!)),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}
