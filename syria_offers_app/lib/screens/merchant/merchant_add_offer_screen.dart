import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/models/category.dart';

class MerchantAddOfferScreen extends StatefulWidget {
  const MerchantAddOfferScreen({super.key});

  @override
  State<MerchantAddOfferScreen> createState() => _MerchantAddOfferScreenState();
}

class _MerchantAddOfferScreenState extends State<MerchantAddOfferScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleArCtrl = TextEditingController();
  final _titleEnCtrl = TextEditingController();
  final _originalPriceCtrl = TextEditingController();
  final _offerPriceCtrl = TextEditingController();
  final _descriptionArCtrl = TextEditingController();

  int? _categoryId;
  final List<File> _images = [];
  bool _isSubmitting = false;

  Future<void> _pickImages() async {
    final picker = ImagePicker();
    final picked = await picker.pickMultiImage();
    setState(() {
      _images.addAll(picked.map((e) => File(e.path)));
    });
  }

  Future<void> _submit() async {
    final loc = AppLocalizations.of(context)!;
    if (!_formKey.currentState!.validate() || _categoryId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.pleaseFillAllFieldsAndCategory!)),
      );
      return;
    }
    setState(() => _isSubmitting = true);
    try {
      final api = Provider.of<ApiService>(context, listen: false);
      List<String> imageUrls = [];
      if (_images.isNotEmpty) {
        imageUrls = await api.uploadImages(_images);
      }
      await api.createMerchantOffer({
        'title_ar': _titleArCtrl.text.trim(),
        'title_en': _titleEnCtrl.text.trim(),
        'description_ar': _descriptionArCtrl.text.trim(),
        'original_price': double.parse(_originalPriceCtrl.text),
        'offer_price': double.parse(_offerPriceCtrl.text),
        'category_id': _categoryId,
        'image_urls': imageUrls,
        'start_date': DateTime.now().toIso8601String(),
        'end_date':
            DateTime.now().add(const Duration(days: 30)).toIso8601String(),
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content: Text(loc.offerSentPendingApproval!),
              backgroundColor: Colors.green),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      setState(() => _isSubmitting = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            content: Text('${loc.failed!}: $e'), backgroundColor: Colors.red),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(title: Text(loc.addNewOffer!)),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              TextFormField(
                  controller: _titleArCtrl,
                  decoration: InputDecoration(labelText: loc.titleAr!),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? loc.required : null),
              const SizedBox(height: 12),
              TextFormField(
                  controller: _titleEnCtrl,
                  decoration: InputDecoration(labelText: loc.titleEn!),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? loc.required : null),
              const SizedBox(height: 12),
              TextFormField(
                  controller: _originalPriceCtrl,
                  decoration: InputDecoration(labelText: loc.originalPrice!),
                  keyboardType: TextInputType.number,
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? loc.required : null),
              const SizedBox(height: 12),
              TextFormField(
                  controller: _offerPriceCtrl,
                  decoration: InputDecoration(labelText: loc.offerPrice!),
                  keyboardType: TextInputType.number),
              const SizedBox(height: 12),
              FutureBuilder<List<Category>>(
                future: Provider.of<ApiService>(context, listen: false)
                    .getCategories(),
                builder: (ctx, snap) {
                  if (!snap.hasData) return const CircularProgressIndicator();
                  final categories = snap.data!;
                  return DropdownButtonFormField<int>(
                    initialValue: _categoryId,
                    items: categories
                        .map((c) => DropdownMenuItem(
                            value: c.id, child: Text(c.nameAr)))
                        .toList(),
                    onChanged: (v) => setState(() => _categoryId = v),
                    decoration: InputDecoration(labelText: loc.category!),
                    validator: (v) => v == null ? loc.selectCategory : null,
                  );
                },
              ),
              const SizedBox(height: 12),
              TextFormField(
                  controller: _descriptionArCtrl,
                  decoration: InputDecoration(labelText: loc.description!),
                  maxLines: 3),
              const SizedBox(height: 16),
              // Bildvorschau mit Lösch-Button (verbessert)
              if (_images.isNotEmpty)
                SizedBox(
                  height: 100,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: _images.length,
                    itemBuilder: (context, index) {
                      final file = _images[index];
                      return Stack(
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(4.0),
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(8),
                              child: Image.file(file,
                                  width: 80, height: 80, fit: BoxFit.cover),
                            ),
                          ),
                          Positioned(
                            top: 0,
                            right: 2,
                            child: GestureDetector(
                              onTap: () {
                                setState(() {
                                  _images.removeAt(index);
                                });
                              },
                              child: const CircleAvatar(
                                radius: 12,
                                backgroundColor: Colors.white,
                                child: Icon(Icons.cancel,
                                    color: Colors.red, size: 20),
                              ),
                            ),
                          ),
                        ],
                      );
                    },
                  ),
                ),
              TextButton.icon(
                onPressed: _pickImages,
                icon: const Icon(Icons.image),
                label: Text(loc.selectImages!),
              ),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                onPressed: _isSubmitting ? null : _submit,
                icon: _isSubmitting
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2))
                    : const Icon(Icons.send),
                label: Text(_isSubmitting ? loc.sending! : loc.sendOffer!),
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(double.infinity, 48),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
