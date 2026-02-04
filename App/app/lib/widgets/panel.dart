import 'package:flutter/material.dart';
import 'controlButton.dart';
import '../services/loadPanelSettings.dart';
import '../services/map.dart';

class ControlPanel extends StatefulWidget {
  const ControlPanel({super.key});

  @override 
  State<ControlPanel> createState() => ControlPanelState();
}

class ControlPanelState extends State<ControlPanel> {
  final PanelSettingsService settingsService = PanelSettingsService();
  bool powerOn = false;
  bool lockOn = false;
  bool cameraOn = false;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadSettings();
  }

  Future<void> loadSettings() async {
    final data = await settingsService.loadSettings();

    setState(() {
      powerOn = data["power"]!;
      lockOn = data["lock"]!;
      cameraOn = data["camera"]!;
      isLoading = false;
    });
  }

  void save() {
    settingsService.saveSettings(
      powerOn: powerOn,
      lockOn: lockOn,
      cameraOn: cameraOn,
    );
  }

  void togglePower() {
    setState(() => powerOn = !powerOn);
    save();
  }

  void toggleLock() {
    setState(() => lockOn = !lockOn);
    save();
  }

  void showMap() {
    showModalBottomSheet(  
      context: context,
      isScrollControlled: true,
      builder: (_) => const TrackLocation(),
    );
  }

  void toggleCamera() {
    setState(() => cameraOn = !cameraOn);
    save();
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(
        child: CircularProgressIndicator()
      );
    }
    
    return Container(
      padding: const EdgeInsets.all(12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          ControlButton(
            icon: Icons.power_settings_new, 
            onPressed: togglePower,
            isOn: powerOn,
          ),
          ControlButton(
            icon: Icons.lock,
            onPressed: toggleLock,
            isOn: lockOn,
          ),
          ControlButton( 
            icon: Icons.map,
            onPressed: showMap,
            isOn: false,
          ),
          ControlButton(
            icon: Icons.camera,
            onPressed: toggleCamera, 
            isOn: cameraOn,
          )
        ],
      )
    );
  }
}