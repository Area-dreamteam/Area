import 'package:flutter/material.dart';
import '../widgets/navbar.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<ProfilePage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: const Center(child: Text("Explore Page Content")),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 4),
    );
  }
}
