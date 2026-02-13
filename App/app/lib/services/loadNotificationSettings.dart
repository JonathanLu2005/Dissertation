import 'package:firebase_database/firebase_database.dart';

class NotificationSettingsService {
  final DatabaseReference database = FirebaseDatabase.instance.ref("AlertSettings");

  Future<Map<String, dynamic>> loadSettings() async {
    final settings = await database.get();
    final data = settings.value as Map?;

    return {
      "App": {
        "enabled": data?["App"]?["enabled"] ?? true,
        "volume": (data?["App"]?["volume"] ?? 1.0).toDouble(),
      },
      "Laptop": {
        "enabled": data?["Laptop"]?["enabled"] ?? true,
        "volume": (data?["Laptop"]?["volume"] ?? 1.0).toDouble(),
      },
      "Vibration": {
        "enabled": data?["Vibration"]?["enabled"] ?? true,
      }
    };
  }

  Future<void> saveSettings({
    required bool appEnabled,
    required double appVolume,
    required bool laptopEnabled,
    required double laptopVolume,
    required bool vibrationEnabled,
  }) async {
    await database.set({
      "App": {
        "enabled": appEnabled,
        "volume": appVolume,
      },
      "Laptop": {
        "enabled": laptopEnabled,
        "volume": laptopVolume,
      },
      "Vibration": {
        "enabled": vibrationEnabled,
      }
    });
  }
}