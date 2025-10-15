import 'package:flutter/material.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/pages/configuration_page.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';

class ChooseActionPage extends StatefulWidget {
  final Service service;
  final String type;
  final ServiceRepository serviceRepository;

  const ChooseActionPage({
    super.key,
    required this.service,
    required this.type,
    required this.serviceRepository,
  });

  @override
  State<ChooseActionPage> createState() => _ChooseActionPageState();
}

class _ChooseActionPageState extends State<ChooseActionPage> {
  late Future<List<dynamic>> _itemsFuture;

  @override
  void initState() {
    super.initState();
    final isAction = widget.type == 'trigger';

    if (isAction) {
      _itemsFuture = widget.serviceRepository.fetchActionsService(
        widget.service.id.toString(),
      );
    } else {
      _itemsFuture = widget.serviceRepository.fetchReactionsService(
        widget.service.id.toString(),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isAction = widget.type == 'trigger';
    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        title: Text(isAction ? 'Choose a trigger' : 'Choose an action'),
        backgroundColor: const Color(0xFF333333),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Row(
              children: [
                const SizedBox(width: 16),
                Text(
                  widget.service.name,
                  style: const TextStyle(color: Colors.white, fontSize: 22),
                ),
              ],
            ),
          ),
          Expanded(
            child: FutureBuilder<List<dynamic>>(
              future: _itemsFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snapshot.hasError) {
                  return Center(
                    child: Text(
                      'Error: ${snapshot.error}',
                      style: const TextStyle(color: Colors.red),
                    ),
                  );
                }
                if (!snapshot.hasData || snapshot.data!.isEmpty) {
                  return const Center(
                    child: Text(
                      'No items found.',
                      style: TextStyle(color: Colors.white),
                    ),
                  );
                }
                final items = snapshot.data!;
                return ListView.builder(
                  itemCount: items.length,
                  itemBuilder: (context, index) {
                    final item = items[index];
                    return ListTile(
                      title: Text(
                        item.name,
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      subtitle: Text(
                        item.description,
                        style: const TextStyle(color: Colors.white70),
                      ),
                      onTap: () async {
                        final simpleItem = items[index]; 
                        List<dynamic> finalConfig = [];
                        dynamic detailedItem;

                        try {
                          showDialog(
                            context: context,
                            barrierDismissible: false,
                            builder: (BuildContext context) => const Center(child: CircularProgressIndicator()),
                          );

                          if (widget.type == 'trigger') {
                            detailedItem = await widget.serviceRepository.fetchActionDetails(simpleItem.id);
                          } else {
                            detailedItem = await widget.serviceRepository.fetchReactionDetails(simpleItem.id);
                          }
                          
                          Navigator.pop(context); 

                          if (detailedItem.configSchema.isNotEmpty) {
                            final result = await Navigator.push<List<dynamic>>(
                              context,
                              MaterialPageRoute(
                                builder: (context) => ConfigurationPage(
                                  configSchema: detailedItem.configSchema, 
                                  serviceName: widget.service.name,
                                  itemName: detailedItem.name,
                                ),
                              ),
                            );
                            
                            if (result != null) {
                              finalConfig = result;
                            } else {
                              return;
                            }
                          }
                          if (widget.type == 'trigger') {
                            final selectedItem = ConfiguredItem<ActionModel>(
                              service: widget.service,
                              item: detailedItem as ActionModel,
                              config: finalConfig,
                            );
                            Navigator.pop(context, selectedItem);
                          } else {
                            final selectedItem = ConfiguredItem<Reaction>(
                              service: widget.service,
                              item: detailedItem as Reaction,
                              config: finalConfig,
                            );
                            Navigator.pop(context, selectedItem);
                          }

                        } catch (e) {
                          if(Navigator.canPop(context)) {
                            Navigator.pop(context);
                          }
                          // Afficher une erreur à l'utilisateur
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Error fetching details: $e'),
                              backgroundColor: Colors.red,
                            ),
                          );
                        }
                      },
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}