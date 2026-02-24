import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseService {
  static Future<void> init() async {
    await Supabase.initialize(
      url: 'https://ovwlozefeqmdsigguxsu.supabase.co',
      anonKey: 'sb_publishable_ybp3YfGi2ErQ0qRfi5h8xw_WRnECuiv',
    );
  }

  static SupabaseClient get client => Supabase.instance.client;
}