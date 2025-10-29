import 'package:flutter/material.dart';
import 'package:mobile/widgets/my_area_card.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:provider/provider.dart';

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
    if (viewModel.isLoading && viewModel.applets.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    if (viewModel.applets.isEmpty && !viewModel.isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.layers_clear, size: 60, color: Colors.white38),
            const SizedBox(height: 20),
            const Text(
              'No Applets yet.',
              style: TextStyle(fontSize: 20, color: Colors.white70),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: viewModel.loadApplets,
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (viewModel.errorMessage.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(bottom: 16.0),
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Center(
                    child: Text(
                      viewModel.errorMessage,
                      style: const TextStyle(color: Colors.white),
                    ),
                  ),
                ),
              ),
            TabWithCount(count: viewModel.applets.length),
            const SizedBox(height: 22),
            ...viewModel.applets.map(
              (applet) => Padding(
                padding: const EdgeInsets.only(bottom: 20),
                child: MyAreaCard(
                  applet: applet,
                  onEdit: () {},
                  onDelete: () async {
                    await viewModel.deleteApplet(applet.id);
                  },
                  onToggleEnabled: (value) {
                    viewModel.toggleAreaEnabled(applet.id);
                  },
                  onTogglePublic: (value) {},
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
