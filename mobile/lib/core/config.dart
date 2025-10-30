class Config {
  static const String _defaultApiUrl = 'https://area-prod-back.onrender.com';
  
  static String get apiUrl {
    const apiUrlFromEnv = String.fromEnvironment('API_URL', defaultValue: _defaultApiUrl);
    return apiUrlFromEnv;
  }
  
  static bool get isDebug {
    bool inDebugMode = false;
    assert(inDebugMode = true);
    return inDebugMode;
  }
  
  static String getApiUrl() {
    if (isDebug) {
      return apiUrl;
    }
    return apiUrl;
  }
  
  static String getImageUrl(String imagePath) {
    if (imagePath.isEmpty) {
      return '';
    }
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
      return imagePath;
    }
    final baseUrl = getApiUrl();
    if (imagePath.startsWith('/')) {
      return '$baseUrl$imagePath';
    }
    return '$baseUrl/$imagePath';
  }
}
