import 'package:mobile/models/service_info_model.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/models/user_model.dart';
import 'dart:convert';

String? _getConfigJson(dynamic configData) {
  if (configData == null) return null;
  if (configData is String) return configData.isNotEmpty ? configData : null;
  if (configData is Map || configData is List) return jsonEncode(configData);
  return null;
}

class ServiceRepository {
  final ApiService _apiService;

  ServiceRepository({required ApiService apiService})
    : _apiService = apiService;

  Future<List<Service>> fetchAvailableServices() async {
    try {
      final response = await _apiService.getServices();

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        return data.map((json) => Service.fromJson(json)).toList();
      }
      throw Exception('Failed to load services');
    } catch (e) {
      rethrow;
    }
  }

  Future<List<ActionModel>> fetchActionsService(String serviceId) async {
    try {
      final response = await _apiService.getActionService(serviceId);

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        return data.map((json) => ActionModel.fromJson(json)).toList();
      }
      throw Exception('Failed to load actions for service $serviceId');
    } catch (e) {
      rethrow;
    }
  }

  Future<List<Reaction>> fetchReactionsService(String serviceId) async {
    try {
      final response = await _apiService.getReactionsService(serviceId);

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        return data.map((json) => Reaction.fromJson(json)).toList();
      }
      throw Exception('Failed to load reactions details for $serviceId');
    } catch (e) {
      rethrow;
    }
  }

  Future<ActionModel> fetchActionDetails(int actionId) async {
    try {
      final response = await _apiService.getActionDetails(actionId);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.data);
        return ActionModel.fromJson(data);
      }
      throw Exception('Failed to load action details for $actionId');
    } catch (e) {
      rethrow;
    }
  }

  Future<Reaction> fetchReactionDetails(int reactionId) async {
    try {
      final response = await _apiService.getReactionDetails(reactionId);

      if (response.statusCode == 200) {
        dynamic data = jsonDecode(response.data);
        if (data is List) {
          if (data.isNotEmpty) {
            data = data.first;
          } else {
            throw Exception(
              'Reaction details response is an empty list for id $reactionId',
            );
          }
        }
        return Reaction.fromJson(data);
      }
      throw Exception('Failed to load reaction details for id $reactionId');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> createApplet({
    required String name,
    required String description,
    required int actionId,
    required List<dynamic> actionConfig,
    required List<Map<String, dynamic>> reactions,
  }) async {
    try {
      final response = await _apiService.createApplet(
        name: name,
        description: description,
        actionId: actionId,
        actionConfig: actionConfig,
        reactions: reactions,
      );
      if (response.statusCode != 200 && response.statusCode != 201) {
        throw Exception('Failed to create applet: ${response.data}');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> deleteArea(int areaId) async {
    try {
      final response = await _apiService.deleteArea(areaId);

      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to delete area');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<List<AppletModel>> fetchMyAreas() async {
    try {
      final response = await _apiService.getMyAreas();
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        return data
            .map((json) => AppletModel.fromJson(json, forceIsPublic: false))
            .toList();
      }
      throw Exception('Failed to load areas');
    } catch (e) {
      rethrow;
    }
  }

  Future<List<AppletModel>> fetchPublicUserAreas() async {
    try {
      final response = await _apiService.getPublicUserAreas();

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        return data
            .map((json) => AppletModel.fromJson(json, forceIsPublic: true))
            .toList();
      }
      throw Exception('Failed to load public user areas');
    } catch (e) {
      rethrow;
    }
  }

  Future<AppletModel> fetchAreaDetails(
    int areaId, {
    required bool isPublic,
  }) async {
    try {
      final response = await _apiService.getAreaDetails(areaId);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.data);

        final areaInfo = data['area_info'] as Map<String, dynamic>;
        final actionData = data['action'] as Map<String, dynamic>;
        final reactionDataList = data['reactions'] as List<dynamic>;

        final triggerService = ServiceInfo.fromJson(actionData['service']);
        final reactionServices = reactionDataList
            .map((r) => ServiceInfo.fromJson(r['service']))
            .toList();

        final reactionsInfoList = reactionDataList
            .map(
              (r) => AppletReactionInfo(
                id: r['id'],
                configJson: _getConfigJson(r['config']),
                service: ServiceInfo.fromJson(r['service']),
              ),
            )
            .toList();

        return AppletModel(
          id: areaInfo['id'],
          name: areaInfo['name'],
          description: areaInfo['description'],
          user: AppletUser.fromJson(areaInfo['user']),
          color: areaInfo['color'],
          isEnabled: areaInfo['enable'],
          isPublic: isPublic,

          triggerService: triggerService,
          reactionServices: reactionServices,
          reactions: reactionsInfoList,

          actionId: actionData['id'],
          actionConfigJson: _getConfigJson(actionData['config']),
        );
      }
      throw Exception('Failed to load area details: ${response.statusCode}');
    } catch (e) {
      rethrow;
    }
  }

  Future<UserModel> fetchCurrentUser() async {
    try {
      final response = await _apiService.getCurrentUser();

      if (response.statusCode == 200) {
        final data = jsonDecode(response.data);
        return UserModel.fromJson(data);
      }
      throw Exception(
        'Failed to load current user: Status ${response.statusCode}',
      );
    } catch (e) {
      rethrow;
    }
  }

  Future<List<AppletModel>> fetchPublicAreas() async {
    try {
      final response = await _apiService.getPublicAreas();
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        return data
            .map((json) => AppletModel.fromJson(json, forceIsPublic: true))
            .toList();
      }
      throw Exception('Failed to load public areas');
    } catch (e) {
      rethrow;
    }
  }

  Future<String?> fetchServiceAuthUrl(String serviceName) async {
    try {
      final response = await _apiService.getServiceAuthUrl(serviceName);

      if (response.statusCode == 200) {
        return response.data as String?;
      }

      if (response.statusCode == 302) {
        if (response.headers.map.containsKey('location')) {
          return response.headers.map['location']![0];
        }
      }

      return null;
    } catch (e) {
      return null;
    }
  }

  Future<List<AppletModel>> fetchPublicApplets({int? serviceId}) async {
    try {
      final response = await _apiService.getPublicApplets();
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        List<AppletModel> applets = data
            .map((json) => AppletModel.fromJson(json, forceIsPublic: true))
            .toList();

        if (serviceId != null) {
          applets = applets.where((applet) {
            bool isTrigger = applet.triggerService?.id == serviceId;
            bool isReaction = applet.reactionServices.any(
              (s) => s.id == serviceId,
            );
            return isTrigger || isReaction;
          }).toList();
        }
        return applets;
      }
      throw Exception('Failed to load public areas');
    } catch (e) {
      rethrow;
    }
  }

  Future<bool> isServiceConnected(int serviceId) async {
    try {
      final response = await _apiService.isServiceConnected(serviceId);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.data);
        if (data is Map && data.containsKey('is_connected')) {
          return data['is_connected'] as bool;
        }
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  Future<UserModel?> updateCurrentUser({String? name, String? email}) async {
    try {
      final response = await _apiService.updateCurrentUser(
        name: name,
        email: email,
      );
      if (response.statusCode == 200 || response.statusCode == 204) {
        if (response.data != null) {
          final data = jsonDecode(response.data);
          return UserModel.fromJson(data);
        }
        return null;
      } else {
        throw Exception('Failed to update user');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> updateUserPassword({
    required String newPassword,
    required String currentPassword,
  }) async {
    String errorMessage = "Problem to update password";
    try {
      final response = await _apiService.updateUserPassword(
        newPassword: newPassword,
        currentPassword: currentPassword,
      );
      if (response.statusCode == 200 || response.statusCode == 204) {
        return;
      }
      throw Exception(errorMessage);
    } catch (e) {
      rethrow;
    }
  }

  Future<Service> fetchServiceDetails(int serviceId) async {
    try {
      final response = await _apiService.getServiceDetails(serviceId);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.data);
        return Service.fromJson(data);
      }
      throw Exception('Failed to load service details for $serviceId');
    } catch (e) {
      rethrow;
    }
  }

  Future<void> enableArea(int areaId) async {
    try {
      final response = await _apiService.enableArea(areaId);
      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to enable area : ${response.data}');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> disableArea(int areaId) async {
    try {
      final response = await _apiService.disableArea(areaId);
      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception("Failed to disable area: ${response.data}");
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> publishArea(int areaId) async {
    try {
      final response = await _apiService.publishArea(areaId);
      if (response.statusCode != 200 &&
          response.statusCode != 201 &&
          response.statusCode != 204) {
        throw Exception("Failed to publish area: ${response.data}");
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> unpublishArea(int areaId) async {
    try {
      final response = await _apiService.unpublishArea(areaId);
      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception(
          "Failed to unpublish area: ${response.statusCode} ${response.data}",
        );
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> copyPublicArea(int areaId) async {
    try {
      final response = await _apiService.copyPublicArea(areaId);
      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception("Failed to copy area : ${response.data}");
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> updateArea({
    required int areaId,
    required String name,
    required String description,
    required int actionId,
    required List<dynamic> actionConfig,
    required List<Map<String, dynamic>> reactions,
  }) async {
    try {
      final response = await _apiService.updateArea(
        areaId: areaId,
        name: name,
        description: description,
        actionId: actionId,
        actionConfig: actionConfig,
        reactions: reactions,
      );

      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Échec de la mise à jour de l\'Area: ${response.data}');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> disconnectService(int serviceId) async {
    try {
      final response = await _apiService.disconnectService(serviceId);
      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to disconnect service: ${response.data}');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> disconnectOAuthLogin(int oauthLoginId) async {
    try {
      final response = await _apiService.disconnectOAuthLogin(oauthLoginId);
      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to disconnect OAuth login: ${response.data}');
      }
    } catch (e) {
      rethrow;
    }
  }

  Future<void> unlinkOAuthAccount(int oauthId) async {
    try {
      final response = await _apiService.unlinkOAuthAccount(oauthId);
      if (response.statusCode != 200 && response.statusCode != 204) {
        throw Exception('Failed to unlink OAuth account: ${response.data}');
      }
    } catch (e) {
      rethrow;
    }
  }
}
