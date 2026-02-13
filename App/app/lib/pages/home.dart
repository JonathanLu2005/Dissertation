import 'package:flutter/material.dart';
import '../widgets/navigation.dart';
import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import '../services/firebase.dart';
import '../widgets/panel.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../services/mic.dart';
import '../services/locationTracker.dart';
import '../services/streamService.dart';
import '../services/loadPanelSettings.dart';
import 'package:flutter/services.dart';
import '../services/TTS.dart';

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
  final LocationService locationTracker = LocationService();
  final PanelSettingsService panelService = PanelSettingsService();

  StreamSubscription? powerSubscription;
  StreamSubscription? subscription;
  StreamSubscription? cameraSubscription;
  StreamSubscription? location;
  StreamSubscription? micSubscription;
  String receivedMessage = "—";
  StreamSubscription? settingsSubscription;
  bool alertsEnabled = true; 
  bool vibrationEnabled = true;
  double alertVolume = 1.0;
  Timer? timeCheck;
  DateTime? lastTimeCheck;
  bool cameraOn = false;
  bool streamLoaded = false;
  bool micOn = false;
  bool powerOn = false;

  Future<void> alarm() async {
    await player.setVolume(alertVolume);
    await player.play(AssetSource("alert.mp3"));
  }

  Future<void> vibrate() async {
    HapticFeedback.heavyImpact();
    await Future.delayed(Duration(milliseconds: 50));
    HapticFeedback.heavyImpact();
    await Future.delayed(Duration(milliseconds: 50));
    HapticFeedback.heavyImpact();
  }

  void checkConnection(Timer time) {
    if (lastTimeCheck == null) return;

    final current = DateTime.now();
    final difference = (current.difference(lastTimeCheck!)).inSeconds;
    
    if (difference > 20) {
      if (mounted) {
        setState(() {
          receivedMessage = "Backend isn't connected - internet or laptop might be off.";
        });
      }

      locationTracker.reset();

      backendDatabase.update({
        "message": receivedMessage
      });

      if (powerOn) {
        if (alertsEnabled) {
          alarm();
        }

        if (vibrationEnabled) {
          vibrate();
        }
      }
    }
  }

  @override
  void initState() {
    super.initState();

    TTSService.pageAnnouncement("Home");

    powerSubscription = panelService.powerValue().listen((powerValue) {
      setState(() {
        powerOn = powerValue;
      });
    });

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

    streamController = StreamService.build("http://172.25.11.164:8000/Stream",);

    cameraSubscription = firebase.listenToCamera().listen((cameraValue) {
      setState(() {
        cameraOn = cameraValue;
      });
    });

    settingsSubscription = firebase.listenToSettings().listen((settings) {
      setState(() {
        alertsEnabled = settings["alert"] as bool? ?? true;
        vibrationEnabled = settings["vibration"] as bool? ?? true;
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

      if (alert && powerOn) {
        if (alertsEnabled) {
          alarm();
        }
        
        if (vibrationEnabled) {
          vibrate();
        }
      }

      setState(() {
        receivedMessage = message;
      });
    });

    location = firebase.listenToLocation().listen((locationData) async {
      locationTracker.processLocation( 
        locationData: locationData,
        powerOn: powerOn,
        alertsEnabled: alertsEnabled,
        vibrationEnabled: vibrationEnabled,
        alarm: alarm,
        vibrate: vibrate,
        onMessage: (message) {
          setState(() => receivedMessage = message); 
        },
        backendUpdate: backendDatabase.update,
      );
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
    powerSubscription?.cancel();
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
