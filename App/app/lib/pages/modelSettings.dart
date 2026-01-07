import 'package:flutter/material.dart';
import 'package:firebase_database/firebase_database.dart';
import '../widgets/enableToggle.dart';

class ModelSettingsPage extends StatefulWidget {
  const ModelSettingsPage({super.key});

  @override
  State<ModelSettingsPage> createState() => _ModelSettingsPageState();
}

class _ModelSettingsPageState extends State<ModelSettingsPage> {
  final database = FirebaseDatabase.instance.ref("ModelSettings");

  bool backgroundEnabled = true;
  bool proximityEnabled = true;
  bool loiteringEnabled = true;
  bool maskEnabled = true;

  void save() {
    database.set({
      "BackgroundEnabled": backgroundEnabled,
      "ProximityEnabled": proximityEnabled,
      "LoiteringEnabled": loiteringEnabled,
      "MaskEnabled": maskEnabled,
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Alert Settings")),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text("Background Detection", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: backgroundEnabled,
            onChanged: (v) {
              setState(() => backgroundEnabled = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          const Text("Proximity Detection", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: proximityEnabled,
            onChanged: (v) {
              setState(() => proximityEnabled = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          const Text("Loitering Detection", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: loiteringEnabled,
            onChanged: (v) {
              setState(() => loiteringEnabled = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          const Text("Mask Detection", style: TextStyle(fontSize: 18)),
          ToggleSetting(
            label: "Enabled",
            value: maskEnabled,
            onChanged: (v) {
              setState(() => maskEnabled = v);
              save();
            },
          ),
        ],
      ),
    );
  }
}