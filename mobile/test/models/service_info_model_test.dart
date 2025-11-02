import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/models/service_info_model.dart';

void main() {
  group('ServiceInfo', () {
    test('fromJson creates valid ServiceInfo', () {
      final json = {
        'id': 1,
        'name': 'Gmail',
        'color': '#FF0000',
        'image_url': 'https://example.com/gmail.png',
      };

      final serviceInfo = ServiceInfo.fromJson(json);

      expect(serviceInfo.id, 1);
      expect(serviceInfo.name, 'Gmail');
      expect(serviceInfo.color, '#FF0000');
      expect(serviceInfo.imageUrl, 'https://example.com/gmail.png');
    });

    test('fromJson handles null image_url', () {
      final json = {'id': 2, 'name': 'Slack', 'color': '#00FF00'};

      final serviceInfo = ServiceInfo.fromJson(json);

      expect(serviceInfo.id, 2);
      expect(serviceInfo.name, 'Slack');
      expect(serviceInfo.color, '#00FF00');
      expect(serviceInfo.imageUrl, isNull);
    });
  });
}
