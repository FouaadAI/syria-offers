import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:syria_offers_app/models/category.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/screens/home_screen.dart';
import 'package:syria_offers_app/services/api_service.dart';

import 'golden_test_harness.dart';

void main() {
  testWidgets('Home screen golden', (tester) async {
    final api = FakeApiService(
      categories: [
        Category(id: 1, nameAr: 'مطاعم', nameEn: 'Restaurants', iconUrl: null, sortOrder: 1),
        Category(id: 2, nameAr: 'حدائق', nameEn: 'Parks', iconUrl: null, sortOrder: 2),
      ],
      offers: [
        Offer(
          id: 1,
          titleAr: 'عرض تجريبي',
          titleEn: 'Test Offer',
          originalPrice: 150,
          offerPrice: 100,
          categoryId: 1,
          isActive: true,
          isFlash: false,
          approved: true,
          startDate: DateTime.now().subtract(const Duration(days: 1)).toIso8601String(),
          endDate: DateTime.now().add(const Duration(days: 2)).toIso8601String(),
          imageUrls: null,
        ),
      ],
    );

    await pumpGoldenWidget(
      tester,
      size: const Size(390, 844),
      child: wrapWithApp(
        home: const HomeScreen(),
        providers: [ Provider<ApiService>.value(value: api) ],
      ),
    );

    await expectLater(find.byType(HomeScreen), matchesGoldenFile('goldens/home_screen.png'));
  });
}
