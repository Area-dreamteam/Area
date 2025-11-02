class OAuthLoginInfo {
  final int id;
  final String name;
  final String? imageUrl;
  final String color;
  final bool connected;

  OAuthLoginInfo({
    required this.id,
    required this.name,
    this.imageUrl,
    required this.color,
    required this.connected,
  });

  factory OAuthLoginInfo.fromJson(Map<String, dynamic> json) {
    return OAuthLoginInfo(
      id: json['id'] as int,
      name: json['name'] as String,
      imageUrl: json['image_url'] as String?,
      color: json['color'] as String,
      connected: json['connected'] as bool,
    );
  }
}

class UserModel {
  final int id;
  final String name;
  final String email;
  final String role;
<<<<<<< Updated upstream
  final List<OAuthLoginInfo> oauthLogin;
=======
  final List<String> linkedAccounts;
  final List<OAuthLoginInfo> oauthLogins;
>>>>>>> Stashed changes

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
<<<<<<< Updated upstream
    this.oauthLogin = const [],
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    var loginList = <OAuthLoginInfo>[];
    if (json['oauth_login'] != null && json['oauth_login'] is List) {
      loginList = (json['oauth_login'] as List)
          .map((item) => OAuthLoginInfo.fromJson(item))
          .toList();
    }

=======
    this.linkedAccounts = const [],
    this.oauthLogins = const [],
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    // Parse oauth_login array if present
    List<OAuthLoginInfo> oauthLogins = [];
    if (json['oauth_login'] != null) {
      final oauthLoginList = json['oauth_login'] as List<dynamic>;
      oauthLogins = oauthLoginList
          .map((item) => OAuthLoginInfo.fromJson(item as Map<String, dynamic>))
          .toList();
    }

    // Extract connected account names from oauth_login for backwards compatibility
    List<String> linkedAccounts = oauthLogins
        .where((oauth) => oauth.connected)
        .map((oauth) => oauth.name)
        .toList();

    // Fallback to old linked_accounts format if oauth_login is not present
    if (json['linked_accounts'] != null) {
      linkedAccounts = List<String>.from(json['linked_accounts']);
    }

>>>>>>> Stashed changes
    return UserModel(
      id: json['id'] as int,
      name: json['name'] as String,
      email: json['email'] as String,
      role: json['role'] as String,
<<<<<<< Updated upstream
      oauthLogin: loginList,
=======
      linkedAccounts: linkedAccounts,
      oauthLogins: oauthLogins,
>>>>>>> Stashed changes
    );
  }
}