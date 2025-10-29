import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/utils/icon_helper.dart';
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
    // --- CORRECTION DE L'ERREUR ---
    final Color cardBackgroundColor = applet.isEnabled
        ? hexToColor(applet.color) // <-- Utilise applet.color
        : Colors.grey.shade800; // Couleur grise si désactivé
    final Color textColor =
        applet.isEnabled ? Colors.white : Colors.grey.shade500;
    // --- FIN DE LA CORRECTION ---

    return Opacity(
      opacity: applet.isEnabled ? 1.0 : 0.65,
      child: Material(
        borderRadius: BorderRadius.circular(14),
        elevation: applet.isEnabled ? 4 : 1,
        color: cardBackgroundColor,
        child: InkWell(
          borderRadius: BorderRadius.circular(14),
          onTap: onEdit,
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(14),
            ),
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // --- Top row: Icon, Public/Private, Edit, Delete ---
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    // Gère les icônes nulles
                    if (applet.triggerService != null &&
                        applet.reactionServices.isNotEmpty)
                      SizedBox(
                        width: 34,
                        height: 20,
                        child: Stack(
                          children: [
                            Positioned(
                              right: 0,
                              child: CircleAvatar(
                                backgroundColor: Colors.white.withOpacity(0.8),
                                radius: 10,
                                child: ClipOval(
                                  child: getServiceIcon(
                                    applet.reactionServices.first.name,
                                    size: 12.0,
                                  ),
                                ),
                              ),
                            ),
                            Positioned(
                              left: 0,
                              child: CircleAvatar(
                                backgroundColor: Colors.white.withOpacity(0.95),
                                radius: 10,
                                child: ClipOval(
                                  child: getServiceIcon(
                                    applet.triggerService!.name,
                                    size: 12.0,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      )
                    else if (applet.triggerService != null)
                      CircleAvatar(
                        backgroundColor: Colors.white.withOpacity(0.9),
                        radius: 10,
                        child: ClipOval(
                          child: getServiceIcon(
                            applet.triggerService!.name,
                            size: 12.0,
                          ),
                        ),
                      )
                    else
                      // Fallback
                      CircleAvatar(
                        backgroundColor: Colors.white.withOpacity(0.5),
                        radius: 10,
                        child: Icon(Icons.electrical_services,
                            color: cardBackgroundColor.withOpacity(0.7),
                            size: 12),
                      ),
                    
                    const Spacer(), 

                    // Bouton Public/Private
                    if (onTogglePublic != null)
                      TextButton(
                        style: TextButton.styleFrom(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 6, vertical: 2),
                            minimumSize: Size.zero,
                            visualDensity: VisualDensity.compact),
                        onPressed: () => onTogglePublic!(!applet.isPublic),
                        child: Text(
                          applet.isPublic ? 'Public' : 'Private',
                          style: TextStyle(
                              color: textColor.withOpacity(0.9),
                              fontWeight: FontWeight.w500,
                              fontSize: 12),
                        ),
                      ),

                    // Bouton Edit
                    if (onEdit != null)
                      IconButton(
                        icon: Icon(Icons.edit_outlined,
                            color: textColor, size: 20),
                        onPressed: onEdit,
                        tooltip: 'Edit',
                        visualDensity: VisualDensity.compact,
                        padding: const EdgeInsets.all(4),
                      ),

                    // Bouton Delete
                    if (onDelete != null)
                      IconButton(
                        icon: Icon(Icons.delete_outline,
                            color: textColor, size: 20),
                        onPressed: onDelete,
                        tooltip: 'Delete',
                        visualDensity: VisualDensity.compact,
                        padding: const EdgeInsets.all(4),
                      ),
                  ],
                ),
                const SizedBox(height: 12),

                // --- Nom de l'Applet ---
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

                // --- Nom de l'utilisateur ---
                Text(
                  'By ${applet.user.name}',
                  style: TextStyle(
                      color: textColor.withOpacity(0.7), fontSize: 12),
                ),
                const SizedBox(height: 12),

                // --- Switch Enable/Disable ---
                if (onToggleEnabled != null)
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      Text(
                        applet.isEnabled ? 'Enabled' : 'Disabled',
                        style: TextStyle(
                            color: textColor.withOpacity(0.9),
                            fontSize: 15, // Votre taille personnalisée
                            fontWeight: FontWeight.w500),
                      ),
                      const SizedBox(width: 20), // Votre espacement
                      Transform.scale(
                        scale: 1.5, // Votre taille de switch
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