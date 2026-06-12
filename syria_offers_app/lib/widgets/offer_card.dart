import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:shimmer/shimmer.dart';
import 'package:syria_offers_app/models/offer.dart';
import 'package:syria_offers_app/screens/offer_detail_screen.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';

class OfferCard extends StatelessWidget {
  final Offer offer;
  final double? userLat;
  final double? userLng;

  const OfferCard({super.key, required this.offer, this.userLat, this.userLng});

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context);
    final displayLoc = offer.getDisplayLocation(context);
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16.0)),
      clipBehavior: Clip.antiAlias,
      elevation: 3,
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => OfferDetailScreen(offer: offer, userLat: userLat, userLng: userLng),
            ),
          );
        },
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (offer.imageUrls != null && offer.imageUrls!.isNotEmpty)
              Stack(
                children: [
                  SizedBox(
                    height: 180,
                    width: double.infinity,
                    child: CachedNetworkImage(
                      imageUrl: offer.imageUrls!.first,
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
                  ),
                  PositionedDirectional(
                    top: 10,
                    start: 12,
                    end: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: Colors.black.withValues(alpha: 0.3),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          const Icon(Icons.location_on_outlined, color: Colors.white, size: 14),
                          const SizedBox(width: 6),
                          if (userLat != null && userLng != null)
                            Text(
                              offer.distanceText(userLat!, userLng!),
                              style: const TextStyle(color: Colors.white, fontSize: 12),
                            ),
                        ],
                      ),
                    ),
                  ),
                ],
              )
            else
              Container(
                height: 180,
                color: Colors.grey[200],
                child: const Center(
                  child: Icon(Icons.image, size: 80, color: Colors.grey),
                ),
              ),
            Padding(
              padding: const EdgeInsetsDirectional.fromSTEB(12,12,12,12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    offer.getDisplayTitle(context),
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.grey[900]),
                  ),
                  const SizedBox(height: 6),
                  if (displayLoc.isNotEmpty)
                    Row(
                      children: [
                        const Icon(Icons.location_on, size: 14, color: Colors.grey),
                        const SizedBox(width: 6),
                        Text(displayLoc, style: const TextStyle(color: Colors.grey, fontSize: 12)),
                      ],
                    ),
                  const SizedBox(height: 8),
                  Text(
                    offer.getDisplayDescription(context),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Text(
                        '${offer.offerPrice} ${loc.currencySymbol}',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).colorScheme.secondary,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        '${offer.originalPrice} ${loc.currencySymbol}',
                        style: const TextStyle(
                          fontSize: 14,
                          decoration: TextDecoration.lineThrough,
                          color: Colors.grey,
                        ),
                      ),
                      const Spacer(),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
