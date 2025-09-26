import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

class TestCounterApp extends StatefulWidget {
  const TestCounterApp({super.key});
  @override
  State<TestCounterApp> createState() => _TestCounterAppState();
}

class _TestCounterAppState extends State<TestCounterApp> {
  int _counter = 0;
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(child: Text('$_counter', key: const Key('counterText'))),
        floatingActionButton: FloatingActionButton(
          onPressed: () => setState(() => _counter++),
          child: const Icon(Icons.add),
        ),
      ),
    );
  }
}

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const TestCounterApp());
    await tester.pumpAndSettle();

    expect(find.text('0'), findsOneWidget);
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();
    expect(find.text('1'), findsOneWidget);
  });
}
