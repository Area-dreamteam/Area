import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/pages/applet_detail_page.dart';
import 'package:mobile/widgets/my_area_card.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:provider/provider.dart';
import 'package:mobile/pages/create_page.dart';

class TabWithCount extends StatelessWidget {
  final int count;
  const TabWithCount({super.key, required this.count});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(color: Colors.blue, borderRadius: BorderRadius.circular(20)),
      child: Text("Applets ($count)", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
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

  void _navigateToDetail(AppletModel applet) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => AppletDetailPage(applet: applet)),
    ).then((result) {
      if (result == true && mounted) {
        context.read<MyAppletViewModel>().loadApplets();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final appletViewModel = context.watch<MyAppletViewModel>();

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        title: const Text('My Areas', style: TextStyle(color: Colors.white)),
        backgroundColor: const Color(0xFF212121),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.white),
            onPressed: () => appletViewModel.loadApplets(),
            tooltip: 'Refresh',
          ),
        ],
      ),
      body: SafeArea(child: _buildBody(appletViewModel)),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 0),
    );
  }

  Widget _buildBody(MyAppletViewModel viewModel) {
    if (viewModel.isLoading && viewModel.applets.isEmpty) {
      return const Center(child: CircularProgressIndicator(color: Colors.white));
    }

    if (viewModel.applets.isEmpty && !viewModel.isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.layers_clear, size: 60, color: Colors.white38),
            const SizedBox(height: 20),
            const Text('No Applets yet.', style: TextStyle(fontSize: 20, color: Colors.white70), textAlign: TextAlign.center),
            const SizedBox(height: 10),
            const Text('Create an Applet to automate your tasks!', style: TextStyle(fontSize: 16, color: Colors.white54), textAlign: TextAlign.center),
            const SizedBox(height: 30),
            ElevatedButton.icon(
              icon: const Icon(Icons.add_circle_outline),
              label: const Text('Create your first Applet'),
              onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CreatePage())),
              style: ElevatedButton.styleFrom(padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12)),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: viewModel.loadApplets,
      color: Colors.white,
      backgroundColor: Colors.blue,
      child: ListView(
        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
        children: [
          if (viewModel.state == MyAppletState.error && viewModel.errorMessage.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(bottom: 16.0, left: 4, right: 4),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(color: Colors.red, borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.red.shade400, width: 1)),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.error_outline, color: Colors.white, size: 18),
                    const SizedBox(width: 8),
                    Expanded(child: Text(viewModel.errorMessage, style: const TextStyle(color: Colors.white), textAlign: TextAlign.center)),
                  ],
                ),
              ),
            ),

          Padding(
             padding: const EdgeInsets.only(left: 4.0, bottom: 16.0),
             child: Align(alignment: Alignment.centerLeft, child: TabWithCount(count: viewModel.applets.length)),
           ),

          ...viewModel.applets.map(
            (applet) => Padding(
              padding: const EdgeInsets.only(bottom: 20),
              child: MyAreaCard(
                applet: applet,
                onTap: () => _navigateToDetail(applet),
                onToggleEnabled: (value) => viewModel.toggleAreaEnabled(applet.id),
              ),
            ),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }
}