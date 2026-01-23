import 'package:flutter/material.dart';
import 'controlButton.dart';
import 'package:firebase_database/firebase_database.dart';

class ControlPanel extends StatefulWidget {
  const ControlPanel({super.key});

  @override 
  State<ControlPanel> createState() => ControlPanelState();
}

class ControlPanelState extends State<ControlPanel> {
  bool powerOn = false;
  final database = FirebaseDatabase.instance.ref("RemoteControl/Power");

  void togglePower() {
    setState(() => powerOn = !powerOn);
    database.set(powerOn);
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
        ],
      )
    );
  }
}