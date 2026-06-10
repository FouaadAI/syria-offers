import 'package:flutter/material.dart';
import 'package:syria_offers_app/models/category.dart';

class CategoryCard extends StatelessWidget {
  final Category category;
  final VoidCallback onTap;

  const CategoryCard({super.key, required this.category, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        elevation: 3,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(14),
            color: Theme.of(context).cardTheme.color,
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                _getIconForCategory(category.nameEn),
                size: 40,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(height: 8),
              Text(
                category.nameAr,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).textTheme.bodyLarge?.color,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getIconForCategory(String nameEn) {
    switch (nameEn.toLowerCase()) {
      case 'restaurants':
        return Icons.restaurant;
      case 'parks':
        return Icons.park;
      case 'museums':
        return Icons.museum;
      case 'cinemas':
        return Icons.movie;
      case 'activities':
        return Icons.sports_handball;
      case 'medical':
        return Icons.local_hospital;
      default:
        return Icons.category;
    }
  }
}
