import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/widgets/hex_convert.dart';

class ServiceHeader extends StatelessWidget implements PreferredSizeWidget {
  final Service service;

  const ServiceHeader({
    super.key,
    required this.service,
    required String title,
  });

  @override
  Widget build(BuildContext context) {
    final Color serviceColor = hexToColor(service.color);
    final Color textColor = serviceColor.computeLuminance() > 0.5 ? Colors.black : Colors.white;

    return Container(
      color: serviceColor,
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: const BoxDecoration(
              color: Colors.white,
              shape: BoxShape.circle,
            ),
            child: getServiceIcon(service.name, size: 40.0, imageUrl: service.imageUrl),
          ),
          const SizedBox(height: 12),

          Text(
            service.name,
            style: TextStyle(
              color: textColor,
              fontSize: 22,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),

          if (service.description != null && service.description!.isNotEmpty) ...[
            const SizedBox(height: 6),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxHeight: 40),
                child: MarkdownBody(
                  data: service.description!,
                  styleSheet: MarkdownStyleSheet(
                    textAlign: WrapAlignment.center,
                    p: TextStyle(
                      color: textColor,
                      fontSize: 14,
                    ),
                    a: TextStyle(
                      color: textColor,
                      decoration: TextDecoration.underline,
                    ),
                    strong: TextStyle(
                      color: textColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(180.0);
}