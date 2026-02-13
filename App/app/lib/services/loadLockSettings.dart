import 'package:firebase_database/firebase_database.dart';

class LockSettingsService {
  final DatabaseReference database = FirebaseDatabase.instance.ref("LockSettings");

  Future<Map<String, dynamic>> loadSettings() async {
    final settings = await database.get();
    final data = settings.value as Map?;

    return {
      "powerlock": data?["powerlock"] ?? true,
      "detectionlock": data?["detectionlock"] ?? true,
    };
  }

  Future<void> saveSettings({
    required bool powerLock,
    required bool detectionLock,
  }) async {
    await database.set({
      "powerlock": powerLock,
      "detectionlock": detectionLock,
    });
  }
}