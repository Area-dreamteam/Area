import 'package:flutter/material.dart';

class CustomTextFormField extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  final IconData icon;
  final TextInputType keyboardType;
  final String? Function(String?)? validator;

  const CustomTextFormField({
    super.key,
    required this.controller,
    required this.hintText,
    required this.icon,
    this.keyboardType = TextInputType.text,
    this.validator,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: hintText,
      textField: true,
      child: TextFormField(
        controller: controller,
        style: const TextStyle(color: Colors.black),
        keyboardType: keyboardType,
        decoration: InputDecoration(
          hintText: hintText,
          border: const OutlineInputBorder(borderSide: BorderSide.none),
          fillColor: Colors.white,
          filled: true,
          prefixIcon: Icon(icon),
        ),
        validator: validator,
      ),
    );
  }
}

class CustomPasswordFormField extends StatefulWidget {
  final TextEditingController controller;

  const CustomPasswordFormField({
    super.key,
    required this.controller,
  });

  @override
  State<CustomPasswordFormField> createState() =>
      _CustomPasswordFormFieldState();
}

class _CustomPasswordFormFieldState extends State<CustomPasswordFormField> {
  bool _obscurePassword = true;

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: "Password",
      textField: true,
      obscured: _obscurePassword,
      child: TextFormField(
        controller: widget.controller,
        obscureText: _obscurePassword,
        style: const TextStyle(color: Colors.black),
        decoration: InputDecoration(
          hintText: "Password",
          border: const OutlineInputBorder(borderSide: BorderSide.none),
          fillColor: Colors.white,
          filled: true,
          prefixIcon: const Icon(Icons.password),
          suffixIcon: IconButton(
            tooltip: _obscurePassword ? 'Display password' : 'Hide password',
            icon: Icon(
              _obscurePassword ? Icons.visibility_off : Icons.visibility,
            ),
            onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
          ),
        ),
      ),
    );
  }
}