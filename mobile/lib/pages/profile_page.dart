import 'package:flutter/material.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<ProfilePage> {
  @override
  void initState() {
    super.initState();
    print("Hello"); // sera affiché dans la console quand la page est ouverte
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Explore Page")),
      body: const Center(
        child: Text("Explore Page Content"),
      ),
    );
  }
}
