import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/widgets/hex_convert.dart';

class MyAreaCard extends StatelessWidget {
  final AppletModel applet;
  final VoidCallback? onEdit;
  final VoidCallback? onDelete;
  final ValueChanged<bool>? onToggleEnabled;
  final ValueChanged<bool>? onTogglePublic;

  const MyAreaCard({
    super.key,
    required this.applet,
    this.onEdit,
    this.onDelete,
    this.onToggleEnabled,
    this.onTogglePublic,
  });

  @override
  Widget build(BuildContext context) {
    final Color cardBackgroundColor = applet.isEnabled
        ? hexToColor(applet.triggerService!.color)
        : Colors.black;
    final Color textColor = applet.isEnabled ? Colors.black : Colors.white;

    return Opacity(
      opacity: applet.isEnabled ? 1.0 : 0.65,
      child: Material(
        borderRadius: BorderRadius.circular(14),
        color: cardBackgroundColor,
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: onEdit,
          child: Container(
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(14)),
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 12),
                Text(
                  applet.name,
                  style: TextStyle(
                    color: textColor,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    height: 1.2,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 6),

                Text(
                  'By ${applet.user.name}',
                  style: TextStyle(color: textColor, fontSize: 12),
                ),
                const SizedBox(height: 12),

                if (onToggleEnabled != null)
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      Text(
                        applet.isEnabled ? 'Enabled' : 'Disabled',
                        style: TextStyle(color: textColor, fontSize: 15),
                      ),
                      const SizedBox(width: 20),
                      Transform.scale(
                        scale: 1.5,
                        child: Switch(
                          value: applet.isEnabled,
                          onChanged: onToggleEnabled,
                          activeThumbColor: Colors.white,
                          inactiveTrackColor: Colors.black,
                          inactiveThumbColor: Colors.grey,
                        ),
                      ),
                    ],
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
