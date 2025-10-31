import 'dart:convert';
import 'service_info_model.dart';

class AppletUser {
  final int id;
  final String name;

  AppletUser({required this.id, required this.name});

  factory AppletUser.fromJson(Map<String, dynamic> json) {
    return AppletUser(id: json['id'] as int, name: json['name'] as String);
  }
}

String? _getConfigJson(dynamic configData) {
  if (configData == null) return null;
  if (configData is String) return configData.isNotEmpty ? configData : null;
  if (configData is Map || configData is List) return jsonEncode(configData);
  return null;
}

class AppletReactionInfo {
  final int id;
  final String? configJson;
  final ServiceInfo service;

  AppletReactionInfo({
    required this.id,
    this.configJson,
    required this.service,
  });
}

class AppletModel {
  final int id;
  final String name;
  final String? description;
  final AppletUser user;
  final String color;

  final ServiceInfo? triggerService;
  final List<ServiceInfo> reactionServices;
  final List<AppletReactionInfo> reactions;

  final bool isEnabled;
  final bool isPublic;
  final int? actionId;
  final String? actionConfigJson;

  AppletModel({
    required this.id,
    required this.name,
    this.description,
    required this.user,
    required this.color,
    this.triggerService,
    this.reactionServices = const [],
    this.reactions = const [],
    required this.isEnabled,
    required this.isPublic,
    this.actionId,
    this.actionConfigJson,
  });

  factory AppletModel.fromJson(
    Map<String, dynamic> json, {
    bool? forceIsPublic,
  }) {
    var reactionsList = <ServiceInfo>[];
    var reactionsInfoList = <AppletReactionInfo>[];
    final dynamic rawReactions = json['reactions'];

    if (rawReactions != null && rawReactions is List<dynamic>) {
      reactionsList = rawReactions
          .where((r) => r is Map && r['service'] != null)
          .map((r) => ServiceInfo.fromJson(r['service']))
          .toList();

      reactionsInfoList = rawReactions
          .where(
            (r) =>
                r is Map &&
                r['service'] != null &&
                (r['id'] ?? r['reaction_id']) != null,
          )
          .map(
            (r) => AppletReactionInfo(
              id: (r['id'] ?? r['reaction_id']) as int,
              configJson: _getConfigJson(r['config']),
              service: ServiceInfo.fromJson(r['service']),
            ),
          )
          .toList();
    }

    ServiceInfo? trigger;
    if (json['action'] is Map && json['action']['service'] != null) {
      trigger = ServiceInfo.fromJson(json['action']['service']);
    }

    return AppletModel(
      id: json['id'] as int,
      name: json['name'] as String,
      description: json['description'] as String?,
      user: AppletUser.fromJson(json['user'] as Map<String, dynamic>),
      color: json['color'] as String? ?? '#CCCCCC',
      triggerService: trigger,
      reactionServices: reactionsList,
      reactions: reactionsInfoList,
      isEnabled: json['enable'] as bool? ?? false,
      isPublic: forceIsPublic ?? (json['public'] as bool? ?? false),
      actionId: (json['action']?['id'] ?? json['action']?['action_id']) as int?,
      actionConfigJson: _getConfigJson(json['action']?['config']),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'description': description,
    'user': user.toJson(),
    'color': color,
    'triggerService': triggerService?.toJson(),
    'reactionServices': reactionServices.map((s) => s.toJson()).toList(),
    'is_enabled': isEnabled,
    'is_public': isPublic,
    if (actionId != null) 'action_id': actionId,
    if (actionConfigJson != null) 'action_config': actionConfigJson,
    'reactions': reactions
        .map(
          (r) => {
            'id': r.id,
            'config': r.configJson,
            'service': r.service.toJson(),
          },
        )
        .toList(),
  };
}

extension AppletUserToJson on AppletUser {
  Map<String, dynamic> toJson() => {'id': id, 'name': name};
}

extension ServiceInfoToJson on ServiceInfo {
  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'color': color,
    'image_url': imageUrl,
  };
}
