class Config {
  static const String _defaultApiUrl = 'http://10.0.2.2:8080';
  
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
}