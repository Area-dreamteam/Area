// services/oauth_service.dart
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
    _linkSubscription = _appLinks.uriLinkStream.listen(
      _handleDeepLink,
      onError: (err) {
        print('OAuth deeplink error: $err');
        _completeOAuth(OAuthResult.error('Deeplink handling error'));
        _completeLink(OAuthLinkResult.error('Deeplink handling error'));
      },
    );
  }

  void dispose() {
    _linkSubscription?.cancel();
  }

  Future<OAuthResult> loginWithOAuth(String serviceName) async {
    if (_oauthCompleter != null && !_oauthCompleter!.isCompleted) {
      _oauthCompleter!.complete(OAuthResult.error('OAuth already in progress'));
    }
    _oauthCompleter = Completer<OAuthResult>();

    try {
      final oauthUrl = '$_baseUrl/oauth/login_index/$serviceName?mobile=true';
      final uri = Uri.parse(oauthUrl);

      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
      } else {
        _completeOAuth(OAuthResult.error('Could not launch OAuth URL'));
        return _oauthCompleter!.future;
      }

      final result = await _oauthCompleter!.future.timeout(
        const Duration(minutes: 5),
        onTimeout: () => OAuthResult.error('OAuth timeout'),
      );

      if (result.isSuccess) {
        await _storeAuthToken(result.token!);
      }
      return result;
    } catch (e) {
      _completeOAuth(OAuthResult.error('OAuth failed: $e'));
      return _oauthCompleter!.future;
    }
  }

  Future<OAuthLinkResult> linkWithOAuth(String serviceName) async {
    if (_linkCompleter != null && !_linkCompleter!.isCompleted) {
      _linkCompleter!
          .complete(OAuthLinkResult.error('Linking already in progress'));
    }
    _linkCompleter = Completer<OAuthLinkResult>();

    try {
      final oauthUrl = '$_baseUrl/oauth/link/$serviceName?mobile=true';
      final uri = Uri.parse(oauthUrl);

      if (await canLaunchUrl(uri)) {
        await launchUrl(
          uri,
          mode: LaunchMode.externalApplication,
        );
      } else {
        _completeLink(OAuthLinkResult.error('Could not launch OAuth URL'));
        return _linkCompleter!.future;
      }

      return await _linkCompleter!.future.timeout(
        const Duration(minutes: 5),
        onTimeout: () => OAuthLinkResult.error('OAuth timeout'),
      );
    } catch (e) {
      print('OAuth error: $e');
      _completeLink(OAuthLinkResult.error('OAuth failed: $e'));
      return _linkCompleter!.future;
    }
  }

  Future<List<OAuthProvider>> getAvailableProviders() async {
    try {
      final dio = Dio(
        BaseOptions(baseUrl: _baseUrl, responseType: ResponseType.json),
      );
      final response = await dio.get('/oauth/available_oauths_login');
      if (response.statusCode == 200 && response.data is List) {
        final List<dynamic> data = response.data;
        final providers = data
            .map((item) => OAuthProvider.fromJson(item as Map<String, dynamic>))
            .toList();
        return providers;
      } else {}
    } catch (e) {}
    return [];
  }

  Future<bool> isAuthenticated() async {
    final sessionCookie = await _storage.read(key: 'session_cookie');
    return sessionCookie != null && sessionCookie.isNotEmpty;
  }

  void _handleDeepLink(Uri uri) {
    print('Received deeplink: $uri');

    if (uri.scheme == 'area' && uri.host == 'oauth-callback') {
      final token = uri.queryParameters['token'];
      final service = uri.queryParameters['service'];
      final error = uri.queryParameters['error'];
      final linked = uri.queryParameters['linked'];

      if (error != null) {
        _completeOAuth(OAuthResult.error('OAuth error: $error'));
        _completeLink(OAuthLinkResult.error('OAuth error: $error'));
      } else if (token != null && service != null) {
        _completeOAuth(OAuthResult.success(token, service));
      } else if (linked == 'true' && service != null) {
        _completeLink(OAuthLinkResult.success(service));
      } else {
        _completeOAuth(OAuthResult.error('Invalid OAuth callback'));
        _completeLink(OAuthLinkResult.error('Invalid OAuth callback'));
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

  OAuthLinkResult.success(this.service)
      : isSuccess = true,
        error = null;

  OAuthLinkResult.error(this.error)
      : isSuccess = false,
        service = null;
}

class OAuthProvider {
  final String name;
  final String imageUrl;
  final String color;

  OAuthProvider({
    required this.name,
    required this.imageUrl,
    required this.color,
  });

  factory OAuthProvider.fromJson(Map<String, dynamic> json) {
    return OAuthProvider(
      name: json['name'] ?? '',
      imageUrl: json['image_url'] ?? '',
      color: json['color'] ?? '#000000',
    );
  }
}