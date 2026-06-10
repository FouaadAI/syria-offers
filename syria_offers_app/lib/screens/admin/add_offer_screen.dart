import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:image_picker/image_picker.dart';
import 'package:syria_offers_app/localization/app_localizations.dart';
import 'package:syria_offers_app/services/admin_api_service.dart';
import 'package:syria_offers_app/services/api_service.dart';
import 'package:syria_offers_app/models/category.dart';

class AddOfferScreen extends StatefulWidget {
  const AddOfferScreen({super.key});

  @override
  State<AddOfferScreen> createState() => _AddOfferScreenState();
}

class _AddOfferScreenState extends State<AddOfferScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleArCtrl = TextEditingController();
  final _titleEnCtrl = TextEditingController();
  final _originalPriceCtrl = TextEditingController();
  final _offerPriceCtrl = TextEditingController();
  final _descriptionArCtrl = TextEditingController();

  int? _selectedCategoryId;
  DateTime _startDate = DateTime.now();
  DateTime _endDate = DateTime.now().add(const Duration(days: 30));
  bool _isFlash = false;
  int _flashPercent = 0;
  bool _isSubmitting = false;
  List<File> _selectedImages = [];

  Future<DateTime?> _pickDate(DateTime initial) async {
    return showDatePicker(
      context: context,
      initialDate: initial,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
      locale: const Locale('ar'),
    );
  }

  Future<void> _pickImages() async {
    final picker = ImagePicker();
    final images = await picker.pickMultiImage();
    setState(() {
      _selectedImages = images.map((img) => File(img.path)).toList();
    });
  }

  Future<void> _submit() async {
    final loc = AppLocalizations.of(context)!;
    if (!_formKey.currentState!.validate()) return;
    if (_selectedCategoryId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(loc.pleaseSelectCategory!)),
      );
      return;
    }

    setState(() => _isSubmitting = true);
    try {
      final api = Provider.of<AdminApiService>(context, listen: false);
      final List<String> imageUrls = _selectedImages.isNotEmpty
          ? await api.uploadImages(_selectedImages)
          : [];

      final originalPrice = double.tryParse(_originalPriceCtrl.text) ?? 0;
      final offerPrice =
          double.tryParse(_offerPriceCtrl.text) ?? originalPrice * 0.7;

      await api.createOffer({
        'title_ar': _titleArCtrl.text.trim(),
        'title_en': _titleEnCtrl.text.trim(),
        'description_ar': _descriptionArCtrl.text.trim(),
        'description_en': '',
        'original_price': originalPrice,
        'offer_price': offerPrice,
        'start_date': _startDate.toIso8601String(),
        'end_date': _endDate.toIso8601String(),
        'category_id': _selectedCategoryId,
        'image_urls': imageUrls,
        'is_flash': _isFlash,
        'flash_discount_percent': _isFlash ? _flashPercent : 0,
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content: Text(loc.offerAddedSuccess!),
              backgroundColor: Colors.green),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content: Text('${loc.failed!}: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
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
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                  controller: _titleArCtrl,
                  decoration: InputDecoration(labelText: loc.titleAr!),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? loc.required : null),
              const SizedBox(height: 8),
              TextFormField(
                  controller: _titleEnCtrl,
                  decoration: InputDecoration(labelText: loc.titleEn!),
                  validator: (v) =>
                      v == null || v.trim().isEmpty ? loc.required : null),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                      child: TextFormField(
                          controller: _originalPriceCtrl,
                          decoration:
                              InputDecoration(labelText: loc.originalPrice!),
                          keyboardType: TextInputType.number,
                          validator: (v) => v == null || v.trim().isEmpty
                              ? loc.required
                              : null)),
                  const SizedBox(width: 8),
                  Expanded(
                      child: TextFormField(
                          controller: _offerPriceCtrl,
                          decoration:
                              InputDecoration(labelText: loc.offerPrice!),
                          keyboardType: TextInputType.number)),
                ],
              ),
              const SizedBox(height: 8),
              FutureBuilder<List<Category>>(
                future: Provider.of<ApiService>(context, listen: false)
                    .getCategories(),
                builder: (ctx, snap) {
                  if (!snap.hasData) return const CircularProgressIndicator();
                  final categories = snap.data!;
                  return DropdownButtonFormField<int>(
                    initialValue: _selectedCategoryId,
                    items: categories
                        .map((c) => DropdownMenuItem(
                            value: c.id, child: Text(c.nameAr)))
                        .toList(),
                    onChanged: (v) => setState(() => _selectedCategoryId = v),
                    decoration: InputDecoration(labelText: loc.category!),
                    validator: (v) => v == null ? loc.selectCategory : null,
                  );
                },
              ),
              const SizedBox(height: 8),
              TextFormField(
                  controller: _descriptionArCtrl,
                  decoration:
                      InputDecoration(labelText: loc.descriptionOptional!),
                  maxLines: 2),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(
                      child: ListTile(
                          title: Text(loc.offerStart!),
                          subtitle:
                              Text(DateFormat.yMd('ar').format(_startDate)),
                          trailing: const Icon(Icons.calendar_today),
                          onTap: () async {
                            final d = await _pickDate(_startDate);
                            if (d != null) setState(() => _startDate = d);
                          })),
                  Expanded(
                      child: ListTile(
                          title: Text(loc.offerEnd!),
                          subtitle: Text(DateFormat.yMd('ar').format(_endDate)),
                          trailing: const Icon(Icons.calendar_today),
                          onTap: () async {
                            final d = await _pickDate(_endDate);
                            if (d != null) setState(() => _endDate = d);
                          })),
                ],
              ),
              const SizedBox(height: 8),
              SwitchListTile(
                  title: Text(loc.flashOffer!),
                  value: _isFlash,
                  onChanged: (v) => setState(() => _isFlash = v),
                  controlAffinity: ListTileControlAffinity.leading),
              if (_isFlash)
                Padding(
                    padding: const EdgeInsets.only(bottom: 8),
                    child: TextFormField(
                        decoration:
                            InputDecoration(labelText: loc.discountPercent!),
                        keyboardType: TextInputType.number,
                        initialValue: _flashPercent.toString(),
                        onChanged: (v) =>
                            _flashPercent = int.tryParse(v) ?? 0)),
              const SizedBox(height: 8),
              if (_selectedImages.isNotEmpty)
                SizedBox(
                  height: 100,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: _selectedImages.length,
                    itemBuilder: (context, index) {
                      final file = _selectedImages[index];
                      return Stack(
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(4.0),
                            child: ClipRRect(
                                borderRadius: BorderRadius.circular(8),
                                child: Image.file(file,
                                    width: 80, height: 80, fit: BoxFit.cover)),
                          ),
                          Positioned(
                              top: 0,
                              right: 2,
                              child: GestureDetector(
                                  onTap: () => setState(
                                      () => _selectedImages.removeAt(index)),
                                  child: const CircleAvatar(
                                      radius: 12,
                                      backgroundColor: Colors.white,
                                      child: Icon(Icons.cancel,
                                          color: Colors.red, size: 20)))),
                        ],
                      );
                    },
                  ),
                ),
              TextButton.icon(
                  onPressed: _pickImages,
                  icon: const Icon(Icons.image),
                  label: Text(loc.selectImages!)),
              const SizedBox(height: 12),
              ElevatedButton.icon(
                onPressed: _isSubmitting ? null : _submit,
                icon: _isSubmitting
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.add),
                label: Text(_isSubmitting ? loc.adding! : loc.addOffer!),
                style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 12)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
