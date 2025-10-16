import 'package:flutter/material.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/widgets/hex_convert.dart';

class ServiceHeader extends StatelessWidget implements PreferredSizeWidget {
  final Service service;
  final String title;

  const ServiceHeader({
    super.key,
    required this.service,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    final serviceColor = hexToColor(service.color);

    return Column(
      children: [
        Container(
          color: serviceColor,
          child: AppBar(
            title: Text(
              title,
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
            backgroundColor: Colors.black,
            elevation: 0,
            iconTheme: const IconThemeData(color: Colors.white),
          ),
        ),
        Container(
          padding: const EdgeInsets.only(left: 16.0, right: 16.0, bottom: 16.0),
          color: serviceColor,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 40),
              Container(
                decoration: const BoxDecoration(
                  color: Colors.white,
                  shape: BoxShape.circle,
                ),
                child: Image.network(
                  service.imageUrl,
                  width: 40,
                  height: 40,
                ),
              ),
              if (service.description != null && service.description!.isNotEmpty) ...[
                const SizedBox(height: 12),
                Text(
                  service.description!,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white, fontSize: 16),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(180.0);

}