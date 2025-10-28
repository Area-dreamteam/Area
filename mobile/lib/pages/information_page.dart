// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:mobile/models/applet_model.dart';
import 'package:mobile/models/service_info_model.dart';
import 'package:mobile/viewmodels/explore_viewmodel.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/repositories/service_repository.dart';
import 'package:mobile/services/oauth_service.dart';
import 'package:mobile/utils/icon_helper.dart';
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
    with TickerProviderStateMixin, WidgetsBindingObserver {
  late TabController _tabController;
  late final int _serviceId;
  late Future<List<AppletModel>> _publicApplets;

  bool _isLoading = true;
  Service? _detailedService;
  bool _isConnected = false;
  // ---

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _tabController = TabController(length: 2, vsync: this);

    int? tempServiceId;
    final appletsRepo = context.read<ServiceRepository>();

    if (widget.item.type == 'Service') {
      final service = widget.item.data as Service;
      tempServiceId = service.id;

      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) {
          context.read<MyAppletViewModel>().loadApplets();
        }
      });
    } else if (widget.item.type == 'Applet') {
      final triggerService = (widget.item.data as AppletModel).triggerService;
      tempServiceId = triggerService?.id;
    }

    if (tempServiceId == null) {
      setState(() => _isLoading = false);
      _publicApplets = Future.value([]);
      _serviceId = -1;
      return;
    }

    _serviceId = tempServiceId;
    _publicApplets = appletsRepo.fetchPublicApplets(serviceId: _serviceId);
    _loadServiceData();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _tabController.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _loadServiceData();
    }
  }

  Future<void> _loadServiceData() async {
    if (!mounted) return;
    setState(() => _isLoading = true);

    try {
      final repo = context.read<ServiceRepository>();

      final results = await Future.wait([
        repo.fetchServiceDetails(_serviceId),
        repo.isServiceConnected(_serviceId),
      ]);

      if (mounted) {
        setState(() {
          _detailedService = results[0] as Service;
          _isConnected = results[1] as bool;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to load service data: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _linkService() async {
    if (_detailedService == null) return;

    final oauthService = context.read<OAuthService>();
    final serviceName = _detailedService!.name;

    setState(() => _isLoading = true);
    try {
      final result = await oauthService.linkWithOAuth(serviceName);

      if (result.isSuccess && mounted) {
        final repo = context.read<ServiceRepository>();
        final status = await repo.isServiceConnected(_serviceId);
        setState(() {
          _isConnected = status;
          _isLoading = false;
        });
      } else {
        throw Exception(result.error ?? 'Failed to link service');
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to connect service: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
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
                getServiceIcon(service.name, size: 60.0),
                // ---
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
                  _detailedService?.description ?? service.description ?? "",
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 16,
                    height: 1.5,
                  ),
                ),
                const SizedBox(height: 24),

                if (_isLoading)
                  const SizedBox(
                    height: 50,
                    child: Center(
                      child: CircularProgressIndicator(color: Colors.white),
                    ),
                  )
                else if (_detailedService != null &&
                    _detailedService!.oauthRequired)
                  _buildConnectButton(showIcon: false)
                else
                  const SizedBox(height: 50),
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
                  ? getServiceIcon(triggerService.name, size: 40.0)
                  // ---
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
              getServiceIcon(triggerService.name, size: 30.0),
              // ---
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

        if (_isLoading)
          const SizedBox(
            height: 50,
            child: Center(
              child: CircularProgressIndicator(color: Colors.white),
            ),
          )
        else if (_detailedService != null && _detailedService!.oauthRequired)
          _buildConnectButton(showIcon: true, serviceInfo: triggerService)
        else
          const SizedBox.shrink(),
        // ---
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

  Widget _buildConnectButton(
      {required bool showIcon, ServiceInfo? serviceInfo}) {
    if (_isLoading) {
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
      onPressed: _linkService,
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
          if (showIcon && serviceInfo != null) ...[
            getServiceIcon(serviceInfo.name, size: 24.0),
            const SizedBox(width: 12),
          ] else if (showIcon) ...[
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