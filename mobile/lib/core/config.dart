import 'package:mobile/services/api_url_service.dart';

class Config {
  static bool get isDebug {
    bool inDebugMode = false;
    assert(inDebugMode = true);
    return inDebugMode;
  }
  
  static Future<String> getApiUrl() async {
    return await ApiUrlService.getApiUrl();
  }
  
  static Future<String> getImageUrl(String imagePath) async {
    if (imagePath.isEmpty) {
      return '';
    }
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
      return imagePath;
    }
    final baseUrl = await getApiUrl();
    if (imagePath.startsWith('/')) {
      return '$baseUrl$imagePath';
    }
    return '$baseUrl/$imagePath';
  }
}
