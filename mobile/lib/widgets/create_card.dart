import 'package:flutter/material.dart';
import 'package:mobile/utils/icon_helper.dart';

class CardDetails {
  final String serviceName;
  final String actionName;
  final String? imageUrl;

  CardDetails({
    required this.serviceName,
    required this.actionName,
    this.imageUrl,
  });
}

class CreateCard extends StatelessWidget {
  final String title;
  final CardDetails? details;
  final VoidCallback onTap;
  final VoidCallback? onRemove;

  const CreateCard({
    super.key,
    required this.title,
    required this.onTap,
    this.details,
    this.onRemove,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.black,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.white38),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                if (details != null && onRemove != null)
                  GestureDetector(
                    onTap: onRemove,
                    child: const Icon(
                      Icons.close,
                      color: Colors.redAccent,
                      size: 24,
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 20),
            details == null
                ? _buildPlaceholder()
                : _buildSelectionDetails(details!),
          ],
        ),
      ),
    );
  }

  Widget _buildPlaceholder() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: const [
        Icon(Icons.add_circle_outline, color: Colors.blue, size: 28),
        SizedBox(width: 10),
        Text(
          'Add',
          style: TextStyle(
            color: Colors.blue,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _buildSelectionDetails(CardDetails details) {
    return Row(
      children: [
        getServiceIcon(
          details.serviceName,
          size: 40.0,
          imageUrl: details.imageUrl,
        ),

        const SizedBox(width: 15),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                details.serviceName,
                style: const TextStyle(color: Colors.white38, fontSize: 20),
              ),
              Text(
                details.actionName,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ],
    );
  }
}