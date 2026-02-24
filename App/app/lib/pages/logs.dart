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
        actions: [
          IconButton(
            icon: const Icon(Icons.delete, color: Colors.red),
            onPressed: () async {
              final confirmation = await showDialog<bool>( 
                context: context,
                builder: (_) => AlertDialog(
                  title: const Text("Delete logs"),
                  content: const Text("This will permanently delete all logs."),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context, false), 
                      child: const Text("Cancel", style: TextStyle(color: Colors.black)),
                    ),
                    TextButton(
                      onPressed: () => Navigator.pop(context, true), 
                      child: const Text("Delete", style: TextStyle(color: Colors.black)),
                    ),
                  ],
                ),
              );

              if (confirmation == true) {
                //await LogService.deleteLogs();
                try {
                  await LogService.deleteLogs();
                  print("RPC success");
                } catch (e) {
                  print("RPC error: $e");
                }
              }
            },
          )
        ],
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