import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:geolocator/geolocator.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/models/category.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/widgets/offer_card.dart';

class OffersScreen extends StatefulWidget {
  final Category category;
  const OffersScreen({super.key, required this.category});

  @override
  State<OffersScreen> createState() => _OffersScreenState();
}

class _OffersScreenState extends State<OffersScreen> {
  late Future<List<Offer>> _offersFuture;
  double? _userLat;
  double? _userLng;

  @override
  void initState() {
    super.initState();
    _getUserLocation();
    _offersFuture = Provider.of<ApiService>(context, listen: false).getOffers(categoryId: widget.category.id);
  }

  Future<void> _getUserLocation() async {
    try {
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.always || permission == LocationPermission.whileInUse) {
        final pos = await Geolocator.getCurrentPosition();
        setState(() {
          _userLat = pos.latitude;
          _userLng = pos.longitude;
        });
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    final catName = Localizations.localeOf(context).languageCode == 'ar'
        ? widget.category.nameAr
        : widget.category.nameEn;

    return Scaffold(
      appBar: AppBar(title: Text(catName)),
      body: FutureBuilder<List<Offer>>(
        future: _offersFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          final offers = snapshot.data ?? [];

          if (_userLat != null && _userLng != null) {
            offers.sort((a, b) => a.distanceTo(_userLat!, _userLng!).compareTo(b.distanceTo(_userLat!, _userLng!)));
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: offers.length,
            itemBuilder: (context, index) => OfferCard(offer: offers[index], userLat: _userLat, userLng: _userLng),
          );
        },
      ),
    );
  }
}
