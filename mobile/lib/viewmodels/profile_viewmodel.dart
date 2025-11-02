import 'package:flutter/material.dart';
import 'package:mobile/models/user_model.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/services/oauth_service.dart';

class LinkedAccountView {
  final int oauthId;
  final OAuthProvider provider;
  final bool isLinked;
  LinkedAccountView({
    required this.oauthId,
    required this.provider,
    required this.isLinked,
  });
}

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
  List<LinkedAccountView> _linkedAccounts = [];

  ProfileState get state => _state;

  UserModel? get currentUser => _currentUser;

  String get errorMessage => _errorMessage;

  bool get isLoading =>
      _state == ProfileState.loading || _state == ProfileState.saving;

  List<OAuthLoginInfo> get linkedAccounts => _currentUser?.oauthLogins ?? [];

  List<LinkedAccountView> get linkedAccountViews => _linkedAccounts;

  Future<void> loadCurrentUser() async {
    if (_state == ProfileState.loading) {
      return;
    }
    _setState(ProfileState.loading);
    try {
      final pendingLinkService = await _oauthService.checkPendingLinkSuccess();
      if (pendingLinkService != null) {
        print('Found pending OAuth link success for: $pendingLinkService');
      }

      _currentUser = await _serviceRepository.fetchCurrentUser();
      
      if (_currentUser?.oauthLogins.isNotEmpty ?? false) {
        _linkedAccounts = _currentUser!.oauthLogins.map((oauth) {
          return LinkedAccountView(
            oauthId: oauth.id,
            provider: OAuthProvider(
              name: oauth.name,
              color: oauth.color,
              imageUrl: oauth.imageUrl,
            ),
            isLinked: oauth.connected,
          );
        }).toList();
      } else {
        final availableProviders = await _oauthService.getAvailableProviders();
        final userLinkedNames = _currentUser?.linkedAccounts ?? [];
        _linkedAccounts = availableProviders.map((provider) {
          return LinkedAccountView(
            oauthId: 0,
            provider: provider,
            isLinked: userLinkedNames.contains(provider.name),
          );
        }).toList();
      }

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

      if (update != null) {
        _currentUser = update;
      } else {
        _currentUser = UserModel(
          id: _currentUser!.id,
          name: newName,
          email: newEmail,
          role: _currentUser!.role,
          linkedAccounts: _currentUser!.linkedAccounts,
          oauthLogins: _currentUser!.oauthLogins,
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

  Future<void> linkAccount(String providerName) async {
    _setState(ProfileState.saving);
    try {
      final result = await _oauthService.loginWithOAuth(providerName);

      if (result.isSuccess) {
        await loadCurrentUser();
      } else {
        throw Exception(result.error ?? "Failed to link account");
      }
    } catch (e) {
      _errorMessage = "Failed to link account: $e";
      _setState(ProfileState.error);
    }
  }

  Future<void> unlinkAccount(int oauthId) async {
    _setState(ProfileState.saving);
    try {
      await _serviceRepository.unlinkOAuthAccount(oauthId);
      await loadCurrentUser();
    } catch (e) {
      _errorMessage = "Failed to unlink account: $e";
      _setState(ProfileState.error);
    }
  }
}
