import 'package:flutter/material.dart'; 
import '../widgets/navigation.dart';
import '../widgets/tiles.dart';
import '../pages/notificationSettings.dart';

class SettingsPage extends StatelessWidget { 
  const SettingsPage({super.key}); 

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Settings")), 
      bottomNavigationBar: const AppNavigationBar(currentPage: 1),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: GridView.count(  
          crossAxisCount: 3,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
          children: [
            Tiles(
              icon: Icons.notifications,
              label: "Alerts",
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const NotificationSettingsPage(),),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}