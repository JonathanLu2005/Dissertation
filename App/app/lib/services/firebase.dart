import 'dart:async';
import 'package:firebase_database/firebase_database.dart';

class FirebaseService {
  final DatabaseReference _database = FirebaseDatabase.instance.ref();

  Stream<Map<String, dynamic>> listenToBackend(
      {Duration interval = const Duration(seconds: 3)}) async* {
    while (true) {
      final transmission = await _database.child("BackendMessages").get();
      final transmissionData = transmission.value as Map?;

      yield {
        "alert": transmissionData?["Alert"] == true,
        "message": transmissionData?["Message"]?.toString() ?? "—",
      };

      await Future.delayed(interval);
    }
  }

  Future<void> sendToBackend(String message) async {
    await _database.child("AppMessages").set(message);
  }
}
