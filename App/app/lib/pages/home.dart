import 'package:flutter/material.dart';
import '../widgets/navigation.dart';
import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import '../services/firebase.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final FirebaseService firebase = FirebaseService();
  final AudioPlayer player = AudioPlayer();

  StreamSubscription? subscription;
  bool receivedAlert = false;
  String receivedMessage = "—";
  StreamSubscription? settingsSubscription;
  bool alertsEnabled = true; 
  double alertVolume = 1.0;

  @override
  void initState() {
    super.initState();

    settingsSubscription = firebase.listenToSettings().listen((settings) {
      setState(() {
        alertsEnabled = settings["Enabled"];
        alertVolume = settings["Volume"];
      });
    });

    subscription = firebase.listenToBackend().listen((transmissionData) async {
      final bool alert = transmissionData["Alert"];
      final String message = transmissionData["Message"];

      if (alert && !receivedAlert && alertsEnabled) {
        await player.setVolume(alertVolume);
        await player.play(AssetSource("alert.mp3"));
      }

      setState(() {
        receivedAlert = alert;
        receivedMessage = message;
      });
    });
  }

  @override
  void dispose() {
    subscription?.cancel();
    settingsSubscription?.cancel();
    player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Status")),
      bottomNavigationBar: const AppNavigationBar(currentPage: 0),
      body: Center(
        child: Text(receivedMessage, style: const TextStyle(fontSize: 18),),
      ),
    );
  }
}
