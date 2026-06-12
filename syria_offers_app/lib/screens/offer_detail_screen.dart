import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:shimmer/shimmer.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/services/favorites_service.dart';
import 'package:syria_offers_app/screens/booking_confirmation_screen.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

class OfferDetailScreen extends StatefulWidget {
  final Offer offer;
  final double? userLat;
  final double? userLng;

  const OfferDetailScreen({super.key, required this.offer, this.userLat, this.userLng});

  @override
  State<OfferDetailScreen> createState() => _OfferDetailScreenState();
}

class _OfferDetailScreenState extends State<OfferDetailScreen> {
  
  

  late final FavoritesService _favoritesService;
  bool _isFavorite = false;
  @override
  void initState() {
    super.initState();
    _favoritesService = context.read<FavoritesService?>() ?? FavoritesService();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadFavoriteState();
    });
  }

  Future<void> _loadFavoriteState() async {
    final isFavorite = await _favoritesService.isFavorite(widget.offer.id);
    if (!mounted) return;
    setState(() => _isFavorite = isFavorite);
  }

  Future<void> _toggleFavorite() async {
    if (_isFavorite) {
      await _favoritesService.removeFavorite(widget.offer.id);
    } else {
      await _favoritesService.addFavorite(widget.offer.id);
    }
    if (!mounted) return;
    setState(() => _isFavorite = !_isFavorite);
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    final currencyFormat = NumberFormat.currency(
      symbol: loc.currencySymbol ?? '',
      decimalDigits: 0,
      locale: Localizations.localeOf(context).toString(),
    );

    final offer = widget.offer;
    final displayLoc = offer.getDisplayLocation(context);


    return Scaffold(
      appBar: AppBar(
        title: Text(offer.getDisplayTitle(context)),
        actions: [
          IconButton(
            tooltip: _isFavorite ? loc.favoritesRemove : loc.favoritesAdd,
            onPressed: () async {
              await _toggleFavorite();
              setState(() {}); // تحديث فوري للأيقونة
            },
            icon: Icon(
              _isFavorite ? Icons.favorite : Icons.favorite_border,
              color: _isFavorite ? Colors.red : null,
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (offer.imageUrls != null && offer.imageUrls!.isNotEmpty)
              SizedBox(
                height: 250,
                child: PageView.builder(
                  itemCount: offer.imageUrls!.length,
                  itemBuilder: (context, index) {
                    return Hero(
                      tag: 'offer-${offer.id}',
                      child: CachedNetworkImage(
                        imageUrl: offer.imageUrls![index],
                        fit: BoxFit.cover,
                        placeholder: (context, url) => Shimmer.fromColors(
                          baseColor: Colors.grey[300]!,
                          highlightColor: Colors.grey[100]!,
                          child: Container(color: Colors.grey[300]),
                        ),
                        errorWidget: (context, url, error) => Container(
                          color: Colors.grey[200],
                          child: const Icon(Icons.broken_image, size: 48, color: Colors.grey),
                        ),
                      ),
                    );
                  },
                ),
              )
            else
              Container(
                height: 250,
                color: Colors.grey[200],
                child: const Center(
                  child: Icon(Icons.image, size: 80, color: Colors.grey),
                ),
              ),
            const SizedBox(height: 16),
            Padding(
              padding: const EdgeInsetsDirectional.only(start: 16, end: 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    offer.getDisplayTitle(context),
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    offer.getDisplayDescription(context),
                    style: const TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Text(
                        currencyFormat.format(offer.offerPrice),
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).primaryColor,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Text(
                        currencyFormat.format(offer.originalPrice),
                        style: const TextStyle(
                          fontSize: 18,
                          decoration: TextDecoration.lineThrough,
                          color: Colors.grey,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  if (offer.endDate != null)
                    Text(
                      '${loc.endDate}: ${DateFormat.yMMMd(Localizations.localeOf(context).toString()).format(DateTime.parse(offer.endDate!))}',
                      style: const TextStyle(color: Colors.red),
                    ),
                  const SizedBox(height: 12),
                  // موقع العرض وزر العرض على الخريطة
                  if (offer.getDisplayLocation(context).isNotEmpty && offer.latitude != null && offer.longitude != null)
                    // offer_detail_screen.dart, ca. Zeile 169
                    Row(
                      children: [
                        const Icon(Icons.location_on, size: 18, color: Colors.grey),
                        const SizedBox(width: 6),
                        Expanded(                                    // ← NEU
                          child: Text(displayLoc,
                            style: const TextStyle(color: Colors.grey),
                            overflow: TextOverflow.ellipsis,         // ← NEU
                          ),
                        ),
                        const SizedBox(width: 8),                    // ← NEU (Abstand)
                        OutlinedButton.icon(
                          onPressed: () => _launchMaps(context),
                          icon: const Icon(Icons.map, size: 18),
                          label: Text(loc.showLocation!),
                          style: OutlinedButton.styleFrom(
                            side: BorderSide(color: Theme.of(context).primaryColor),
                            foregroundColor: Theme.of(context).primaryColor,
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                            padding: const EdgeInsets.symmetric(horizontal: 8),   // ← NEU
                          ),
                        ),
                      ],
                    ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      onPressed: () => _showBookingSheet(context),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Theme.of(context).colorScheme.secondary,
                        foregroundColor: Theme.of(context).colorScheme.onSecondary,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: Text(
                        loc.bookNow!,
                        style: const TextStyle(fontSize: 18),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _launchMaps(BuildContext context) async {
    final offer = widget.offer;
    if (offer.latitude == null || offer.longitude == null) return;
    final lat = offer.latitude!;
    final lng = offer.longitude!;
    final label = Uri.encodeComponent(
        offer.getDisplayLocation(context).isNotEmpty
            ? offer.getDisplayLocation(context)
            : '$lat,$lng',);

    try {
      final geoUri = Uri.parse('geo:$lat,$lng?q=$label');
      await launchUrl(geoUri, mode: LaunchMode.externalApplication);
      return;
    } catch (_) {}

    try {
      final fallback = Uri.parse(
          'https://www.google.com/maps/search/?api=1&query=$label',);
      await launchUrl(fallback, mode: LaunchMode.externalApplication);
    } catch (_) {}
  }

  void _showBookingSheet(BuildContext context) {
    final loc = AppLocalizations.of(context);
    final offer = widget.offer;
    final nameController = TextEditingController();
    final phoneController = TextEditingController();
    DateTime selectedDate = DateTime.now().add(const Duration(days: 1));
    int quantity = 1;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (BuildContext sheetContext, StateSetter setState) {
            return Padding(
              padding: EdgeInsetsDirectional.only(
                start: 16,
                end: 16,
                top: 16,
                bottom: MediaQuery.of(sheetContext).viewInsets.bottom + 16,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    loc.bookingInfo!,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: nameController,
                    decoration: InputDecoration(
                      labelText: loc.fullName,
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: phoneController,
                    keyboardType: TextInputType.phone,
                    decoration: InputDecoration(
                      labelText: loc.phone,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Text('${loc.bookingDate}: '),
                      const SizedBox(width: 8),
                      TextButton(
                        onPressed: () async {
                          final date = await showDatePicker(
                            context: sheetContext,
                            initialDate: selectedDate,
                            firstDate: DateTime.now(),
                            lastDate: DateTime.now().add(const Duration(days: 90)),
                            locale: Localizations.localeOf(sheetContext),
                          );
                          if (date != null) {
                            setState(() => selectedDate = date);
                          }
                        },
                        child: Text(
                          DateFormat.yMMMd(Localizations.localeOf(sheetContext).toString()).format(selectedDate),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Text('${loc.quantity}: '),
                      IconButton(
                        onPressed: () => setState(() => quantity++),
                        icon: const Icon(Icons.add_circle),
                      ),
                      Text('$quantity'),
                      IconButton(
                        onPressed: () {
                          if (quantity > 1) setState(() => quantity--);
                        },
                        icon: const Icon(Icons.remove_circle),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () async {
                      if (nameController.text.isEmpty ||
                          phoneController.text.isEmpty) {
                        ScaffoldMessenger.of(sheetContext).showSnackBar(
                          SnackBar(content: Text(loc.pleaseFillAllFields!)),
                        );
                        return;
                      }

                      // إغلاق الـ Bottom Sheet فوراً
                      Navigator.pop(sheetContext);

                      // جلب ApiService وبدء عملية الحجز
                      final apiService =
                          Provider.of<ApiService>(sheetContext, listen: false);
                      try {
                        final bookingData = await apiService.createBooking(
                          userName: nameController.text,
                          userPhone: phoneController.text,
                          offerId: offer.id,
                          bookedAt: selectedDate.toIso8601String(),
                          quantity: quantity,
                          totalPrice: offer.offerPrice * quantity,
                        );

                        if (context.mounted) {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => BookingConfirmationScreen(
                                bookingCode: bookingData['booking_code'],
                                userName: bookingData['user_name'],
                                userPhone: bookingData['user_phone'],
                                bookedAt:
                                    DateTime.parse(bookingData['booked_at']),
                                quantity: bookingData['quantity'],
                                totalPrice:
                                    (bookingData['total_price'] as num)
                                        .toDouble(),
                                bookingId: bookingData['id'], // ✅ تمت الإضافة
                              ),
                            ),
                          );
                        }
                      } catch (e) {
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('${loc.error}: $e')),
                          );
                        }
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                    ),
                    child: Text(loc.confirmBooking!),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}
