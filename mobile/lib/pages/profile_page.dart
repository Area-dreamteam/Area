// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:mobile/viewmodels/profile_viewmodel.dart';
import 'package:provider/provider.dart';
import 'package:mobile/pages/change_password_page.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/repositories/auth_repository.dart';
import 'package:provider/provider.dart';
import 'package:mobile/scaffolds/main_scaffold.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final viewModel = context.read<ProfileViewModel>();
      viewModel.loadCurrentUser().then((_) {
        if (mounted && viewModel.currentUser != null) {
          _usernameController.text = viewModel.currentUser!.name;
          _emailController.text = viewModel.currentUser!.email;
          _emailController.addListener(() {});
        }
      });
    });
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _emailController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer<ProfileViewModel>(
      builder: (context, viewModel, child) {
        return Scaffold(
          backgroundColor: const Color(0xFF212121),
          appBar: AppBar(
            title: const Text('Account', style: TextStyle(color: Colors.white)),
            backgroundColor: const Color(0xFF212121),
            automaticallyImplyLeading: false,
            elevation: 3,
          ),
          body: _buildBody(context, viewModel),
          bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 3),
        );
      },
    );
  }

  Widget _buildBody(BuildContext context, ProfileViewModel viewModel) {
    if (viewModel.state == ProfileState.initial ||
        (viewModel.isLoading && viewModel.currentUser == null)) {
      return const Center(
        child: CircularProgressIndicator(color: Colors.white),
      );
    }

    return Stack(
      children: [
        ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            _buildTextFieldSection(
              label: 'Username',
              controller: _usernameController,
            ),
            const SizedBox(height: 24),
            _buildPasswordSection(),
            const SizedBox(height: 24),
            _buildTextFieldSection(
              label: 'Email',
              controller: _emailController,
            ),
            const SizedBox(height: 40),
            _buildLinkedAccountsSection(),
            const SizedBox(height: 40),
            _buildSaveButton(viewModel),
            const SizedBox(height: 40),
            _buildLogoutButton(context),
          ],
        ),
        if (viewModel.state == ProfileState.saving)
          Container(
            color: Colors.black,
            child: const Center(
              child: CircularProgressIndicator(color: Colors.white),
            ),
          ),
      ],
    );
  }

  Widget _buildTextFieldSection({
    required String label,
    required TextEditingController controller,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(color: Colors.white, fontSize: 16)),
        const SizedBox(height: 8),
        TextField(
          controller: controller,
          style: TextStyle(color: Colors.white, fontSize: 18),
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
          ),
        ),
        const SizedBox(height: 8),
      ],
    );
  }

  Widget _buildPasswordSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Password',
          style: TextStyle(color: Colors.white, fontSize: 16),
        ),
        const SizedBox(height: 8),
        TextField(
          readOnly: true,
          style: const TextStyle(color: Colors.white, fontSize: 18),
          decoration: InputDecoration(
            hintText: '********',
            hintStyle: const TextStyle(color: Colors.white),
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
          ),
        ),
        const SizedBox(height: 8),
        InkWell(
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => ChangePasswordPage()),
            );
          },
          child: const Text(
            'Change password',
            style: TextStyle(color: Colors.blue, fontSize: 15),
          ),
        ),
      ],
    );
  }

  Widget _buildLinkedAccountsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Linked accounts',
          style: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        const Text(
          'You can use these to quickly sign into your Area account.',
          style: TextStyle(color: Colors.white70, fontSize: 14),
        ),
        const SizedBox(height: 16),
        _buildLinkTile(
          'Github',
          const Image(image: AssetImage('assets/icons/github.png')),
          false,
        ),
        _buildLinkTile(
          'Google',
          const Image(image: AssetImage('assets/icons/logo_google.png')),
          false,
        ),
        _buildLinkTile(
          'Facebook',
          const Image(image: AssetImage('assets/icons/logo_facebook.png')),
          false,
        ),
      ],
    );
  }

  Widget _buildLinkTile(String name, Widget leadingWidget, bool isLinked) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: SizedBox(width: 30, height: 30, child: leadingWidget),
      title: Text(
        name,
        style: const TextStyle(color: Colors.white, fontSize: 18),
      ),
      trailing: TextButton(
        onPressed: () {
          // oauth link
        },
        child: Text(
          isLinked ? 'Unlink' : 'Link',
          style: TextStyle(
            color: isLinked ? Colors.red : Colors.blue,
            fontSize: 16,
          ),
        ),
      ),
    );
  }

  Widget _buildSaveButton(ProfileViewModel viewModel) {
    return ElevatedButton(
      onPressed: viewModel.isLoading
          ? null
          : () async {
              final newName = _usernameController.text.trim();
              final newEmail = _emailController.text.trim();
              await viewModel.saveInformation(
                newName: newName,
                newEmail: newEmail,
              );
              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Profile update.'),
                    backgroundColor: Colors.green,
                  ),
                );
              }
            },
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        disabledBackgroundColor: Colors.grey.shade300,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        padding: const EdgeInsets.symmetric(vertical: 16),
      ),
      child: viewModel.state == ProfileState.saving
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

  Widget _buildLogoutButton(BuildContext context) {
    return TextButton(
      onPressed: () async {
        try {
          final authRepository = context.read<AuthRepository>();
          await authRepository.logout();
          if (mounted) {
            Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(builder: (context) => const MainPageApp()),
              (Route<dynamic> route) => false,
            );
          }
        } catch (e) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Logout failed: $e'),
                backgroundColor: Colors.red,
              ),
            );
          }
        }
      },
      child: const Text(
        'Sign out',
        style: TextStyle(color: Colors.red, fontSize: 20),
      ),
    );
  }
}
