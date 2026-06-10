import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:syria_offers_app/screens/merchant/merchant_dashboard_screen.dart';
import 'package:syria_offers_app/services/api_service.dart';

import 'golden_test_harness.dart';

void main() {
  testWidgets('Merchant dashboard golden', (tester) async {
    final api = FakeApiService(
      dashboard: {
        'active_offers': 8,
        'pending_offers': 2,
        'total_bookings': 41,
        'total_views': 1280,
      },
    );

    await pumpGoldenWidget(
      tester,
      size: const Size(430, 900),
      child: wrapWithApp(
        home: const MerchantDashboardScreen(),
        providers: [ Provider<ApiService>.value(value: api) ],
      ),

    );

    await expectLater(find.byType(MerchantDashboardScreen), matchesGoldenFile('goldens/merchant_dashboard.png'));
  });
}
