import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';

enum ChangePasswordState { initial, loading, success, error }

class ChangePasswordViewModel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;

  ChangePasswordViewModel({required ServiceRepository serviceRepository})
      : _serviceRepository = serviceRepository;

  ChangePasswordState _state = ChangePasswordState.initial;
  String _errorMessage = '';

  ChangePasswordState get state => _state;
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == ChangePasswordState.loading;

  Future<bool> changePassword({
    required String newPassword,
    required String currentPassword,
  }) async {
    _setState(ChangePasswordState.loading);

    try {
      await _serviceRepository.updateUserPassword(
        newPassword: newPassword,
        currentPassword: currentPassword,
      );
      _setState(ChangePasswordState.success);
      return true;
    } catch (e) {
      _errorMessage = "Failed to change password: $e";
      _setState(ChangePasswordState.error);
      return false;
    }
  }

  void _setState(ChangePasswordState newState) {
    _state = newState;
    notifyListeners();
  }
}