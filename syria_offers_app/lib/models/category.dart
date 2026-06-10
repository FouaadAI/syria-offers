class Category {
  final int id;
  final String nameAr;
  final String nameEn;
  final String? iconUrl;
  final int sortOrder;

  Category({
    required this.id,
    required this.nameAr,
    required this.nameEn,
    this.iconUrl,
    required this.sortOrder,
  });

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id'],
      nameAr: json['name_ar'],
      nameEn: json['name_en'],
      iconUrl: json['icon_url'],
      sortOrder: json['sort_order'],
    );
  }
}