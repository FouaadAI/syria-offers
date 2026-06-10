import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/widgets/offer_card.dart';

import 'golden_test_harness.dart';

void main() {
  testWidgets('Offer card golden', (tester) async {
    final offer = Offer(
      id: 1,
      titleAr: 'عرض تجريبي',
      titleEn: 'Test Offer',
      originalPrice: 150,
      offerPrice: 100,
      categoryId: 1,
      isActive: true,
      isFlash: false,
      approved: true,
      descriptionAr: 'وصف العرض',
      descriptionEn: 'Offer description',
      startDate: DateTime.now().subtract(const Duration(days: 1)).toIso8601String(),
      endDate: DateTime.now().add(const Duration(days: 2)).toIso8601String(),
      imageUrls: null,
      locationNameAr: 'دمشق',
      locationNameEn: 'Damascus',
    );

    await pumpGoldenWidget(
      tester,
      size: const Size(390, 420),
      child: wrapWithApp(
        home: Scaffold(
          body: Padding(
            padding: const EdgeInsets.all(16),
            child: OfferCard(offer: offer),
          ),
        ),
      ),

    );

    await expectLater(find.byType(OfferCard), matchesGoldenFile('goldens/offer_card.png'));
  });
}
