import 'package:flutter/material.dart';

class ControlButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onPressed;
  final bool isOn;

  const ControlButton({
    super.key,
    required this.icon, 
    required this.onPressed,
    required this.isOn,
  });

  @override
  Widget build(BuildContext context) {
    return IconButton( 
      icon: Icon(
        icon, 
        size: 28,
        color: isOn ? Colors.green : Colors.grey,
      ),
      onPressed: onPressed,
    );
  }
}