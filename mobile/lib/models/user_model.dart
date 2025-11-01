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
  final List<OAuthLoginInfo> oauthLogin;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    this.oauthLogin = const [],
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    var loginList = <OAuthLoginInfo>[];
    if (json['oauth_login'] != null && json['oauth_login'] is List) {
      loginList = (json['oauth_login'] as List)
          .map((item) => OAuthLoginInfo.fromJson(item))
          .toList();
    }

    return UserModel(
      id: json['id'] as int,
      name: json['name'] as String,
      email: json['email'] as String,
      role: json['role'] as String,
      oauthLogin: loginList,
    );
  }
}