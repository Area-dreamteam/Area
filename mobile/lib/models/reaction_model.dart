class Reaction {
  final int id;
  final String name;
  final String description;
  final List<dynamic> configSchema;

  Reaction({
    required this.id,
    required this.name,
    required this.description,
    required this.configSchema,
  });

  factory Reaction.fromJson(Map<String, dynamic> json) {
    return Reaction(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      configSchema: json['config_schema'] ?? [],
    );
  }
}
