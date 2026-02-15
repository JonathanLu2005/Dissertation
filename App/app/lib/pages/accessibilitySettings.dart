import 'package:flutter/material.dart';
import '../widgets/enableToggle.dart';
import '../loaders/loadAccessibilitySettings.dart';
import '../widgets/informationButton.dart';
import '../services/TTS.dart';

class AccessibilitySettingsPage extends StatefulWidget {
  const AccessibilitySettingsPage({super.key});

  @override
  State<AccessibilitySettingsPage> createState() => _AccessibilitySettingsPageState();
}

class _AccessibilitySettingsPageState extends State<AccessibilitySettingsPage> {
  final AccessibilitySettingsService settingsService = AccessibilitySettingsService();

  bool pageAudio = false;
  bool buttonAudio = false; 
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    TTSService.pageAnnouncement("Accessibility Settings");
    loadSettings();
  }

  Future<void> loadSettings() async {
    final data = await settingsService.loadSettings();

    setState(() {
      pageAudio = data["pageaudio"];
      buttonAudio = data["buttonaudio"];
      isLoading = false;
    });
  }

  void save() {
    settingsService.saveSettings(
      pageAudio: pageAudio,
      buttonAudio: buttonAudio,
    );
  }

  @override  
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator()
        ),
      );
    }
    
    return Scaffold(
      appBar: AppBar(
        title: const Text("Accessibility Settings"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      body: ListView(  
        padding: const EdgeInsets.all(16), 
        children: [
          Row(
            children: [
              const Text("Page Guidance", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Page Guidance",
                description: "Verbally informs you what page you are on."
              ),
            ],
          ),
          ToggleSetting(
            label: "Enabled",
            value: pageAudio,
            onChanged: (v) {
              setState(() => pageAudio = v);
              save();
              TTSService.buttonAnnouncement("Page Guidance", v);
            },
          ),

          const SizedBox(height: 24),

          Row(
            children: [
              const Text("Button Guidance", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Button Guidance",
                description: "Verbally informs you if you have activated or deactivated a button and which button it was."
              ),
            ],
          ),
          ToggleSetting(
            label: "Enabled", 
            value: buttonAudio,
            onChanged: (v) {
              setState(() => buttonAudio = v);
              save();
              TTSService.buttonAnnouncement("Button Guidance", v);
            },
          ),
        ],
      ),
    );
  }
}