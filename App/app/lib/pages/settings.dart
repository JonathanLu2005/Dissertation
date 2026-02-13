import 'package:flutter/material.dart'; 
import '../widgets/navigation.dart';
import '../widgets/tiles.dart';
import '../pages/notificationSettings.dart';
import '../pages/modelSettings.dart';
import '../pages/lockSettings.dart';

class SettingsPage extends StatelessWidget { 
  const SettingsPage({super.key}); 

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Settings"),
        backgroundColor: const Color(0xFFEFF2F1)
      ), 
      bottomNavigationBar: const AppNavigationBar(currentPage: 1),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: GridView.count(  
          crossAxisCount: 3,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          children: [
            Tiles(
              icon: Icons.laptop,
              label: "Model",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const ModelSettingsPage(),),
                );
              },
            ),

            Tiles(
              icon: Icons.notifications,
              label: "Alarms",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const NotificationSettingsPage(),),
                );
              },
            ),

            Tiles(
              icon: Icons.lock_person_rounded,
              label: "Locking",
              onTap: () {
                Navigator.push( 
                  context, 
                  MaterialPageRoute(builder: (_) => const LockSettingsPage(),),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}