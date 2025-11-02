import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/models/applet_model.dart';

void main() {
  group('AppletUser', () {
    test('fromJson creates valid AppletUser', () {
      final json = {'id': 1, 'name': 'John Doe'};
      final user = AppletUser.fromJson(json);

      expect(user.id, 1);
      expect(user.name, 'John Doe');
    });

    test('toJson returns correct map', () {
      final user = AppletUser(id: 1, name: 'Jane Doe');
      final json = user.toJson();

      expect(json['id'], 1);
      expect(json['name'], 'Jane Doe');
    });
  });


    test('toJson returns correct structure', () {
      final applet = AppletModel(
        id: 1,
        name: 'Test',
        user: AppletUser(id: 1, name: 'User'),
        color: '#FF0000',
        isEnabled: true,
        isPublic: false,
        reactions: [],
      );

      final json = applet.toJson();

      expect(json['id'], 1);
      expect(json['name'], 'Test');
      expect(json['color'], '#FF0000');
      expect(json['is_enabled'], true);
      expect(json['is_public'], false);
    });

}
