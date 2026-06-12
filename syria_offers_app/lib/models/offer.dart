import 'dart:math';
import 'package:flutter/widgets.dart';

class Offer {
  final int id;
  final String titleAr;
  final String titleEn;
  final String? descriptionAr;
  final String? descriptionEn;
  final double originalPrice;
  final double offerPrice;
  final String? startDate;
  final String? endDate;
  final List<String>? imageUrls;
  final int categoryId;
  final bool isActive;
  final bool isFlash;               // <-- إضافة هذه الخاصية
  final int? flashDiscountPercent;
  bool approved;
  final double? latitude;
  final double? longitude;
  final String? locationNameAr;
  final String? locationNameEn;
  final DateTime? purchaseTimestamp;

  Offer({
    required this.id,
    required this.titleAr,
    required this.titleEn,
    this.descriptionAr,
    this.descriptionEn,
    required this.originalPrice,
    required this.offerPrice,
    this.startDate,
    this.endDate,
    this.imageUrls,
    required this.categoryId,
    required this.isActive,
    required this.isFlash,           // <-- إضافة هذه الخاصية
    this.flashDiscountPercent,
    required this.approved,
    this.latitude,
    this.longitude,
    this.locationNameAr,
    this.locationNameEn,
    this.purchaseTimestamp,
  });

  factory Offer.fromJson(Map<String, dynamic> json) {
    return Offer(
      id: json['id'],
      titleAr: json['title_ar'] ?? '',
      titleEn: json['title_en'] ?? '',
      descriptionAr: json['description_ar'],
      descriptionEn: json['description_en'],
      originalPrice: (json['original_price'] as num).toDouble(),
      offerPrice: (json['offer_price'] as num).toDouble(),
      startDate: json['start_date'],
      endDate: json['end_date'],
      imageUrls: json['image_urls'] != null
          ? List<String>.from(json['image_urls'])
          : null,
      categoryId: json['category_id'],
      isActive: json['is_active'],
      isFlash: json['is_flash'] ?? false,  // <-- افتراضيًا false
      flashDiscountPercent: json['flash_discount_percent'],
      approved: json['approved'] ?? false,  // <-- افتراضيًا false
      latitude: json['latitude'] != null ? (json['latitude'] as num).toDouble() : null,
      longitude: json['longitude'] != null ? (json['longitude'] as num).toDouble() : null,
      locationNameAr: json['location_name_ar'],
      locationNameEn: json['location_name_en'],
      purchaseTimestamp: json['purchase_timestamp'] != null ? DateTime.tryParse(json['purchase_timestamp']) : null,
    );
  }

  String? preferredLocation([String locale = 'ar']) {
    final isEn = locale.toLowerCase().startsWith('en');
    if (isEn) return locationNameEn ?? locationNameAr;
    return locationNameAr ?? locationNameEn;
  }

  String get displayLocation => locationNameAr ?? locationNameEn ?? '';

  String getDisplayTitle(BuildContext context) {
    final code = Localizations.localeOf(context).languageCode;
    if (code == 'ar') return titleAr.isNotEmpty ? titleAr : titleEn;
    return titleEn.isNotEmpty ? titleEn : titleAr;
  }

  String getDisplayLocation(BuildContext context) {
    final code = Localizations.localeOf(context).languageCode;
    if (code == 'ar') return locationNameAr ?? locationNameEn ?? '';
    return locationNameEn ?? locationNameAr ?? '';
  }

  String getDisplayDescription(BuildContext context) {
    final code = Localizations.localeOf(context).languageCode;
    if (code == 'ar') return descriptionAr ?? descriptionEn ?? '';
    return descriptionEn ?? descriptionAr ?? '';
  }

  // returns distance in kilometers; returns double.infinity if coords are missing
  double distanceTo(double userLat, double userLng) {
    if (latitude == null || longitude == null) return double.infinity;
    const double R = 6371.0; // Earth radius in km
    double toRad(double deg) => deg * pi / 180.0;
    final dLat = toRad(latitude! - userLat);
    final dLon = toRad(longitude! - userLng);
    final a = sin(dLat / 2) * sin(dLat / 2) +
        cos(toRad(userLat)) * cos(toRad(latitude!)) * sin(dLon / 2) * sin(dLon / 2);
    final c = 2 * atan2(sqrt(a), sqrt(1 - a));
    return R * c; // kilometers
  }

  String distanceText(double userLat, double userLng) {
    final km = distanceTo(userLat, userLng);
    if (km == double.infinity) return '';
    if (km < 1) return '${(km * 1000).round()} m';
    return '${km.toStringAsFixed(1)} km';
  }

  // Placeholder refund logic: refundable if purchase exists and is at least 1 hour before now
  bool get isRefundable {
    if (purchaseTimestamp == null) return false;
    return DateTime.now().isBefore(purchaseTimestamp!.subtract(const Duration(hours: 1)));
  }
}
