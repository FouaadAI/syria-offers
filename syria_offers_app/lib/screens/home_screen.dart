import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/models/category.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/widgets/flash_deal_card.dart';
import 'package:syria_offers_app/widgets/offer_card.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:syria_offers_app/screens/offer_detail_screen.dart';
import 'package:syria_offers_app/screens/admin/admin_login_screen.dart';
import 'package:syria_offers_app/screens/favorites_screen.dart';
import 'package:syria_offers_app/services/auth_service.dart';
import 'package:syria_offers_app/services/location_service.dart';
import 'package:syria_offers_app/screens/discover_screen.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late Future<List<Category>> _categoriesFuture;

  double? _userLat;
  double? _userLng;
  List<Offer> _offers = [];
  String _search = '';
  int? _selectedCategoryId;
  final TextEditingController _searchController = TextEditingController();
  int _currentIndex = 0;
  int _userId = 1;

  @override
  void initState() {
    super.initState();
    _loadUserId();
    _categoriesFuture =
        Provider.of<ApiService>(context, listen: false).getCategories();
    _loadOffers();
    _getUserLocation();
  }

  Future<void> _loadUserId() async {
    final authService = Provider.of<AuthService>(context, listen: false);
    final token = await authService.getToken();
    if (token != null) {
      try {
        final parts = token.split('.');
        if (parts.length == 3) {
          final payload = json.decode(
              utf8.decode(base64Url.decode(base64.normalize(parts[1]))),);
          final sub = payload['sub'];
          if (sub != null) {
            _userId = int.tryParse(sub.toString()) ?? 1;
          }
        }
      } catch (_) {
        // fallback to guest
      }
    }
    setState(() {}); // update UI if needed
  }

  Future<void> _loadOffers() async {
    try {
      final list =
          await Provider.of<ApiService>(context, listen: false).getOffers();
      setState(() => _offers = list);
    } catch (_) {}
  }

  Future<void> _getUserLocation() async {
    try {
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.always ||
          permission == LocationPermission.whileInUse) {
        final pos = await Geolocator.getCurrentPosition();
        setState(() {
          _userLat = pos.latitude;
          _userLng = pos.longitude;
        });
      }
    } catch (e) {
      // ignore
    }
  }

  @override
  Widget build(BuildContext context) {
    final filtered = _offers.where((o) {
      if (_selectedCategoryId != null && o.categoryId != _selectedCategoryId) {
        return false;
      }
      if (_search.isEmpty) return true;
      final q = _search.toLowerCase();
      return (o.titleAr.toLowerCase().contains(q) ||
          o.titleEn.toLowerCase().contains(q) ||
          (o.locationNameAr ?? '').toLowerCase().contains(q) ||
          (o.locationNameEn ?? '').toLowerCase().contains(q));
    }).toList();

    if (_userLat != null && _userLng != null) {
      final sorted = LocationService.sortOffersByDistance(
        offers: filtered,
        userLat: _userLat!,
        userLon: _userLng!,
      );
      filtered
        ..clear()
        ..addAll(sorted);
    }

    final loc = AppLocalizations.of(context);
    String catName(Category c) {
      final lang = Localizations.localeOf(context).languageCode;
      return lang == 'ar' ? c.nameAr : c.nameEn;
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Offria'),
        actions: [
          IconButton(
            icon: const Icon(Icons.account_balance),
            tooltip: loc.culturalSites,
            onPressed: () => Navigator.pushNamed(context, '/cultural'),
          ),
          IconButton(
            icon: const Icon(Icons.chat),
            tooltip: loc.chat,
            onPressed: () => Navigator.pushNamed(context, '/chat'),
          ),
          // Favoriten
          IconButton(
            icon: const Icon(Icons.favorite_border),
            tooltip: loc.favorites,
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const FavoritesScreen()),
            ),
          ),
          // Admin
          IconButton(
            icon: const Icon(Icons.admin_panel_settings),
            tooltip: loc.admin,
            onPressed: () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (_) => AdminLoginScreen()),);
            },
          ),
          // Logout
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: loc.logout,
            onPressed: () async {
              await Provider.of<AuthService>(context, listen: false).logout();
              if (context.mounted) {
                Navigator.pushReplacementNamed(context, '/');
              }
            },
          ),
        ],
      ),
      body: _currentIndex == 0
          ? DiscoverScreen(userLat: _userLat, userLng: _userLng)
          : _buildOffersTab(filtered, loc, catName),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        selectedItemColor: Theme.of(context).colorScheme.primary,
        items: [
          BottomNavigationBarItem(
            icon: const Icon(Icons.explore),
            label: loc.discover,
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.local_offer),
            label: loc.offers,
          ),
        ],
      ),
    );
  }

  // ---------- Offers-Tab (die bisherige Startseite) ----------
  Widget _buildOffersTab(List<Offer> filtered, AppLocalizations loc,
      String Function(Category) catName,) {
    return SafeArea(
      child: SingleChildScrollView(
        child: Column(
          children: [
            // Header (greeting + search)
            Padding(
              padding:
                  const EdgeInsetsDirectional.fromSTEB(16, 12, 16, 8),
              child: Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(loc.welcome!,
                            style: GoogleFonts.cairo(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                                color: Colors.grey[800],),),
                        const SizedBox(height: 4),
                        Text(loc.exploreOffers!,
                            style: GoogleFonts.cairo(
                                fontSize: 16, color: Colors.grey[700],),),
                        const SizedBox(height: 12),
                        // Search field
                        TextField(
                          controller: _searchController,
                          onChanged: (v) => setState(() => _search = v),
                          decoration: InputDecoration(
                            hintText: loc.searchHint,
                            filled: true,
                            fillColor: Theme.of(context).cardTheme.color,
                            contentPadding: const EdgeInsets.symmetric(
                                horizontal: 14, vertical: 12,),
                            border: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide: BorderSide(
                                  color: Theme.of(context)
                                      .primaryColor
                                      .withValues(alpha: 0.25),),
                            ),
                            enabledBorder: OutlineInputBorder(
                              borderRadius: BorderRadius.circular(12),
                              borderSide: BorderSide(
                                  color: Theme.of(context)
                                      .primaryColor
                                      .withValues(alpha: 0.18),),
                            ),
                            prefixIcon: Icon(Icons.search,
                                color: Theme.of(context).primaryColor,),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 8),
                ],
              ),
            ),
            // Categories horizontal
            FutureBuilder<List<Category>>(
              future: _categoriesFuture,
              builder: (context, catSnap) {
                final cats = catSnap.data ?? [];
                return SizedBox(
                  height: 68,
                  child: ListView.separated(
                    padding: const EdgeInsetsDirectional.only(
                        start: 16, end: 16,),
                    scrollDirection: Axis.horizontal,
                    itemBuilder: (context, index) {
                      final c = cats[index];
                      final selected = _selectedCategoryId == c.id;
                      return GestureDetector(
                        onTap: () {
                          setState(() {
                            _selectedCategoryId =
                                selected ? null : c.id;
                          });
                        },
                        child: Container(
                          padding:
                              const EdgeInsetsDirectional.symmetric(
                                  horizontal: 14, vertical: 10,),
                          decoration: BoxDecoration(
                            color: selected
                                ? Theme.of(context).colorScheme.primary
                                : Theme.of(context).cardTheme.color,
                            borderRadius: BorderRadius.circular(24),
                            boxShadow: [
                              BoxShadow(
                                  color: Colors.black.withValues(alpha: 0.05),
                                  blurRadius: 8,),
                            ],
                            border: Border.all(
                                color: selected
                                    ? Theme.of(context).primaryColor
                                    : Colors.transparent,),
                          ),
                          child: Row(
                            children: [
                              Icon(
                                _iconForCategory(c.nameEn),
                                color: selected
                                    ? Colors.white
                                    : Theme.of(context)
                                        .colorScheme
                                        .primary,
                              ),
                              const SizedBox(width: 8),
                              Text(catName(c),
                                  style: TextStyle(
                                      color: selected
                                          ? Colors.white
                                          : Colors.grey[800],),),
                            ],
                          ),
                        ),
                      );
                    },
                    separatorBuilder: (_, __) =>
                        const SizedBox(width: 12),
                    itemCount: cats.length,
                  ),
                );
              },
            ),
            const SizedBox(height: 12),
            // ══════════════════════════════════════
            // Flash Deals Sektion
            // ══════════════════════════════════════
            _buildFlashDealsSection(loc),
            const SizedBox(height: 12),
            // ══════════════════════════════════════
            // Empfehlungen Sektion
            // ══════════════════════════════════════
            _buildRecommendationsSection(loc),
            const SizedBox(height: 12),
            // Angebotsliste (vertikal)
            if (filtered.isEmpty)
              Center(
                  child: Text(loc.noOffers!,
                      style: TextStyle(color: Colors.grey[600]),),)
            else
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: filtered.length,
                separatorBuilder: (_, __) => const SizedBox(height: 12),
                itemBuilder: (context, index) {
                  final offer = filtered[index];
                  return OfferCard(
                      offer: offer,
                      userLat: _userLat,
                      userLng: _userLng,);
                },
              ),
          ],
        ),
      ),
    );
  }

  IconData _iconForCategory(String nameEn) {
    switch (nameEn.toLowerCase()) {
      case 'restaurants':
        return Icons.restaurant;
      case 'parks':
        return Icons.park;
      case 'museums':
        return Icons.museum;
      case 'cinemas':
        return Icons.movie;
      default:
        return Icons.category;
    }
  }

  Widget _buildFlashDealsSection(AppLocalizations loc) {
    return FutureBuilder<List<Offer>>(
      future:
          Provider.of<ApiService>(context, listen: false).getFlashDeals(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const SizedBox.shrink();
        }
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const SizedBox.shrink();
        }

        final deals = snapshot.data!;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding:
                  const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              child: Row(
                children: [
                  Icon(Icons.bolt,
                      color: Theme.of(context).colorScheme.secondary,
                      size: 22,),
                  const SizedBox(width: 6),
                  Text(loc.flashDeals!,
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Theme.of(context).colorScheme.secondary,
                      ),),
                ],
              ),
            ),
            SizedBox(
              height: 240,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                itemCount: deals.length,
                itemBuilder: (context, index) =>
                    FlashDealCard(offer: deals[index]),
              ),
            ),
          ],
        );
      },
    );
  }

  Widget _buildRecommendationsSection(AppLocalizations loc) {
    return FutureBuilder<List<Offer>>(
      future: Provider.of<ApiService>(context, listen: false)
          .getRecommendations(userId: _userId),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const SizedBox(
            height: 200,
            child: Center(child: CircularProgressIndicator()),
          );
        }
        if (snapshot.hasError ||
            !snapshot.hasData ||
            snapshot.data!.isEmpty) {
          return const SizedBox.shrink();
        }

        final recommendations = snapshot.data!;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding:
                  const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              child: Text(loc.recommendedForYou!,
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.secondary,
                  ),),
            ),
            SizedBox(
              height: 200,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                itemCount: recommendations.length,
                itemBuilder: (context, index) {
                  final offer = recommendations[index];
                  return _buildRecommendationCard(offer);
                },
              ),
            ),
          ],
        );
      },
    );
  }

  Widget _buildRecommendationCard(Offer offer) {
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => OfferDetailScreen(offer: offer),
          ),
        );
      },
      child: Card(
        margin: const EdgeInsets.all(8),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        child: SizedBox(
          width: 160,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Expanded(
                child: ClipRRect(
                  borderRadius:
                      const BorderRadius.vertical(top: Radius.circular(12)),
                  child: offer.imageUrls != null &&
                          offer.imageUrls!.isNotEmpty
                      ? CachedNetworkImage(
                          imageUrl: offer.imageUrls!.first,
                          fit: BoxFit.cover,
                          placeholder: (context, url) =>
                              Container(color: Colors.grey[200]),
                          errorWidget: (context, url, error) =>
                              Container(
                            color: Colors.grey[200],
                            child: const Icon(Icons.broken_image,
                                size: 40, color: Colors.grey,),
                          ),
                        )
                      : Container(
                          color: Colors.grey[200],
                          child: const Icon(Icons.image,
                              size: 40, color: Colors.grey,),
                        ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  offer.getDisplayTitle(context),
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 8.0),
                child: Text(
                  '${offer.offerPrice} ل.س',
                  style: TextStyle(
                    color: Theme.of(context).colorScheme.secondary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 4),
            ],
          ),
        ),
      ),
    );
  }
}