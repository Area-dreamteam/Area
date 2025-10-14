class AppletModel {
  final int id;
  final String name;

  AppletModel({
    required this.id,
    required this.name,
  });

  factory AppletModel.fromJson(Map<String, dynamic> json) {
    return AppletModel(
      id: json['id'],
      name: json['name'],
    );
  }
}