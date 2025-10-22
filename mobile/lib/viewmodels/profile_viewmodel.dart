import 'package:flutter/material.dart';
import 'package:mobile/models/user_model.dart';
import 'package:mobile/repositories/service_repository.dart';

enum ProfileState { initial, loading, loaded, error, saving }

class ProfileViewModel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;

  ProfileViewModel({required ServiceRepository serviceRepository})
    : _serviceRepository = serviceRepository;

  ProfileState _state = ProfileState.initial;
  UserModel? _currentUser;
  String _errorMessage = '';

  ProfileState get state => _state;
  UserModel? get currentUser => _currentUser;
  String get errorMessage => _errorMessage;
  bool get isLoading =>
      _state == ProfileState.loading || _state == ProfileState.saving;

  Future<void> loadCurrentUser() async {
    if (_state == ProfileState.loading) {
      return;
    }
    _setState(ProfileState.loading);
    try {
      _currentUser = await _serviceRepository.fetchCurrentUser();
      _setState(ProfileState.loaded);
    } catch (e) {
      _errorMessage = "Failed to get user data";
      _setState(ProfileState.error);
    }
  }

  Future<bool> saveInformation({
    required String newName,
    required String newEmail,
  }) async {
    _setState(ProfileState.saving);
    try {
      if (newName.compareTo(_currentUser!.name) == 0 &&
          newEmail.compareTo(_currentUser!.email) == 0) {
        _setState(ProfileState.loaded);
        return true;
      }
      bool nameChanged = newName != _currentUser!.name;
      bool emailChanged = newEmail != _currentUser!.email;
      final update = await _serviceRepository.updateCurrentUser(
        name: nameChanged ? newName : _currentUser!.name,
        email: emailChanged ? newEmail : _currentUser!.email,
      );

      if (update != null) {
        _currentUser = update;
      } else {
        _currentUser = UserModel(
          id: _currentUser!.id,
          name: newName,
          email: newEmail,
          role: _currentUser!.role,
        );
      }
      _setState(ProfileState.loaded);
      return true;
    } catch (e) {
      _errorMessage = "Failed to save profile: $e";
      _setState(ProfileState.error);
      return false;
    }
  }

  void _setState(ProfileState newState) {
    _state = newState;
    notifyListeners();
  }
}
