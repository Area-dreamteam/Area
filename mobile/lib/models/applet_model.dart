import 'service_info_model.dart';

class AppletUser {
  final int id;
  final String name;

  AppletUser({required this.id, required this.name});

  factory AppletUser.fromJson(Map<String, dynamic> json) {
    return AppletUser(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }
}

class AppletModel {
  final int id;
  final String name;
  final String? description;
  final AppletUser user;
  final String color;
  final ServiceInfo? triggerService;
  final List<ServiceInfo> reactionServices;

  AppletModel({
    required this.id,
    required this.name,
    this.description,
    required this.user,
    required this.color,
    this.triggerService,
    this.reactionServices = const [],
  });

  factory AppletModel.fromJson(Map<String, dynamic> json) {
    final info = json['area_info'] ?? json;

    var reactionsList = <ServiceInfo>[];
    if (json['reactions'] != null && json['reactions'] is List) {
      reactionsList = (json['reactions'] as List)
          .map((r) => ServiceInfo.fromJson(r['service']))
          .toList();
    }

    ServiceInfo? trigger;
    if (json['action'] != null && json['action']['service'] != null) {
      trigger = ServiceInfo.fromJson(json['action']['service']);
    }

    return AppletModel(
      id: info['id'] as int,
      name: info['name'] as String,
      description: info['description'] as String?,
      user: AppletUser.fromJson(info['user'] as Map<String, dynamic>),
      color: info['color'] as String,
      triggerService: trigger,
      reactionServices: reactionsList,
    );
  }
}
