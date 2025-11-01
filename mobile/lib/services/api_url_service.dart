import 'package:shared_preferences/shared_preferences.dart';

class ApiUrlService {
  static const String _apiUrlKey = 'custom_api_url';
  static const String _defaultApiUrl = 'https://area-prod-back.onrender.com';
  
  static String? _cachedApiUrl;

  static Future<String> getApiUrl() async {
    if (_cachedApiUrl != null) {
      return _cachedApiUrl!;
    }
    
    final prefs = await SharedPreferences.getInstance();
    final customUrl = prefs.getString(_apiUrlKey);
    
    if (customUrl != null && customUrl.isNotEmpty) {
      _cachedApiUrl = customUrl;
      return customUrl;
    }
    
    // Fallback to environment variable or default
    const apiUrlFromEnv = String.fromEnvironment('API_URL', defaultValue: _defaultApiUrl);
    _cachedApiUrl = apiUrlFromEnv;
    return apiUrlFromEnv;
  }

  static Future<void> setApiUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_apiUrlKey, url);
    _cachedApiUrl = url;
  }

  static Future<void> resetApiUrl() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_apiUrlKey);
    const apiUrlFromEnv = String.fromEnvironment('API_URL', defaultValue: _defaultApiUrl);
    _cachedApiUrl = apiUrlFromEnv;
  }

  static Future<String> getDefaultApiUrl() async {
    const apiUrlFromEnv = String.fromEnvironment('API_URL', defaultValue: _defaultApiUrl);
    return apiUrlFromEnv;
  }

  static void clearCache() {
    _cachedApiUrl = null;
  }
}
