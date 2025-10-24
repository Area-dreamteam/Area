class Config {
  static const String _defaultApiUrl = 'http://10.0.2.2:8080';
  
  /// Get API base URL from environment or use default
  static String get apiUrl {
    // For Flutter, we'll use compile-time constants
    // You can override this during build with --dart-define
    const apiUrlFromEnv = String.fromEnvironment('API_URL', defaultValue: _defaultApiUrl);
    return apiUrlFromEnv;
  }
  
  /// Check if running in debug mode
  static bool get isDebug {
    bool inDebugMode = false;
    assert(inDebugMode = true);
    return inDebugMode;
  }
  
  /// Get the appropriate API URL based on environment
  static String getApiUrl() {
    if (isDebug) {
      // In debug mode, you might want to use your local machine's IP
      // This will be configurable via --dart-define API_URL=http://YOUR_IP:8080
      return apiUrl;
    }
    return apiUrl;
  }
}