import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/models/applet_model.dart';

class ExploreItem {
  final String id;
  final String type;
  final String title;
  final String? byText;
  final String colorHex;
  final dynamic data;

  ExploreItem({
    required this.id,
    required this.type,
    required this.title,
    this.byText,
    required this.colorHex,
    required this.data,
  });
}

class ExploreViewModel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;
  ExploreViewModel({required ServiceRepository serviceRepository})
      : _serviceRepository = serviceRepository;

  List<ExploreItem> _allItems = [];
  bool _isLoading = false;
  String? _errorMessage;

  List<ExploreItem> get allItems => _allItems;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  Future<void> fetchExploreItems() async {
    if (_isLoading) return;

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final servicesFuture = _serviceRepository.fetchAvailableServices();
      final publicAreasFuture = _serviceRepository.fetchPublicAreas();

      final results = await Future.wait([servicesFuture, publicAreasFuture]);

      final List<Service> services = results[0] as List<Service>;
      final List<AppletModel> publicAreas = results[1] as List<AppletModel>;

      final List<ExploreItem> items = [];

      for (var service in services) {
        items.add(ExploreItem(
          id: 'S-${service.id}',
          type: 'Service',
          title: service.name,
          colorHex: service.color ?? '#CCCCCC',
          data: service,
        ));
      }

      for (var applet in publicAreas) {
        items.add(ExploreItem(
          id: 'A-${applet.id}',
          type: 'Applet',
          title: applet.name,
          byText: 'By ${applet.user.name}',
          colorHex: applet.color,
          data: applet,
        ));
      }

      _allItems = items;
    } catch (e) {
      _errorMessage = 'Failed to load items: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}