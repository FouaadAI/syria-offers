import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:syria_offers_app/models/category.dart';
import 'package:syria_offers_app/widgets/category_card.dart';

import 'golden_test_harness.dart';

void main() {
  testWidgets('Category card golden', (tester) async {
    final category = Category(
      id: 1,
      nameAr: 'مطاعم',
      nameEn: 'Restaurants',
      iconUrl: null,
      sortOrder: 1,
    );

    await pumpGoldenWidget(
      tester,
      size: const Size(180, 180),
      child: wrapWithApp(
        home: Scaffold(
          body: Center(
            child: SizedBox(
              width: 160, height: 160,
              child: CategoryCard(category: category, onTap: () {}),
            ),
          ),
        ),
      ),
    );

    await expectLater(find.byType(CategoryCard), matchesGoldenFile('goldens/category_card.png'));
  });
}
