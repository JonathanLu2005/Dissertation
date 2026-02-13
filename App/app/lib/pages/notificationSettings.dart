import 'package:flutter/material.dart';
import '../widgets/enableToggle.dart';
import '../widgets/volumeToggle.dart';
import '../services/loadNotificationSettings.dart';
import '../services/TTS.dart';

class NotificationSettingsPage extends StatefulWidget {
  const NotificationSettingsPage({super.key});

  @override
  State<NotificationSettingsPage> createState() => _NotificationSettingsPageState();
}

class _NotificationSettingsPageState extends State<NotificationSettingsPage> {
  final NotificationSettingsService settingsService = NotificationSettingsService();

  bool appEnabled = true;
  double appVolume = 0;
  bool laptopEnabled = true;
  double laptopVolume = 0;
  bool vibrationEnabled = true;

  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    TTSService.pageAnnouncement("Alarm Settings");
    loadSettings();
  }

  Future<void> loadSettings() async {
    final data = await settingsService.loadSettings();
    
    setState(() {
      appEnabled = data["App"]["enabled"];
      appVolume = data["App"]["volume"];
      laptopEnabled = data["Laptop"]["enabled"];
      laptopVolume = data["Laptop"]["volume"];
      vibrationEnabled = data["Vibration"]["enabled"];
      isLoading = false;
    });
  }

  void save() {
    settingsService.saveSettings(
      appEnabled: appEnabled,
      appVolume: appVolume,
      laptopEnabled: laptopEnabled,
      laptopVolume: laptopVolume,
      vibrationEnabled: vibrationEnabled,
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
        title: const Text("Alarm Settings"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text("Phone Alarm", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: appEnabled,
            onChanged: (v) {
              setState(() => appEnabled = v);
              save();
              TTSService.buttonAnnouncement("Phone Alarm", v);
            },
          ),
          VolumeSetting(
            value: appVolume,
            onChanged: (v) {
              setState(() => appVolume = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          const Text("Laptop Alarm", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: laptopEnabled,
            onChanged: (v) {
              setState(() => laptopEnabled = v);
              save();
              TTSService.buttonAnnouncement("Laptop Alarm", v);
            },
          ),
          VolumeSetting(
            value: laptopVolume,
            onChanged: (v) {
              setState(() => laptopVolume = v);
              save();
            },
          ),

          const SizedBox(height: 24), 
          const Text("Phone Vibration", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled", 
            value: vibrationEnabled, 
            onChanged: (v) {
              setState(() => vibrationEnabled = v);
              save();
              TTSService.buttonAnnouncement("Phone Vibration", v);
            },
          ),
        ],
      ),
    );
  }
}