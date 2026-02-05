import 'package:firebase_database/firebase_database.dart';

class PanelSettingsService {
  final DatabaseReference database = FirebaseDatabase.instance.ref("RemoteControl");

  Future<Map<String, bool>> loadSettings() async {
    final settings = await database.get();
    final data = settings.value as Map?;

    return {
      "power": data?["power"] ?? false,
      "lock": data?["lock"] ?? false,
      "camera": data?["camera"] ?? false,
      "mic": data?["mic"] ?? false,
    };
  }

  Future<void> saveSettings({
    required bool powerOn,
    required bool lockOn,
    required bool cameraOn,
    required bool micOn
  }) async {
    await database.set({
      "power": powerOn,
      "lock": lockOn,
      "camera": cameraOn,
      "mic": micOn,
    });
  }
}