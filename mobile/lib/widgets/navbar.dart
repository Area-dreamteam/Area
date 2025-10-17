import 'package:flutter/material.dart';
import 'package:mobile/pages/my_area.dart';
//import 'package:mobile/pages/explore_page.dart';
import 'package:mobile/pages/create_page.dart';
import 'package:mobile/pages/history.dart';
import 'package:mobile/pages/profile_page.dart';

class MyBottomNavigationBar extends StatelessWidget {
  final int selectedIndex;

  const MyBottomNavigationBar({super.key, this.selectedIndex = 0});

  void _navigate(BuildContext context, int index) {
    if (index == selectedIndex) return;

    final pages = [
      const MyAreaPage(),
   //   const ExplorePage(),
      const CreatePage(),
      const AreaPage(),
      const ProfilePage(),
    ];

    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => pages[index]),
    );
  }

  @override
  Widget build(BuildContext context) {
    return NavigationBar(
      selectedIndex: selectedIndex,
      onDestinationSelected: (index) => _navigate(context, index),
      indicatorColor: Colors.blue,
      destinations: const [
        NavigationDestination(
          icon: Icon(Icons.home_outlined),
          selectedIcon: Icon(Icons.home),
          label: 'Home',
        ),
        NavigationDestination(
          icon: Icon(Icons.search_outlined),
          selectedIcon: Icon(Icons.search),
          label: 'Explore',
        ),
        NavigationDestination(
          icon: Icon(Icons.create_outlined),
          selectedIcon: Icon(Icons.create),
          label: 'Create',
        ),
        NavigationDestination(
          icon: Icon(Icons.menu_outlined),
          selectedIcon: Icon(Icons.menu),
          label: 'My AREA',
        ),
        NavigationDestination(
          icon: Icon(Icons.account_circle_outlined),
          selectedIcon: Icon(Icons.account_circle),
          label: 'Profile',
        ),
      ],
    );
  }
}
