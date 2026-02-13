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
        "alert": transmissionData?["alert"] == true,
        "message": transmissionData?["message"]?.toString() ?? "—",
        "timestamp": transmissionData?["timestamp"] as int?,
      };

      await Future.delayed(interval);
    }
  }

  Stream<Map<String, dynamic>> listenToLocation(
    {Duration interval = const Duration(seconds: 3)}) async* {
      while (true) {
        final snapshot = await _database.child("LaptopLocation").get();
        final transmissionData = snapshot.value as Map?;

        yield {
          "latitude": transmissionData?["latitude"] as double?,
          "longitude": transmissionData?["longitude"] as double?,
        };

        await Future.delayed(interval);
      }
    }

  Stream<Map<String, dynamic>> listenToSettings() {
    return FirebaseDatabase.instance.ref("AlertSettings").onValue.map((event) {
      final transmissionData = event.snapshot.value as Map?;
      return {
        "alert": transmissionData?["App"]["enabled"] == true,
        "volume": (transmissionData?["App"]["volume"] ?? 1.0).toDouble(),
        "vibration": transmissionData?["Vibration"]["enabled"] == true,
      };
    });
  }

  Stream<bool> listenToCamera() {
    return FirebaseDatabase.instance.ref("RemoteControl/camera").onValue.map((event) {
      return event.snapshot.value == true;
    });
  }

  Stream<bool> listenToMic() {
    return FirebaseDatabase.instance.ref("RemoteControl/mic").onValue.map((event) {
      return event.snapshot.value == true;
    });
  }

  Future<void> sendToBackend(String message) async {
    await _database.child("AppMessages").set(message);
  }
}
