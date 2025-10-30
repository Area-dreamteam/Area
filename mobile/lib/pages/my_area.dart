import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/pages/applet_detail_page.dart';
import 'package:mobile/widgets/my_area_card.dart';
import 'package:mobile/widgets/navbar.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:provider/provider.dart';
import 'package:mobile/pages/create_page.dart';

class MyAreaPage extends StatefulWidget {
  const MyAreaPage({super.key});
  @override
  State<MyAreaPage> createState() => _MyAppletPageState();
}

class _MyAppletPageState extends State<MyAreaPage>
    with TickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<MyAppletViewModel>().loadApplets();
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
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

    final privateApplets = appletViewModel.privateApplets;
    final publicApplets = appletViewModel.publicApplets;

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
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.blue,
          labelColor: Colors.white,
          unselectedLabelColor: Colors.grey,
          tabs: [
            Tab(text: "Private (${privateApplets.length})"),
            Tab(text: "Public (${publicApplets.length})"),
          ],
        ),
      ),
      body: SafeArea(
        child: _buildBody(appletViewModel, privateApplets, publicApplets),
      ),
      bottomNavigationBar: const MyBottomNavigationBar(selectedIndex: 0),
    );
  }

  Widget _buildBody(
    MyAppletViewModel viewModel,
    List<AppletModel> privateApplets,
    List<AppletModel> publicApplets,
  ) {
    if (viewModel.isLoading && viewModel.applets.isEmpty) {
      return const Center(
        child: CircularProgressIndicator(color: Colors.white),
      );
    }

    if (viewModel.applets.isEmpty && !viewModel.isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(height: 20),
            const Text(
              'No Applets yet.',
              style: TextStyle(fontSize: 20, color: Colors.white70),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 10),
            const Text(
              'Create an Applet to automate your tasks!',
              style: TextStyle(fontSize: 16, color: Colors.white54),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 30),
            ElevatedButton.icon(
              icon: const Icon(Icons.add_circle_outline),
              label: const Text('Create your first Applet'),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const CreatePage()),
              ),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 20,
                  vertical: 12,
                ),
              ),
            ),
          ],
        ),
      );
    }

    return Column(
      children: [
        if (viewModel.state == MyAppletState.error &&
            viewModel.errorMessage.isNotEmpty)
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.red,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.red.shade400, width: 1),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    color: Colors.white,
                    size: 18,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      viewModel.errorMessage,
                      style: const TextStyle(color: Colors.white),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            ),
          ),
        Expanded(
          child: RefreshIndicator(
            onRefresh: viewModel.loadApplets,
            color: Colors.white,
            backgroundColor: Colors.blue,
            child: TabBarView(
              controller: _tabController,
              children: [
                _buildAppletList(
                  privateApplets,
                  'No private applets.',
                  'Create an applet to see it here.',
                ),
                _buildAppletList(
                  publicApplets,
                  'No public applets.',
                  'Publish a private applet to see it here.',
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildAppletList(
    List<AppletModel> applets,
    String emptyTitle,
    String emptySubtitle,
  ) {
    if (applets.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(height: 16),
            Text(
              emptyTitle,
              style: TextStyle(fontSize: 18, color: Colors.white70),
            ),
            SizedBox(height: 8),
            Text(
              emptySubtitle,
              style: TextStyle(fontSize: 14, color: Colors.white54),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
      itemCount: applets.length,
      itemBuilder: (context, index) {
        final applet = applets[index];
        return Padding(
          padding: const EdgeInsets.only(bottom: 20),
          child: MyAreaCard(
            applet: applet,
            onTap: () => _navigateToDetail(applet),
            onToggleEnabled: applet.isPublic
                ? null
                : (value) => context
                      .read<MyAppletViewModel>()
                      .toggleAreaEnabled(applet.id),
          ),
        );
      },
    );
  }
}
