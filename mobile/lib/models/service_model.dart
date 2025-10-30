class Service {
  final int id;
  final String name;
  final String? description;
  final String? category;
  final String? color;
  final bool oauthRequired;
  final String? imageUrl;

  Service({
    required this.id,
    required this.name,
    this.description,
    this.category,
    this.color,
    this.oauthRequired = false,
    this.imageUrl,
  });

  factory Service.fromJson(Map<String, dynamic> json) {
    return Service(
      id: json['id'] as int,
      name: json['name'] as String,
      description: json['description'] as String?,
      category: json['category'] as String?,
      color: json['color'] as String?,
      oauthRequired: json['oauth_required'] ?? false,
      imageUrl: json['image_url'] as String?,
    );
  }
}
