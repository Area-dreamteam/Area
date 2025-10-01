import 'package:flutter/material.dart';
import '../widgets/navbar.dart';
import '../pages/account.dart';
import '../pages/my_service.dart';
import '../scaffolds/main_scaffold.dart';

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});
  final String userName = 'boris cheng';
  final List<String> menuOptions = const ['Account', 'My services', 'Sign out'];

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final paddingTop = MediaQuery.of(context).padding.top;
    final availableHeight =
        screenHeight - kBottomNavigationBarHeight - paddingTop;

    return Scaffold(
      backgroundColor: Colors.black,
      body: SingleChildScrollView(
        child: SizedBox(
          height: availableHeight,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [_menu(context)],
          ),
        ),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 4),
    );
  }

  Widget _menu(BuildContext context) {
    return Center(
      child: Column(
        children: menuOptions.map((title) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: SizedBox(
              width: 300,
              child: ListTile(
                title: Text(
                  title,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 22.0,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                onTap: () {
                  _navigateToPage(context, title);
                },
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  void _navigateToPage(BuildContext context, String pageTitle) {
    if (pageTitle == 'Account') {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const Account()),
      );
    } else if (pageTitle == 'My services') {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const MyService()),
      );
    } else if (pageTitle == 'Sign out') {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const MainPage()),
      );
    }
  }
}
