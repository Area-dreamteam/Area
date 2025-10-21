import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/viewmodels/explore_viewmodel.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/viewmodels/my_applet_viewmodel.dart';
import 'package:mobile/widgets/card.dart';
import 'package:mobile/widgets/hex_convert.dart';
import 'package:provider/provider.dart';

class InformationPage extends StatefulWidget {
  final ExploreItem item;

  const InformationPage({super.key, required this.item});

  @override
  State<InformationPage> createState() => _InformationPageState();
}

class _InformationPageState extends State<InformationPage>
    with TickerProviderStateMixin {
  late TabController _tabController;
  late final int? _serviceId;
  bool _isConnected = false;
  bool _isLoadingConnection = true;
  late Future<List<AppletModel>> _publicApplets;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    final applets = context.read<ServiceRepository>();

    if (widget.item.type == 'Service') {
      final service = widget.item.data as Service;
      _serviceId = service.id;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) {
          context.read<MyAppletViewModel>().loadApplets();
        }
      });

      _publicApplets = applets.fetchPublicApplets(serviceId: _serviceId!);
    } else if (widget.item.type == 'Applet') {
      final triggerService = (widget.item.data as AppletModel).triggerService;
      _serviceId = triggerService?.id;
      _publicApplets = _serviceId != null
          ? applets.fetchPublicApplets(serviceId: _serviceId)
          : Future.value([]);
    } else {
      _serviceId = null;
      _publicApplets = Future.value([]);
    }
    _fetchConnectionStatus();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _fetchConnectionStatus() async {
    if (_serviceId == null) {
      setState(() => _isLoadingConnection = false);
      return;
    }

    setState(() => _isLoadingConnection = true);
    final repo = context.read<ServiceRepository>();
    final status = await repo.isServiceConnected(_serviceId);

    if (mounted) {
      setState(() {
        _isConnected = status;
        _isLoadingConnection = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final bool isApplet = widget.item.type == 'Applet';
    final color = hexToColor(widget.item.colorHex);

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        backgroundColor: color,
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: isApplet
          ? _buildAppletLayout(context, color)
          : _buildServiceLayout(context, color),
    );
  }

  Widget _buildServiceLayout(BuildContext context, Color color) {
    final service = widget.item.data as Service;

    return Container(
      color: color,
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: 20.0,
              vertical: 10.0,
            ),
            child: Column(
              children: [
                Image.network(service.imageUrl, width: 60, height: 60),
                const SizedBox(height: 16),
                Text(
                  service.name,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  service.description ?? "",
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 16,
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: 24),
                _buildConnectButton(showIcon: false),
                const SizedBox(height: 24),
              ],
            ),
          ),
          Expanded(
            child: Container(
              color: const Color(0xFF212121),
              child: Column(
                children: [
                  TabBar(
                    controller: _tabController,
                    labelColor: Colors.white,
                    unselectedLabelColor: Colors.white54,
                    indicatorColor: Colors.blue,
                    tabs: const [
                      Tab(text: "Applets"),
                      Tab(text: "My Applets"),
                    ],
                  ),
                  Expanded(
                    child: TabBarView(
                      controller: _tabController,
                      children: [
                        _buildPublicAppletsTab(),
                        _buildMyAppletsTab(service.id),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAppletLayout(BuildContext context, Color color) {
    final applet = widget.item.data as AppletModel;
    final triggerService = applet.triggerService;

    return ListView(
      padding: const EdgeInsets.all(20.0),
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 70,
              height: 70,
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(15),
              ),
              child: triggerService != null
                  ? Image.network(triggerService.imageUrl, scale: 1.5)
                  : const Icon(Icons.apps, color: Colors.white, size: 40),
            ),
            IconButton(
              icon: const Icon(Icons.ios_share, color: Colors.white),
              onPressed: () {},
            ),
          ],
        ),
        const SizedBox(height: 20),
        Text(
          widget.item.title,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 28,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 20),
        if (triggerService != null)
          Row(
            children: [
              Image.network(triggerService.imageUrl, width: 30, height: 30),
              const SizedBox(width: 10),
              Text(
                triggerService.name,
                style: const TextStyle(color: Colors.white, fontSize: 18),
              ),
            ],
          ),
        const SizedBox(height: 10),
        Row(
          children: [
            const Icon(Icons.person_outline, color: Colors.white70, size: 20),
            const SizedBox(width: 12),
            Text(
              widget.item.byText ?? 'by ${applet.user.name}',
              style: const TextStyle(color: Colors.white70, fontSize: 16),
            ),
          ],
        ),
        const SizedBox(height: 30),
        _buildConnectButton(showIcon: true),
        const SizedBox(height: 30),

        const Text(
          "Description",
          style: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 10),
        Text(
          applet.description ?? "",
          style: const TextStyle(
            color: Colors.white70,
            fontSize: 16,
            height: 1.5,
          ),
        ),
      ],
    );
  }

  Widget _buildPublicAppletsTab() {
    return FutureBuilder<List<AppletModel>>(
      future: _publicApplets,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }

        final applets = snapshot.data ?? [];

        if (applets.isEmpty) {
          return const Center(
            child: Text(
              "No public applets found for this service.",
              style: TextStyle(color: Colors.white70),
            ),
          );
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: applets.length,
          itemBuilder: (context, index) {
            final applet = applets[index];
            return Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: AppletCard(
                title: applet.name,
                byText: 'By ${applet.user.name}',
                colorHex: applet.color,
                icon: Icons.public,
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildMyAppletsTab(int currentServiceId) {
    return Consumer<MyAppletViewModel>(
      builder: (context, viewModel, child) {
        if (viewModel.isLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        final myAppletsForThisService = viewModel.applets;

        if (myAppletsForThisService.isEmpty) {
          return const Center(
            child: Text(
              "You have no applets.",
              style: TextStyle(color: Colors.white70, fontSize: 16),
            ),
          );
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: myAppletsForThisService.length,
          itemBuilder: (context, index) {
            final applet = myAppletsForThisService[index];
            return Padding(
              padding: const EdgeInsets.only(bottom: 16),
              child: AppletCard(
                title: applet.name,
                byText: 'By ${applet.user.name}',
                colorHex: applet.color,
                icon: Icons.electrical_services_outlined,
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildConnectButton({required bool showIcon}) {
    if (_isLoadingConnection) {
      return ElevatedButton(
        onPressed: null,
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.grey,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(30.0),
          ),
          padding: const EdgeInsets.symmetric(vertical: 16),
        ),
        child: const SizedBox(
          width: 20,
          height: 20,
          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black),
        ),
      );
    }

    if (_isConnected) {
      return ElevatedButton(
        onPressed: null,
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.green,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(30.0),
          ),
          padding: const EdgeInsets.symmetric(vertical: 16),
        ),
        child: const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.check_circle_outline, size: 20),
            SizedBox(width: 12),
            Text(
              "Connected",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      );
    }

    return ElevatedButton(
      onPressed: null,
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30.0),
        ),
        padding: const EdgeInsets.symmetric(vertical: 16),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (showIcon) ...[
            const CircleAvatar(backgroundColor: Colors.blue, radius: 12),
            const SizedBox(width: 12),
          ],
          const Text(
            "Connect",
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}
