import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/screens/admin/category_list_screen.dart';
import 'package:syria_offers_app/screens/admin/offer_list_screen.dart';
import 'package:syria_offers_app/screens/admin/booking_list_screen.dart';
import 'package:syria_offers_app/screens/auth/login_screen.dart';

class AdminDashboardScreen extends StatelessWidget {
  const AdminDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(
        title: Text(loc.adminDashboardTitle!),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await Provider.of<AuthService>(context, listen: false).logout();
              if (context.mounted) {
                await Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (_) => const LoginScreen()),
                );
              }
            },
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future:
            Provider.of<AdminApiService>(context, listen: false).getDashboard(),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final d = snapshot.data!;
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
                        context,
                        loc.activeOffers!,
                        d['active_offers'].toString(),
                        Theme.of(context).colorScheme.primary),
                    _statCard(
                        context,
                        loc.totalBookings!,
                        d['total_bookings'].toString(),
                        Theme.of(context).colorScheme.primary),
                    _statCard(
                        context,
                        loc.revenue!,
                        '${d['total_revenue']} ${loc.price}',
                        Theme.of(context).colorScheme.secondary),
                    _statCard(
                        context,
                        loc.flashDealsShort!,
                        d['flash_deals'].toString(),
                        Theme.of(context).colorScheme.secondary),
                    _statCard(
                        context,
                        loc.needsApproval!,
                        d['pending_approval'].toString(),
                        Theme.of(context).colorScheme.primary),
                    Container(),
                  ],
                ),
                const SizedBox(height: 24),
                _adminButton(context, loc.manageCategories!, Icons.category,
                    const CategoryListScreen()),
                _adminButton(context, loc.manageOffers!, Icons.local_offer,
                    const OfferListScreen()),
                _adminButton(context, loc.manageBookings!, Icons.book_online,
                    const BookingListScreen()),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _statCard(
      BuildContext context, String title, String value, Color color) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isSmallScreen = screenWidth <= 360;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              value,
              style: TextStyle(
                fontSize: isSmallScreen ? 22 : 30,
                color: color,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              title,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: isSmallScreen ? 12 : 14,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _adminButton(
      BuildContext context, String title, IconData icon, Widget screen) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: ListTile(
        leading: Icon(icon, color: Theme.of(context).colorScheme.secondary),
        title: Text(title),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: () =>
            Navigator.push(context, MaterialPageRoute(builder: (_) => screen)),
      ),
    );
  }
}
