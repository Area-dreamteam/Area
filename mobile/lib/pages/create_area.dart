import 'package:flutter/material.dart';
import 'package:mobile/models/user_model.dart';
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
  late Future<UserModel> _currentUser; // Déclaration du Future

  @override
  void initState() {
    super.initState();
    final viewModel = context.read<CreateViewModel>();

    _nameController.addListener(() {
      viewModel.setName(_nameController.text);
      viewModel.setDescription("AREA: ${_nameController.text}");
    });

    try {
      final serviceRepository = viewModel.serviceRepository;
      _currentUser = serviceRepository.fetchCurrentUser();
    } catch (e) {
      _currentUser = Future.error('error user');
    }
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
            'Create AREA',
            style: TextStyle(fontSize: 18),
          );
        }

        if (viewModel.isReadyToCreate && !viewModel.isLoading) {
          onPressedCallback = () async {
            final success = await viewModel.createApplet();
            if (success && context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text("Applet created"),
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
            title: const Text(
              "Review and finish",
              style: TextStyle(color: Colors.white),
            ),
            backgroundColor: const Color(0xFF212121),
            iconTheme: const IconThemeData(color: Colors.white),
          ),
          body: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 40),
                if (actionService != null && reactionService != null)
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _buildServiceImage(actionService.imageUrl),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 16.0),
                      ),
                      _buildServiceImage(reactionService.imageUrl),
                    ],
                  ),
                const SizedBox(height: 50),
                const Text(
                  'Applet Title',
                  textAlign: TextAlign.left,
                  style: TextStyle(color: Colors.white70, fontSize: 16),
                ),
                const SizedBox(height: 8),

                TextField(
                  controller: _nameController,
                  style: const TextStyle(color: Colors.black, fontSize: 18),
                  decoration: InputDecoration(
                    hintText: 'Add a title',
                    hintStyle: const TextStyle(color: Colors.grey),
                    filled: true,
                    fillColor: Colors.white,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8),
                      borderSide: BorderSide.none,
                    ),
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 90,
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                FutureBuilder<UserModel>(
                  future: _currentUser,
                  builder: (context, snapshot) {
                    String userName = 'Loading...';

                    if (snapshot.connectionState == ConnectionState.done) {
                      if (snapshot.hasData) {
                        userName = snapshot.data!.name;
                      } else if (snapshot.hasError) {
                        userName = 'Error: user not found';
                      }
                    }

                    return Text(
                      'By $userName',
                      textAlign: TextAlign.left,
                      style: const TextStyle(
                        color: Colors.white70,
                        fontSize: 16,
                      ),
                    );
                  },
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
                    minimumSize: const Size(
                      double.infinity,
                      50,
                    ),
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
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

  Widget _buildServiceImage(String imageUrl) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(15.0),
      child: Image.network(
        imageUrl,
        width: 60,
        height: 60,
        fit: BoxFit.cover,
      ),
    );
  }
}
