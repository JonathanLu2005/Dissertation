import 'package:flutter/material.dart';
import '../services/TTS.dart';
import '../widgets/navigation.dart';
import '../widgets/expansionTiles.dart';
import '../widgets/infoRow.dart';

class ManualPage extends StatefulWidget {
  const ManualPage({super.key});

  @override 
  State<ManualPage> createState() => _ManualPageState();
}

class _ManualPageState extends State<ManualPage> {
  @override
  void initState() {
    super.initState();
    TTSService.pageAnnouncement("Manual");
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Manual"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      bottomNavigationBar: const AppNavigationBar(currentPage: 3),
      body: Padding(
        padding: const EdgeInsets.all(16),

        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "System Overview", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),

            Expanded(
              child: ListView(
                children: [
                  ExpansionTiles( 
                    title: "Camera Detection",
                    prelude: "Under your choosing, the camera can detect and inform you regarding:",
                    children: const [
                      InfoRow(Icons.image, "Significant background changes"),
                      InfoRow(Icons.people, "Anyone in close proximity"),
                      InfoRow(Icons.masks, "Anyone wearing a mask"),
                      InfoRow(Icons.access_time, "Anyone loitering"),
                    ],
                  ),

                  ExpansionTiles(
                    title: "Physical Detection",
                    prelude: "The system will detect physical alteractions, including:",
                    children: const [
                      InfoRow(Icons.usb, "USB being removed or added"),
                      InfoRow(Icons.mouse, "Mouse being used"),
                      InfoRow(Icons.keyboard, "Keyboard being used"),
                    ],
                  ),

                  ExpansionTiles(
                    title: "Mitigation Strategies",
                    prelude: "If anything suspicious occurs, you are provided a range of strategies, including:",
                    children: const [
                      InfoRow(Icons.camera, "Access what the laptop sees"),
                      InfoRow(Icons.lock, "Manual or automatic locking"),
                      InfoRow(Icons.map, "Track laptop location"),
                      InfoRow(Icons.mic, "Speak to any perpetrators"),
                    ],
                  ),

                  ExpansionTiles( 
                    title: "Mobile Interface",
                    prelude: "To navigate the system, you are provided with:",
                    children: const [
                      InfoRow(Icons.home, "Main system control"),
                      InfoRow(Icons.settings, "System configuration for detection and mitigations"),
                      InfoRow(Icons.accessibility_new, "Accessibility configurations"),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}