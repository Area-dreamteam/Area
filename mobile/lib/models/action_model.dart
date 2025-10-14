class ActionModel {
  final int id;
  final String name;
  final String description;
  final List<dynamic> configSchema;

  ActionModel({
    required this.id,
    required this.name,
    required this.description,
    required this.configSchema,
  });

  factory ActionModel.fromJson(Map<String, dynamic> json) {
    return ActionModel(
      id: json['id'],
      name: json['name'],
      description: json['description'],
      configSchema: json['config_schema'] ?? [],
    );
  }
}
