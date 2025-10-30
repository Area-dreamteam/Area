import 'package:flutter/material.dart';
import 'package:mobile/repositories/auth_repository.dart';

enum LoginState { nothing, loading, error, success }

class LoginViewModel extends ChangeNotifier {
  final AuthRepository _authRepository;

  LoginViewModel({required AuthRepository authRepository})
    : _authRepository = authRepository;

  LoginState _state = LoginState.nothing;
  String _errorMessage = '';

  LoginState get state => _state;
  String get errorMessage => _errorMessage;
  bool get isLoading => _state == LoginState.loading;

  Future<bool> loginWithEmailPassword(String email, String password) async {
    _setState(LoginState.loading);
    final error = await _authRepository.loginWithEmailPassword(email, password);

    if (error == null) {
      _setState(LoginState.success);
      return true;
    } else {
      _errorMessage = error;
      _setState(LoginState.error);
      return false;
    }
  }

  void _setState(LoginState newState) {
    _state = newState;
    notifyListeners();
  }
}
