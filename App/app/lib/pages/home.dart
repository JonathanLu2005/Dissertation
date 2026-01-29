import 'package:flutter/material.dart';
import '../widgets/navigation.dart';
import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import '../services/firebase.dart';
import '../widgets/panel.dart';
import 'package:firebase_database/firebase_database.dart';
import 'dart:math';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final FirebaseService firebase = FirebaseService();
  final AudioPlayer player = AudioPlayer();
  final backendDatabase = FirebaseDatabase.instance.ref("BackendMessages");

  StreamSubscription? subscription;
  StreamSubscription? location;
  bool receivedAlert = false;
  String receivedMessage = "—";
  StreamSubscription? settingsSubscription;
  bool alertsEnabled = true; 
  double alertVolume = 1.0;
  bool powerOn = false;
  Timer? timeCheck;
  DateTime? lastTimeCheck;
  bool trackLocation = false;
  double trackedLatitude = 0;
  double trackedLongitude = 0;

  Future<void> alarm() async {
    await player.setVolume(alertVolume);
    await player.play(AssetSource("alert.mp3"));
  }

  void checkConnection(Timer time) {
    if (lastTimeCheck == null) return;

    final current = DateTime.now();
    final difference = (current.difference(lastTimeCheck!)).inSeconds;
    
    if (difference > 20) {
      if (mounted) {
        setState(() {
          receivedMessage = "Backend isn't connected";
        });
      }

      trackLocation = false;

      backendDatabase.update({
        "message": receivedMessage
      });

      if (powerOn && alertsEnabled) {
        alarm();
      }
    }
  }

  @override
  void initState() {
    super.initState();

    settingsSubscription = firebase.listenToSettings().listen((settings) {
      setState(() {
        alertsEnabled = settings["enabled"] as bool? ?? true;
        alertVolume = (settings["volume"] as num?)?.toDouble() ?? 1.0;
      });
    });

    subscription = firebase.listenToBackend().listen((transmissionData) async {
      final bool alert = transmissionData["alert"] as bool? ?? false;
      final String message = transmissionData["message"] as String? ?? "-";
      final int? messageTimestamp = transmissionData["timestamp"] as int?;

      if (messageTimestamp != null) {
        lastTimeCheck = DateTime.fromMillisecondsSinceEpoch(messageTimestamp * 1000);
      }

      if (alert && !receivedAlert && alertsEnabled && powerOn) {
        alarm();
      }

      setState(() {
        receivedAlert = alert;
        receivedMessage = message;
      });
    });

    location = firebase.listenToLocation().listen((locationData) async {
      final double? latitude = locationData["latitude"] as double?;
      final double? longitude = locationData["longitude"] as double?;

      if (latitude == null || longitude == null) return;

      if (!trackLocation) {
        trackedLatitude = latitude;
        trackedLongitude = longitude;
        trackLocation = true;
      } else {
        const Radius = 6371000;
        final Phi1 = trackedLatitude * pi / 180;
        final Phi2 = latitude * pi / 180;
        final DistancePhi = (latitude - trackedLatitude) * pi / 180;
        final DistanceLambda = (longitude - trackedLongitude) * pi / 180;

        final Calculation = sin(DistancePhi / 2) * sin(DistancePhi / 2) + cos(Phi1) * cos(Phi2) * sin(DistanceLambda / 2) * sin(DistanceLambda / 2);
        final Result = 2 * atan2(sqrt(Calculation), sqrt(1-Calculation)) * Radius;
        if (Result > 4.2) {
          receivedMessage = "Suspicious activity detected";
          backendDatabase.update({
            "message": receivedMessage
          });

          if (powerOn && alertsEnabled) {
            alarm();
          }
        }
      }
    });

    timeCheck = Timer.periodic(const Duration(seconds: 1), checkConnection);
  }

  @override
  void dispose() {
    subscription?.cancel();
    location?.cancel();
    settingsSubscription?.cancel();
    timeCheck?.cancel();
    player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Status")),
      bottomNavigationBar: const AppNavigationBar(currentPage: 0),
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: Text(
                receivedMessage,
                style: const TextStyle(fontSize: 18),
              ),
            ),
          ),
          const ControlPanel(),
        ],
      ),
    );
  }
}
