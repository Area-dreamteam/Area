import 'package:flutter/material.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/widgets/hex_convert.dart';

class ServiceCard extends StatelessWidget {
  final int id;
  final String name;
  final String? description;
  final String? category;
  final String? colorHex;
  final String? imageUrl;
  final VoidCallback? onTap;

  const ServiceCard({
    super.key,
    required this.id,
    required this.name,
    this.description,
    this.category,
    this.colorHex,
    this.imageUrl,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final cardColor = hexToColor(colorHex);
    final bool isDark = cardColor.computeLuminance() < 0.5;
    final Color textColor = isDark ? Colors.white : Colors.black;

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
          SizedBox(height: 20),
          SizedBox(
            width: 40,
            height: 40,
            child: getServiceIcon(name, size: 20.0, imageUrl: imageUrl),
          ),
          const SizedBox(height: 18),
          Text(
            name,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
              color: textColor,
              fontWeight: FontWeight.bold,
              height: 1,
            ),
          ),
        ],
      ),
    );

    return Semantics(
      label: "Service $name",
      button: true,
      enabled: onTap != null,
      child: Material(
        borderRadius: BorderRadius.circular(14),
        elevation: 4,
        color: cardColor,
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: onTap,
          child: cardContent,
        ),
      ),
    );
  }
}