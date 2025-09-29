import 'package:flutter/material.dart';

class BigCard extends StatelessWidget {
  final Color color;
  final IconData icon;
  final String title;
  final String byText;
  final String usersText;
  final VoidCallback? onTap; // optionnel: action au clic
  final double borderRadius;
  final double padding;

  const BigCard({
    super.key,
    required this.color,
    required this.icon,
    required this.title,
    required this.byText,
    required this.usersText,
    this.onTap,
    this.borderRadius = 14.0,
    this.padding = 22.0,
  });

  @override
  Widget build(BuildContext context) {
    final textColor = Colors.white;

    final card = Material(
      borderRadius: BorderRadius.circular(borderRadius),
      elevation: 2,
      child: Container(
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(borderRadius),
        ),
        width: double.infinity,
        padding: EdgeInsets.all(padding),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: const BoxDecoration(
                    color: Colors.white24,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(icon, color: textColor, size: 20),
                ),
                const Spacer(),
              ],
            ),
            const SizedBox(height: 18),
            Text(
              title,
              style: TextStyle(
                color: textColor,
                fontSize: 26,
                fontWeight: FontWeight.w800,
                height: 1.02,
              ),
            ),
            const SizedBox(height: 14),
            Text(
              byText,
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 18),
            Row(
              children: [
                const Icon(Icons.person, color: Colors.white70, size: 18),
                const SizedBox(width: 8),
                Text(
                  usersText,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
    if (onTap != null) {
      return InkWell(
        borderRadius: BorderRadius.circular(borderRadius),
        onTap: onTap,
        child: card,
      );
    }

    return card;
  }
}
