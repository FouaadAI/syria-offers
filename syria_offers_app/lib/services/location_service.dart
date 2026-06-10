import 'dart:math';

import 'package:syria_offers_app/models/offer.dart';

class LocationService {
  static double haversineDistanceKm({
    required double fromLat,
    required double fromLon,
    required double toLat,
    required double toLon,
  }) {
    const earthRadiusKm = 6371.0;
    double toRad(double d) => d * pi / 180.0;
    final dLat = toRad(toLat - fromLat);
    final dLon = toRad(toLon - fromLon);
    final a = sin(dLat / 2) * sin(dLat / 2) +
        cos(toRad(fromLat)) * cos(toRad(toLat)) * sin(dLon / 2) * sin(dLon / 2);
    final c = 2 * atan2(sqrt(a), sqrt(1 - a));
    return earthRadiusKm * c;
  }

  static List<Offer> sortOffersByDistance({
    required List<Offer> offers,
    required double userLat,
    required double userLon,
  }) {
    final sorted = List<Offer>.from(offers);
    sorted.sort((a, b) {
      final aDistance = (a.latitude == null || a.longitude == null)
          ? double.infinity
          : haversineDistanceKm(
              fromLat: userLat,
              fromLon: userLon,
              toLat: a.latitude!,
              toLon: a.longitude!,
            );
      final bDistance = (b.latitude == null || b.longitude == null)
          ? double.infinity
          : haversineDistanceKm(
              fromLat: userLat,
              fromLon: userLon,
              toLat: b.latitude!,
              toLon: b.longitude!,
            );
      return aDistance.compareTo(bDistance);
    });
    return sorted;
  }
}
