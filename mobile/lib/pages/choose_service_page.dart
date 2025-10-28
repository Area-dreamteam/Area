// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/viewmodels/select_service_viewmodel.dart';
import 'package:mobile/widgets/service_card.dart';
import 'package:provider/provider.dart';
import 'choose_action_page.dart';
import 'package:mobile/widgets/search_bar.dart';
import 'package:mobile/pages/connect_service_page.dart';

class ChooseServicePage extends StatefulWidget {
  final String type;
  const ChooseServicePage({super.key, required this.type});

  @override
  State<ChooseServicePage> createState() => _ChooseServicePageState();
}

class _ChooseServicePageState extends State<ChooseServicePage> {
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SelectServiceViewmodel>().fetchServices();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Choose a service",
          style: TextStyle(color: Colors.white),
        ),
        backgroundColor: const Color(0xFF212121),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      backgroundColor: const Color(0xFF212121),
      body: Consumer<SelectServiceViewmodel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const Center(
              child: CircularProgressIndicator(color: Colors.white),
            );
          }

          final search = _searchController.text.toLowerCase();
          List<dynamic> filteredServices;

          if (search.isEmpty) {
            filteredServices = viewModel.services;
          } else {
            filteredServices = viewModel.services.where((service) {
              return service.name.toLowerCase().contains(search);
            }).toList();
          }
          return Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16.0,
                  vertical: 12.0,
                ),
                child: MySearchBar(
                  controller: _searchController,
                  onChanged: (value) {
                    setState(() {});
                  },
                ),
              ),
              Expanded(
                child: GridView.builder(
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    crossAxisSpacing: 10,
                    mainAxisSpacing: 10,
                    childAspectRatio: 1.0,
                  ),
                  padding: const EdgeInsets.all(10),
                  itemCount: filteredServices.length,
                  itemBuilder: (context, index) {
                    final serviceFromList = filteredServices[index];
                    final serviceRepo = context.read<ServiceRepository>();

                    return ServiceCard(
                      id: serviceFromList.id,
                      name: serviceFromList.name,
                      description: serviceFromList.description,
                      category: serviceFromList.category,
                      colorHex: serviceFromList.color,
                      onTap: () async {
                        showDialog(
                          context: context,
                          barrierDismissible: false,
                          builder: (context) => const Center(
                            child: CircularProgressIndicator(color: Colors.white),
                          ),
                        );

                        Service detailedService;
                        try {
                          detailedService = await serviceRepo
                              .fetchServiceDetails(serviceFromList.id);
                          if (context.mounted) Navigator.pop(context);
                        } catch (e) {
                          if (context.mounted) Navigator.pop(context);
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                                content:
                                    Text("Error fetching service details: $e"),
                                backgroundColor: Colors.red),
                          );
                          return;
                        }
                        bool proceedToActions = false;

                        if (detailedService.oauthRequired) {
                          final isConnected = await serviceRepo
                              .isServiceConnected(detailedService.id);

                          if (isConnected) {
                            proceedToActions = true;
                          } else {
                            if (!context.mounted) return;
                            final connectionResult = await Navigator.push<bool>(
                              context,
                              MaterialPageRoute(
                                builder: (context) =>
                                    ConnectServicePage(service: detailedService),
                              ),
                            );
                            if (connectionResult == true) {
                              proceedToActions = true;
                            }
                          }
                        } else {
                          proceedToActions = true;
                        }

                        if (proceedToActions && context.mounted) {
                          final result =
                              await Navigator.push<ConfiguredItem<dynamic>?>(
                            context,
                            MaterialPageRoute(
                              builder: (context) => ChooseActionPage(
                                service:
                                    detailedService,
                                type: widget.type,
                                serviceRepository: serviceRepo,
                              ),
                            ),
                          );
                          if (result != null && context.mounted) {
                            Navigator.pop(context, result);
                          }
                        }
                      },
                    );
                  },
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}