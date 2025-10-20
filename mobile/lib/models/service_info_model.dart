class ServiceInfo {
  final int id;
  final String name;
  final String imageUrl;

  ServiceInfo({
    required this.id,
    required this.name,
    required this.imageUrl,
  });

  factory ServiceInfo.fromJson(Map<String, dynamic> json) {
    return ServiceInfo(
      id: json['id'] as int,
      name: json['name'] as String,
      imageUrl: json['image_url'] as String,
    );
  }
}