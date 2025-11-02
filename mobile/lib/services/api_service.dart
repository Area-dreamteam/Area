import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:mobile/core/config.dart';

class ApiService {
  late Dio _dio;
  final _storage = const FlutterSecureStorage();
  bool _initialized = false;

  ApiService() {
    _initializeWithDefaultUrl();
  }

  void _initializeWithDefaultUrl() {
    _dio = Dio(
      BaseOptions(
        baseUrl: 'http://localhost:8080',
        validateStatus: (status) {
          return status != null && status < 500;
        },
        responseType: ResponseType.plain,
      ),
    );
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final sessionCookie = await _storage.read(key: 'session_cookie');

          if (sessionCookie != null) {
            options.headers['Cookie'] = sessionCookie;
          }
          return handler.next(options);
        },
        onError: (DioException e, handler) async {
          if (e.response?.statusCode == 401) {
            await _storage.delete(key: 'session_cookie');
          }
          return handler.next(e);
        },
      ),
    );
  }

  Future<void> initialize() async {
    if (_initialized) return;
    
    final baseUrl = await Config.getApiUrl();
    _dio.options.baseUrl = baseUrl;
    _initialized = true;
  }

  Future<void> updateBaseUrl(String newUrl) async {
    _dio.options.baseUrl = newUrl;
  }

  Future<Response> loginWithEmail(String email, String password) {
    return _dio.post(
      '/auth/login',
      data: {'email': email, 'password': password},
    );
  }

  Future<Response> register({required String email, required String password}) {
    return _dio.post(
      '/auth/register',
      data: {'email': email, 'password': password},
    );
  }

  Future<Response> logout() async {
    await _storage.delete(key: 'session_cookie');
    return _dio.post('/auth/logout');
  }

  Future<Response> getMyAreas() {
    return _dio.get('/users/areas/me');
  }

  Future<Response> getAreaDetails(int areaId) {
    return _dio.get('/areas/$areaId');
  }

  Future<Response> getServices() {
    return _dio.get('/services/list');
  }

  Future<Response> deleteArea(int areaId) {
    return _dio.delete('/areas/$areaId');
  }

  Future<Response> getActionService(String serviceId) {
    return _dio.get('/services/$serviceId/actions');
  }

  Future<Response> getReactionsService(String serviceId) {
    return _dio.get('/services/$serviceId/reactions');
  }

  Future<Response> getActionDetails(int actionId) {
    return _dio.get('/actions/$actionId');
  }

  Future<Response> getReactionDetails(int reactionId) {
    return _dio.get('/reactions/$reactionId');
  }

  Future<Response> getPublicAreas() {
    return _dio.get('/areas/public');
  }

  Future<Response> isServiceConnected(int serviceId) {
    return _dio.get('/services/$serviceId/is_connected');
  }

  Future<Response> enableArea(int areaId) {
    return _dio.patch('/users/areas/$areaId/enable');
  }

  Future<Response> disableArea(int areaId) {
    return _dio.patch('/users/areas/$areaId/disable');
  }

  Future<Response> publishArea(int areaId) {
    return _dio.post('/users/areas/$areaId/publish');
  }

  Future<Response> unpublishArea(int areaId) {
    return _dio.delete('/users/areas/public/$areaId/unpublish');
  }

  Future<Response> getServiceAuthUrl(String serviceName) async {
    final sessionCookie = await _storage.read(key: 'session_cookie');
    print('DEBUG getServiceAuthUrl - sessionCookie: $sessionCookie');
    
    String? token;
    if (sessionCookie != null) {
      // Handle both formats: access_token="Bearer ..." and access_token=Bearer ...
      if (sessionCookie.startsWith('access_token="Bearer ')) {
        // Extract token from quoted format: access_token="Bearer TOKEN"
        final startIndex = 'access_token="Bearer '.length;
        final endIndex = sessionCookie.indexOf('"', startIndex);
        if (endIndex != -1) {
          token = sessionCookie.substring(startIndex, endIndex);
        }
      } else if (sessionCookie.startsWith('access_token=Bearer ')) {
        // Extract token from unquoted format: access_token=Bearer TOKEN
        token = sessionCookie.substring('access_token=Bearer '.length);
      }
      
      if (token != null) {
        print('DEBUG getServiceAuthUrl - extracted token: $token');
      } else {
        print('DEBUG getServiceAuthUrl - failed to extract token from cookie');
      }
    } else {
      print('DEBUG getServiceAuthUrl - sessionCookie is null');
    }

    final path = token != null
        ? '/oauth/index/$serviceName?token=$token'
        : '/oauth/index/$serviceName';
    
    print('DEBUG getServiceAuthUrl - path: $path');

    return _dio.get(
      path,
      options: Options(
        followRedirects: false,
        validateStatus: (status) {
          return (status != null && status < 400);
        },
      ),
    );
  }

  Future<Response> getPublicApplets() {
    return _dio.get('/areas/public');
  }

  Future<Response> getAbout() {
    return _dio.get('/about.json');
  }

  Future<Response> createApplet({
    required String name,
    required String description,
    required int actionId,
    required List<dynamic> actionConfig,
    required List<Map<String, dynamic>> reactions,
  }) {
    return _dio.post(
      '/users/areas/me',
      data: {
        'name': name,
        'description': description,
        'action': {'action_id': actionId, 'config': actionConfig},
        'reactions': reactions,
      },
    );
  }

  Future<Response> getCurrentUser() {
    return _dio.get('/users/me');
  }

  Future<Response> getPublicUserAreas() {
    return _dio.get('/users/areas/public');
  }

  Future<Response> deleteUser(int userId) {
    return _dio.delete('/users/$userId');
  }

  Future<Response> updateCurrentUser({String? name, String? email}) {
    final Map<String, dynamic> data = {};
    if (name != null) {
      data['name'] = name;
    }
    if (email != null) {
      data['email'] = email;
    }
    return _dio.patch('/users/me', data: data);
  }

  Future<Response> updateUserPassword({
    required String newPassword,
    required String currentPassword,
  }) {
    return _dio.patch('/users/me/password',
        data: {"current_password": currentPassword, "new_password": newPassword});
  }

  Future<Response> unlinkOAuthAccount(int oauthId) {
    return _dio.delete('/oauth/oauth_login/$oauthId/disconnect');
  }

  Future<Response> getServiceDetails(int serviceId) {
    return _dio.get('/services/$serviceId');
  }

  Future<Response> copyPublicArea(int areaId) {
    return _dio.post('/areas/public/$areaId/copy');
  }

  Future<Response> updateArea({
    required int areaId,
    required String name,
    required String description,
    required int actionId,
    required List<dynamic> actionConfig,
    required List<Map<String, dynamic>> reactions,
  }) {
    final Map<String, dynamic> data = {
      'name': name,
      'description': description,
      'action': {'action_id': actionId, 'config': actionConfig},
      'reactions': reactions,
    };

    return _dio.patch('/users/areas/$areaId', data: data);
  }

  Future<Response> disconnectService(int serviceId) {
    return _dio.delete('/services/$serviceId/disconnect');
  }

  Future<Response> disconnectOAuthLogin(int oauthLoginId) {
    return _dio.delete('/oauth/oauth_login/$oauthLoginId/disconnect');
  }
}