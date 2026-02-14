import 'package:flutter/material.dart';

class InfoRow extends StatelessWidget {
  final IconData icon; 
  final String sentence;

  const InfoRow( 
    this.icon, 
    this.sentence, 
    {super.key}
  );

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        children: [
          Icon(icon, size: 20),
          const SizedBox(width: 12),
          Expanded(child: Text(sentence)),
        ],
      ),
    );
  }
}