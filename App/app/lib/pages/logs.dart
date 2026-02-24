import 'package:flutter/material.dart';
import '../services/TTS.dart';
import '../services/logsRetrieval.dart';
import '../widgets/logsTile.dart';
import '../widgets/navigation.dart';

class LogsPage extends StatelessWidget {
  const LogsPage({super.key});

  @override 
  Widget build(BuildContext context) {
    TTSService.pageAnnouncement("Logs");

    return Scaffold(
      appBar: AppBar(
        title: const Text("Security Logs"),
        backgroundColor: const Color(0xFFEFF2F1),
      ),
      bottomNavigationBar: const AppNavigationBar(currentPage: 2),
      body: StreamBuilder<List<Map<String, dynamic>>>(
        stream: LogService.retrieveAllLogs(),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }

          final logs = snapshot.data!;

          if (logs.isEmpty) {
            return const Center(child: Text("No logs available"));
          }

          return ListView.builder(
            itemCount: logs.length,
            itemBuilder: (context, index) {
              return LogsTile(log: logs[index]);
            },
          );
        },
      ),
    );
  }
}