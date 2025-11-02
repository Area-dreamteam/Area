import 'package:flutter/material.dart';
import 'package:mobile/pages/my_area.dart';
import 'package:mobile/viewmodels/register_viewmodel.dart';
import 'package:provider/provider.dart';
import 'package:mobile/pages/login.dart';
import 'package:mobile/widgets/text_form.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});

  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _onRegisterSuccess() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Account created! Redirecting to MyAreaPage...'),
        backgroundColor: Colors.green,
      ),
    );

    Future.delayed(const Duration(seconds: 1), () {
      if (mounted) {
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (context) => const MyAreaPage()),
          (Route<dynamic> route) => false,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  _header(),
                  const SizedBox(height: 40),
                  _inputFields(),
                  const SizedBox(height: 20),
                  _feedbackAndActionSection(),
                  const SizedBox(height: 20),
                  _loginNavigation(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _header() {
    return Semantics(
      header: true,
      child: Text(
        "Sign up",
        style: Theme.of(context).textTheme.displayMedium?.copyWith(
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
    );
  }

  Widget _inputFields() {
    return Column(
      children: <Widget>[
        const SizedBox(height: 20),
        CustomTextFormField(
          controller: _emailController,
          hintText: "Email",
          icon: Icons.email,
          keyboardType: TextInputType.emailAddress,
          validator: (value) {
            if (value != null && !value.contains('@')) {
              return 'This email is not valid.';
            }
            return null;
          },
        ),
        const SizedBox(height: 20),
        CustomPasswordFormField(controller: _passwordController),
      ],
    );
  }

  Widget _feedbackAndActionSection() {
    final registerViewModel = context.read<RegisterViewModel>();

    return Consumer<RegisterViewModel>(
      builder: (context, viewModel, child) {
        return Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (viewModel.state == RegisterState.error)
              Text(
                viewModel.errorMessage,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.redAccent, fontSize: 15),
              ),
            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: viewModel.isLoading
                  ? null
                  : () {
                      if (_formKey.currentState!.validate()) {
                        registerViewModel
                            .register(
                              email: _emailController.text.trim(),
                              password: _passwordController.text.trim(),
                            )
                            .then((success) {
                              if (success) _onRegisterSuccess();
                            });
                      }
                    },
              child: viewModel.isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(color: Colors.black),
                    )
                  : const Text("Sign up", style: TextStyle(fontSize: 20)),
            ),
          ],
        );
      },
    );
  }

  Widget _loginNavigation() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        const Text(
          "Already have an account?",
          style: TextStyle(color: Colors.white),
        ),
        TextButton(
          onPressed: () {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(builder: (context) => const LoginPage()),
            );
          },
          child: const Text(
            "Login",
            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
          ),
        ),
      ],
    );
  }
}
