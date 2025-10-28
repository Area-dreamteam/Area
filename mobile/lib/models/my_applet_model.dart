import 'package:mobile/models/service_info_model.dart';

class MyAppletModel {
  final int id;
  final String name;
  final bool isEnabled;
  final bool isPublic;
  final ServiceInfo? serviceTrigger;
  final ServiceInfo? serviceReaction;

  MyAppletModel({
    required this.id,
    required this.name,
    required this.isEnabled,
    required this.isPublic,
    this.serviceTrigger,
    this.serviceReaction,
  });

  factory MyAppletModel.fromJson(Map<String, dynamic> json) {
    
    ServiceInfo? trigger;
    if (json['action'] is Map && json['action']['service'] != null) {
      trigger = ServiceInfo.fromJson(json['action']['service']);
    }

    ServiceInfo? reaction;
    if (json['reactions'] is List &&
        (json['reactions'] as List).isNotEmpty &&
        json['reactions'].first['service'] != null) {
      reaction = ServiceInfo.fromJson(json['reactions'].first['service']);
    }

    return MyAppletModel(
      id: json['id'] as int,
      name: json['name'] as String,
      isEnabled: json['is_enabled'] as bool? ?? false,
      isPublic: json['is_public'] as bool? ?? false,
      serviceTrigger: trigger,
      serviceReaction: reaction,
    );
  }
}
