import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/services/api_url_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  group('ApiUrlService', () {
    setUp(() async {
      SharedPreferences.setMockInitialValues({});
      ApiUrlService.clearCache();
    });

    tearDown(() {
      ApiUrlService.clearCache();
    });

    test('getApiUrl returns a non-empty string', () async {
      final url = await ApiUrlService.getApiUrl();
      expect(url, isNotEmpty);
      expect(url, isA<String>());
    });
  });
}
