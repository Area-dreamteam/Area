// ignore_for_file: empty_catches, avoid_print

import 'package:app_links/app_links.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:dio/dio.dart';
import 'package:mobile/core/config.dart';
import 'dart:async';

class OAuthService {
  final String _baseUrl = Config.getApiUrl();
  static const _storage = FlutterSecureStorage();

  final AppLinks _appLinks = AppLinks();
  StreamSubscription<Uri>? _linkSubscription;
  Completer<OAuthResult>? _oauthCompleter;
  Completer<OAuthLinkResult>? _linkCompleter;

  void initialize() {
    _checkInitialLink();
    _linkSubscription = _appLinks.uriLinkStream.listen(
      _handleDeepLink,
      onError: (err) {
        print('OAuth deeplink error: $err');
        _completeOAuth(OAuthResult.error('Deeplink handling error'));
        _completeLink(OAuthLinkResult.error('Deeplink handling error'));
      },
    );
  }

  Future<void> _checkInitialLink() async {
    try {
      final initialLink = await _appLinks.getInitialLink();
      if (initialLink != null) {
        print('Processing initial deep link: $initialLink');
        _handleDeepLink(initialLink);
      }
    } catch (e) {
      print('Error checking initial deep link: $e');
    }
  }

  void dispose() {
    _linkSubscription?.cancel();
  }

  Future<void> _clearOAuthState() async {
    try {
      await _storage.delete(key: 'oauth_operation');
      await _storage.delete(key: 'oauth_service');
    } catch (e) {
      print('Error clearing OAuth state: $e');
    }
  }

