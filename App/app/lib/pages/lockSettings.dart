import 'package:flutter/material.dart';
import '../widgets/enableToggle.dart';
import '../services/loadLockSettings.dart';
import '../widgets/informationButton.dart';

class LockSettingsPage extends StatefulWidget {
  const LockSettingsPage({super.key});

  @override
  State<LockSettingsPage> createState() => _LockSettingsPageState();
}

class _LockSettingsPageState extends State<LockSettingsPage> {
  final LockSettingsService settingsService = LockSettingsService();

  bool powerLock = false;
  bool detectionLock = false; 
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadSettings();
  }

  Future<void> loadSettings() async {
    final data = await settingsService.loadSettings();

    setState(() {
      powerLock = data["powerlock"];
      detectionLock = data["detectionlock"];
      isLoading = false;
    });
  }

  void save() {
    settingsService.saveSettings(
      powerLock: powerLock,
      detectionLock: detectionLock,
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
        title: const Text("Lock Settings"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      body: ListView(  
        padding: const EdgeInsets.all(16), 
        children: [
          Row(
            children: [
              const Text("Automatic Power Lock", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Automatic Power Lock",
                description: "Automatically locks the laptop if the system is enabled"
              ),
            ],
          ),
          ToggleSetting(
            label: "Enabled",
            value: powerLock,
            onChanged: (v) {
              setState(() => powerLock = v);
              save();
            },
          ),

          const SizedBox(height: 24),

          Row(
            children: [
              const Text("Automatic Detection Lock", style: TextStyle(fontSize: 18)),
              InformationButton(
                title: "Automatic Detection Lock",
                description: "Automatically locks the laptop if the system detects a suspicious action"
              ),
            ],
          ),
          ToggleSetting(
            label: "Enabled", 
            value: detectionLock,
            onChanged: (v) {
              setState(() => detectionLock = v);
              save();
            },
          ),
        ],
      ),
    );
  }
}