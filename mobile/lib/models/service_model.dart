class Service {
  final int id;
  final String name;
  final String category;
  final String? iconUrl;
  final String color;

  Service({
    required this.id,
    required this.name,
    required this.iconUrl,
    required this.category,
    required this.color,
  });

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id'],
      name: json['name'],
      category: json['category'],
      color: json['color'],
      iconUrl: json['icon'],
    );
  }
}
