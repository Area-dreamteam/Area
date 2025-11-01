import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

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
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Material(
        borderRadius: BorderRadius.circular(14),
        elevation: 4,
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: onTap,
          child: Container(
            decoration: BoxDecoration(
              color: color,
              borderRadius: BorderRadius.circular(14),
            ),
            padding: const EdgeInsets.all(16),
            width: double.infinity,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                ConstrainedBox(
                  constraints: const BoxConstraints(maxHeight: 42),
                  child: MarkdownBody(
                    data: description,
                    styleSheet: MarkdownStyleSheet(
                      p: const TextStyle(
                        color: Colors.white70,
                        fontSize: 14,
                      ),
                      a: const TextStyle(
                        color: Colors.lightBlue,
                        decoration: TextDecoration.underline,
                      ),
                      strong: const TextStyle(
                        color: Colors.white70,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}