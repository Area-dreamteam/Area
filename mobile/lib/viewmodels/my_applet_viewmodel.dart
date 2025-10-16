// lib/viewmodels/my_applet_viewmodel.dart

import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart'; // CHANGÉ
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
  List<AppletModel> get applets => _applets;
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == MyAppletState.loading;

  Future<bool> loadApplets() async {
    _setState(MyAppletState.loading);
    try {
      _applets = await _serviceRepository.fetchMyAreas();
      _setState(MyAppletState.success);
      return true;
    } catch (e) {
      _errorMessage = "Impossible to load Applets";
      _setState(MyAppletState.error);
      return false;
    }
  }

  Future<bool> deleteApplet(int appletId) async {
    try {
      await _serviceRepository.deleteArea(appletId);
      _applets.removeWhere((applet) => applet.id == appletId);
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = "Error delete Applet.";
      notifyListeners();
      return false;
    }
  }

  void _setState(MyAppletState newState) {
    _state = newState;
    notifyListeners();
  }
}