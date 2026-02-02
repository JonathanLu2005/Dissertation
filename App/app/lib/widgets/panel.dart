import 'package:flutter/material.dart';
import 'controlButton.dart';
import 'package:firebase_database/firebase_database.dart';
import '../services/map.dart';

class ControlPanel extends StatefulWidget {
  const ControlPanel({super.key});

  @override 
  State<ControlPanel> createState() => ControlPanelState();
}

class ControlPanelState extends State<ControlPanel> {
  bool powerOn = false;
  final databasePower = FirebaseDatabase.instance.ref("RemoteControl/power");

  bool lockOn = false;
  final databaseLock = FirebaseDatabase.instance.ref("RemoteControl/lock");

  bool cameraOn = false;
  final databaseCamera = FirebaseDatabase.instance.ref("RemoteControl/camera");

  void togglePower() {
    setState(() => powerOn = !powerOn);
    databasePower.set(powerOn);
  }

  void toggleLock() {
    setState(() => lockOn = !lockOn);
    databaseLock.set(lockOn);
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
    databaseCamera.set(cameraOn);
  }

  @override
  Widget build(BuildContext context) {
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