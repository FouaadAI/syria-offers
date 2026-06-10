import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/screens/merchant/merchant_offer_list_screen.dart';
import 'package:syria_offers_app/screens/merchant/merchant_booking_list_screen.dart';
// أو أي شاشة تسجيل

class MerchantDashboardScreen extends StatefulWidget {
  const MerchantDashboardScreen({super.key});

  @override
  State<MerchantDashboardScreen> createState() =>
      _MerchantDashboardScreenState();
}

class _MerchantDashboardScreenState extends State<MerchantDashboardScreen> {
  late Future<Map<String, dynamic>> _dashboardFuture;

  @override
  void initState() {
    super.initState();
    _loadDashboard();
  }

  void _loadDashboard() {
    _dashboardFuture =
        Provider.of<ApiService>(context, listen: false).getMerchantDashboard();
    setState(() {}); // rebuil
  }

  Future<void> _logout() async {
    await Provider.of<AuthService>(context, listen: false).logout();
    if (mounted) {
      Navigator.pushReplacementNamed(
          context, '/home'); // أو إلى شاشة تسجيل الدخول
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(
        title: Text(loc.merchantDashboardTitle!),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _dashboardFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('${loc.error}: ${snapshot.error}'));
          }
          final data = snapshot.data!;
          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                GridView.count(
                  crossAxisCount: 2,
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  children: [
                    _statCard(
                        loc.activeOffers!,
                        data['active_offers'].toString(),
                        Theme.of(context).colorScheme.primary),
                    _statCard(loc.pending!, data['pending_offers'].toString(),
                        Theme.of(context).colorScheme.secondary),
                    _statCard(
                        loc.totalBookings!,
                        data['total_bookings'].toString(),
                        Theme.of(context).colorScheme.primary),
                    _statCard(loc.views!, data['total_views'].toString(),
                        Theme.of(context).colorScheme.secondary),
                  ],
                ),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      await Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (_) => const MerchantOfferListScreen()),
                      );
                      _loadDashboard();
                    },
                    icon: const Icon(Icons.local_offer),
                    label: Text(loc.manageMyOffers!),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () async {
                      await Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (_) => const MerchantBookingListScreen()),
                      );
                    },
                    icon: const Icon(Icons.book_online),
                    label: Text(loc.trackBookings!),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _statCard(String title, String value, Color color) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(value,
                style: TextStyle(
                    fontSize: 28, color: color, fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            Text(title, textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}
