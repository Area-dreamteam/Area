import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/repositories/service_repository.dart';

enum MyAppletState { nothing, loading, success, error }

class MyAppletViewModel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;

  MyAppletViewModel({required ServiceRepository serviceRepository})
    : _serviceRepository = serviceRepository;

  MyAppletState _state = MyAppletState.nothing;
  List<AppletModel> _privateApplets = [];
  List<AppletModel> _publicApplets = [];
  String _errorMessage = '';
  
  MyAppletState get state => _state;
  List<AppletModel> get privateApplets => List.unmodifiable(_privateApplets);
  List<AppletModel> get publicApplets => List.unmodifiable(_publicApplets);
  List<AppletModel> get applets => List.unmodifiable([..._privateApplets, ..._publicApplets]);
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == MyAppletState.loading;

  Future<bool> loadApplets() async {
    _setState(MyAppletState.loading);
    try {
      final privateFuture = _serviceRepository.fetchMyAreas();
      final publicFuture = _serviceRepository.fetchPublicUserAreas();

      final results = await Future.wait([privateFuture, publicFuture]);
      
      _privateApplets = results[0];
      _publicApplets = results[1];
      
      _errorMessage = '';
      _setState(MyAppletState.success);
      return true;
    } catch (e) {
      _errorMessage = "Failed to load Applets: $e";
      _privateApplets = [];
      _publicApplets = [];
      _setState(MyAppletState.error);
      return false;
    }
  }

  Future<bool> deleteApplet(int appletId) async {
    _errorMessage = '';
    notifyListeners();
    try {
      await _serviceRepository.deleteArea(appletId);
      await loadApplets();
      return true;
    } catch (e) {
      _errorMessage = "Failed to delete: $e";
      notifyListeners();
      return false;
    }
  }

  Future<bool> toggleAreaEnabled(int appletId) async {
    final index = _privateApplets.indexWhere((a) => a.id == appletId);
    if (index == -1) return false;
    
    final currentApplet = _privateApplets[index];
    final newState = !currentApplet.isEnabled;
    _privateApplets[index] = _copyWithApplet(currentApplet, isEnabled: newState);
    _errorMessage = '';
    notifyListeners();
    
    try {
      if (newState) {
        await _serviceRepository.enableArea(appletId);
      } else {
        await _serviceRepository.disableArea(appletId);
      }
      return true;
    } catch (e) {
      _errorMessage = "Toggle failed: $e";
      _privateApplets[index] = currentApplet;
      notifyListeners();
      return false;
    }
  }

  Future<bool> toggleAreaPublic(int appletId, bool isCurrentlyPublic) async {
    _errorMessage = '';
    notifyListeners();

    try {
      if (isCurrentlyPublic) {
        await _serviceRepository.unpublishArea(appletId);
      } else {
        await _serviceRepository.publishArea(appletId);
      }
      await loadApplets();
      return true;
    } catch (e) {
      _errorMessage = "Visibility toggle failed: $e";
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

  AppletModel _copyWithApplet(
    AppletModel applet, {
    bool? isEnabled,
    bool? isPublic,
  }) {
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