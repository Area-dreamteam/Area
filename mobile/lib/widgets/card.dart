import 'package:flutter/material.dart';
import 'package:mobile/widgets/hex_convert.dart';

class AppletCard extends StatelessWidget {
  final Color? color;
  final IconData? icon;
  final String title;
  final String byText;
  final String? colorHex;
  final VoidCallback? onTap;
  final VoidCallback? onDelete;

  const AppletCard({
    super.key,
    required this.title,
    required this.byText,
    this.color,
    this.colorHex,
    this.icon,
    this.onTap,
    this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    final cardColor = color ?? hexToColor(colorHex ?? '#212121');
    final textColor = Colors.white;
    bool isDeletable = onDelete != null;

    final cardContent = Container(
      decoration: BoxDecoration(
        color: cardColor,
        borderRadius: BorderRadius.circular(14),
      ),
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              if (isDeletable)
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: textColor,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(icon, color: cardColor, size: 20),
                ),
              const Spacer(),
              if (onDelete != null)
                IconButton(
                  icon: const Icon(Icons.delete_outline, color: Colors.white),
                  tooltip: 'Delete $title',
                  onPressed: onDelete,
                ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            title,
            style: TextStyle(
              color: textColor,
              fontSize: 24,
              fontWeight: FontWeight.bold,
              height: 1.2,
            ),
          ),
          const SizedBox(height: 12),
          Text(byText, style: TextStyle(color: textColor, fontSize: 16)),

          if (!isDeletable) const SizedBox(height: 40),
        ],
      ),
    );

    return Semantics(
      label: "$title, $byText",
      button: onTap != null,
      enabled: onTap != null,
      child: Material (
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
