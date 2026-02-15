import 'package:firebase_database/firebase_database.dart';
import 'ipState.dart';

class IPListener {
  static final DatabaseReference database = FirebaseDatabase.instance.ref("IP");

  static bool initialised = false;

  static void init() {
    if (initialised) return;

    initialised = true;

    database.onValue.listen((event) {
      final data = event.snapshot.value as Map?;

      IPState.ip = data?["ip"] ?? "192.168.1.92";
      IPState.isLoading = true;
    });
  }
}