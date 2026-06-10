import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:async';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/screens/merchant/merchant_add_offer_screen.dart';
import 'package:syria_offers_app/services/auth_service.dart';

class MerchantOfferListScreen extends StatefulWidget {
  const MerchantOfferListScreen({super.key});

  @override
  State<MerchantOfferListScreen> createState() =>
      _MerchantOfferListScreenState();
}

class _MerchantOfferListScreenState extends State<MerchantOfferListScreen> {
  late Future<List<Offer>> _offersFuture;
  Timer? _autoRefreshTimer;

  @override
  void initState() {
    super.initState();
    _loadOffers();
    // تحديث تلقائي كل 30 ثانية
    _autoRefreshTimer = Timer.periodic(const Duration(seconds: 30), (_) {
      if (mounted) {
        setState(() {
          _loadOffers();
        });
      }
    });
  }

  @override
  void dispose() {
    _autoRefreshTimer?.cancel();
    super.dispose();
  }

  void _loadOffers() {
    _offersFuture =
        Provider.of<ApiService>(context, listen: false).getMyMerchantOffers();
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(
        title: Text(loc.myOffers!),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => setState(() => _loadOffers()),
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await Provider.of<AuthService>(context, listen: false).logout();
              if (context.mounted) {
                Navigator.pushReplacementNamed(context, '/home');
              }
            },
          ),
        ],
      ),
      body: FutureBuilder<List<Offer>>(
        future: _offersFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('${loc.error}: ${snapshot.error}'));
          }
          final offers = snapshot.data ?? [];
          if (offers.isEmpty) {
            return Center(child: Text(loc.noOffersYet!));
          }

          // العدد الذي تمت الموافقة عليه حديثاً (مؤشر بصري)
          final approvedCount = offers.where((o) => o.approved).length;

          return Column(
            children: [
              if (approvedCount > 0)
                Container(
                  width: double.infinity,
                  color: Colors.green.shade50,
                  padding: const EdgeInsets.all(8),
                  child: Text(
                    loc.approvedOffersCount!
                        .replaceFirst('%count%', '$approvedCount'),
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                        color: Colors.green, fontWeight: FontWeight.bold),
                  ),
                ),
              Expanded(
                child: RefreshIndicator(
                  onRefresh: () async {
                    _loadOffers();
                    setState(() {});
                  },
                  child: ListView.builder(
                    itemCount: offers.length,
                    itemBuilder: (context, index) {
                      final offer = offers[index];
                      return ListTile(
                        title: Text(offer.titleAr),
                        subtitle: Text(
                          '${offer.offerPrice} ${loc.price} - ${offer.approved ? loc.approved! : loc.pendingApproval!}',
                        ),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () => _confirmDelete(offer),
                        ),
                      );
                    },
                  ),
                ),
              ),
            ],
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final result = await Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const MerchantAddOfferScreen()),
          );
          if (result == true) {
            setState(() => _loadOffers());
          }
        },
        child: const Icon(Icons.add),
      ),
    );
  }

  void _confirmDelete(Offer offer) {
    final loc = AppLocalizations.of(context)!;
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(loc.confirmDelete!),
        content: Text('${loc.confirmDeleteMessage} "${offer.titleAr}"?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: Text(loc.no!)),
          TextButton(
              onPressed: () {
                Navigator.pop(ctx);
                _deleteOffer(offer.id);
              },
              child: Text(loc.yes!)),
        ],
      ),
    );
  }

  Future<void> _deleteOffer(int offerId) async {
    final loc = AppLocalizations.of(context)!;
    await Provider.of<ApiService>(context, listen: false)
        .deleteMyOffer(offerId);
    setState(() => _loadOffers());
    if (mounted) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(loc.offerDeleted!)));
    }
  }
}
