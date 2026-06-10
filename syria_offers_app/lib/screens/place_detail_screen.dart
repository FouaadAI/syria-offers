import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:syria_offers_app/models/place.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

class PlaceDetailScreen extends StatelessWidget {
  final Place place;
  const PlaceDetailScreen({super.key, required this.place});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 280, pinned: true, elevation: 0,
            flexibleSpace: FlexibleSpaceBar(
              background: place.galleryUrls.isNotEmpty
                  ? PageView.builder(
                      itemCount: place.galleryUrls.length,
                      itemBuilder: (context, index) => Image.network(place.galleryUrls[index], fit: BoxFit.cover,
                          errorBuilder: (_, __, ___) => Container(
                              color: Colors.grey[300],
                              child: Icon(place.category.icon, size: 60, color: Colors.grey[500]),),),
                    )
                  : Container(color: Colors.grey[300], child: Icon(place.category.icon, size: 80, color: Colors.grey[500])),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(place.getName(context), style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
                  if (place.nameEn.toUpperCase() != place.nameAr.toUpperCase()) ...[
                    const SizedBox(height: 4),
                    Text(place.nameEn, style: TextStyle(fontSize: 16, color: Colors.grey[600])),
                  ],
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.08),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(place.category.getLabel(context),
                        style: TextStyle(fontSize: 12, color: Theme.of(context).colorScheme.primary),),
                  ),
                  const SizedBox(height: 20),
                  Text(place.getDescription(context),
                      style: TextStyle(fontSize: 15, height: 1.7, color: Colors.grey[800]),),
                  const SizedBox(height: 24),
                  if (place.openingHours != null)
                    _infoCard(context, Icons.access_time, 'أوقات العمل', place.openingHours!),
                  if (place.phone != null)
                    _infoCard(context, Icons.phone, 'رقم الهاتف', place.phone!),
                  if (place.website != null)
                    _infoCard(context, Icons.language, 'الموقع الإلكتروني', place.website!),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      onPressed: () async {
                        final lat = place.latitude;
                        final lng = place.longitude;
                        final label = Uri.encodeComponent(place.nameAr);
                        try {
                          final geoUri = Uri.parse('geo:$lat,$lng?q=$label');
                          await launchUrl(geoUri, mode: LaunchMode.externalApplication);
                          return;
                        } catch (_) {}
                        try {
                          final mapsUri = Uri.parse('https://www.google.com/maps/search/?api=1&query=$lat,$lng');
                          await launchUrl(mapsUri, mode: LaunchMode.externalApplication);
                        } catch (_) {
                          if (context.mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text(loc.openInMaps!)),
                            );
                          }
                        }
                      },
                      icon: const Icon(Icons.map),
                      label: Text(loc.openInMaps!),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        side: BorderSide(color: Theme.of(context).colorScheme.primary),
                        foregroundColor: Theme.of(context).colorScheme.primary,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _infoCard(BuildContext context, IconData icon, String title, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Icon(icon, size: 20, color: Theme.of(context).colorScheme.primary),
        const SizedBox(width: 10),
        Expanded(
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(title, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
            const SizedBox(height: 2),
            Text(value, style: TextStyle(fontSize: 15, color: Colors.grey[700])),
          ],),
        ),
      ],),
    );
  }
}