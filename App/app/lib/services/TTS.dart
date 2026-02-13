import 'package:flutter_tts/flutter_tts.dart';
import '../global/accessibilityState.dart';

class TTSService {
  static final FlutterTts TTS = FlutterTts();

  static Future<void> execute(String sentence) async {
    await TTS.stop();
    await TTS.setLanguage("en-gb");
    await TTS.setSpeechRate(0.45);
    await TTS.speak(sentence);
  }

  static Future<void> pageAnnouncement(String page) async {
    if (!AccessibilityState.isLoading) return;
    if (!AccessibilityState.pageAudio) return;

    await execute(page);
  }

  static Future<void> buttonAnnouncement(String button, bool isEnabled) async {
    if (!AccessibilityState.isLoading) return;
    if (!AccessibilityState.buttonAudio) return;

    final result = isEnabled ? "Activated" : "Deactivated";
    await execute("$button $result");
  }

  static Future<void> stop() async {
    await TTS.stop();
  }
}