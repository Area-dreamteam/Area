import 'package:flutter/material.dart';
import 'package:mobile/models/user_model.dart';
import 'package:mobile/pages/my_area.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/viewmodels/create_viewmodel.dart';
import 'package:provider/provider.dart';

class ReviewAndFinishPage extends StatefulWidget {
  const ReviewAndFinishPage({super.key});

  @override
  State<ReviewAndFinishPage> createState() => _ReviewAndFinishPageState();
}

class _ReviewAndFinishPageState extends State<ReviewAndFinishPage> {
  final _nameController = TextEditingController();
  final _descriptionController = TextEditingController();
  late Future<UserModel> _userFuture;

  @override
  void initState() {
    super.initState();

    final viewModel = context.read<CreateViewModel>();
    _userFuture = context.read<ServiceRepository>().fetchCurrentUser();

    _nameController.text = viewModel.name;
    _descriptionController.text = viewModel.description;

    _nameController.addListener(() {
      viewModel.setName(_nameController.text);
    });

    _descriptionController.addListener(() {
      viewModel.setDescription(_descriptionController.text);
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
        return Scaffold(
          backgroundColor: const Color(0xFF212121),
          appBar: AppBar(
            title: const Text(
              'Review and finish',
              style: TextStyle(color: Colors.white),
            ),
            backgroundColor: const Color(0xFF212121),
            iconTheme: const IconThemeData(color: Colors.white),
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 20),
                _buildLogos(viewModel),
                const SizedBox(height: 40),
                const Text(
                  'Applet title',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 10),
                _buildTextField(
                  controller: _nameController,
                  hint: "Title Area",
                  maxLines: 3,
                ),
                const SizedBox(height: 24),
                const Text(
                  'Description',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 10),
                _buildTextField(
                  controller: _descriptionController,
                  hint: "Describe your area",
                  maxLines: 5,
                ),
                const SizedBox(height: 20),
                _buildUserInfo(),
                const SizedBox(height: 40),
                _buildCreateButton(context, viewModel),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildLogos(CreateViewModel viewModel) {
    final actionService = viewModel.selectedAction?.service;
    final reactionServices = viewModel.selectedReactions.map((r) => r.service).toList();

    if (actionService == null || reactionServices.isEmpty) {
      return const Center(
        child: Text(
          'Error loading services',
          style: TextStyle(color: Colors.red),
        ),
      );
    }

    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        getServiceIcon(
          actionService.name,
          size: 80,
          imageUrl: actionService.imageUrl,
        ),
        const SizedBox(width: 20),
        const Icon(Icons.arrow_forward, color: Colors.white, size: 30),
        const SizedBox(width: 20),
        
        Expanded(
          child: Wrap(
            alignment: WrapAlignment.center,
            spacing: 15.0,
            runSpacing: 10.0,
            children: reactionServices.map((service) {
              return getServiceIcon(
                service.name,
                size: 60,
                imageUrl: service.imageUrl,
              );
            }).toList(),
          ),
        ),
      ],
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String hint,
    int maxLines = 1,
  }) {
    return TextField(
      controller: controller,
      style: const TextStyle(color: Colors.black, fontSize: 18),
      maxLines: maxLines,
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: const TextStyle(color: Colors.black45),
        filled: true,
        fillColor: Colors.white,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10.0),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }

  Widget _buildUserInfo() {
    return FutureBuilder<UserModel>(
      future: _userFuture,
      builder: (context, snapshot) {
        String username = '...';
        if (snapshot.connectionState == ConnectionState.done) {
          if (snapshot.hasData) {
            username = snapshot.data!.name;
          } else {
            username = 'Unknown User';
          }
        }
        return Text(
          'by $username',
          textAlign: TextAlign.left,
          style: const TextStyle(color: Colors.white70, fontSize: 16),
        );
      },
    );
  }

  Widget _buildCreateButton(BuildContext context, CreateViewModel viewModel) {
    final bool isReady = viewModel.isReadyToCreateOrUpdate;

    final String buttonText = viewModel.isEditing
        ? 'Update Applet'
        : 'Create Applet';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: isReady ? Colors.blue : Colors.grey,
            foregroundColor: Colors.white,
            minimumSize: const Size(double.infinity, 50),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(30.0),
            ),
            elevation: isReady ? 2 : 0,
          ),
          onPressed: isReady && !viewModel.isLoading
              ? () async {
                  final success = await viewModel.saveApplet();

                  if (success && context.mounted) {
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const MyAreaPage(),
                      ),
                      (Route<dynamic> route) => false,
                    );
                  }
                }
              : null,
          child: viewModel.isLoading
              ? const SizedBox(
                  height: 24,
                  width: 24,
                  child: CircularProgressIndicator(color: Colors.white),
                )
              : Text(buttonText, style: const TextStyle(fontSize: 18)),
        ),
      ],
    );
  }
}