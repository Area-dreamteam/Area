import 'package:flutter/material.dart';
import 'package:mobile/repositories/service_repository.dart';

class SelectActionReactionPage extends StatefulWidget {
  final String serviceId;
  final String serviceName;
  final String type;  
  final ServiceRepository serviceRepository;

  const SelectActionReactionPage({
    super.key,
    required this.serviceId,
    required this.serviceName,
    required this.type,
    required this.serviceRepository,
  });

  @override
  State<SelectActionReactionPage> createState() =>
      _SelectActionReactionPageState();
}

class _SelectActionReactionPageState extends State<SelectActionReactionPage> {
  late Future<List<dynamic>> _itemsFuture;

  @override
  void initState() {
    super.initState();
    if (widget.type == 'action') {
      _itemsFuture = widget.serviceRepository.fetchActionsService(widget.serviceId);
    } else {
      _itemsFuture = widget.serviceRepository.fetchReactionsService(widget.serviceId);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        title: Text('Select a ${widget.type}'),
        backgroundColor: Colors.black,
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _itemsFuture,
        builder: (context, state) {
          if (state.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state.hasError) {
            return Center(child: Text('Error: ${state.error}', style: const TextStyle(color: Colors.red)));
          }
          if (!state.hasData || state.data!.isEmpty) {
            return const Center(child: Text('No items found.', style: TextStyle(color: Colors.white)));
          }

          final items = state.data!;
          return ListView.builder(
            itemCount: items.length,
            itemBuilder: (context, index) {
              final item = items[index];
              return ListTile(
                title: Text(item.name, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                subtitle: Text(item.description, style: const TextStyle(color: Colors.white)),
              );
            },
          );
        },
      ),
    );
  }
}