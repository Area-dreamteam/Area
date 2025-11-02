import 'package:flutter/material.dart';
import 'package:mobile/models/action_model.dart';
import 'package:mobile/models/reaction_model.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/pages/configuration_page.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/widgets/hex_convert.dart';
import 'package:mobile/widgets/service_header.dart';
import 'package:mobile/widgets/item_card.dart';

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
    _fetchItems();
  }

  void _fetchItems() {
    final isAction = widget.type == 'trigger';
    final serviceId = widget.service.id.toString();

    if (isAction) {
      _itemsFuture = widget.serviceRepository.fetchActionsService(serviceId);
    } else {
      _itemsFuture = widget.serviceRepository.fetchReactionsService(serviceId);
    }
  }

  Future<void> _handleItemTap(dynamic simpleItem) async {
    List<dynamic> finalConfig = [];
    dynamic detailedItem;

    try {
      if (widget.type == 'trigger') {
        detailedItem = await widget.serviceRepository.fetchActionDetails(
          simpleItem.id,
        );
      } else {
        detailedItem = await widget.serviceRepository.fetchReactionDetails(
          simpleItem.id,
        );
      }

      if (!mounted) return;
      final String itemDescription =
          detailedItem.description ?? 'No description';

      if (detailedItem.configSchema.isNotEmpty) {
        final result = await Navigator.push<List<dynamic>>(
          context,
          MaterialPageRoute(
            builder: (context) => ConfigurationPage(
              configSchema: detailedItem.configSchema,
              serviceName: widget.service.name,
              itemName: detailedItem.name,
              itemDescription: itemDescription,
              itemType: widget.type,
            ),
          ),
        );

        if (!mounted) return;
        if (result != null) {
          finalConfig = result;
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
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error fetching details: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isAction = widget.type == 'trigger';
    final service = widget.service;
    final serviceColor = hexToColor(service.color);
    final title = isAction ? 'Choose a trigger' : 'Choose an action';
    final bool isDark = serviceColor.computeLuminance() < 0.5;
    final Color textColor = isDark ? Colors.white : Colors.black;

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        title: Text(title, style: TextStyle(color: textColor)),
        backgroundColor: serviceColor,
        iconTheme: IconThemeData(color: textColor),
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: textColor),
          tooltip: 'Retour',
          onPressed: () => Navigator.of(context).pop(),
        ),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(180),
          child: ServiceHeader(service: service, title: ''),
        ),
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _itemsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(color: Colors.blue),
            );
          }
          final items = snapshot.data ?? [];
          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, index) {
                final item = items[index];
                return Semantics(
                  label: "${item.name}, ${item.description}",
                  hint: "Appuyez pour choisir cet élément",
                  button: true,
                  child: ItemCard(
                    name: item.name,
                    description: item.description,
                    color: serviceColor,
                    onTap: () => _handleItemTap(item),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
