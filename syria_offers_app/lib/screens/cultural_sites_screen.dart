import 'package:flutter/material.dart';
import 'package:syria_offers_app/models/cultural_site_model.dart';
import 'package:syria_offers_app/services/cultural_data_service.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/screens/cultural_site_detail_screen.dart';

class CulturalSitesScreen extends StatefulWidget {
  const CulturalSitesScreen({super.key});

  @override
  State<CulturalSitesScreen> createState() => _CulturalSitesScreenState();
}

class _CulturalSitesScreenState extends State<CulturalSitesScreen> {
  CulturalCategory? _selectedCategory;

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    final allSites = CulturalDataService.getSyrianCulturalSites();
    final filtered = _selectedCategory == null
        ? allSites
        : allSites.where((s) => s.category == _selectedCategory).toList();

    const categories = CulturalCategory.values;

    return Scaffold(
      appBar: AppBar(
        title: Text(loc.culturalSites!),
        elevation: 0,
      ),
      body: Column(
        children: [
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: Row(
              children: [
                _filterChip(loc.all!, null),
                const SizedBox(width: 8),
                ...categories.map((cat) => Padding(
                      padding: const EdgeInsets.only(left: 8),
                      child: _filterChip(cat.getLabel(context), cat),
                    ),),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: filtered.length,
              itemBuilder: (context, index) {
                final site = filtered[index];
                return _buildSiteCard(context, site, loc);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _filterChip(String label, CulturalCategory? category) {
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

  Widget _buildSiteCard(BuildContext context, CulturalSite site, AppLocalizations loc) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => CulturalSiteDetailScreen(site: site)),
          );
        },
        child: Row(
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.horizontal(right: Radius.circular(14)),
              child: Image.network(
                site.gallery.first,
                width: 120, height: 140, fit: BoxFit.cover,
                errorBuilder: (_, __, ___) => Container(
                  width: 120, height: 140, color: Colors.grey[200],
                  child: Icon(site.category.icon, color: Colors.grey[400], size: 40),
                ),
              ),
            ),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: site.unescoStatus ? Colors.amber.shade50 : Colors.grey[100],
                        borderRadius: BorderRadius.circular(6),
                        border: site.unescoStatus ? Border.all(color: Colors.amber.shade300) : null,
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          if (site.unescoStatus) ...[
                            Icon(Icons.shield, size: 14, color: Colors.amber[700]),
                            const SizedBox(width: 4),
                            const Text('UNESCO',
                                style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold,
                                    color: Color.fromARGB(255, 184, 134, 11),),),
                            const SizedBox(width: 8),
                          ],
                          Text(site.category.getLabel(context),
                              style: TextStyle(fontSize: 11, color: Colors.grey[600]),),
                        ],
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(site.getName(context),
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),),
                    if (site.officialTitle != null) ...[
                      const SizedBox(height: 2),
                      Text(site.officialTitle!,
                          style: TextStyle(fontSize: 12, color: Colors.grey[500]),),
                    ],
                    const SizedBox(height: 6),
                    Row(
                      children: [
                        Icon(Icons.location_on, size: 14, color: Colors.grey[400]),
                        const SizedBox(width: 4),
                        Text(
                          '${site.latitude.toStringAsFixed(4)}, ${site.longitude.toStringAsFixed(4)}',
                          style: TextStyle(fontSize: 11, color: Colors.grey[500]),
                        ),
                      ],
                    ),
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
}