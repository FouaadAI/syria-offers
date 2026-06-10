import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/services/favorites_service.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/screens/offer_detail_screen.dart';

class FavoritesScreen extends StatefulWidget {
  const FavoritesScreen({super.key});

  @override
  State<FavoritesScreen> createState() => _FavoritesScreenState();
}

class _FavoritesScreenState extends State<FavoritesScreen> {
  List<Offer> _favorites = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadFavorites();
  }

  Future<void> _loadFavorites() async {
    final favService = FavoritesService();
    final apiService = Provider.of<ApiService>(context, listen: false);
    try {
      final ids = await favService.listFavorites();
      final allOffers = await apiService.getOffers();
      setState(() {
        _favorites = allOffers.where((o) => ids.contains(o.id)).toList();
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(loc.favorites!),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: loc.refresh,
            onPressed: () {
              setState(() => _isLoading = true);
              _loadFavorites();
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _favorites.isEmpty
              ? Center(child: Text(loc.noFavorites!))
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _favorites.length,
                  itemBuilder: (context, index) {
                    final offer = _favorites[index];
                    // Titel und Preis je nach Sprache
                    final title = Localizations.localeOf(context).languageCode == 'ar'
                        ? offer.titleAr
                        : offer.titleEn;
                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                        leading: offer.imageUrls != null && offer.imageUrls!.isNotEmpty
                            ? Image.network(offer.imageUrls!.first, width: 60, fit: BoxFit.cover)
                            : const Icon(Icons.image, size: 60),
                        title: Text(title),
                        subtitle: Text('${offer.offerPrice} ${loc.price}'),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete_outline, color: Colors.red),
                          onPressed: () async {
                            await FavoritesService().removeFavorite(offer.id);
                            setState(() {
                              _favorites.removeAt(index);
                            });
                          },
                        ),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (_) => OfferDetailScreen(offer: offer)),
                          );
                        },
                      ),
                    );
                  },
                ),
    );
  }
}