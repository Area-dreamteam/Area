import 'package:flutter/material.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/viewmodels/profile_viewmodel.dart';
import 'package:provider/provider.dart';
import 'package:mobile/pages/change_password_page.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/repositories/auth_repository.dart';
import 'package:mobile/scaffolds/main_scaffold.dart';
import 'package:mobile/core/config.dart';
import 'package:mobile/services/api_url_service.dart';
import 'package:mobile/services/api_service.dart';
import 'package:mobile/services/oauth_service.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> with WidgetsBindingObserver {
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _apiUrlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final viewModel = context.read<ProfileViewModel>();
      viewModel.loadCurrentUser().then((_) {
        if (mounted && viewModel.currentUser != null) {
          _usernameController.text = viewModel.currentUser!.name;
          _emailController.text = viewModel.currentUser!.email;
        }
      });
      _loadApiUrl();
    });
  }

  Future<void> _loadApiUrl() async {
    final url = await Config.getApiUrl();
    if (mounted) {
      _apiUrlController.text = url;
    }
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    super.didChangeAppLifecycleState(state);
    if (state == AppLifecycleState.resumed) {
      print('ProfilePage: App resumed - reloading user data');
      Future.delayed(const Duration(milliseconds: 500), () {
        if (mounted) {
          final viewModel = context.read<ProfileViewModel>();
          viewModel.loadCurrentUser().then((_) {
            if (mounted && viewModel.currentUser != null) {
              _usernameController.text = viewModel.currentUser!.name;
              _emailController.text = viewModel.currentUser!.email;
            }
          });
        }
      });
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _usernameController.dispose();
    _emailController.dispose();
    _apiUrlController.dispose();
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
            _buildApiUrlSection(),
            const SizedBox(height: 40),
            _buildLinkedAccountsSection(viewModel),
            const SizedBox(height: 40),
            _buildSaveButton(viewModel),
            const SizedBox(height: 40),
            _buildLogoutButton(context),
            const SizedBox(height: 40),
            _buildDeleteButton(context, viewModel),
            const SizedBox(height: 40),
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
          style: const TextStyle(color: Colors.white, fontSize: 18),
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
              MaterialPageRoute(
                builder: (context) => const ChangePasswordPage(),
              ),
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

  Widget _buildApiUrlSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'API Server URL',
          style: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 8),
        const Text(
          'Configure the API server URL for the mobile app.',
          style: TextStyle(color: Colors.white70, fontSize: 14),
        ),
        const SizedBox(height: 16),
        TextField(
          controller: _apiUrlController,
          style: const TextStyle(color: Colors.white, fontSize: 16),
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
            hintText: 'https://your-api-server.com',
            hintStyle: TextStyle(color: Colors.grey.shade600),
          ),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: ElevatedButton(
                onPressed: _saveApiUrl,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8.0),
                  ),
                  padding: const EdgeInsets.symmetric(vertical: 12),
                ),
                child: const Text('Save URL'),
              ),
            ),
            const SizedBox(width: 12),
            ElevatedButton(
              onPressed: _resetApiUrl,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.grey.shade700,
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8.0),
                ),
                padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
              ),
              child: const Text('Reset'),
            ),
          ],
        ),
      ],
    );
  }

  Future<void> _saveApiUrl() async {
    final newUrl = _apiUrlController.text.trim();
    
    if (newUrl.isEmpty) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Please enter a valid URL'),
            backgroundColor: Colors.red,
          ),
        );
      }
      return;
    }

    try {
      await ApiUrlService.setApiUrl(newUrl);
      
      if (!mounted) return;
      
      final apiService = context.read<ApiService>();
      await apiService.updateBaseUrl(newUrl);
      
      if (!mounted) return;
      
      final oauthService = context.read<OAuthService>();
      await oauthService.updateBaseUrl(newUrl);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('API URL updated successfully. Please restart the app for full effect.'),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 4),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to update API URL: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _resetApiUrl() async {
    try {
      await ApiUrlService.resetApiUrl();
      final defaultUrl = await ApiUrlService.getDefaultApiUrl();
      
      if (mounted) {
        _apiUrlController.text = defaultUrl;
      }
      
      if (!mounted) return;
      
      final apiService = context.read<ApiService>();
      await apiService.updateBaseUrl(defaultUrl);
      
      if (!mounted) return;
      
      final oauthService = context.read<OAuthService>();
      await oauthService.updateBaseUrl(defaultUrl);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('API URL reset to default. Please restart the app for full effect.'),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 4),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to reset API URL: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Widget _buildLinkedAccountsSection(ProfileViewModel viewModel) {
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
        ...viewModel.linkedAccounts.map((account) {
          final String displayName = account.name.replaceAll(
            '_oauth',
            '',
          );

          return _buildLinkTile(
            displayName.toLowerCase(),
            getServiceIcon(
              account.name,
              size: 30.0,
              imageUrl: account.imageUrl,
            ),
            account.connected,
            () {
              if (account.connected) {
                viewModel.unlinkAccount(account.id);
              } else {
              }
            },
          );
        }),
      ],
    );
  }

  Widget _buildLinkTile(
      String name,
      Widget leadingWidget,
      bool isLinked,
      VoidCallback onPressed,
      ) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: SizedBox(width: 30, height: 30, child: leadingWidget),
      title: Text(
        name,
        style: const TextStyle(color: Colors.white, fontSize: 18),
      ),
      trailing: TextButton(
        onPressed: onPressed,
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
              content: Text('Profile updated.'),
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

  Widget _buildDeleteButton(BuildContext context, ProfileViewModel viewmodels) {
    return TextButton(
      onPressed: () async {
        final bool? confirm = await showDialog<bool>(
          context: context,
          builder: (BuildContext dialogContext) {
            return AlertDialog(
              backgroundColor: Color(0xFF212121),
              title: const Text(
                "Confirm to delete account",
                style: TextStyle(color: Colors.white),
              ),
              content: const Text(
                "Are you sure to delete your account ?",
                style: TextStyle(color: Colors.white),
              ),
              actions: <Widget>[
                TextButton(
                  onPressed: () {
                    Navigator.pop(dialogContext, false);
                  },
                  child: const Text(
                    'Cancel',
                    style: TextStyle(color: Colors.blueAccent),
                  ),
                ),
                TextButton(
                  onPressed: () {
                    Navigator.pop(dialogContext, true);
                  },
                  style: TextButton.styleFrom(
                    foregroundColor: Colors.redAccent,
                  ),
                  child: const Text('Delete'),
                ),
              ],
            );
          },
        );
        if (confirm == true && context.mounted) {
          final authRepository = context.read<AuthRepository>();
          final navigator = Navigator.of(context);
          final scaffoldMessenger = ScaffoldMessenger.of(context);
          try {
            await authRepository.deleteProfile(viewmodels.currentUser!.id);
            if (mounted) {
              navigator.pushAndRemoveUntil(
                MaterialPageRoute(builder: (context) => const MainPageApp()),
                    (Route<dynamic> route) => false,
              );
            }
          } catch (e) {
            if (mounted) {
              scaffoldMessenger.showSnackBar(
                SnackBar(
                  content: Text("Account delete failed: $e"),
                  backgroundColor: Colors.red,
                ),
              );
            }
          }
        }
      },
      child: const Text(
        "Delete Account",
        style: TextStyle(color: Colors.red, fontSize: 20),
      ),
    );
  }

  Widget _buildLogoutButton(BuildContext context) {
    return TextButton(
      onPressed: () async {
        final authRepository = context.read<AuthRepository>();
        final navigator = Navigator.of(context);
        final scaffoldMessenger = ScaffoldMessenger.of(context);
        try {
          await authRepository.logout();
          if (mounted) {
            navigator.pushAndRemoveUntil(
              MaterialPageRoute(builder: (context) => const MainPageApp()),
                  (Route<dynamic> route) => false,
            );
          }
        } catch (e) {
          if (mounted) {
            scaffoldMessenger.showSnackBar(
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