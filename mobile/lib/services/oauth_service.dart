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

  /// Initialize OAuth deeplink listener
  void initialize() {
    // Listen for incoming deeplinks
    _linkSubscription = _appLinks.uriLinkStream.listen(
      _handleDeepLink,
      onError: (err) {
        print('OAuth deeplink error: $err');
        _completeOAuth(OAuthResult.error('Deeplink handling error'));
      },
    );
  }

  /// Clean up resources
  void dispose() {
    _linkSubscription?.cancel();
  }

  /// Handle incoming deeplinks
  void _handleDeepLink(Uri uri) {
    print('Received deeplink: $uri');
    
    if (uri.scheme == 'area' && uri.host == 'oauth-callback') {
      final token = uri.queryParameters['token'];
      final service = uri.queryParameters['service'];
      final error = uri.queryParameters['error'];

      if (error != null) {
        _completeOAuth(OAuthResult.error('OAuth error: $error'));
      } else if (token != null && service != null) {
        _completeOAuth(OAuthResult.success(token, service));
      } else {
        _completeOAuth(OAuthResult.error('Invalid OAuth callback'));
      }
    }
  }

  /// Complete OAuth flow
  void _completeOAuth(OAuthResult result) {
    if (_oauthCompleter != null && !_oauthCompleter!.isCompleted) {
      _oauthCompleter!.complete(result);
      _oauthCompleter = null;
    }
  }

  /// Start OAuth login flow for a service
  Future<OAuthResult> loginWithOAuth(String serviceName) async {
    if (_oauthCompleter != null && !_oauthCompleter!.isCompleted) {
      _oauthCompleter!.complete(OAuthResult.error('OAuth already in progress'));
    }

    _oauthCompleter = Completer<OAuthResult>();

    try {
      // Get OAuth URL from backend with mobile indicator
      final oauthUrl = '$_baseUrl/oauth/login_index/$serviceName?mobile=true';
      
      final uri = Uri.parse(oauthUrl);
      
      // Add mobile app header to identify mobile requests
      final dio = Dio();
      dio.options.headers['X-Mobile-App'] = 'true';
      dio.options.headers['User-Agent'] = 'Flutter/Dart Mobile App';
      
      // Launch browser with OAuth URL
      if (await canLaunchUrl(uri)) {
        await launchUrl(
          uri,
          mode: LaunchMode.externalApplication,
        );
      } else {
        _completeOAuth(OAuthResult.error('Could not launch OAuth URL'));
        return _oauthCompleter!.future;
      }

      // Wait for deeplink callback (with timeout)
      final result = await _oauthCompleter!.future.timeout(
        const Duration(minutes: 5),
        onTimeout: () => OAuthResult.error('OAuth timeout'),
      );

      // If successful, store token
      if (result.isSuccess) {
        await _storeAuthToken(result.token!);
      }

      return result;
    } catch (e) {
      print('OAuth error: $e');
      _completeOAuth(OAuthResult.error('OAuth failed: $e'));
      return _oauthCompleter!.future;
    }
  }

  /// Store authentication token securely
  Future<void> _storeAuthToken(String token) async {
    // Store as cookie format for compatibility with existing API service
    await _storage.write(key: 'session_cookie', value: 'access_token=Bearer $token');
  }

  /// Check if user is authenticated
  Future<bool> isAuthenticated() async {
    final sessionCookie = await _storage.read(key: 'session_cookie');
    return sessionCookie != null && sessionCookie.isNotEmpty;
  }

  /// Get available OAuth providers
  Future<List<OAuthProvider>> getAvailableProviders() async {
    try {
      print('Fetching OAuth providers from: $_baseUrl/oauth/available_oauths_login');
      final dio = Dio(BaseOptions(
        baseUrl: _baseUrl,
        responseType: ResponseType.json,
      ));
      final response = await dio.get('/oauth/available_oauths_login');
      
      print('OAuth providers response status: ${response.statusCode}');
      print('OAuth providers response data: ${response.data}');
      
      if (response.statusCode == 200 && response.data is List) {
        final List<dynamic> data = response.data;
        final providers = data.map((item) => OAuthProvider.fromJson(item as Map<String, dynamic>)).toList();
        print('Parsed ${providers.length} OAuth providers: ${providers.map((p) => p.name).toList()}');
        return providers;
      } else {
        print('Invalid response: status=${response.statusCode}, data type=${response.data.runtimeType}');
      }
    } catch (e) {
      print('Error fetching OAuth providers: $e');
    }
    return [];
  }
}

/// OAuth result wrapper
class OAuthResult {
  final bool isSuccess;
  final String? token;
  final String? service;
  final String? error;

  OAuthResult.success(this.token, this.service) 
      : isSuccess = true, error = null;
  
  OAuthResult.error(this.error) 
      : isSuccess = false, token = null, service = null;
}

/// OAuth provider model
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