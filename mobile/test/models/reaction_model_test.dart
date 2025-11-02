import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/models/reaction_model.dart';

void main() {
  group('Reaction', () {
    test('fromJson creates valid Reaction', () {
      final json = {
        'id': 1,
        'name': 'Test Reaction',
        'description': 'Test Description',
        'config_schema': [
          {'name': 'field1', 'type': 'select'}
        ]
      };

      final reaction = Reaction.fromJson(json);

      expect(reaction.id, 1);
      expect(reaction.name, 'Test Reaction');
      expect(reaction.description, 'Test Description');
      expect(reaction.configSchema.length, 1);
    });

    test('fromJson handles empty config_schema', () {
      final json = {
        'id': 2,
        'name': 'Reaction Without Schema',
        'description': 'No config',
      };

      final reaction = Reaction.fromJson(json);

      expect(reaction.id, 2);
      expect(reaction.configSchema, isEmpty);
    });
  });
}