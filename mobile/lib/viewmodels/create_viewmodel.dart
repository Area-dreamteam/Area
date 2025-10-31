import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/models/applet_model.dart';
import 'dart:convert';

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

  ConfiguredItem<ActionModel>? _selectedAction;
  List<ConfiguredItem<Reaction>> _selectedReactions = [];
  String _name = '';
  String _description = '';
  String _errorMessage = '';
  CreateState _state = CreateState.nothing;

  bool _isEditing = false;
  int? _editingAppletId;

  ConfiguredItem<ActionModel>? get selectedAction => _selectedAction;
  List<ConfiguredItem<Reaction>> get selectedReactions => _selectedReactions;
  String get name => _name;
  String get description => _description;
  CreateState get state => _state;
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == CreateState.loading;
  bool get isEditing => _isEditing;

  bool get isActionAndReactionSelected =>
      _selectedAction != null && _selectedReactions.isNotEmpty;

  bool get isReadyToCreateOrUpdate =>
      _selectedAction != null &&
      _selectedReactions.isNotEmpty &&
      _name.isNotEmpty;

  void setName(String name) {
    if (_name != name) {
      _name = name;
      notifyListeners();
    }
  }

  void setDescription(String description) {
    if (_description != description) {
      _description = description;
      notifyListeners();
    }
  }

  void selectAction(ConfiguredItem<ActionModel> action) {
    _selectedAction = action;
    notifyListeners();
  }

  void addReaction(ConfiguredItem<Reaction> reaction) {
    _selectedReactions.add(reaction);
    notifyListeners();
  }

  void removeReaction(ConfiguredItem<Reaction> reaction) {
    _selectedReactions.remove(reaction);
    notifyListeners();
  }

  List<dynamic> _decodeConfig(String? configJson) {
    if (configJson != null && configJson.isNotEmpty) {
      try {
        final decoded = jsonDecode(configJson);
        if (decoded is List) {
          return decoded;
        }
      } catch (e) {
        print("Erreur décodage config: $e");
      }
    }
    return [];
  }

  Future<bool> startEditing(AppletModel appletToEdit) async {
    _setState(CreateState.loading);
    try {
      if (appletToEdit.actionId == null ||
          appletToEdit.reactions.isEmpty ||
          appletToEdit.triggerService == null) {
        throw Exception("Données Applet incomplètes pour l'édition.");
      }

      final actionDetailsFuture = _serviceRepository.fetchActionDetails(
        appletToEdit.actionId!,
      );
      final triggerServiceFuture = _serviceRepository.fetchServiceDetails(
        appletToEdit.triggerService!.id,
      );

      List<Future<Reaction>> reactionDetailsFutures = [];
      List<Future<Service>> reactionServiceFutures = [];

      for (var reactionInfo in appletToEdit.reactions) {
        reactionDetailsFutures.add(
          _serviceRepository.fetchReactionDetails(reactionInfo.id),
        );
        reactionServiceFutures.add(
          _serviceRepository.fetchServiceDetails(reactionInfo.service.id),
        );
      }

      final actionDetails = await actionDetailsFuture;
      final triggerServiceDetails = await triggerServiceFuture;
      final reactionModels = await Future.wait(reactionDetailsFutures);
      final reactionServiceDetailsList = await Future.wait(
        reactionServiceFutures,
      );

      _isEditing = true;
      _editingAppletId = appletToEdit.id;
      _name = appletToEdit.name;
      _description = appletToEdit.description ?? '';

      _selectedAction = ConfiguredItem<ActionModel>(
        service: triggerServiceDetails,
        item: actionDetails,
        config: _decodeConfig(appletToEdit.actionConfigJson),
      );

      _selectedReactions = [];
      for (int i = 0; i < appletToEdit.reactions.length; i++) {
        final reactionInfo = appletToEdit.reactions[i];
        _selectedReactions.add(
          ConfiguredItem<Reaction>(
            service: reactionServiceDetailsList[i],
            item: reactionModels[i],
            config: _decodeConfig(reactionInfo.configJson),
          ),
        );
      }

      _setState(CreateState.nothing);
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = "Erreur préparation édition: $e";
      _setState(CreateState.error);
      _isEditing = false;
      _editingAppletId = null;
      notifyListeners();
      return false;
    }
  }

  Future<bool> saveApplet() async {
    if (!isReadyToCreateOrUpdate) {
      _errorMessage =
          'Choose one action and at least one reactions.';
      _setState(CreateState.error);
      return false;
    }
    _setState(CreateState.loading);
    try {
      final reactionsPayload = _selectedReactions
          .map((item) => {'reaction_id': item.item.id, 'config': item.config})
          .toList();

      if (_isEditing && _editingAppletId != null) {
        await _serviceRepository.updateArea(
          areaId: _editingAppletId!,
          name: _name,
          description: _description,
          actionId: _selectedAction!.item.id,
          actionConfig: _selectedAction!.config,
          reactions: reactionsPayload,
        );
      } else {
        await _serviceRepository.createApplet(
          name: _name,
          description: _description,
          actionId: _selectedAction!.item.id,
          actionConfig: _selectedAction!.config,
          reactions: reactionsPayload,
        );
      }

      _setState(CreateState.success);
      clearSelection();
      return true;
    } catch (e) {
      _errorMessage = 'Erreur sauvegarde Applet: $e';
      _setState(CreateState.error);
      return false;
    }
  }

  void clearSelection() {
    _selectedAction = null;
    _selectedReactions = [];
    _name = '';
    _description = '';
    _isEditing = false;
    _editingAppletId = null;
    _state = CreateState.nothing;
    _errorMessage = '';
    notifyListeners();
  }

  void _setState(CreateState newState) {
    if (_state != newState) {
      if (newState != CreateState.error) _errorMessage = '';
      _state = newState;
      notifyListeners();
    }
  }
}
