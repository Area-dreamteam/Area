import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:mobile/services/api_service.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthRepository {
  final ApiService _apiService;

  AuthRepository({required ApiService apiService}) : _apiService = apiService;

  Future<String?> loginWithEmailPassword(String email, String password) async {
    try {
      final response = await _apiService.loginWithEmail(email, password);

      if (response.statusCode == 200 || response.statusCode == 204) {
        if (response.headers.map['set-cookie'] != null) {
          String rawCookie = response.headers.map['set-cookie']![0];
          print('DEBUG loginWithEmailPassword - rawCookie: $rawCookie');
          
          String? sessionCookie = rawCookie.split(';').first;
          print('DEBUG loginWithEmailPassword - sessionCookie after split: $sessionCookie');

          const storage = FlutterSecureStorage();
          await storage.write(key: 'session_cookie', value: sessionCookie);
          
          final storedCookie = await storage.read(key: 'session_cookie');
          print('DEBUG loginWithEmailPassword - storedCookie verification: $storedCookie');
        } else {
          print('DEBUG loginWithEmailPassword - No set-cookie header found!');
        }
        return null;
      }

      if (response.statusCode == 422) {
        return _parseValidationError(response.data);
      }

      if (response.data is String && response.data.isNotEmpty) {
        try {
          final data = jsonDecode(response.data);
          if (data is Map<String, dynamic> && data.containsKey('detail')) {
            final detail = data['detail'];
            if (detail is String) {
              return detail;
            }
          }
        } catch (e) {
          return "Invalid Server response.";
        }
      }

      return "Error ${response.statusCode}: Invalid email or password.";
    } on DioException catch (e) {
      return _handleDioError(e, "Connection Error");
    } catch (e) {
      return "Unknown error: $e";
    }
  }

  Future<String?> register({
    required String email,
    required String password,
  }) async {
    try {
      final response = await _apiService.register(
        email: email,
        password: password,
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        return null;
      }

      if (response.statusCode == 422) {
        return _parseValidationError(response.data);
      }

      if (response.data is String && response.data.isNotEmpty) {
        try {
          final data = jsonDecode(response.data);
          if (data is Map<String, dynamic> && data.containsKey('detail')) {
            final detail = data['detail'];
            if (detail is String) {
              return detail;
            }
          }
        } catch (e) {
          return "Invalid Server response.";
        }
      }

      return "Account creation failed";
    } on DioException catch (e) {
      return _handleDioError(e, "Unable to create account");
    } catch (e) {
      return "Unknown error: $e";
    }
  }

  Future<void> logout() async {
    await _apiService.logout();
  }

  Future<void> deleteProfile(int userId) async {
    await _apiService.deleteUser(userId);
  }

  String _handleDioError(DioException e, String defaultMessage) {
    if (e.response != null && e.response!.statusCode == 422) {
      return _parseValidationError(e.response!.data);
    }

    if (e.response != null &&
        e.response?.data is String &&
        e.response!.data.isNotEmpty) {
      try {
        final data = jsonDecode(e.response!.data);
        if (data is Map<String, dynamic> && data.containsKey('detail')) {
          return data['detail'];
        }
      } catch (parseError) {
        // Fallback to default message
      }
    }

    if (e.type == DioExceptionType.connectionTimeout ||
        e.type == DioExceptionType.unknown) {
      return "Connection error. Please check your internet connection.";
    }

    return defaultMessage;
  }

  String _parseValidationError(dynamic data) {
    try {
      Map<String, dynamic> jsonData;
      if (data is String && data.isNotEmpty) {
        jsonData = jsonDecode(data);
      } else if (data is Map<String, dynamic>) {
        jsonData = data;
      } else {
        return "Invalid input. Please check your data.";
      }

      if (jsonData.containsKey('detail')) {
        final detail = jsonData['detail'];

        if (detail is List && detail.isNotEmpty) {
          final firstError = detail[0];
          if (firstError is Map<String, dynamic> &&
              firstError.containsKey('msg')) {
            String msg = firstError['msg'];
            final type = firstError['type'] as String?;
            final loc = firstError['loc'] as List?;

            final isPasswordError = loc != null && loc.contains('password');

            if (type == 'string_too_short' && isPasswordError) {
              return 'Password must be at least 8 characters long';
            }

            if (msg.startsWith('Value error, ')) {
              msg = msg.substring(13);
            }

            return msg;
          }
        }

        if (detail is String) {
          return detail;
        }
      }

      return "Invalid input. Please check your data.";
    } catch (parseError) {
      return "Invalid input. Please check your data.";
    }
  }
}
