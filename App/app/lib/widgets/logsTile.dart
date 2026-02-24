import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class LogsTile extends StatelessWidget {
  final Map<String, dynamic> log;

  const LogsTile({super.key, required this.log});

  @override
  Widget build(BuildContext context) {
    DateTime timestamp = DateTime.parse(log['created_at']);
    String time = DateFormat('yyyy-MM-dd HH:mm:ss').format(timestamp);

    return InkWell( 
      onTap: () { 
        showDialog( 
          context: context, 
          barrierDismissible: true, 
          builder: (_) => AlertDialog(
            title: const Text('Security Log'),
            content: Text(log['message']),
          ),
        );
      },
      borderRadius: BorderRadius.circular(12),
      child: Container(  
        margin: const EdgeInsets.symmetric(vertical: 6, horizontal: 12),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration( 
          color: Theme.of(context).colorScheme.surfaceVariant,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black12,
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Icon(Icons.security, size: 28),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'Security Log',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
            ),
            Text(
              time,
              style: const TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}