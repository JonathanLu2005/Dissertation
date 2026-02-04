import 'package:flutter/material.dart';
import '../widgets/enableToggle.dart';
import '../services/loadModelSettings.dart';

class ModelSettingsPage extends StatefulWidget {
  const ModelSettingsPage({super.key});

  @override
  State<ModelSettingsPage> createState() => _ModelSettingsPageState();
}

class _ModelSettingsPageState extends State<ModelSettingsPage> {
  final ModelSettingsService settingsService = ModelSettingsService();
  bool backgroundEnabled = true;
  bool proximityEnabled = true;
  bool loiteringEnabled = true;
  bool maskEnabled = true;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadSettings();
  }

  Future<void> loadSettings() async {
    final data = await settingsService.loadSettings();

    setState(() {
      backgroundEnabled = data["background"]!;
      proximityEnabled = data["proximity"]!;
      loiteringEnabled = data["loitering"]!;
      maskEnabled = data["mask"]!;
      isLoading = false;
    });
  }

  void save() {
    settingsService.saveSettings(
      backgroundEnabled: backgroundEnabled,
      proximityEnabled: proximityEnabled,
      loiteringEnabled: loiteringEnabled,
      maskEnabled: maskEnabled,
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