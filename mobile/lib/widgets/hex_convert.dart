import 'package:flutter/material.dart';

Color hexToColor(String? hexString) {
  if (hexString == null) return const Color(0xFF212121);
  String formattedHex = hexString.replaceAll('#', '');

  if (formattedHex.length == 6) {
    formattedHex = 'FF$formattedHex';
  }

  try {
    if (formattedHex.length == 8) {
      return Color(int.parse(formattedHex, radix: 16));
    }
  } catch (_) {}
  return const Color(0xFF212121);
}
