import '../services/cloud.dart';

class LogService {
  static Stream<List<Map<String, dynamic>>> retrieveAllLogs() {
    return SupabaseService.client.from('logs').stream(primaryKey: ['id']).order('created_at', ascending: false);
  }
}