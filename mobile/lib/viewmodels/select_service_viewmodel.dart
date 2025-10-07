import 'package:flutter/material.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/repositories/service_repository.dart';

enum SelectServiceState { nothing, loading, success, error }

class SelectServiceViewmodel extends ChangeNotifier {
  final ServiceRepository _serviceRepository;

  SelectServiceViewmodel({required ServiceRepository serviceRepository})
    : _serviceRepository = serviceRepository;

  SelectServiceState _state = SelectServiceState.nothing;
  String _errorMessage = '';
  List<Service> _services = [];

  SelectServiceState get state => _state;
  String get errorMessage => _errorMessage;
  List<Service> get services => _services;
  bool get isLoading => _state == SelectServiceState.loading;

  Future<bool> fetchServices() async {
    _setState(SelectServiceState.loading);
    try {
      _services = await _serviceRepository.fetchAvailableServices();
      _setState(SelectServiceState.success);
      return true;
    } catch (e) {
      _errorMessage = "Can't load services";
      _setState(SelectServiceState.error);
      return false;
    }
  }

  void _setState(SelectServiceState newState) {
    _state = newState;
    notifyListeners();
  }
}
