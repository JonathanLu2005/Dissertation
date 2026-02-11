import 'package:flutter/material.dart';

class InformationButton extends StatelessWidget {
  final String title;
  final String description;

  const InformationButton({
    super.key,
    required this.title, 
    required this.description,
  });

  void displayInformation(BuildContext context) {
    showDialog(
      context: context, 
      builder: (_) => AlertDialog( 
        title: Text(title), 
        content: Text(description),
        backgroundColor: const Color(0xFFEFF2F1),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text(""),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.info_outline),
      color: const Color(0xFF6B7280),
      onPressed: () => displayInformation(context),
    );
  }
}