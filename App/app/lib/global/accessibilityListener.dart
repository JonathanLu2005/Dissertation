import 'package:firebase_database/firebase_database.dart';
import 'accessibilityState.dart';

class AccessibilityListener {
  static final DatabaseReference database = FirebaseDatabase.instance.ref("AccessibilitySettings");

  static bool initialised = false;

  static void init() {
    if (initialised) return;

    initialised = true;

    database.onValue.listen((event) {
      final data = event.snapshot.value as Map?;

      AccessibilityState.pageAudio = data?["pageaudio"] ?? true;
      AccessibilityState.buttonAudio = data?["buttonaudio"] ?? true;
      AccessibilityState.isLoading = true;
    });
  }
}