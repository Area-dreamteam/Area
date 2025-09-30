import 'package:flutter/material.dart';
import '../widgets/navbar.dart';
import '../widgets/create_card.dart';

class CreatePage extends StatelessWidget {
  const CreatePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text('Create', style: TextStyle(fontSize: 30)),
      ),
      body: Center(
        child: Column(
          children: [
            CreateCard(
              title: 'If This',
              onTap: () {
              },
            ),
            SizedBox(height: 20),
            CreateCard(
              title: 'Then That',
              onTap: () {
              },
            ),
          ],
        ),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 2),
    );
  }
}
