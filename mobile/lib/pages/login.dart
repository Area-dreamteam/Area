// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:mobile/pages/my_area.dart';
import 'package:mobile/pages/register.dart';
import 'package:mobile/services/oauth_service.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/viewmodels/login_viewmodel.dart';
import 'package:provider/provider.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _obscurePassword = true;

  List<OAuthProvider> _oauthProviders = [];
  bool _isOAuthLoading = false;
  String _oauthError = '';

  @override
  void initState() {
    super.initState();
    _loadOAuthProviders();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _loadOAuthProviders() async {
    print('Loading OAuth providers...');
    final oauthService = context.read<OAuthService>();
    try {
      final providers = await oauthService.getAvailableProviders();
      print(
        'Loaded ${providers.length} OAuth providers: ${providers.map((p) => p.name).toList()}',
      );
      setState(() {
        _oauthProviders = providers;
      });
      print('State updated with OAuth providers');
    } catch (e) {
      print('Failed to load OAuth providers: $e');
    }
  }

  Future<void> _loginWithOAuth(String serviceName) async {
    setState(() {
      _isOAuthLoading = true;
      _oauthError = '';
    });

    final oauthService = context.read<OAuthService>();

    try {
      final result = await oauthService.loginWithOAuth(serviceName);

      if (result.isSuccess) {
        _onLoginSuccess();
      } else {
        setState(() {
          _oauthError = result.error ?? 'OAuth login failed';
        });
      }
    } catch (e) {
      setState(() {
        _oauthError = 'OAuth login error: $e';
      });
    } finally {
      if (mounted) {
        setState(() {
          _isOAuthLoading = false;
        });
      }
    }
  }

  void _onLoginSuccess() {
    Navigator.of(
      context,
    ).pushReplacement(MaterialPageRoute(builder: (_) => const MyAreaPage()));
  }

  @override
  Widget build(BuildContext context) {
    final loginViewModel = context.watch<LoginViewModel>();

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      body: Center(
        child: SingleChildScrollView(
          child: Container(
            margin: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _header(),
                  const SizedBox(height: 50),
                  _inputFields(loginViewModel),
                  const SizedBox(height: 20),
                  _oauthSection(),
                  const SizedBox(height: 30),
                  _signup(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _header() {
    return const Column(
      children: [
        Text(
          "What's your email ?",
          style: TextStyle(
            color: Colors.white,
            fontSize: 40,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  Widget _inputFields(LoginViewModel viewModel) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextFormField(
          controller: _emailController,
          style: const TextStyle(color: Colors.black),
          decoration: InputDecoration(
            hintText: "E-mail",
            border: const OutlineInputBorder(borderSide: BorderSide.none),
            fillColor: Colors.white,
            filled: true,
            prefixIcon: const Icon(Icons.person),
          ),
          validator: (value) {
            if (value == null || !value.contains('@')) {
              return 'Email not valid.';
            }
            return null;
          },
        ),
        const SizedBox(height: 10),
        TextFormField(
          controller: _passwordController,
          obscureText: _obscurePassword,
          style: const TextStyle(color: Colors.black),
          decoration: InputDecoration(
            hintText: "Password",
            border: const OutlineInputBorder(borderSide: BorderSide.none),
            fillColor: Colors.white,
            filled: true,
            prefixIcon: const Icon(Icons.password),
            suffixIcon: IconButton(
              icon: Icon(
                _obscurePassword ? Icons.visibility_off : Icons.visibility,
              ),
              onPressed: () {
                setState(() {
                  _obscurePassword = !_obscurePassword;
                });
              },
            ),
          ),
          validator: (value) {
            if (value == null) {
              return 'Enter your password.';
            }
            return null;
          },
        ),
        const SizedBox(height: 20),
        if (viewModel.state == LoginState.error)
          Padding(
            padding: const EdgeInsets.only(bottom: 15),
            child: Text(
              viewModel.errorMessage,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.redAccent, fontSize: 15),
            ),
          ),
        const SizedBox(height: 20),
        ElevatedButton(
          onPressed: viewModel.isLoading
              ? null
              : () async {
                  if (_formKey.currentState!.validate()) {
                    final success = await viewModel.loginWithEmailPassword(
                      _emailController.text.trim(),
                      _passwordController.text.trim(),
                    );
                    if (success) {
                      _onLoginSuccess();
                    }
                  }
                },
          child: viewModel.isLoading
              ? const SizedBox(
                  height: 24,
                  width: 24,
                  child: CircularProgressIndicator(
                    color: Colors.black,
                    strokeWidth: 3,
                  ),
                )
              : const Text(
                  "Login",
                  style: TextStyle(fontSize: 20, color: Colors.black),
                ),
        ),
      ],
    );
  }

  Widget _oauthSection() {
    print('Building OAuth section with ${_oauthProviders.length} providers');
    return Column(
      children: [
        if (_oauthError.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(bottom: 15),
            child: Text(
              _oauthError,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.redAccent, fontSize: 14),
            ),
          ),
        if (_oauthProviders.isNotEmpty) ...[
          const Row(
            children: [
              Expanded(child: Divider(color: Colors.grey)),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 16),
                child: Text(
                  'OR',
                  style: TextStyle(color: Colors.grey, fontSize: 14),
                ),
              ),
              Expanded(child: Divider(color: Colors.grey)),
            ],
          ),
          const SizedBox(height: 20),
          
          ..._oauthProviders.map((provider) {
            final displayName = provider.name.toUpperCase();

            return Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: _isOAuthLoading
                      ? null
                      : () => _loginWithOAuth(provider.name),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  icon: _isOAuthLoading
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : getServiceIcon(provider.name, size: 20.0),
                  label: Text(
                    'Continue with $displayName',
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              ),
            );
          }),
        ],
      ],
    );
  }

  Widget _signup() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text(
          "Dont have an account?",
          style: TextStyle(color: Colors.white),
        ),
        TextButton(
          onPressed: () {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => const RegisterPage()),
            );
          },
          child: const Text("Sign Up", style: TextStyle(color: Colors.white)),
        ),
      ],
    );
  }
}