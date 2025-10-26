import 'package:flutter/material.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/widgets/hex_convert.dart';

class ServiceCard extends StatelessWidget {
  final int id;
  final String name;
  final String? description;
  final String imageUrl;
  final String? category;
  final String? colorHex;
  final VoidCallback? onTap;

  const ServiceCard({
    super.key,
    required this.id,
    required this.name,
    this.description,
    required this.imageUrl,
    this.category,
    this.colorHex,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final cardColor = hexToColor(colorHex);

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
              child: getServiceIcon(name, size: 20.0),
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

    return Material(
      borderRadius: BorderRadius.circular(14),
      elevation: 4,
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: cardContent,
      ),
    );
  }
}
