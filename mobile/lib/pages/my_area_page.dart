import 'package:flutter/material.dart';

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
      appBar: AppBar(title: const Text("Explore Page")),
      body: const Center(
        child: Text("Explore Page Content"),
      ),
    );
  }
}
