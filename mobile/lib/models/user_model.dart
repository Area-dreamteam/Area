class UserModel {
  final int id;
  final String name;
  final String email;
  final String role;
  final List<String> linkedAccounts;

  UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    this.linkedAccounts = const [],
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as int,
      name: json['name'] as String,
      email: json['email'] as String, 
      role: json['role'] as String,
      linkedAccounts: List<String>.from(json['linked_accounts'] ?? []),
    );
  }
}