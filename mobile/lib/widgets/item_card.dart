import 'package:flutter/material.dart';

class ItemCard extends StatelessWidget {
  final String name;
  final String description;
  final Color color;
  final VoidCallback onTap;

  const ItemCard({
    super.key,
    required this.name,
    required this.description,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final bool isDark = color.computeLuminance() < 0.5;
    final Color textColor = isDark ? Colors.white : Colors.black;
    final Color descriptionColor = isDark ? Colors.white70 : Colors.black87;

    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Semantics(
        label: "$name, $description",
        button: true,
        enabled: true,
        child: Material(
          borderRadius: BorderRadius.circular(14),
          elevation: 4,
          color: color,
          child: InkWell(
            borderRadius: BorderRadius.circular(14),
            onTap: onTap,
            child: Container(
              padding: const EdgeInsets.all(16),
              width: double.infinity,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    name,
                    style: theme.textTheme.titleMedium?.copyWith(
                      color: textColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    description,
                    style: theme.textTheme.bodyMedium?.copyWith(
                      color: descriptionColor,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}