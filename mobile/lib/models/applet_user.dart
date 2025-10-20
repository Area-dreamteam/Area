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