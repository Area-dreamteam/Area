import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/models/service_model.dart';

void main() {
  group('CreateViewModel', () {
    late CreateViewModel viewModel;
    late ServiceRepository serviceRepository;

    setUp(() {
      final apiService = ApiService();
      serviceRepository = ServiceRepository(apiService: apiService);
      viewModel = CreateViewModel(serviceRepository: serviceRepository);
    });

    test('initial state', () {
      expect(viewModel.selectedAction, isNull);
      expect(viewModel.selectedReactions, isEmpty);
      expect(viewModel.name, isEmpty);
      expect(viewModel.description, isEmpty);
      expect(viewModel.isLoading, false);
      expect(viewModel.isEditing, false);
      expect(viewModel.errorMessage, '');
    });

    test('setName updates name', () {
      viewModel.setName('Test Name');
      expect(viewModel.name, 'Test Name');
    });

    test('setDescription updates description', () {
      viewModel.setDescription('Test Description');
      expect(viewModel.description, 'Test Description');
    });

    test('clearSelection resets all fields', () {
      viewModel.setName('Test');
      viewModel.setDescription('Desc');

      viewModel.clearSelection();

      expect(viewModel.selectedAction, isNull);
      expect(viewModel.selectedReactions, isEmpty);
      expect(viewModel.name, isEmpty);
      expect(viewModel.description, isEmpty);
      expect(viewModel.isEditing, false);
    });

    test('selectAction sets action correctly', () {
      final service = Service(
        id: 1,
        name: 'Test Service',
        oauthRequired: false,
      );

      final action = ActionModel(
        id: 1,
        name: 'Test Action',
        description: 'Description',
        configSchema: [],
      );

      final configuredItem = ConfiguredItem<ActionModel>(
        service: service,
        item: action,
        config: [],
      );

      viewModel.selectAction(configuredItem);

      expect(viewModel.selectedAction, configuredItem);
    });

    test('addReaction adds reaction to list', () {
      final service = Service(
        id: 1,
        name: 'Test Service',
        oauthRequired: false,
      );

      final reaction = Reaction(
        id: 1,
        name: 'Test Reaction',
        description: 'Description',
        configSchema: [],
      );

      final configuredItem = ConfiguredItem<Reaction>(
        service: service,
        item: reaction,
        config: [],
      );

      viewModel.addReaction(configuredItem);

      expect(viewModel.selectedReactions.length, 1);
      expect(viewModel.selectedReactions.first, configuredItem);
    });

    test('removeReaction removes reaction from list', () {
      final service = Service(
        id: 1,
        name: 'Test Service',
        oauthRequired: false,
      );

      final reaction = Reaction(
        id: 1,
        name: 'Test Reaction',
        description: 'Description',
        configSchema: [],
      );

      final configuredItem = ConfiguredItem<Reaction>(
        service: service,
        item: reaction,
        config: [],
      );

      viewModel.addReaction(configuredItem);
      expect(viewModel.selectedReactions.length, 1);

      viewModel.removeReaction(configuredItem);
      expect(viewModel.selectedReactions, isEmpty);
    });
  });
}