  Future<OAuthResult> loginWithOAuth(String serviceName) async {
    if (_oauthCompleter != null && !_oauthCompleter!.isCompleted) {
      _oauthCompleter!.complete(OAuthResult.error('OAuth already in progress'));
    }
    _oauthCompleter = Completer<OAuthResult>();

    try {
      await _storage.write(key: 'oauth_operation', value: 'login');
      await _storage.write(key: 'oauth_service', value: serviceName);

      final oauthUrl = '$_baseUrl/oauth/login_index/$serviceName?mobile=true';
      final uri = Uri.parse(oauthUrl);

      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      } else {
        await _clearOAuthState();
        _completeOAuth(OAuthResult.error('Could not launch OAuth URL'));
        return _oauthCompleter!.future;
      }

      final result = await _oauthCompleter!.future.timeout(
        const Duration(minutes: 5),
        onTimeout: () {
          _clearOAuthState();
          return OAuthResult.error('OAuth timeout');
        },
      );

      if (result.isSuccess) {
        await _storeAuthToken(result.token!);
      }
      await _clearOAuthState();
      return result;
    } catch (e) {
      await _clearOAuthState();
      _completeOAuth(OAuthResult.error('OAuth failed: $e'));
      return _oauthCompleter!.future;
    }
  }

  Future<OAuthLinkResult> linkWithOAuth(String serviceName) async {
    if (_linkCompleter != null && !_linkCompleter!.isCompleted) {
      _linkCompleter!.complete(
        OAuthLinkResult.error('Linking already in progress'),
      );
    }
    _linkCompleter = Completer<OAuthLinkResult>();

    try {
      await _storage.write(key: 'oauth_operation', value: 'link');
      await _storage.write(key: 'oauth_service', value: serviceName);

      final sessionCookie = await _storage.read(key: 'session_cookie');
      String? token;
      if (sessionCookie != null &&
          sessionCookie.startsWith('access_token=Bearer ')) {
        token = sessionCookie.substring('access_token=Bearer '.length);
      }

      final oauthUrl = token != null
          ? '$_baseUrl/oauth/index/$serviceName?mobile=true&token=$token'
          : '$_baseUrl/oauth/index/$serviceName?mobile=true';
      final uri = Uri.parse(oauthUrl);

      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      } else {
        await _clearOAuthState();
        _completeLink(OAuthLinkResult.error('Could not launch OAuth URL'));
        return _linkCompleter!.future;
      }

      final result = await _linkCompleter!.future.timeout(
        const Duration(minutes: 5),
        onTimeout: () {
          _clearOAuthState();
          return OAuthLinkResult.error('OAuth timeout');
        },
      );

      await _clearOAuthState();
      return result;
    } catch (e) {
      print('OAuth error: $e');
      await _clearOAuthState();
      _completeLink(OAuthLinkResult.error('OAuth failed: $e'));
      return _linkCompleter!.future;
    }
  }

  Future<List<OAuthProvider>> getAvailableProviders() async {
    try {
      print(
        'Fetching OAuth providers from: $_baseUrl/oauth/available_oauths_login',
      );
      final dio = Dio(
        BaseOptions(baseUrl: _baseUrl, responseType: ResponseType.json),
      );
      final response = await dio.get('/oauth/available_oauths_login');
      print('OAuth providers response status: ${response.statusCode}');
      print('OAuth providers response data: ${response.data}');
      if (response.statusCode == 200 && response.data is List) {
        final List<dynamic> data = response.data;
        final providers = data
            .map((item) => OAuthProvider.fromJson(item as Map<String, dynamic>))
            .toList();
        print(
          'Parsed ${providers.length} OAuth providers: ${providers.map((p) => p.name).toList()}',
        );
        return providers;
      } else {
        print(
          'Invalid response: status=${response.statusCode}, data type=${response.data.runtimeType}',
        );
      }
    } catch (e) {
      print('Error fetching OAuth providers: $e');
    }
    return [];
  }

  Future<bool> isAuthenticated() async {
    final sessionCookie = await _storage.read(key: 'session_cookie');
    return sessionCookie != null && sessionCookie.isNotEmpty;
  }

  Future<String?> checkPendingLinkSuccess() async {
    final service = await _storage.read(key: 'oauth_link_success');
    if (service != null) {
      await _storage.delete(key: 'oauth_link_success');
    }
    return service;
  }

  void _handleDeepLink(Uri uri) async {
    print('Received deeplink: $uri');
    if (uri.scheme == 'area' && uri.host == 'oauth-callback') {
      final token = uri.queryParameters['token'];
      final service = uri.queryParameters['service'];
      final error = uri.queryParameters['error'];
      final linked = uri.queryParameters['linked'];

      final storedOperation = await _storage.read(key: 'oauth_operation');
      final storedService = await _storage.read(key: 'oauth_service');

      print('Stored operation: $storedOperation, service: $storedService');
      print(
        'Deep link params - token: ${token != null}, linked: $linked, error: $error',
      );

      if (error != null) {
        _completeOAuth(OAuthResult.error('OAuth error: $error'));
        _completeLink(OAuthLinkResult.error('OAuth error: $error'));
        await _clearOAuthState();
      } else if (token != null && service != null) {
        _completeOAuth(OAuthResult.success(token, service));
        await _clearOAuthState();
      } else if (linked == 'true' && service != null) {
        if (_linkCompleter == null && storedOperation == 'link') {
          print(
            'OAuth linking succeeded after app restart - storing success flag',
          );
          await _storage.write(key: 'oauth_link_success', value: service);
        }
        _completeLink(OAuthLinkResult.success(service));
        await _clearOAuthState();
      } else {
        _completeOAuth(OAuthResult.error('Invalid OAuth callback'));
        _completeLink(OAuthLinkResult.error('Invalid OAuth callback'));
        await _clearOAuthState();
      }
    }
  }

  void _completeOAuth(OAuthResult result) {
    if (_oauthCompleter != null && !_oauthCompleter!.isCompleted) {
      _oauthCompleter!.complete(result);
      _oauthCompleter = null;
    }
  }

  void _completeLink(OAuthLinkResult result) {
    if (_linkCompleter != null && !_linkCompleter!.isCompleted) {
      _linkCompleter!.complete(result);
      _linkCompleter = null;
    }
  }

  Future<void> _storeAuthToken(String token) async {
    await _storage.write(
      key: 'session_cookie',
      value: 'access_token=Bearer $token',
    );
  }
}

class OAuthResult {
  final bool isSuccess;
  final String? token;
  final String? service;
  final String? error;

  OAuthResult.success(this.token, this.service)
    : isSuccess = true,
      error = null;

  OAuthResult.error(this.error)
    : isSuccess = false,
      token = null,
      service = null;
}

class OAuthLinkResult {
  final bool isSuccess;
  final String? service;
  final String? error;

  OAuthLinkResult.success(this.service) : isSuccess = true, error = null;

  OAuthLinkResult.error(this.error) : isSuccess = false, service = null;
}

class OAuthProvider {
  final String name;
  final String color;
  final String? imageUrl;

  OAuthProvider({required this.name, required this.color, this.imageUrl});

  factory OAuthProvider.fromJson(Map<String, dynamic> json) {
    return OAuthProvider(
      name: json['name'] ?? '',
      color: json['color'] ?? '#000000',
      imageUrl: json['image_url'] as String?,
    );
  }
}
