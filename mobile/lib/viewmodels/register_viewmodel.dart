import 'package:flutter/material.dart';
import 'package:mobile/repositories/auth_repository.dart';

enum RegisterState { nothing, loading, error, success }

class RegisterViewModel extends ChangeNotifier {
  final AuthRepository _authRepository;

  RegisterViewModel({required AuthRepository authRepository})
    : _authRepository = authRepository;

  RegisterState _state = RegisterState.nothing;
  String _errorMessage = '';

  RegisterState get state => _state;
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == RegisterState.loading;

  Future<bool> register({
    required String email,
    required String password,
  }) async {
    _setState(RegisterState.loading);
    final error = await _authRepository.register(
      email: email,
      password: password,
    );

    if (error == null) {
      final loginError = await _authRepository.loginWithEmailPassword(
        email,
        password,
      );
      if (loginError == null) {
        _setState(RegisterState.success);
        return true;
      } else {
        _errorMessage = "Account created but error to login";
        _setState(RegisterState.error);
        return false;
      }
    } else {
      _errorMessage = error;
      _setState(RegisterState.error);
      return false;
    }
  }

  void _setState(RegisterState newState) {
    _state = newState;
    notifyListeners();
  }
}
