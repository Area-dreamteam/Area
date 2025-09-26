import 'package:flutter/material.dart';
import 'scaffolds/mainScaffold.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AREA HomePage',
      theme: ThemeData(primarySwatch: Colors.blue, useMaterial3: true),
      home: const MainPage(),
      debugShowCheckedModeBanner: false,
    );
  }
}
