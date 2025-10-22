import 'package:flutter/material.dart';
import 'package:mobile/pages/change_password_page.dart';

enum ChangePasswordState {initial, loading, loaded, error}

class ChangePasswordViewmodel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;

  ChangePasswordViewmodel({required ServiceRepository serviceRepository})
  : _serviceRepository = serviceRepository;

  ChangePasswordState _state = ChangePasswordState.initial;
  UserModel _currentUser;

  ChangePasswordState get state => _state;
  bool get isLoading => _state == ChangePasswordState.loading;

  void _setState(ChangePasswordState newState) {
    _state = newState;
    notifyListeners();
  }

}

