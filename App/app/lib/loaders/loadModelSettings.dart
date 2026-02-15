import 'package:firebase_database/firebase_database.dart';

class ModelSettingsService {
  final DatabaseReference database = FirebaseDatabase.instance.ref("ModelSettings");

  Future<Map<String, bool>> loadSettings() async {
    final settings = await database.get();
    final data = settings.value as Map?;

    return {
      "background": data?["background"] ?? true,
      "proximity": data?["proximity"] ?? true,
      "loitering": data?["loitering"] ?? true,
      "mask": data?["mask"] ?? true,
    };
  }

  Future<void> saveSettings({
    required bool backgroundEnabled,
    required bool proximityEnabled,
    required bool loiteringEnabled,
    required bool maskEnabled
  }) async {
    await database.set({
      "background": backgroundEnabled,
      "proximity": proximityEnabled,
      "loitering": loiteringEnabled,
      "mask": maskEnabled,
    });
  }
}