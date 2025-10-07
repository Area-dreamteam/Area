import 'package:flutter/material.dart';

class BigCard extends StatelessWidget {
  final Color color;
  final IconData icon;
  final String title;
  final String byText;
  final VoidCallback? onTap;
  final VoidCallback? onDelete;

  const BigCard({
    super.key,
    required this.color,
    required this.icon,
    required this.title,
    required this.byText,
    this.onTap,
    this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    final textColor = Colors.white;

    final cardContent = Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(12),
      ),
      width: double.infinity,
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
              if (onDelete != null)
                IconButton(
                  icon: const Icon(Icons.delete_outline, color: Colors.white70),
                  onPressed: onDelete,
                ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            title,
            style: TextStyle(
              color: textColor,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            byText,
            style: TextStyle(fontSize: 14),
          ),
        ],
      ),
    );

    if (onTap != null) {
      return InkWell(
        onTap: onTap,
        child: Material(
          color: Colors.transparent,
          elevation: 2,
          borderRadius: BorderRadius.circular(12),
          child: cardContent,
        ),
      );
    }

    return Material(
      color: Colors.transparent,
      elevation: 2,
      borderRadius: BorderRadius.circular(12),
      child: cardContent,
    );
  }
}
