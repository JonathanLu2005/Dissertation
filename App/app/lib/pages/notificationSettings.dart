import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import '../widgets/enableToggle.dart';
import '../widgets/volumeToggle.dart';

class NotificationSettingsPage extends StatefulWidget {
  const NotificationSettingsPage({super.key});

  @override
  State<NotificationSettingsPage> createState() => _NotificationSettingsPageState();
}

class _NotificationSettingsPageState extends State<NotificationSettingsPage> {
  final database = FirebaseDatabase.instance.ref("AlertSettings");

  bool appEnabled = true;
  double appVolume = 0.8;
  bool laptopEnabled = true;
  double laptopVolume = 1.0;

  void save() {
    database.set({
      "App": {
        "Enabled": appEnabled,
        "Volume": appVolume,
      },
      "Laptop": {
        "Enabled": laptopEnabled,
        "Volume": laptopVolume,
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Alert Settings")),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text("App Alerts", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: appEnabled,
            onChanged: (v) {
              setState(() => appEnabled = v);
              save();
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
          const Text("Laptop Alerts", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: laptopEnabled,
            onChanged: (v) {
              setState(() => laptopEnabled = v);
              save();
            },
          ),
          VolumeSetting(
            value: laptopVolume,
            onChanged: (v) {
              setState(() => laptopVolume = v);
              save();
            },
          ),
        ],
      ),
    );
  }
}