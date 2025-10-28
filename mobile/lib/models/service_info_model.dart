class ServiceInfo {
  final int id;
  final String name;
  final String color;

  ServiceInfo({
    required this.id,
    required this.name,
    required this.color,
  });

  factory ServiceInfo.fromJson(Map<String, dynamic> json) {
    return ServiceInfo(
      id: json['id'] as int,
      name: json['name'] as String,
      color: json['color'] as String,
    );
  }
}