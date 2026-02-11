import 'package:flutter/material.dart';
import '../widgets/navigation.dart';
import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import '../services/firebase.dart';
import '../widgets/panel.dart';
import 'package:firebase_database/firebase_database.dart';
import 'dart:math';
import 'package:webview_flutter/webview_flutter.dart';
import '../services/mic.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final FirebaseService firebase = FirebaseService();
  final AudioPlayer player = AudioPlayer();
  final backendDatabase = FirebaseDatabase.instance.ref("BackendMessages");
  late final WebViewController streamController;
  final MicStreamer micStreamer = MicStreamer();

  StreamSubscription? subscription;
  StreamSubscription? cameraSubscription;
  StreamSubscription? location;
  StreamSubscription? micSubscription;
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
  bool cameraOn = false;
  bool streamLoaded = false;
  bool micOn = false;

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

    micSubscription = firebase.listenToMic().listen((micValue) async {
      if (micValue && !micOn) {
        await micStreamer.startRecording();
      } else if (!micValue && micOn) {
        await micStreamer.stopRecording();
      }

      setState(() {
        micOn = micValue;
      });
    });

    streamController = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadHtmlString("""
        <!DOCTYPE html>
        <html>
          <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
              html, body {
                margin: 0;
                padding: 0;
                background: black;
                height: 100%;
                overflow: hidden;
              }
              img {
                width: 100%;
                height: 100%;
                object-fit: contain;
              }
            </style>
          </head>
          <body>
            <img src="http://192.168.1.94:8000/Stream" />
          </body>
      """);

    cameraSubscription = firebase.listenToCamera().listen((cameraValue) {
      setState(() {
        cameraOn = cameraValue;
      });
    });

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
    cameraSubscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Status"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      bottomNavigationBar: const AppNavigationBar(currentPage: 0),
      body: Column(
        children: [
          Expanded(
            child: Column(
              children: [
                SizedBox(
                  height: MediaQuery.of(context).size.width * 0.6,
                  child: cameraOn ? WebViewWidget(controller: streamController) : Container(
                    color: Colors.black,
                    child: const Center(
                      child: Text(
                        "No recording available",
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                  ),
                ),

                const SizedBox(height: 12),
                Text(
                  receivedMessage,
                  style: const TextStyle(fontSize: 18),
                  textAlign: TextAlign.center,
                ),
              ]
            ),
          ),
          const ControlPanel(),
        ],
      ),
    );
  }
}
