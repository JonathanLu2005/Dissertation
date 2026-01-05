import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late DatabaseReference db;
  String sentMessage = "—";
  String receivedMessage = "—";

  @override
  void initState() {
    super.initState();
    db = FirebaseDatabase.instance.ref();

    Timer.periodic(const Duration(seconds: 3), (_) async {
      const message = "Hello from Flutter";
      await db.child("AppMessages").set(message);

      final snapshot = await db.child("BackendMessages").get();

      setState(() {
        sentMessage = message;
        receivedMessage = snapshot.value?.toString() ?? "null";
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text("Initial App")),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("Sent to backend:", style: Theme.of(context).textTheme.titleMedium),
              Text(sentMessage, style: const TextStyle(fontSize: 18)),
              const SizedBox(height: 20),
              Text("Received from backend:", style: Theme.of(context).textTheme.titleMedium),
              Text(receivedMessage, style: const TextStyle(fontSize: 18)),
            ],
          ),
        ),
      ),
    );
  }
}
