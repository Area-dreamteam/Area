// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';

class CreateCard extends StatelessWidget {
  final String title;
  final VoidCallback onTap;

  const CreateCard({
    super.key,
    required this.title,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.all(16),
        decoration: BoxDecoration(color: Colors.white),
        child: Row(
          children: [
            SizedBox(width: 16),
            Column(
              children: [
                Text(
                  title,
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
