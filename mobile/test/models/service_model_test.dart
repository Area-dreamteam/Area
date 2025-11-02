import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/models/service_model.dart';

void main() {
  group('Service', () {
    test('fromJson creates valid Service with all fields', () {
      final json = {
        'id': 1,
        'name': 'Gmail',
        'description': 'Email service',
        'category': 'Communication',
        'color': '#FF0000',
        'image_url': 'https://example.com/gmail.png',
        'oauth_required': true,
      };

      final service = Service.fromJson(json);

      expect(service.id, 1);
      expect(service.name, 'Gmail');
      expect(service.description, 'Email service');
      expect(service.category, 'Communication');
      expect(service.color, '#FF0000');
      expect(service.imageUrl, 'https://example.com/gmail.png');
      expect(service.oauthRequired, true);
    });
  });
}
