import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:syria_offers_app/screens/admin/admin_dashboard_screen.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';

import 'golden_test_harness.dart';

void main() {
  testWidgets('Admin dashboard golden', (tester) async {
    final adminApi = FakeAdminApiService(
      dashboard: {
        'active_offers': 12,
        'total_bookings': 84,
        'total_revenue': 154000,
        'flash_deals': 3,
        'pending_approval': 5,
      },
    );

    await pumpGoldenWidget(
      tester,
      size: const Size(430, 900),
      child: wrapWithApp(
        home: const AdminDashboardScreen(),
        providers: [ Provider<AdminApiService>.value(value: adminApi) ],
      ),
    );  

    await expectLater(find.byType(AdminDashboardScreen), matchesGoldenFile('goldens/admin_dashboard.png'));
  });
}
