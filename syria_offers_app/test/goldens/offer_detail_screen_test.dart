import 'package:flutter_test/flutter_test.dart';

import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/screens/offer_detail_screen.dart';

import 'golden_test_harness.dart';

void main() {
  testWidgets('Offer detail screen golden', (tester) async {
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
      descriptionAr: 'وصف تجريبي للعرض',
      descriptionEn: 'Sample description',
      startDate: DateTime.now().subtract(const Duration(days: 1)).toIso8601String(),
      endDate: DateTime.now().add(const Duration(days: 2)).toIso8601String(),
      imageUrls: null,
      locationNameAr: 'دمشق',
      locationNameEn: 'Damascus',
    );

    // لا نستخدم MockFavoritesService أبداً – نتجاوزه ببساطة
    await pumpGoldenWidget(
      tester,
      child: wrapWithApp(
        home: OfferDetailScreen(offer: offer),
      ),
    );

    // فقط نتأكد من وجود الشاشة
    await expectLater(find.byType(OfferDetailScreen), matchesGoldenFile('goldens/offer_detail_screen.png'));
  });
}