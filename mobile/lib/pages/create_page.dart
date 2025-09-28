import 'package:flutter/material.dart';
import '../widgets/navbar.dart';

class CreatePage extends StatefulWidget {
  const CreatePage({super.key});

  @override
  State<CreatePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<CreatePage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: const Center(child: Text("Explore Page Content")),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 2),
    );
  }
}
