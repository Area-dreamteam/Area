import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/viewmodels/select_service_viewmodel.dart';
import 'package:provider/provider.dart';
import 'choose_action_page.dart';

class ChooseServicePage extends StatefulWidget {
  final String type;
  const ChooseServicePage({super.key, required this.type});

  @override
  State<ChooseServicePage> createState() => _ChooseServicePageState();
}

class _ChooseServicePageState extends State<ChooseServicePage> {
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
        backgroundColor: Colors.white,
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
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                onTap: () async {
                  final result = await Navigator.push<ConfiguredItem<dynamic>?>(
                    context,
                    MaterialPageRoute(
                      builder: (context) => ChooseActionPage(
                        service: service,
                        type: widget.type,
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
