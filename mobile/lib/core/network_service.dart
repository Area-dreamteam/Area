import 'dart:convert';
import 'constants.dart';
import 'package:dio/dio.dart';

class NetworkService {
  late final Dio _dio;
  final JsonEncoder _encoder = const JsonEncoder();

  static final NetworkService _instance = NetworkService.internal();
  NetworkService.internal();
  static NetworkService get instance => _instance;

  Future<void> initClient() async {
    _dio = Dio(
      BaseOptions(
        baseUrl: Constant.baseUrl,
        connectTimeout: const Duration(seconds: 60),
        receiveTimeout: const Duration(seconds: 60),
      ),
    );
  }

  Future<dynamic> get(
    String path, {
    Map<String, dynamic>? queryParameters,
    Map<String, dynamic>? headers,
  }) async {
    try {
      final response = await _dio.get(
        path,
        queryParameters: queryParameters,
        options: Options(headers: headers),
      );
      return response.data;
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? e.toString());
    }
  }

  Future<dynamic> post(
    String url, {
    required dynamic body,
    Map<String, dynamic>? headers,
  }) async {
    try {
      final response = await _dio.post(
        url,
        data: _encoder.convert(body),
        options: Options(headers: headers, contentType: 'application/json'),
      );
      return response.data;
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? e.toString());
    }
  }

  Future<dynamic> patch(
    String url, {
    required dynamic body,
    Map<String, dynamic>? encoding,
  }) async {
    try {
      final response = await _dio.patch(url, data: _encoder.convert(body));
      return response.data;
    } on DioException catch (e) {
      throw Exception(e.response?.data['detail'] ?? e.toString());
    } catch (e) {
      rethrow;
    }
  }
}
