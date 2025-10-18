import 'package:mobile/models/service_model.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/models/user_model.dart';
import 'dart:convert';

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
    required int reactionId,
    required List<dynamic> reactionConfig,
  }) async {
    try {
      final response = await _apiService.createApplet(
        name: name,
        description: description,
        actionId: actionId,
        actionConfig: actionConfig,
        reactionId: reactionId,
        reactionConfig: reactionConfig,
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
      final response = await _apiService
          .getMyAreas();
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.data);
        return data.map((json) => AppletModel.fromJson(json)).toList();
      }
      throw Exception('Failed to load areas');
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
        return data.map((json) => AppletModel.fromJson(json)).toList();
      }
      throw Exception('Failed to load public areas');
    } catch (e) {
      rethrow;
    }
  }
}
