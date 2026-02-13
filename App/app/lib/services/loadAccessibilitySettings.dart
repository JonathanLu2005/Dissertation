import 'package:firebase_database/firebase_database.dart';

class AccessibilitySettingsService {
  final DatabaseReference database = FirebaseDatabase.instance.ref("AccessibilitySettings");

  Future<Map<String, dynamic>> loadSettings() async {
    final settings = await database.get();
    final data = settings.value as Map?;

    return {
      "pageaudio": data?["pageaudio"] ?? true,
      "buttonaudio": data?["buttonaudio"] ?? true,
    };
  }

  Future<void> saveSettings({
    required bool pageAudio,
    required bool buttonAudio,
  }) async {
    await database.set({
      "pageaudio": pageAudio,
      "buttonaudio": buttonAudio,
    });
  }
}