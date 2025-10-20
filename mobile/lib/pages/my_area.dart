import 'package:flutter/material.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:provider/provider.dart';
import 'package:mobile/widgets/card.dart';

class TabWithCount extends StatelessWidget {
  final int count;

  const TabWithCount({super.key, required this.count});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.blue,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Text(
        "Applets ($count)",
        style: const TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }
}

class MyAreaPage extends StatefulWidget {
  const MyAreaPage({super.key});

  @override
  State<MyAreaPage> createState() => _MyAppletPageState();
}

class _MyAppletPageState extends State<MyAreaPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<MyAppletViewModel>().loadApplets();
    });
  }

  @override
  Widget build(BuildContext context) {
    final appletViewModel = context.watch<MyAppletViewModel>();

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      body: SafeArea(child: _buildBody(appletViewModel)),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 0),
    );
  }

  Widget _buildBody(MyAppletViewModel viewModel) {
    if (viewModel.isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (viewModel.applets.isEmpty) {
      return const Center(
        child: Text(
          'No Applet.',
          style: TextStyle(fontSize: 20, color: Colors.white70),
        ),
      );
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TabWithCount(count: viewModel.applets.length),
          const SizedBox(height: 22),
          ...viewModel.applets.map(
            (applet) => Padding(
              padding: const EdgeInsets.only(bottom: 20),
              child: AppletCard( 
                icon: Icons.electrical_services,
                title: applet.name,
                byText: 'ID: ${applet.id}',
                onDelete: () async {
                  final success = await viewModel.deleteApplet(applet.id);
                  if (!mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        success
                            ? "Applet deleted successfully"
                            : viewModel.errorMessage,
                      ),
                      backgroundColor: success ? Colors.green : Colors.red,
                    ),
                  );
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}