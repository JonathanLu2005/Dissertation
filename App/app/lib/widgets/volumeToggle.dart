import 'package:flutter/material.dart';

class VolumeSetting extends StatelessWidget {
  final double value;
  final ValueChanged<double> onChanged;

  const VolumeSetting({
    super.key,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Slider(
      min: 0,
      max: 1,
      divisions: 10,
      label: value.toStringAsFixed(1),
      value: value,
      onChanged: onChanged,
      activeColor: const Color(0xFF1D7303),
    );
  }
}