import '../services/cloud.dart';

class LogService {
  static Future<List<Map<String, dynamic>>> retrieveRecentLogs() async {
    try {
      final logs = await SupabaseService.client.from('logs').select().order('created_at', ascending: false).limit(5);
      return List<Map<String, dynamic>>.from(logs);
    } catch(e) {
      return [];
    }
  }

  static Future<List<Map<String, dynamic>>> retrieveAllLogs() async {
    try {
      final logs = await SupabaseService.client.from('logs').select().order('created_at', ascending: false);
      return List<Map<String, dynamic>>.from(logs);
    } catch(e) {
      return [];
    }
  }
}