import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/widgets/hex_convert.dart';

class MyAreaCard extends StatelessWidget {
  final AppletModel applet;
  final VoidCallback? onTap;
  final ValueChanged<bool>? onToggleEnabled;

  const MyAreaCard({
    super.key,
    required this.applet,
    this.onTap,
    this.onToggleEnabled,
  });

  @override
  Widget build(BuildContext context) {
    final Color cardBackgroundColor = applet.isEnabled
        ? hexToColor(applet.color)
        : Colors.grey.shade800;
    final Color textColor = applet.isEnabled
        ? Colors.white
        : Colors.grey.shade500;

    return Opacity(
      opacity: applet.isEnabled ? 1.0 : 0.65,
      child: Material(
        borderRadius: BorderRadius.circular(14),
        elevation: applet.isEnabled ? 4 : 1,
        color: cardBackgroundColor,
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: onTap,
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
                        style: TextStyle(
                          color: textColor,
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Switch(
                        value: applet.isEnabled,
                        onChanged: onToggleEnabled,
                        activeThumbColor: Colors.white,
                        inactiveTrackColor: Colors.black,
                        inactiveThumbColor: Colors.grey.shade400,
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
