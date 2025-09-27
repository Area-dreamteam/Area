import 'package:flutter/material.dart';

class CreatePage extends StatefulWidget {
  const CreatePage({super.key});

  @override
  State<CreatePage> createState() => _ExplorePageState();
}

class _ExplorePageState extends State<CreatePage> {
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
