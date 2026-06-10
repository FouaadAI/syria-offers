import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

class FavoritesService {
  // إزالة الـ Singleton لصالح حقن التبعية
  FavoritesService();

  Database? _db;

  Future<Database> _database() async {
    if (_db != null) return _db!;
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'favorites.db');
    _db = await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE favorites (
            offer_id INTEGER PRIMARY KEY
          )
        ''');
      },
    );
    return _db!;
  }

  Future<void> addFavorite(int offerId) async {
    final db = await _database();
    await db.insert(
      'favorites',
      {'offer_id': offerId},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<void> removeFavorite(int offerId) async {
    final db = await _database();
    await db.delete('favorites', where: 'offer_id = ?', whereArgs: [offerId]);
  }

  Future<bool> isFavorite(int offerId) async {
    final db = await _database();
    final rows = await db.query('favorites', where: 'offer_id = ?', whereArgs: [offerId], limit: 1);
    return rows.isNotEmpty;
  }

  Future<List<int>> listFavorites() async {
    final db = await _database();
    final rows = await db.query('favorites', columns: ['offer_id']);
    return rows.map((r) => r['offer_id'] as int).toList();
  }
}