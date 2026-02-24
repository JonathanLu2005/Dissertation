import 'package:flutter/material.dart';
import '../services/TTS.dart';
import '../services/logsRetrieval.dart';
import '../widgets/logsTile.dart';
import '../widgets/navigation.dart';

class LogsPage extends StatefulWidget {
  const LogsPage({super.key});

  @override 
  State<LogsPage> createState() => _LogsPageState();
}

class _LogsPageState extends State<LogsPage> {
  List<Map<String, dynamic>> finalLogs = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    TTSService.pageAnnouncement("Logs");
    fetchLogs();
  }

  Future<void> fetchLogs() async {
    final logs = await LogService.retrieveAllLogs();
    setState(() {
      finalLogs = logs;
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Security Logs"),
        backgroundColor: const Color(0xFFEFF2F1)
      ),
      bottomNavigationBar: const AppNavigationBar(currentPage: 3),
      body: isLoading ? const Center(child: CircularProgressIndicator()) : ListView.builder(
        itemCount: finalLogs.length,
        itemBuilder: (context, index) {
          return LogsTile(log: finalLogs[index]);
        },
      ),
    );
  }
}