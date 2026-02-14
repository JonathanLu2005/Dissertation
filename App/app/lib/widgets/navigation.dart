import 'package:flutter/material.dart';

class AppNavigationBar extends StatelessWidget {
  final int currentPage;
  const AppNavigationBar({super.key, required this.currentPage});

  void _onClick(BuildContext context, int receivedPage) {
    if (receivedPage == currentPage) return;

    switch (receivedPage) {
      case 0:
        Navigator.pushReplacementNamed(context, "/");
        break;
      case 1:
        Navigator.pushReplacementNamed(context, "/settings");
        break;
      case 2:
        Navigator.pushReplacementNamed(context, "/manual");
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      backgroundColor: const Color(0xFFEFF2F1),
      unselectedItemColor: const Color(0xFF363835),
      selectedItemColor: const Color(0xFF1D7303),
      currentIndex: currentPage,
      onTap: (i) => _onClick(context, i),
      items: const [
        BottomNavigationBarItem(
          icon: Icon(Icons.home),
          label: "Home",
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.settings),
          label: "Settings",
        ),
        BottomNavigationBarItem( 
          icon: Icon(Icons.book),
          label: "Manual"
        ),
      ],
    );
  }
}
