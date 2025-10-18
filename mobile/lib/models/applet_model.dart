class AppletModel {
  final int id;
  final String name;
  final AppletUser user;
  final String color;

  AppletModel({
    required this.id,
    required this.name,
    required this.user,
    required this.color,
  });

  factory AppletModel.fromJson(Map<String, dynamic> json) {
    return AppletModel(
      id: json['id'] as int,
      name: json['name'] as String,
      user: AppletUser.fromJson(json['user'] as Map<String, dynamic>), 
      color: json['color'] as String,
    );
  }
}

class AppletUser {
  final int id;
  final String name;

  AppletUser({required this.id, required this.name});

  factory AppletUser.fromJson(Map<String, dynamic> json) {
    return AppletUser(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }
}