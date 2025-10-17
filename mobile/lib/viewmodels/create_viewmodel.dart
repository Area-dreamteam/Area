import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/models/service_model.dart';

class ConfiguredItem<T> {
  final Service service;
  final T item;
  final List<dynamic> config;

  ConfiguredItem({
    required this.service,
    required this.item,
    required this.config,
  });
}

enum CreateState { nothing, loading, success, error }

class CreateViewModel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;
  CreateViewModel({required ServiceRepository serviceRepository})
    : _serviceRepository = serviceRepository;

  ServiceRepository get serviceRepository => _serviceRepository;

  ConfiguredItem<ActionModel>? _selectedAction;
  ConfiguredItem<Reaction>? _selectedReaction;
  String _name = '';
  String _description = '';
  String _errorMessage = '';
  CreateState _state = CreateState.nothing;

  ConfiguredItem<ActionModel>? get selectedAction => _selectedAction;
  ConfiguredItem<Reaction>? get selectedReaction => _selectedReaction;

  bool get isActionAndReactionSelected =>
      _selectedAction != null && _selectedReaction != null;

  String get name => _name;
  String get description => _description;
  CreateState get state => _state;
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == CreateState.loading;

  bool get isReadyToCreate =>
      _selectedAction != null &&
      _selectedReaction != null &&
      _name.isNotEmpty &&
      _description.isNotEmpty;

  void setName(String name) {
    _name = name;
    notifyListeners();
  }

  void setDescription(String description) {
    _description = description;
    notifyListeners();
  }

  void selectAction(ConfiguredItem<ActionModel> action) {
    _selectedAction = action;
    notifyListeners();
  }

  void selectReaction(ConfiguredItem<Reaction> reaction) {
    _selectedReaction = reaction;
    notifyListeners();
  }

  void clearSelection() {
    _selectedAction = null;
    _selectedReaction = null;
    _name = '';
    _description = '';
    _state = CreateState.nothing;
    notifyListeners();
  }

  Future<bool> createApplet() async {
    if (!isReadyToCreate) {
      return false;
    }
    _setState(CreateState.loading);
    try {
      await _serviceRepository.createApplet(
        name: _name,
        description: _description,
        actionId: _selectedAction!.item.id,
        actionConfig: _selectedAction!.config,
        reactionId: _selectedReaction!.item.id,
        reactionConfig: _selectedReaction!.config,
      );

      _setState(CreateState.success);
      return true;
    } catch (e) {
      _errorMessage = 'Error creating applet: $e';
      _setState(CreateState.error);
      return false;
    }
  }

  void _setState(CreateState newState) {
    _state = newState;
    notifyListeners();
  }
}