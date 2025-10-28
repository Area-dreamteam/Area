class ServiceInfo {
  final int id;
  final String name;

  ServiceInfo({
    required this.id,
    required this.name,
  });

  factory ServiceInfo.fromJson(Map<String, dynamic> json) {
    return ServiceInfo(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }
}