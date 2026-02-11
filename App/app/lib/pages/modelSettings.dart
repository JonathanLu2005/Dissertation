import 'package:flutter/material.dart';
import '../widgets/enableToggle.dart';
import '../services/loadModelSettings.dart';
import '../widgets/informationButton.dart';

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
      appBar: AppBar(
        title: const Text("Model Settings"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: [
              const Text("Background Detection", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Background Detection",
                description: "Detects if the scene or brightness has changed significantly."
              ),
            ],
          ),
          ToggleSetting(
            label: "Enabled",
            value: backgroundEnabled,
            onChanged: (v) {
              setState(() => backgroundEnabled = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          Row(
            children: [
              const Text("Proximity Detection", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Proximity Detection",
                description: "Detects if someone is standing or sitting too close to the laptop."
              ),
            ],
          ),
          ToggleSetting(
            label: "Enabled",
            value: proximityEnabled,
            onChanged: (v) {
              setState(() => proximityEnabled = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          Row(
            children: [
              const Text("Loitering Detection", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Loitering Detection",
                description: "Detects if someone is loitering around the laptop for a prolonged period."
              ),
            ],
          ),
          ToggleSetting(
            label: "Enabled",
            value: loiteringEnabled,
            onChanged: (v) {
              setState(() => loiteringEnabled = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          Row( 
            children: [ 
              const Text("Mask Detection", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Mask Detection", 
                description: "Detects if someone is wearing a mask or not."
              ),
            ],
          ),
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