import 'package:flutter/material.dart';
import 'package:mobile/widgets/hex_convert.dart';

class ServiceCard extends StatelessWidget {
  final int id;
  final String name;
  final String? description;
  final String? imageUrl;
  final String? category;
  final String? colorHex;
  final VoidCallback? onTap;

  const ServiceCard({
    super.key,
    required this.id,
    required this.name,
    this.description,
    this.imageUrl,
    this.category,
    this.colorHex,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final cardColor = hexToColor(colorHex);
    final safeImageUrl = imageUrl ?? 'https://via.placeholder.com/20';

    final cardContent = Container(
      decoration: BoxDecoration(
        color: cardColor,
        borderRadius: BorderRadius.circular(14),
      ),
      width: double.infinity,
      padding: const EdgeInsets.all(22),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
        const SizedBox(height: 20),
          Container(
            padding: const EdgeInsets.all(8),
            decoration: const BoxDecoration(
              color: Colors.white,
              shape: BoxShape.circle,
            ),
            child: ClipOval(
              child: Image.network(
                safeImageUrl,
                width: 20,
                height: 20,
                fit: BoxFit.cover,
              ),
            ),
          ),
          const SizedBox(height: 18),
          Text(
            name,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 22,
              fontWeight: FontWeight.bold,
              height: 1,
            ),
          ),
        ],
      ),
    );

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Material(
        borderRadius: BorderRadius.circular(14),
        elevation: 4,
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: onTap,
          child: cardContent,
        ),
      ),
    );
  }
}
