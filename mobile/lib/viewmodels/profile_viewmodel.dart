import 'package:flutter/material.dart';
import 'package:mobile/models/user_model.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/services/oauth_service.dart';

enum ProfileState { initial, loading, loaded, error, saving }

class ProfileViewModel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;
  final OAuthService _oauthService;

  ProfileViewModel({
    required ServiceRepository serviceRepository,
    required OAuthService oauthService,
  }) : _serviceRepository = serviceRepository,
       _oauthService = oauthService;

  ProfileState _state = ProfileState.initial;
  UserModel? _currentUser;
  String _errorMessage = '';

  ProfileState get state => _state;

  UserModel? get currentUser => _currentUser;

  String get errorMessage => _errorMessage;

  bool get isLoading =>
      _state == ProfileState.loading || _state == ProfileState.saving;

  List<OAuthLoginInfo> get linkedAccounts => _currentUser?.oauthLogin ?? [];

  Future<void> loadCurrentUser() async {
    if (_state == ProfileState.loading) {
      return;
    }
    _setState(ProfileState.loading);
    try {
      _currentUser = await _serviceRepository.fetchCurrentUser();
      _setState(ProfileState.loaded);
    } catch (e) {
      _errorMessage = "Failed to get user data: $e";
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

      await loadCurrentUser();
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


  Future<void> unlinkAccount(int oauthLoginId) async {
    _setState(ProfileState.saving);
    try {
      await _serviceRepository.disconnectOAuthLogin(oauthLoginId);
      await loadCurrentUser();
    } catch (e) {
      _errorMessage = "Failed to unlink account: $e";
      _setState(ProfileState.error);
    }
  }
}
