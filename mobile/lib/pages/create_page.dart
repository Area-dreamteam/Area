import 'package:flutter/material.dart';
import '../widgets/navbar.dart';
import '../widgets/create_card.dart';

class CreatePage extends StatelessWidget {
  const CreatePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            SizedBox(height: 60,),
            Title(color: Colors.black, child: Text('Create', style: TextStyle(fontSize: 50),)),
            SizedBox(height: 60,),
            CreateCard(title: 'If This', onTap: () {}),
            SizedBox(height: 20),
            CreateCard(title: 'Then That', onTap: () {}),
          ],
        ),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 2),
    );
  }
}
