import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';
import 'package:syria_offers_app/models/category.dart';

class CategoryListScreen extends StatefulWidget {
  const CategoryListScreen({super.key});

  @override
  State<CategoryListScreen> createState() => _CategoryListScreenState();
}

class _CategoryListScreenState extends State<CategoryListScreen> {
  final _nameArController = TextEditingController();
  final _nameEnController = TextEditingController();

  void _addCategory() async {
    final nameAr = _nameArController.text.trim();
    final nameEn = _nameEnController.text.trim();
    if (nameAr.isEmpty || nameEn.isEmpty) return;
    await Provider.of<AdminApiService>(context, listen: false).createCategory({
      'name_ar': nameAr,
      'name_en': nameEn,
      'sort_order': 0,
    });
    _nameArController.clear();
    _nameEnController.clear();
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(title: Text(loc.categoryListTitle!)),
      body: FutureBuilder<List<Category>>(
        future: Provider.of<AdminApiService>(context, listen: false)
            .getCategories(),
        builder: (context, snapshot) {
          if (!snapshot.hasData)
            return const Center(child: CircularProgressIndicator());
          final categories = snapshot.data!;
          return Column(
            children: [
              Padding(
                padding: const EdgeInsets.all(8),
                child: Row(
                  children: [
                    Expanded(
                        child: TextField(
                            controller: _nameArController,
                            decoration:
                                InputDecoration(labelText: loc.nameArabic))),
                    const SizedBox(width: 8),
                    Expanded(
                        child: TextField(
                            controller: _nameEnController,
                            decoration:
                                InputDecoration(labelText: loc.nameEnglish))),
                    IconButton(
                        onPressed: _addCategory,
                        icon:
                            const Icon(Icons.add_circle, color: Colors.green)),
                  ],
                ),
              ),
              Expanded(
                child: ListView.builder(
                  itemCount: categories.length,
                  itemBuilder: (context, index) {
                    final cat = categories[index];
                    return ListTile(
                      title: Text(cat.nameAr),
                      trailing: IconButton(
                        icon: const Icon(Icons.delete, color: Colors.red),
                        onPressed: () async {
                          await Provider.of<AdminApiService>(context,
                                  listen: false)
                              .deleteCategory(cat.id);
                          setState(() {});
                        },
                      ),
                    );
                  },
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
