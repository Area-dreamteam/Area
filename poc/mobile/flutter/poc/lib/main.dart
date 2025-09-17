import 'package:flutter/material.dart';
import 'screens/login.dart';
import 'screens/register.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(debugShowCheckedModeBanner: false, home: HomePage());
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start, // éléments en haut
        children: [
          SizedBox(height: 100), // gap top (comme margin-top)
          Row(
            mainAxisAlignment: MainAxisAlignment.center, // centrer les cercles
            children: [
              ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  fixedSize: const Size(150, 150),
                  shape: const CircleBorder(),
                ),
                child: const Text('Register', style: TextStyle(fontSize: 24)),
              ),

              SizedBox(width: 40), // espace entre les deux cercles

              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => RegisterPage()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  fixedSize: const Size(150, 150),
                  shape: const CircleBorder(),
                ),
                child: const Text('Register', style: TextStyle(fontSize: 24)),
              ),

              SizedBox(width: 40),

              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => LoginPage()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  fixedSize: const Size(150, 150),
                  shape: const CircleBorder(),
                ),
                child: const Text('Login', style: TextStyle(fontSize: 24)),
              ),

              SizedBox(width: 40),

              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => LoginPage()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  fixedSize: const Size(150, 150),
                  shape: const CircleBorder(),
                ),
                child: const Text('Login', style: TextStyle(fontSize: 24)),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
