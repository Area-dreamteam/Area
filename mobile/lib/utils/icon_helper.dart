import 'package:flutter/material.dart';

const Map<String, String> _serviceIconMap = {
  'google': 'assets/icons/logo_google.png',
  'facebook': 'assets/icons/logo_facebook.png',
  'github': 'assets/icons/logo_github.png',
  'gmail': 'assets/icons/logo_gmail.png',
  'todoist': 'assets/icons/logo_todoist.png',
  'dateandtime': 'assets/icons/logo_dateAndTime.png'
};

Widget getServiceIcon(String serviceName, {double size = 30.0}) {
  
  final String normalizedName = serviceName.toLowerCase();

  for (final key in _serviceIconMap.keys) {
    if (normalizedName.contains(key)) {
      final assetPath = _serviceIconMap[key]!;
      return Image.asset(
        assetPath,
        width: size,
        height: size,
        errorBuilder: (context, error, stackTrace) {
          return Icon(Icons.broken_image, size: size, color: Colors.grey);
        },
      );
    }
  }

  return Icon(Icons.link, size: size, color: Colors.white);
}