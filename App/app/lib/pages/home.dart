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

  @override
  void initState() {
    super.initState();

    subscription = firebase.listenToBackend().listen((transmissionData) async {
      final bool alert = transmissionData["alert"];
      final String message = transmissionData["message"];

      if (alert && !receivedAlert) {
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
