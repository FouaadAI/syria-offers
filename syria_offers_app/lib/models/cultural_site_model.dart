import 'package:flutter/material.dart';

enum CulturalCategory {
  unescoSite,
  museum,
  historicalMarket,
  religiousSite,
}

extension CulturalCategoryExtension on CulturalCategory {
  String get labelAr {
    switch (this) {
      case CulturalCategory.unescoSite:
        return 'مواقع التراث العالمي';
      case CulturalCategory.museum:
        return 'متاحف';
      case CulturalCategory.historicalMarket:
        return 'أسواق تاريخية';
      case CulturalCategory.religiousSite:
        return 'مواقع دينية';
    }
  }

  String get labelEn {
    switch (this) {
      case CulturalCategory.unescoSite:
        return 'UNESCO Sites';
      case CulturalCategory.museum:
        return 'Museums';
      case CulturalCategory.historicalMarket:
        return 'Historical Markets';
      case CulturalCategory.religiousSite:
        return 'Religious Sites';
    }
  }

  IconData get icon {
    switch (this) {
      case CulturalCategory.unescoSite:
        return Icons.account_balance;
      case CulturalCategory.museum:
        return Icons.museum;
      case CulturalCategory.historicalMarket:
        return Icons.storefront;
      case CulturalCategory.religiousSite:
        return Icons.church;
    }
  }

  String getLabel(BuildContext context) {
    final lang = Localizations.localeOf(context).languageCode;
    return lang == 'ar' ? labelAr : labelEn;
  }
}

class CulturalSite {
  final String id;
  final String nameAr;
  final String nameEn;
  final String? officialTitle;
  final CulturalCategory category;
  final String descriptionAr;
  final String descriptionEn;
  final List<String> gallery;
  final double latitude;
  final double longitude;
  final String? openingHours;
  final String? entryFee;
  final bool unescoStatus;

  const CulturalSite({
    required this.id,
    required this.nameAr,
    required this.nameEn,
    this.officialTitle,
    required this.category,
    required this.descriptionAr,
    required this.descriptionEn,
    required this.gallery,
    required this.latitude,
    required this.longitude,
    this.openingHours,
    this.entryFee,
    required this.unescoStatus,
  });

  String getName(BuildContext context) {
    final lang = Localizations.localeOf(context).languageCode;
    return lang == 'ar' ? nameAr : nameEn;
  }

  String getDescription(BuildContext context) {
    final lang = Localizations.localeOf(context).languageCode;
    return lang == 'ar' ? descriptionAr : descriptionEn;
  }
}