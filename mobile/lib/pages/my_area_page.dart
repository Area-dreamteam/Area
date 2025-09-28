import 'package:flutter/material.dart';
import '../widgets/navbar.dart';

class AreaPage extends StatefulWidget {
  const AreaPage({super.key});

  @override
  State<AreaPage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<AreaPage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: const Center(
        child: Text("My Area", style: TextStyle(fontSize: 24)),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 3),
    );
  }
}
