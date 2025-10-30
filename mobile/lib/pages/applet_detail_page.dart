// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:mobile/widgets/hex_convert.dart';
import 'package:provider/provider.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:mobile/pages/create_page.dart';
import 'package:mobile/repositories/service_repository.dart';

class AppletDetailPage extends StatefulWidget {
  final AppletModel applet;

  const AppletDetailPage({super.key, required this.applet});

  @override
  State<AppletDetailPage> createState() => _AppletDetailPageState();
}

class _AppletDetailPageState extends State<AppletDetailPage> {
  late AppletModel currentApplet;

  @override
  void initState() {
    super.initState();
    currentApplet = widget.applet;
  }

  Future<void> _togglePublic() async {
    final viewModel = context.read<MyAppletViewModel>();
    final String newStatusText = currentApplet.isPublic ? "private" : "public";
    final success = await viewModel.toggleAreaPublic(
      currentApplet.id,
      currentApplet.isPublic,
    );

    if (success && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Action successful. Applet is now $newStatusText.'),
          backgroundColor: Colors.green,
        ),
      );
      Navigator.pop(context, true);
    } else if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(viewModel.errorMessage),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> _deleteApplet() async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF303030),
        title: const Text(
          'Confirm Delete',
          style: TextStyle(color: Colors.white),
        ),
        content: Text(
          'Delete ${currentApplet.name}. This action is permanent.',
          style: const TextStyle(color: Colors.white70),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text(
              'Cancel',
              style: TextStyle(color: Colors.blueAccent),
            ),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.redAccent),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirm == true && mounted) {
      final viewModel = context.read<MyAppletViewModel>();
      final success = await viewModel.deleteApplet(currentApplet.id);
      if (success && mounted) {
        Navigator.pop(context, true);
      } else if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(viewModel.errorMessage),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _navigateToEdit() async {
    final createViewModel = context.read<CreateViewModel>();
    final serviceRepo = context.read<ServiceRepository>();

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) =>
          const Center(child: CircularProgressIndicator(color: Colors.white)),
    );
    try {
      final completeApplet = await serviceRepo.fetchAreaDetails(
        currentApplet.id,
        isPublic: currentApplet.isPublic,
      );

      if (!mounted) return;

      final prepared = await createViewModel.startEditing(completeApplet);

      if (!mounted) return;
      Navigator.pop(context);

      if (prepared) {
        final editResult = await Navigator.push<bool>(
          context,
          MaterialPageRoute(builder: (_) => const CreatePage()),
        );
        if (editResult == true && mounted) {
          Navigator.pop(context, true);
        } else if (mounted) {
          createViewModel.clearSelection();
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(createViewModel.errorMessage),
            backgroundColor: Colors.red,
          ),
        );
        createViewModel.clearSelection();
      }
    } catch (e) {
      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Erreur chargement détails: $e'),
            backgroundColor: Colors.red,
          ),
        );
        createViewModel.clearSelection();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final Color pageColor = hexToColor(currentApplet.color);
    final myAppletViewModel = context.watch<MyAppletViewModel>();

    // ignore: deprecated_member_use
    return WillPopScope(
      onWillPop: () async {
        Navigator.pop(context, false);
        return false;
      },
      child: Scaffold(
        backgroundColor: pageColor,
        appBar: AppBar(
          leading: IconButton(
            icon: const Icon(Icons.arrow_back, color: Colors.white),
            onPressed: () {
              Navigator.pop(context, false);
            },
          ),
          title: Text(
            currentApplet.name,
            style: const TextStyle(color: Colors.white),
          ),
          backgroundColor: Colors.transparent,
          elevation: 0,
        ),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                if (currentApplet.triggerService != null)
                  getServiceIcon(
                    currentApplet.triggerService!.name,
                    size: 100.0,
                  )
                else
                  const Icon(
                    Icons.electrical_services,
                    size: 100,
                    color: Colors.white70,
                  ),
                const SizedBox(height: 24),
                Text(
                  currentApplet.name,
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                if (currentApplet.description != null &&
                    currentApplet.description!.isNotEmpty)
                  Text(
                    currentApplet.description!,
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.white70, fontSize: 16),
                  ),
                const SizedBox(height: 48),
                if (myAppletViewModel.state == MyAppletState.error &&
                    myAppletViewModel.errorMessage.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 15.0),
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 5,
                      ),
                      color: Colors.redAccent,
                      child: Text(
                        myAppletViewModel.errorMessage,
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: Colors.white),
                      ),
                    ),
                  ),

                if (currentApplet.isPublic) ...[
                  _buildActionButton(
                    text: 'Unpublish',
                    icon: Icons.public_off_outlined,
                    onPressed: _togglePublic,
                    backgroundColor: Colors.redAccent,
                    foregroundColor: Colors.white,
                  ),
                ]
                else ...[
                  _buildActionButton(
                    text: 'Edit',
                    icon: Icons.edit_outlined,
                    onPressed: _navigateToEdit,
                  ),
                  const SizedBox(height: 16),
                  _buildActionButton(
                    text: 'Publish',
                    icon: Icons.public_outlined,
                    onPressed: _togglePublic,
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.black,
                  ),
                  const SizedBox(height: 16),
                  _buildActionButton(
                    text: 'Delete',
                    icon: Icons.delete_outline,
                    onPressed: _deleteApplet,
                    backgroundColor: Colors.redAccent,
                    foregroundColor: Colors.white,
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildActionButton({
    required String text,
    required IconData icon,
    required VoidCallback onPressed,
    Color backgroundColor = Colors.white,
    Color foregroundColor = Colors.black,
  }) {
    return ElevatedButton.icon(
      icon: Icon(icon, size: 20),
      label: Text(
        text,
        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor,
        foregroundColor: foregroundColor,
        padding: const EdgeInsets.symmetric(vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        elevation: 2,
      ),
    );
  }
}
