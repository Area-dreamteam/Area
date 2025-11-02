import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/core/config.dart';
import 'package:mobile/services/api_url_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  group('Config', () {
    setUp(() {
      SharedPreferences.setMockInitialValues({});
      ApiUrlService.clearCache();
    });

    test('getApiUrl returns a non-empty string', () async {
      final url = await Config.getApiUrl();
      expect(url, isNotEmpty);
      expect(url, isA<String>());
    });

    test('handles concurrent getApiUrl calls', () async {
      final results = await Future.wait([
        Config.getApiUrl(),
        Config.getApiUrl(),
        Config.getApiUrl(),
      ]);

      expect(results[0], results[1]);
      expect(results[1], results[2]);
    });

    test('Config respects ApiUrlService changes', () async {
      const url1 = 'https://api1.com';
      const url2 = 'https://api2.com';

      await ApiUrlService.setApiUrl(url1);
      expect(await Config.getApiUrl(), url1);

      await ApiUrlService.setApiUrl(url2);
      expect(await Config.getApiUrl(), url2);
    });

    test('Config image URLs update when API URL changes', () async {
      const imagePath = 'test.png';

      await ApiUrlService.setApiUrl('https://api1.com');
      final imageUrl1 = await Config.getImageUrl(imagePath);

      await ApiUrlService.setApiUrl('https://api2.com');
      ApiUrlService.clearCache();
      final imageUrl2 = await Config.getImageUrl(imagePath);

      expect(imageUrl1, isNot(imageUrl2));
    });
  });
}