import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:syria_offers_app/models/cultural_site_model.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

class CulturalSiteDetailScreen extends StatelessWidget {
  final CulturalSite site;
  const CulturalSiteDetailScreen({super.key, required this.site});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 280, pinned: true, elevation: 0,
            flexibleSpace: FlexibleSpaceBar(
              background: PageView.builder(
                itemCount: site.gallery.length,
                itemBuilder: (context, index) => Image.network(
                  site.gallery[index], fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => Container(
                      color: Colors.grey[300],
                      child: Icon(site.category.icon, size: 60, color: Colors.grey[500]),),
                ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (site.unescoStatus)
                    Container(
                      margin: const EdgeInsets.only(bottom: 12),
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: Colors.amber.shade50,
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(color: Colors.amber.shade300),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.shield, color: Colors.amber[700]),
                          const SizedBox(width: 6),
                          Text(loc.site!,
                              style: TextStyle(fontWeight: FontWeight.bold, color: Colors.amber[800]),),
                        ],
                      ),
                    ),
                  Text(site.getName(context),
                      style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold),),
                  if (site.officialTitle != null) ...[
                    const SizedBox(height: 4),
                    Text(site.officialTitle!, style: TextStyle(fontSize: 15, color: Colors.grey[600])),
                  ],
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.08),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(site.category.getLabel(context),
                            style: TextStyle(fontSize: 12, color: Theme.of(context).colorScheme.primary),),
                      ),
                      const SizedBox(width: 8),
                      Text(site.nameEn, style: TextStyle(fontSize: 13, color: Colors.grey[500])),
                    ],
                  ),
                  const SizedBox(height: 20),
                  Text(loc.historicalOverview!,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),),
                  const SizedBox(height: 8),
                  Text(site.getDescription(context),
                      style: TextStyle(fontSize: 15, height: 1.7, color: Colors.grey[800]),),
                  const SizedBox(height: 24),
                  Row(
                    children: [
                      if (site.openingHours != null)
                        Expanded(
                          child: _infoCard(context, Icons.access_time, loc.visitingHours!, site.openingHours!),
                        ),
                      if (site.entryFee != null) ...[
                        const SizedBox(width: 12),
                        Expanded(
                          child: _infoCard(context, Icons.confirmation_number, loc.entryFee!, site.entryFee!),
                        ),
                      ],
                    ],
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton.icon(
                      onPressed: () async {
                        final url = Uri.parse(
                            'https://www.google.com/maps?q=${site.latitude},${site.longitude}',);
                        if (await canLaunchUrl(url)) {
                          await launchUrl(url);
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
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 18, color: Theme.of(context).colorScheme.primary),
              const SizedBox(width: 6),
              Text(title, style: TextStyle(fontSize: 13, color: Colors.grey[600])),
            ],
          ),
          const SizedBox(height: 8),
          Text(value, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}