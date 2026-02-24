import '../services/cloud.dart';

class GalleryService {
  static Stream<List<Map<String, dynamic>>> retrieveImages() {
    return SupabaseService.client.from('snapshots').stream(primaryKey: ['id']).order('created_at', ascending: false);
  }
}