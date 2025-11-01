import 'package:flutter/material.dart';
import 'package:mobile/viewmodels/change_password_viewmodel.dart';
import 'package:provider/provider.dart';

class ChangePasswordPage extends StatefulWidget {
  const ChangePasswordPage({super.key});

  @override
  State<ChangePasswordPage> createState() => _ChangePasswordPageState();
}

class _ChangePasswordPageState extends State<ChangePasswordPage> {
  final _formKey = GlobalKey<FormState>();
  final _currentPasswordController = TextEditingController();
  final _newPasswordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  bool _obscureCurrent = true;
  bool _obscureNew = true;
  bool _obscureConfirm = true;

  @override
  void dispose() {
    _currentPasswordController.dispose();
    _newPasswordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _savePassword() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }
    final newPassword = _newPasswordController.text;

    final viewModel = context.read<ChangePasswordViewModel>();
    final success = await viewModel.changePassword(newPassword: newPassword);

    if (success && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Password changed successfully!'),
          backgroundColor: Colors.green,
        ),
      );
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ChangePasswordViewModel>(
      builder: (context, viewModel, child) {
        return Scaffold(
          backgroundColor: const Color(0xFF212121),
          appBar: AppBar(
            title: const Text(
              'Change password',
              style: TextStyle(color: Colors.white),
            ),  
            backgroundColor: const Color(0xFF212121),
            iconTheme: const IconThemeData(color: Colors.white),
          ),
          body: Stack(
            children: [
              SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      _buildPasswordField(
                        label: 'Current password',
                        controller: _currentPasswordController,
                        obscureText: _obscureCurrent,
                        toggleObscure: () =>
                            setState(() => _obscureCurrent = !_obscureCurrent),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter your current password';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 24),
                      _buildPasswordField(
                        label: 'New password',
                        controller: _newPasswordController,
                        obscureText: _obscureNew,
                        toggleObscure: () =>
                            setState(() => _obscureNew = !_obscureNew),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter a new password';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 24),

                      _buildPasswordField(
                        label: 'Confirm new password',
                        controller: _confirmPasswordController,
                        obscureText: _obscureConfirm,
                        toggleObscure: () =>
                            setState(() => _obscureConfirm = !_obscureConfirm),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please confirm your new password';
                          }
                          if (value != _newPasswordController.text) {
                            return 'Passwords do not match';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 40),
                      _buildSaveButton(viewModel),
                    ],
                  ),
                ),
              ),
              if (viewModel.isLoading)
                Container(
                  color: Colors.black,
                  child: const Center(
                    child: CircularProgressIndicator(color: Colors.white),
                  ),
                ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildPasswordField({
    required String label,
    required TextEditingController controller,
    required bool obscureText,
    required VoidCallback toggleObscure,
    required String? Function(String?) validator,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            color: Colors.white70,
            fontSize: 16,
          ),
        ),
        const SizedBox(height: 8),
        TextFormField(
          controller: controller,
          obscureText: obscureText,
          style: const TextStyle(color: Colors.white, fontSize: 18),
          validator: validator,
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.grey.shade800,
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8.0),
              borderSide: BorderSide.none,
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 14,
            ),
            suffixIcon: IconButton(
              icon: Icon(
                obscureText
                    ? Icons.visibility_off
                    : Icons.visibility,
                color: Colors.white,
              ),
              tooltip: 'hide password',
              onPressed: toggleObscure,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSaveButton(ChangePasswordViewModel viewModel) {
    return ElevatedButton(
      onPressed: viewModel.isLoading ? null : _savePassword,
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        disabledBackgroundColor: Colors.grey,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        padding: const EdgeInsets.symmetric(vertical: 16),
      ),
      child: viewModel.isLoading
          ? const SizedBox(
              width: 24,
              height: 24,
              child: CircularProgressIndicator(
                strokeWidth: 3,
                color: Colors.black,
              ),
            )
          : const Text(
              'Save',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
    );
  }
}
