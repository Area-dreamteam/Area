import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/widgets/text_form.dart';

void main() {
  group('CustomTextFormField', () {
    testWidgets('renders with correct hint text', (tester) async {
      final controller = TextEditingController();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomTextFormField(
              controller: controller,
              hintText: 'Test Hint',
              icon: Icons.person,
            ),
          ),
        ),
      );

      expect(find.text('Test Hint'), findsOneWidget);
      expect(find.byIcon(Icons.person), findsOneWidget);
    });

    testWidgets('validates input correctly', (tester) async {
      final controller = TextEditingController();
      final formKey = GlobalKey<FormState>();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Form(
              key: formKey,
              child: CustomTextFormField(
                controller: controller,
                hintText: 'Email',
                icon: Icons.email,
                validator: (value) {
                  if (value == null || !value.contains('@')) {
                    return 'Invalid email';
                  }
                  return null;
                },
              ),
            ),
          ),
        ),
      );

      // Trigger validation with invalid input
      controller.text = 'invalid';
      formKey.currentState!.validate();
      await tester.pump();

      expect(find.text('Invalid email'), findsOneWidget);
    });

    testWidgets('accepts valid input', (tester) async {
      final controller = TextEditingController();
      final formKey = GlobalKey<FormState>();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Form(
              key: formKey,
              child: CustomTextFormField(
                controller: controller,
                hintText: 'Email',
                icon: Icons.email,
                validator: (value) {
                  if (value == null || !value.contains('@')) {
                    return 'Invalid email';
                  }
                  return null;
                },
              ),
            ),
          ),
        ),
      );

      controller.text = 'test@example.com';
      final isValid = formKey.currentState!.validate();

      expect(isValid, true);
    });
  });

  group('CustomPasswordFormField', () {
    testWidgets('initially obscures text', (tester) async {
      final controller = TextEditingController();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPasswordFormField(controller: controller),
          ),
        ),
      );

      final textField = tester.widget<TextField>(find.byType(TextField));
      expect(textField.obscureText, true);
    });

    testWidgets('toggles password visibility', (tester) async {
      final controller = TextEditingController();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPasswordFormField(controller: controller),
          ),
        ),
      );

      // Initially obscured
      TextField textField = tester.widget<TextField>(find.byType(TextField));
      expect(textField.obscureText, true);

      await tester.tap(find.byType(IconButton));
      await tester.pump();

      textField = tester.widget<TextField>(find.byType(TextField));
      expect(textField.obscureText, false);

      await tester.tap(find.byType(IconButton));
      await tester.pump();

      textField = tester.widget<TextField>(find.byType(TextField));
      expect(textField.obscureText, true);
    });

    testWidgets('shows correct hint text', (tester) async {
      final controller = TextEditingController();

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomPasswordFormField(controller: controller),
          ),
        ),
      );

      expect(find.text('Password'), findsOneWidget);
      expect(find.byIcon(Icons.password), findsOneWidget);
    });
  });
}