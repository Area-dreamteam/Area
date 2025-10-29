import 'package:flutter/material.dart';
import '../core/config.dart';

Widget getServiceIcon(String serviceName, {double size = 30.0, String? imageUrl}) {
  // If imageUrl is provided, use it from the backend
  if (imageUrl != null && imageUrl.isNotEmpty) {
    final fullImageUrl = Config.getImageUrl(imageUrl);
    return Image.network(
      fullImageUrl,
      width: size,
      height: size,
      errorBuilder: (context, error, stackTrace) {
        return Icon(Icons.broken_image, size: size, color: Colors.grey);
      },
      loadingBuilder: (context, child, loadingProgress) {
        if (loadingProgress == null) return child;
        return SizedBox(
          width: size,
          height: size,
          child: Center(
            child: CircularProgressIndicator(
              value: loadingProgress.expectedTotalBytes != null
                  ? loadingProgress.cumulativeBytesLoaded /
                      loadingProgress.expectedTotalBytes!
                  : null,
            ),
          ),
        );
      },
    );
  }

  // Fallback to default icon if no image URL is provided
  return Icon(Icons.link, size: size, color: Colors.white);
}
