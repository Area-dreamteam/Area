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
  ConfiguredItem<Reaction>? _selectedReaction;
  String _name = '';
  String _description = '';
  String _errorMessage = '';
  CreateState _state = CreateState.nothing;

  bool _isEditing = false;
  int? _editingAppletId;

  ConfiguredItem<ActionModel>? get selectedAction => _selectedAction;
  ConfiguredItem<Reaction>? get selectedReaction => _selectedReaction;
  String get name => _name;
  String get description => _description;
  CreateState get state => _state;
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == CreateState.loading;
  bool get isEditing => _isEditing;

  bool get isActionAndReactionSelected =>
      _selectedAction != null && _selectedReaction != null;

  bool get isReadyToCreateOrUpdate =>
      _selectedAction != null && _selectedReaction != null && _name.isNotEmpty;

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

  void selectReaction(ConfiguredItem<Reaction> reaction) {
    _selectedReaction = reaction;
    notifyListeners();
  }

  Future<bool> startEditing(AppletModel appletToEdit) async {
    _setState(CreateState.loading);
    try {
      if (appletToEdit.actionId == null ||
          appletToEdit.reactionId == null ||
          appletToEdit.triggerService == null ||
          appletToEdit.reactionServices.isEmpty) {
        throw Exception("Données Applet incomplètes pour l'édition.");
      }

      final actionDetailsFuture = _serviceRepository.fetchActionDetails(appletToEdit.actionId!);
      final reactionDetailsFuture = _serviceRepository.fetchReactionDetails(appletToEdit.reactionId!);
      final triggerServiceFuture = _serviceRepository.fetchServiceDetails(appletToEdit.triggerService!.id);
      final reactionServiceFuture = _serviceRepository.fetchServiceDetails(appletToEdit.reactionServices.first.id);

      final results = await Future.wait([
        actionDetailsFuture,
        reactionDetailsFuture,
        triggerServiceFuture,
        reactionServiceFuture,
      ]);

      final actionModel = results[0] as ActionModel;
      final reactionModel = results[1] as Reaction;
      final triggerServiceDetails = results[2] as Service;
      final reactionServiceDetails = results[3] as Service;

      List<dynamic> actionConfig = [];
      if (appletToEdit.actionConfigJson != null && appletToEdit.actionConfigJson!.isNotEmpty) {
        try { actionConfig = jsonDecode(appletToEdit.actionConfigJson!); } catch (e) { print("Erreur décodage config action: $e"); /* Config reste vide */ }
      }
      List<dynamic> reactionConfig = [];
      if (appletToEdit.reactionConfigJson != null && appletToEdit.reactionConfigJson!.isNotEmpty) {
        try { reactionConfig = jsonDecode(appletToEdit.reactionConfigJson!); } catch (e) { print("Erreur décodage config réaction: $e"); /* Config reste vide */ }
      }

      _isEditing = true;
      _editingAppletId = appletToEdit.id;
      _name = appletToEdit.name;
      _description = appletToEdit.description ?? '';
      _selectedAction = ConfiguredItem<ActionModel>(
        service: triggerServiceDetails,
        item: actionModel,
        config: actionConfig,
      );
      _selectedReaction = ConfiguredItem<Reaction>(
        service: reactionServiceDetails,
        item: reactionModel,
        config: reactionConfig,
      );

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
      _errorMessage = 'Veuillez sélectionner une action, une réaction et donner un nom.';
      _setState(CreateState.error);
      return false;
    }
    _setState(CreateState.loading);

    try {
      if (_isEditing && _editingAppletId != null) {
        await _serviceRepository.updateArea(
          areaId: _editingAppletId!,
          name: _name,
          description: _description,
          actionId: _selectedAction!.item.id,
          actionConfig: _selectedAction!.config,
          reactionId: _selectedReaction!.item.id,
          reactionConfig: _selectedReaction!.config,
        );
      }
      else {
        await _serviceRepository.createApplet(
          name: _name,
          description: _description,
          actionId: _selectedAction!.item.id,
          actionConfig: _selectedAction!.config,
          reactionId: _selectedReaction!.item.id,
          reactionConfig: _selectedReaction!.config,
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
    _selectedReaction = null;
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