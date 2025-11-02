import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/models/action_model.dart';

void main() {
  group('ActionModel', () {
    test('fromJson creates valid ActionModel', () {
      final json = {
        'id': 1,
        'name': 'Test Action',
        'description': 'Test Description',
        'config_schema': [
          {'name': 'field1', 'type': 'input'}
        ]
      };

      final action = ActionModel.fromJson(json);

      expect(action.id, 1);
      expect(action.name, 'Test Action');
      expect(action.description, 'Test Description');
      expect(action.configSchema.length, 1);
    });

    test('fromJson handles empty config_schema', () {
      final json = {
        'id': 2,
        'name': 'Action Without Schema',
        'description': 'No config',
      };

      final action = ActionModel.fromJson(json);

      expect(action.id, 2);
      expect(action.configSchema, isEmpty);
    });
  });
}