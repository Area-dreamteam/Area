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
    final theme = Theme.of(context);
    final Color cardBackgroundColor = applet.isEnabled
        ? hexToColor(applet.color)
        : Colors.grey.shade800;

    final bool isDark = cardBackgroundColor.computeLuminance() < 0.5;
    final Color baseTextColor = isDark ? Colors.white : Colors.black;

    final Color textColor = applet.isEnabled
        ? baseTextColor
        : Colors.grey.shade500;

    final String switchLabel = "Applet ${applet.name}";

    return Opacity(
      opacity: applet.isEnabled ? 1.0 : 0.65,
      child: Semantics(
        label:
            "${applet.name}, par ${applet.user.name}. Click to see details.",
        button: true,
        enabled: onTap != null,
        child: Material(
          borderRadius: BorderRadius.circular(14),
          color: cardBackgroundColor,
          child: InkWell(
            borderRadius: BorderRadius.circular(14),
            onTap: onTap,
            child: Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(14),
              ),
              width: double.infinity,
              padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 12),
                  Text(
                    applet.name,
                    style: theme.textTheme.titleLarge?.copyWith(
                      color: textColor,
                      fontWeight: FontWeight.bold,
                      height: 1.2,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'By ${applet.user.name}',
                    style: theme.textTheme.bodyMedium?.copyWith(
                      color: textColor,
                    ),
                  ),
                  const SizedBox(height: 12),

                  if (onToggleEnabled != null)
                    Semantics(
                      label: switchLabel,
                      toggled: applet.isEnabled,
                      onTapHint:
                          "Click for ${applet.isEnabled ? 'disable' : 'enable'} l'applet",
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          ExcludeSemantics(
                            child: Text(
                              applet.isEnabled ? 'Enabled' : 'Disabled',
                              style: theme.textTheme.bodyMedium?.copyWith(
                                color: textColor,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Switch(
                            value: applet.isEnabled,
                            onChanged: onToggleEnabled,
                            activeThumbColor: Colors.white,
                            inactiveTrackColor: Colors.black,
                            inactiveThumbColor: Colors.grey.shade500,
                          ),
                        ],
                      ),
                    ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
