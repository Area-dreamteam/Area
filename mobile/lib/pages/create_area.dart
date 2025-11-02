import 'package:flutter/material.dart';
import 'package:mobile/widgets/card.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:provider/provider.dart';

class CreateAreaPage extends StatefulWidget {
  const CreateAreaPage({super.key});

  @override
  State<CreateAreaPage> createState() => _MyAppletPageState();
}

class _MyAppletPageState extends State<CreateAreaPage> {
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
      return Center(
        child: Text(
          'No Applet.',
          style: Theme.of(
            context,
          ).textTheme.titleLarge?.copyWith(color: Colors.white70),
        ),
      );
    }

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: 22),
          ...viewModel.applets.map(
            (applet) => Padding(
              padding: const EdgeInsets.only(bottom: 20),
              child: Semantics(
                label: "Applet: ${applet.name}, ID: ${applet.id}",
                button: true,
                child: AppletCard(
                  color: Colors.black,
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
          ),
        ],
      ),
    );
  }
}
