import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiService {
  late Dio _dio;
  static const String _baseUrl = 'http://10.0.2.2:8080/';
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
    return _dio.get('/areas');
  }

  Future<Response> getServices() {
    return _dio.get('/services');
  }

  Future<Response> deleteArea(String areaId) {
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

  Future<Response> createApplet({
    required String name,
    required String description,
    required int actionId,
    required int reactionId,
    required List<dynamic> actionConfig,
    required List<dynamic> reactionConfig,
  }) {
    return _dio.post(
      '/areas',
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
}
