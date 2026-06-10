import 'package:flutter/material.dart';
import 'package:syria_offers_app/models/place.dart';
import 'package:syria_offers_app/services/tourist_data_service.dart';
import 'package:syria_offers_app/services/location_service.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/screens/place_detail_screen.dart';

class DiscoverScreen extends StatefulWidget {
  final double? userLat;
  final double? userLng;
  const DiscoverScreen({super.key, this.userLat, this.userLng});

  @override
  State<DiscoverScreen> createState() => _DiscoverScreenState();
}

class _DiscoverScreenState extends State<DiscoverScreen> {
  PlaceCategory? _selectedCategory;

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    final allPlaces = TouristDataService.getAllPlaces();
    final filtered = _selectedCategory == null
        ? allPlaces
        : allPlaces.where((p) => p.category == _selectedCategory).toList();

    return Column(
      children: [
        SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          child: Row(
            children: [
              _buildChip(loc.all!, null),
              const SizedBox(width: 8),
              ...PlaceCategory.values.map((cat) => Padding(
                    padding: const EdgeInsets.only(left: 8),
                    child: _buildChip(cat.getLabel(context), cat),
                  ),),
            ],
          ),
        ),
        Expanded(
          child: filtered.isEmpty
              ? Center(child: Text(loc.noPlaces!))
              : ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: filtered.length,
                  itemBuilder: (context, index) {
                    final place = filtered[index];
                    return _PlaceCard(
                      place: place,
                      userLat: widget.userLat,
                      userLng: widget.userLng,
                    );
                  },
                ),
        ),
      ],
    );
  }

  Widget _buildChip(String label, PlaceCategory? category) {
    final selected = _selectedCategory == category;
    return FilterChip(
      label: Text(label),
      selected: selected,
      onSelected: (_) => setState(() => _selectedCategory = category),
      selectedColor: Theme.of(context).colorScheme.primary.withValues(alpha: 0.15),
      checkmarkColor: Theme.of(context).colorScheme.primary,
      labelStyle: TextStyle(
        color: selected ? Theme.of(context).colorScheme.primary : Colors.grey[700],
        fontWeight: selected ? FontWeight.bold : FontWeight.normal,
      ),
    );
  }
}

class _PlaceCard extends StatelessWidget {
  final Place place;
  final double? userLat;
  final double? userLng;
  const _PlaceCard({required this.place, this.userLat, this.userLng});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    String? distanceText;
    if (userLat != null && userLng != null) {
      final km = LocationService.haversineDistanceKm(
        fromLat: userLat!, fromLon: userLng!,
        toLat: place.latitude, toLon: place.longitude,
      );
      distanceText = km < 1 ? '${(km * 1000).round()} م' : km < 100 ? '${km.toStringAsFixed(1)} ${loc.distance}' : '${km.round()} ${loc.distance}';
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => PlaceDetailScreen(place: place))),
        child: Row(
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.horizontal(right: Radius.circular(14)),
              child: place.galleryUrls.isNotEmpty
                  ? Image.network(place.galleryUrls.first, width: 120, height: 140, fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => _placeholder(),)
                  : _placeholder(),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(color: Colors.grey[100], borderRadius: BorderRadius.circular(6)),
                      child: Text(place.category.getLabel(context),
                          style: TextStyle(fontSize: 11, color: Colors.grey[600]),),
                    ),
                    const SizedBox(height: 8),
                    Text(place.getName(context),
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        maxLines: 1, overflow: TextOverflow.ellipsis,),
                    const SizedBox(height: 4),
                    _buildInfoRow(context, distanceText),
                  ],
                ),
              ),
            ),
            const Padding(
              padding: EdgeInsets.only(left: 8, right: 8),
              child: Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(BuildContext context, String? dist) {
    final chips = <Widget>[];
    if (place.openingHours != null) {
      chips.add(Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(Icons.access_time, size: 14, color: Colors.grey[400]),
        const SizedBox(width: 4),
        Flexible(child: Text(place.openingHours!, style: TextStyle(fontSize: 12, color: Colors.grey[500]), overflow: TextOverflow.ellipsis)),
      ],),);
    }
    if (dist != null) {
      chips.add(Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(Icons.location_on, size: 14, color: Colors.grey[400]),
        const SizedBox(width: 4),
        Text(dist, style: TextStyle(fontSize: 12, color: Colors.grey[500])),
      ],),);
    }
    if (chips.isEmpty) return const SizedBox.shrink();
    return Wrap(spacing: 12, runSpacing: 4, children: chips);
  }

  Widget _placeholder() => Container(
      width: 120, height: 140, color: Colors.grey[200],
      child: Icon(place.category.icon, color: Colors.grey[400], size: 40),);
}