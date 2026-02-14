import 'package:flutter/material.dart';

class ExpansionTiles extends StatefulWidget {
  final String title;
  final String prelude;
  final List<Widget> children;

  const ExpansionTiles({
    super.key,
    required this.title,
    required this.prelude,
    required this.children,
  });

  @override
  State<ExpansionTiles> createState() => _ExpansionTilesState();
}

class _ExpansionTilesState extends State<ExpansionTiles> {
  static _ExpansionTilesState? currentlyOpen;
  bool expanded = false;

  void toggle() {
    if (currentlyOpen != null && currentlyOpen != this) {
      currentlyOpen!.collapse();
    }

    setState(() {
      expanded = !expanded;
    });

    currentlyOpen = expanded ? this : null;
  }

  void collapse() {
    setState(() => expanded = false);
  }

  @override 
  Widget build(BuildContext context) {
    return Column(
      children: [
        InkWell( 
          onTap: toggle,
          borderRadius: BorderRadius.circular(12),
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration( 
              borderRadius: BorderRadius.circular(12),
              color: Theme.of(context).colorScheme.surfaceVariant,
            ),
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    widget.title,
                    style: const TextStyle( 
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
                Icon(expanded ? Icons.expand_less : Icons.expand_more),
              ],
            ),
          ),
        ),

        if (expanded)
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  widget.prelude, 
                  style: const TextStyle(fontSize: 14),
                ),
                const SizedBox(height: 12),
                ...widget.children,
              ],
            ),
          ),
        const SizedBox(height: 12),
      ],
    );
  }
}