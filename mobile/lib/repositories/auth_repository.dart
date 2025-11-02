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
          
          // Verify it was stored correctly
          final storedCookie = await storage.read(key: 'session_cookie');
          print('DEBUG loginWithEmailPassword - storedCookie verification: $storedCookie');
        } else {
          print('DEBUG loginWithEmailPassword - No set-cookie header found!');
        }
        return null;
      }

      if (response.data is String && response.data.isNotEmpty) {
        try {
          final data = jsonDecode(response.data);
          if (data is Map<String, dynamic> && data.containsKey('detail')) {
            return data['detail'];
          }
        } catch (e) {
          return "Réponse invalide du serveur.";
        }
      }

      return "Erreur ${response.statusCode}: email ou mot de passe invalide.";
    } on DioException catch (e) {
      return _handleDioError(e, "Erreur de connexion");
    } catch (e) {
      return "Erreur inconnue.";
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
      return "Creation account failed";
    } on DioException catch (e) {
      return _handleDioError(e, "Impossible to create account");
    } catch (e) {
      return "Unknown error";
    }
  }

  Future<void> logout() async {
    await _apiService.logout();
  }

  Future<void> deleteProfile(int userId) async {
    await _apiService.deleteUser(userId);
  }

  String _handleDioError(DioException e, String defaultMessage) {
    if (e.response != null &&
        e.response?.data is String &&
        e.response!.data.isNotEmpty) {
      final data = jsonDecode(e.response!.data);
      if (data is Map<String, dynamic> && data.containsKey('detail')) {
        return data['detail'];
      }
    }
    if (e.type == DioExceptionType.connectionTimeout ||
        e.type == DioExceptionType.unknown) {
      return "Erreur connexion to server";
    }
    return defaultMessage;
  }
}
