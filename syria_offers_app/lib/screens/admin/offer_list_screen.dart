import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/screens/admin/add_offer_screen.dart';

class OfferListScreen extends StatefulWidget {
  const OfferListScreen({super.key});

  @override
  State<OfferListScreen> createState() => _OfferListScreenState();
}

class _OfferListScreenState extends State<OfferListScreen> {
  List<Offer> _offers = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchOffers();
  }

  Future<void> _fetchOffers() async {
    setState(() => _isLoading = true);
    try {
      final api = Provider.of<AdminApiService>(context, listen: false);
      final offers = await api.getOffers();
      setState(() {
        _offers = offers;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        final loc = AppLocalizations.of(context)!;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('${loc.failedToLoadOffers}: $e')),
        );
      }
    }
  }

  Future<void> _approveOffer(Offer offer) async {
    final api = Provider.of<AdminApiService>(context, listen: false);
    await api.approveOffer(offer.id);

    // تحديث الحالة محلياً (فوري)
    setState(() {
      offer.approved = true;
    });
    // 2. إعادة جلب القائمة من الخادم لضمان التزامن الكامل
    _fetchOffers();
  }

  Future<void> _deleteOffer(Offer offer) async {
    final loc = AppLocalizations.of(context)!;
    final confirm = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(loc.confirmDelete!),
        content: Text('${loc.confirmDeleteMessage} "${offer.titleAr}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: Text(loc.no!),
          ),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: Text(loc.yes!),
          ),
        ],
      ),
    );
    if (confirm == true) {
      final api = Provider.of<AdminApiService>(context, listen: false);
      await api.deleteOffer(offer.id);
      setState(() {
        _offers.removeWhere((o) => o.id == offer.id);
      });
    }
  }

  Future<void> _navigateToAddOffer() async {
    final result = await Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const AddOfferScreen()),
    );
    if (result == true) {
      _fetchOffers(); // إعادة جلب البيانات بعد إضافة عرض جديد
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(
        title: Text(loc.manageOffers!),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: _navigateToAddOffer,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _fetchOffers,
              child: _offers.isEmpty
                  ? ListView(
                      children: [
                        const SizedBox(height: 200),
                        Center(child: Text(loc.noOffersCurrently!)),
                      ],
                    )
                  : ListView.builder(
                      itemCount: _offers.length,
                      itemBuilder: (context, index) {
                        final offer = _offers[index];
                        return ListTile(
                          title: Text(offer.titleAr),
                          subtitle: Text(
                            '${offer.offerPrice} ${loc.price} - ${offer.approved ? loc.approved! : loc.notApproved!}',
                          ),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              if (!offer.approved)
                                IconButton(
                                  icon: const Icon(Icons.check_circle,
                                      color: Colors.green),
                                  onPressed: () => _approveOffer(offer),
                                ),
                              IconButton(
                                icon:
                                    const Icon(Icons.delete, color: Colors.red),
                                onPressed: () => _deleteOffer(offer),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
            ),
    );
  }
}
