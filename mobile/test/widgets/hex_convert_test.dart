import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/widgets/hex_convert.dart';

void main() {
  group('hexToColor', () {
    test('converts valid 6-digit hex string with # to Color', () {
      final color = hexToColor('#FF0000');
      expect(color, const Color(0xFFFF0000));
    });

    test('returns default color for null input', () {
      final color = hexToColor(null);
      expect(color, const Color(0xFF212121));
    });

    test('returns default color for empty string', () {
      final color = hexToColor('');
      expect(color, const Color(0xFF212121));
    });

    test('returns default color for invalid hex string', () {
      final color = hexToColor('invalid');
      expect(color, const Color(0xFF212121));
    });


    test('returns default color for too short string', () {
      final color = hexToColor('FF');
      expect(color, const Color(0xFF212121));
    });

    test('returns default color for too long string', () {
      final color = hexToColor('FFFFFFFFFF');
      expect(color, const Color(0xFF212121));
    });

    test('handles various valid hex formats', () {
      expect(hexToColor('#FFFFFF'), const Color(0xFFFFFFFF));
      expect(hexToColor('000000'), const Color(0xFF000000));
      expect(hexToColor('#123456'), const Color(0xFF123456));
      expect(hexToColor('ABCDEF'), const Color(0xFFABCDEF));
    });

    test('handles lowercase hex values', () {
      expect(hexToColor('#ff0000'), const Color(0xFFFF0000));
      expect(hexToColor('00ff00'), const Color(0xFF00FF00));
      expect(hexToColor('#abcdef'), const Color(0xFFABCDEF));
    });
  });
}