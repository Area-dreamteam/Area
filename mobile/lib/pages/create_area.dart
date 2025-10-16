import 'package:flutter/material.dart';
import 'package:mobile/pages/my_area.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:provider/provider.dart';

class CreateAreaPage extends StatefulWidget {
  const CreateAreaPage({super.key});

  @override
  State<CreateAreaPage> createState() => _CreateAreaPageState();
}

class _CreateAreaPageState extends State<CreateAreaPage> {
  final _nameController = TextEditingController();
  final _descriptionController = TextEditingController();

  @override
  void initState() {
    super.initState();
    final viewModel = context.read<CreateViewModel>();
    _nameController.addListener(() => viewModel.setName(_nameController.text));

    _nameController.addListener(() {
      viewModel.setName(_nameController.text);
      viewModel.setDescription("AREA: ${_nameController.text}");
    });
  }

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<CreateViewModel>(
      builder: (context, viewModel, child) {
        VoidCallback? onPressedCallback;
        Widget buttonChild;

        if (viewModel.isLoading) {
          buttonChild = const SizedBox(
            height: 24,
            width: 24,
            child: CircularProgressIndicator(
              color: Colors.white,
              strokeWidth: 3,
            ),
          );
        } else {
          buttonChild = const Text(
            'Create Applet',
            style: TextStyle(fontSize: 18),
          );
        }

        if (viewModel.isReadyToCreate && !viewModel.isLoading) {
          onPressedCallback = () async {
            final success = await viewModel.createApplet();
            if (success && context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text("Applet create"),
                  backgroundColor: Colors.green,
                ),
              );
              viewModel.clearSelection();
              Navigator.of(context).pushAndRemoveUntil(
                MaterialPageRoute(builder: (context) => const MyAreaPage()),
                (Route<dynamic> route) => false,
              );
            }
          };
        } else {
          onPressedCallback = null;
        }

        final actionService = viewModel.selectedAction?.service;
        final reactionService = viewModel.selectedReaction?.service;

        return Scaffold(
          backgroundColor: const Color(0xFF212121),
          appBar: AppBar(
            title: const Text("Create AREA"),
            backgroundColor: Colors.white,
          ),
          body: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 40),
                if (actionService != null && reactionService != null)
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      CircleAvatar(
                        radius: 30,
                        backgroundColor: Colors.white24,
                        child: Image.network(
                          actionService.imageUrl,
                          width: 40,
                          height: 40,
                        ),
                      ),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 16.0),
                      ),
                      CircleAvatar(
                        radius: 30,
                        backgroundColor: Colors.white24,
                        child: Image.network(
                          reactionService.imageUrl,
                          width: 40,
                          height: 40,
                        ),
                      ),
                    ],
                  ),
                const SizedBox(height: 50),
                const Text(
                  'Applet Title',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _nameController,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white, fontSize: 18),
                  decoration: InputDecoration(
                    hintText: 'Add a title',
                    hintStyle: const TextStyle(color: Colors.white),
                    border: OutlineInputBorder(),
                  ),
                ),
                const Spacer(),
                if (viewModel.state == CreateState.error)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 15),
                    child: Text(
                      viewModel.errorMessage,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Colors.redAccent,
                        fontSize: 15,
                      ),
                    ),
                  ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    disabledBackgroundColor: Colors.grey.shade800,
                  ),
                  onPressed: onPressedCallback,
                  child: buttonChild,
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
