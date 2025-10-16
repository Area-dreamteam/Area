import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/viewmodels/select_service_viewmodel.dart';
import 'package:mobile/widgets/service_card.dart';
import 'package:provider/provider.dart';
import 'choose_action_page.dart';
import 'package:mobile/widgets/search_bar.dart';

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
        title: const Text("Choose a service"),
        backgroundColor: Colors.white,
        iconTheme: const IconThemeData(color: Colors.black),
      ),
      backgroundColor: const Color(0xFF212121),
      body: Consumer<SelectServiceViewmodel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const Center(
              child: CircularProgressIndicator(color: Colors.white),
            );
          }
          if (viewModel.state == SelectServiceState.error) {
            return Center(
              child: Text(
                viewModel.errorMessage,
                style: const TextStyle(color: Colors.red),
              ),
            );
          }

          final search = _searchController.text.toLowerCase();
          List<dynamic> filteredServices;

          if (search.isEmpty) {
            filteredServices = viewModel.services;
          } else {
            filteredServices = viewModel.services.where((service) {
              return service.name.toLowerCase().contains(search) ||
                  (service.category?.toLowerCase().contains(search) ?? false);
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
                    final service = filteredServices[index];

                    return ServiceCard(
                      id: service.id,
                      name: service.name,
                      description: service.description,
                      imageUrl: service.imageUrl,
                      category: service.category,
                      colorHex: service.color,
                      onTap: () async {
                        final result =
                            await Navigator.push<ConfiguredItem<dynamic>?>(
                              context,
                              MaterialPageRoute(
                                builder: (context) => ChooseActionPage(
                                  service: service,
                                  type: widget.type,
                                  serviceRepository: context
                                      .read<ServiceRepository>(),
                                ),
                              ),
                            );
                        if (result != null && context.mounted) {
                          Navigator.pop(context, result);
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
