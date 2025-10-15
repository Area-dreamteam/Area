class Service {
  final int id;
  final String name;
  final String? description;
  final String imageUrl;
  final String? category;
  final String? color;

  Service({
    required this.id,
    required this.name,
    this.description,
    required this.imageUrl,
    this.category,
    this.color,
  });

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id'] as int,
      name: json['name'] as String,
      description: json['description'] as String?, 
      imageUrl: json['image_url'] as String,
      category: json['category'] as String?,
      color: json['color'] as String?,
    );
  }
}