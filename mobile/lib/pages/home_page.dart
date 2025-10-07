import 'package:flutter/material.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/widgets/card.dart';

class TabWithCount extends StatelessWidget {
  final int count;

  const TabWithCount({super.key, required this.count});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.blue,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        "All ($count)",
        style: const TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final double horizontalPadding = 18;

  final List<Map<String, dynamic>> items = [
    {
      'color': const Color(0xFFE86E66),
      'icon': Icons.local_florist,
      'title': "Save screenshots to a\nseparate iOS album",
      'byText': "by IFTTT",
      'usersText': "36k",
    },
    {
      'color': const Color(0xFF2B2140),
      'icon': Icons.public,
      'title': "Image of the day from\nNASA → iOS Reading List",
      'byText': "by IFTTT",
      'usersText': "33k",
    },
    {
      'color': const Color(0xFF2B2140),
      'icon': Icons.public,
      'title': "Image of the day from\nNASA → iOS Reading List",
      'byText': "by IFTTT",
      'usersText': "33k",
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.only(bottom: 120),
          child: Padding(
            padding: EdgeInsets.symmetric(horizontal: horizontalPadding),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 8),
                TabWithCount(count: items.length),
                const SizedBox(height: 22),

                for (final item in items) ...[
                  BigCard(
                    color: item['color'] as Color,
                    icon: item['icon'] as IconData,
                    title: item['title'] as String,
                    byText: item['byText'] as String,
                    usersText: item['usersText'] as String,
                  ),
                  const SizedBox(height: 18),
                ],
                const SizedBox(height: 220),
              ],
            ),
          ),
        ),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 0),
    );
  }
}
