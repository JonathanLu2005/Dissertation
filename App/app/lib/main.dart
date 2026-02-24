import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'pages/home.dart';
import 'pages/settings.dart';
import 'pages/manual.dart';
import 'pages/gallery.dart';
import '../global/accessibilityListener.dart';
import '../global/ipListener.dart';
import '../services/cloud.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  await SupabaseService.init();
  AccessibilityListener.init();
  IPListener.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        scaffoldBackgroundColor: const Color(0xFFEFF2F1),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomePage(), 
        '/settings': (context) => const SettingsPage(),
        '/gallery': (context) => const GalleryPage(),
        '/manual': (context) => const ManualPage(),
      },
    );
  }
}