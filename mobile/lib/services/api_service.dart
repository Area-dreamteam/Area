import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:mobile/core/config.dart';

class ApiService {
  late Dio _dio;
  final String _baseUrl = Config.getApiUrl();
  final _storage = const FlutterSecureStorage();

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: _baseUrl,
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

  Future<Response> getServiceAuthUrl(String serviceName) {
    return _dio.get(
      '/oauth/index/$serviceName',
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
    required int reactionId,
    required List<dynamic> actionConfig,
    required List<dynamic> reactionConfig,
  }) {
    return _dio.post(
      '/users/areas/me',
      data: {
        'name': name,
        'description': description,
        'action': {'action_id': actionId, 'config': actionConfig},
        'reactions': [
          {'reaction_id': reactionId, 'config': reactionConfig},
        ],
      },
    );
  }

  Future<Response> getCurrentUser() {
    return _dio.get('/users/me');
  }

  Future<Response> deleteUser() {
    return _dio.delete('/users/me');
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

  Future<Response> updateUserPassword({required String newPassword}) {
    return _dio.patch('/users/me/password', data: {"password": newPassword});
  }

  Future<Response> unlinkOAuthAccount(String providerName) {
    return _dio.delete('/oauth/unlink/$providerName');
  }

  Future<Response> getServiceDetails(int serviceId) {
    return _dio.get('/services/$serviceId');
  }

  Future<Response> updateArea({
    required int areaId,
    required String name,
    required String description,
    required int actionId,
    required List<dynamic> actionConfig,
    required int reactionId,
    required List<dynamic> reactionConfig,
  }) {
    final Map<String, dynamic> data = {
      'name': name,
      'description': description,
      'action': {'action_id': actionId, 'config': actionConfig},
      'reactions': [
        {'reaction_id': reactionId, 'config': reactionConfig},
      ],
    };

    return _dio.patch('/users/areas/$areaId', data: data);
  }
}
