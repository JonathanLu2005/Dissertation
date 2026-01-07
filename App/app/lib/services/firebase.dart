import 'dart:async';
import 'package:firebase_database/firebase_database.dart';

class FirebaseService {
  final DatabaseReference _database = FirebaseDatabase.instance.ref();

  Stream<Map<String, dynamic>> listenToBackend(
      {Duration interval = const Duration(seconds: 3)}) async* {
    while (true) {
      final snapshot = await _database.child("BackendMessages").get();
      final transmissionData = snapshot.value as Map?;

      yield {
        "alert": transmissionData?["Alert"] == true,
        "message": transmissionData?["Message"]?.toString() ?? "—",
      };

      await Future.delayed(interval);
    }
  }

  Stream<Map<String, dynamic>> listenToSettings() {
    return FirebaseDatabase.instance.ref("UserSettings/app").onValue.map((event) {
      final transmissionData = event.snapshot.value as Map?;
      return {
        "enabled": transmissionData?["enabled"] == true,
        "volume": (transmissionData?["volume"] ?? 1.0).toDouble(),
      };
    });
  }

  Future<void> sendToBackend(String message) async {
    await _database.child("AppMessages").set(message);
  }
}
