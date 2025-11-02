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
  final List<String> linkedAccounts;
  final List<OAuthLoginInfo> oauthLogins;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    this.linkedAccounts = const [],
    this.oauthLogins = const [],
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    List<OAuthLoginInfo> oauthLogins = [];
    if (json['oauth_login'] != null) {
      final oauthLoginList = json['oauth_login'] as List<dynamic>;
      oauthLogins = oauthLoginList
          .map((item) => OAuthLoginInfo.fromJson(item as Map<String, dynamic>))
          .toList();
    }

    List<String> linkedAccounts = oauthLogins
        .where((oauth) => oauth.connected)
        .map((oauth) => oauth.name)
        .toList();

    if (json['linked_accounts'] != null) {
      linkedAccounts = List<String>.from(json['linked_accounts']);
    }

    return UserModel(
      id: json['id'] as int,
      name: json['name'] as String,
      email: json['email'] as String,
      role: json['role'] as String,
      linkedAccounts: linkedAccounts,
      oauthLogins: oauthLogins,
    );
  }
}