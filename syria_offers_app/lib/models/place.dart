import 'package:flutter/material.dart';

enum PlaceCategory {
  hotel,
  restaurant,
  park,
  activity,
  event,
  cinema,
}

extension PlaceCategoryExtension on PlaceCategory {
  String get labelAr {
    switch (this) {
      case PlaceCategory.hotel:     return 'فنادق';
      case PlaceCategory.restaurant: return 'مطاعم';
      case PlaceCategory.park:       return 'منتزهات';
      case PlaceCategory.activity:   return 'أنشطة';
      case PlaceCategory.event:      return 'فعاليات';
      case PlaceCategory.cinema:     return 'سينما';
    }
  }
  String get labelEn {
    switch (this) {
      case PlaceCategory.hotel:     return 'Hotels';
      case PlaceCategory.restaurant: return 'Restaurants';
      case PlaceCategory.park:       return 'Parks';
      case PlaceCategory.activity:   return 'Activities';
      case PlaceCategory.event:      return 'Events';
      case PlaceCategory.cinema:     return 'Cinema';
    }
  }
  IconData get icon {
    switch (this) {
      case PlaceCategory.hotel:     return Icons.hotel;
      case PlaceCategory.restaurant: return Icons.restaurant;
      case PlaceCategory.park:       return Icons.park;
      case PlaceCategory.activity:   return Icons.hiking;
      case PlaceCategory.event:      return Icons.event;
      case PlaceCategory.cinema:     return Icons.movie;
    }
  }

  String getLabel(BuildContext context) {
    final lang = Localizations.localeOf(context).languageCode;
    return lang == 'ar' ? labelAr : labelEn;
  }
}

class Place {
  final String id;
  final String nameAr;
  final String nameEn;
  final String? officialTitle;
  final PlaceCategory category;
  final String descriptionAr;
  final String descriptionEn;
  final List<String> galleryUrls;
  final List<String> galleryAssets;
  final double latitude;
  final double longitude;
  final String? openingHours;
  final String? phone;
  final String? website;

  const Place({
    required this.id,
    required this.nameAr,
    required this.nameEn,
    this.officialTitle,
    required this.category,
    required this.descriptionAr,
    required this.descriptionEn,
    required this.galleryUrls,
    this.galleryAssets = const [],
    required this.latitude,
    required this.longitude,
    this.openingHours,
    this.phone,
    this.website,
  });

  String getName(BuildContext context) {
    final lang = Localizations.localeOf(context).languageCode;
    return lang == 'ar' ? nameAr : nameEn;
  }

  String getDescription(BuildContext context) {
    final lang = Localizations.localeOf(context).languageCode;
    return lang == 'ar' ? descriptionAr : descriptionEn;
  }

  List<ImageProvider> get imageProviders {
    final list = <ImageProvider>[];
    for (final asset in galleryAssets) {
      list.add(AssetImage(asset));
    }
    for (final url in galleryUrls) {
      list.add(NetworkImage(url));
    }
    return list;
  }
}