import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/select_service_viewmodel.dart';
import 'package:provider/provider.dart';
import 'select_action_reaction_page.dart';

class SelectServicePage extends StatefulWidget {
  final String type;
  const SelectServicePage({super.key, required this.type});

  @override
  State<SelectServicePage> createState() => _SelectServicePageState();
}

class _SelectServicePageState extends State<SelectServicePage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SelectServiceViewmodel>().fetchServices();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Choose a service"),
        backgroundColor: Color(0xFF212121),
        elevation: 0,
      ),
      backgroundColor: const Color(0xFF212121),
      body: Consumer<SelectServiceViewmodel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (viewModel.state == SelectServiceState.error) {
            return Center(
              child: Text(
                viewModel.errorMessage,
                style: const TextStyle(color: Colors.red),
              ),
            );
          }

          return ListView.builder(
            itemCount: viewModel.services.length,
            itemBuilder: (context, index) {
              final service = viewModel.services[index];
              return ListTile(
                title: Text(
                  service.name,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                onTap: () async {
                  final result = await Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => SelectActionReactionPage(
                        serviceId: service.id.toString(),
                        serviceName: service.name,
                        type: widget.type == 'trigger' ? 'action' : 'reaction',
                        serviceRepository: context.read<ServiceRepository>(),
                      ),
                    ),
                  );
                  if (result != null && context.mounted) {
                    Navigator.pop(context, result);
                  }
                },
              );
            },
          );
        },
      ),
    );
  }
}
