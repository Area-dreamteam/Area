import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/repositories/service_repository.dart';

enum MyAppletState { nothing, loading, success, error }

class MyAppletViewModel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;

  MyAppletViewModel({required ServiceRepository serviceRepository})
      : _serviceRepository = serviceRepository;

  MyAppletState _state = MyAppletState.nothing;
  List<AppletModel> _applets = [];
  String _errorMessage = '';

  MyAppletState get state => _state;
  List<AppletModel> get applets => List.unmodifiable(_applets);
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == MyAppletState.loading;

  Future<bool> loadApplets() async {
    _setState(MyAppletState.loading);
    try {
      _applets = await _serviceRepository.fetchMyAreas();
      _errorMessage = '';
      _setState(MyAppletState.success);
      return true;
    } catch (e) {
      _errorMessage = "Impossible de charger les Applets: $e";
      _setState(MyAppletState.error);
      return false;
    }
  }

  Future<bool> deleteApplet(int appletId) async {
    final originalApplets = List<AppletModel>.from(_applets);
    
    _applets.removeWhere((applet) => applet.id == appletId);
    _errorMessage = '';
    notifyListeners();

    try {
      await _serviceRepository.deleteArea(appletId);
      return true;
    } catch (e) {
      _errorMessage = "Delete error: $e";
      _applets = originalApplets;
      notifyListeners();
      return false;
    }
  }

  Future<bool> toggleAreaEnabled(int appletId) async {
    final index = _applets.indexWhere((a) => a.id == appletId);
    if (index == -1) return false;

    final currentApplet = _applets[index];
    final newState = !currentApplet.isEnabled;
    _applets[index] = _copyWithApplet(currentApplet, isEnabled: newState);
    _errorMessage = '';
    notifyListeners();

    try {
      if (newState == true) {
        await _serviceRepository.enableArea(appletId);
      } else {
        await _serviceRepository.disableArea(appletId);
      }
      return true;
    } catch (e) {
      _errorMessage = "Error switch state: $e";
      _applets[index] = currentApplet;
      notifyListeners();
      return false;
    }
  }

  void _setState(MyAppletState newState) {
    if (_state != newState) {
      _state = newState;
      notifyListeners();
    }
  }

  AppletModel _copyWithApplet(AppletModel applet, {bool? isEnabled, bool? isPublic}) {
    return AppletModel(
      id: applet.id,
      name: applet.name,
      description: applet.description,
      user: applet.user,
      color: applet.color,
      triggerService: applet.triggerService,
      reactionServices: applet.reactionServices,
      isEnabled: isEnabled ?? applet.isEnabled,
      isPublic: isPublic ?? applet.isPublic,
      actionId: applet.actionId,
      actionConfigJson: applet.actionConfigJson,
      reactionId: applet.reactionId,
      reactionConfigJson: applet.reactionConfigJson,
    );
  }
}