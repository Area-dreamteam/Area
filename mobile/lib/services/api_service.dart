import 'package:dio/dio.dart';

class ApiService {
  late Dio _dio;
  static const String _baseUrl = 'http://10.0.2.2:8080/';

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

  Future<Response> logout() {
    return _dio.post('/auth/logout');
  }

//  Future<Response> getMyApplet() {
  //  return _dio.get('/applet/user');
 // }
}
