import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
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
import 'package:mobile/pages/my_area.dart';

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
  bool _isCopying = false;

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

  Future<void> _unlinkService() async {
    if (_detailedService == null) return;

    final repo = context.read<ServiceRepository>();

    setState(() => _isLoading = true);
    try {
      await repo.disconnectService(_serviceId);

      if (mounted) {
        setState(() {
          _isLoading = false;
          _isConnected = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Failed to disconnect service: $e"),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _copyApplet() async {
    if (_isCopying) return;

    setState(() => _isCopying = true);

    final applet = widget.item.data as AppletModel;
    final repo = context.read<ServiceRepository>();

    try {
      await repo.copyPublicArea(applet.id);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Applet copied to your Private Areas!'),
          backgroundColor: Colors.green,
        ),
      );

      Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (context) => const MyAreaPage()),
        (Route<dynamic> route) => false,
      );
    } catch (e) {
      if (!mounted) return;
      setState(() => _isCopying = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Failed to copy Applet: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final bool isApplet = widget.item.type == 'Applet';
    final color = hexToColor(widget.item.colorHex);
    final bool isDark = color.computeLuminance() < 0.5;
    final Color appBarIconColor = isDark ? Colors.white : Colors.black;

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        backgroundColor: color,
        iconTheme: IconThemeData(color: appBarIconColor),
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: appBarIconColor),
          tooltip: 'Retour',
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: isApplet
          ? _buildAppletLayout(context, color)
          : _buildServiceLayout(context, color),
    );
  }

  Widget _buildServiceLayout(BuildContext context, Color color) {
    final service = widget.item.data as Service;
    final theme = Theme.of(context);
    final bool isDark = color.computeLuminance() < 0.5;
    final Color headerTextColor = isDark ? Colors.white : Colors.black;

    return Container(
      color: color,
      child: Column(
        children: [
          MergeSemantics(
            child: Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 20.0,
                vertical: 10.0,
              ),
              child: Column(
                children: [
                  getServiceIcon(
                    service.name,
                    size: 60.0,
                    imageUrl: service.imageUrl,
                  ),
                  const SizedBox(height: 16),
                  Semantics(
                    header: true,
                    child: Text(
                      service.name,
                      style: theme.textTheme.headlineLarge?.copyWith(
                        color: headerTextColor,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    _detailedService?.description ?? service.description ?? "",
                    textAlign: TextAlign.center,
                    style: theme.textTheme.bodyLarge?.copyWith(
                      color: headerTextColor,
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
                    _buildConnectButton(
                      showIcon: false,
                      serviceName: service.name,
                    )
                  else
                    const SizedBox(height: 50),
                  const SizedBox(height: 24),
                ],
              ),
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
    final theme = Theme.of(context);

    return ListView(
      padding: const EdgeInsets.all(20.0),
      children: [
        MergeSemantics(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
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
                        ? getServiceIcon(
                            triggerService.name,
                            size: 40.0,
                            imageUrl: triggerService.imageUrl,
                          )
                        : const ExcludeSemantics(
                            child: Icon(
                              Icons.apps,
                              color: Colors.white,
                              size: 40,
                            ),
                          ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              Semantics(
                header: true,
                child: Text(
                  widget.item.title,
                  style: theme.textTheme.headlineMedium?.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 20),
              if (triggerService != null)
                Row(
                  children: [
                    getServiceIcon(
                      triggerService.name,
                      size: 30.0,
                      imageUrl: triggerService.imageUrl,
                    ),
                    const SizedBox(width: 10),
                    Text(
                      triggerService.name,
                      style: theme.textTheme.titleMedium?.copyWith(
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
              const SizedBox(height: 10),
              Row(
                children: [
                  const ExcludeSemantics(
                    child: Icon(
                      Icons.person_outline,
                      color: Colors.white70,
                      size: 20,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    widget.item.byText ?? 'by ${applet.user.name}',
                    style: theme.textTheme.bodyLarge?.copyWith(
                      color: Colors.white70,
                    ),
                  ),
                ],
              ),
            ],
          ),
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
          _buildConnectButton(
            showIcon: true,
            serviceInfo: triggerService,
            serviceName: _detailedService!.name,
          )
        else
          const SizedBox.shrink(),
        const SizedBox(height: 30),

        _buildActionButton(
          text: 'Get this Applet',
          icon: Icons.download_for_offline_outlined,
          onPressed: _copyApplet,
          isLoading: _isCopying,
        ),
        const SizedBox(height: 30),

        Semantics(
          header: true,
          child: Text(
            "Description",
            style: theme.textTheme.titleLarge?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        const SizedBox(height: 10),
        Text(
          applet.description ?? "",
          style: theme.textTheme.bodyLarge?.copyWith(
            color: Colors.white70,
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
          return Center(
            child: Text(
              "No public applets found for this service.",
              style: Theme.of(
                context,
              ).textTheme.bodyLarge?.copyWith(color: Colors.white70),
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
              child: Semantics(
                label: "Applet: ${applet.name}, par ${applet.user.name}",
                button: true,
                child: AppletCard(
                  title: applet.name,
                  byText: 'By ${applet.user.name}',
                  colorHex: applet.color,
                ),
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
        final myAppletsForThisService = viewModel.privateApplets;
        if (myAppletsForThisService.isEmpty) {
          return Center(
            child: Text(
              "You have no applets.",
              style: Theme.of(
                context,
              ).textTheme.bodyLarge?.copyWith(color: Colors.white70),
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
              child: Semantics(
                label: "Applet: ${applet.name}, par ${applet.user.name}",
                button: true,
                child: AppletCard(
                  title: applet.name,
                  byText: 'By ${applet.user.name}',
                  colorHex: applet.color,
                ),
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildConnectButton({
    required bool showIcon,
    required String serviceName,
    ServiceInfo? serviceInfo,
  }) {
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
      return Semantics(
        label: "Déconnecter le service $serviceName",
        button: true,
        toggled: true,
        child: ElevatedButton(
          onPressed: _unlinkService,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.redAccent,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(30.0),
            ),
            padding: const EdgeInsets.symmetric(vertical: 16),
          ),
          child: const Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.link_off, size: 20),
              SizedBox(width: 12),
              Text(
                "Disconnect",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ),
      );
    }
    return Semantics(
      label: "Connecter le service $serviceName",
      button: true,
      toggled: false,
      child: ElevatedButton(
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
              getServiceIcon(
                serviceInfo.name,
                size: 24.0,
                imageUrl: serviceInfo.imageUrl,
              ),
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
      ),
    );
  }

  Widget _buildActionButton({
    required String text,
    required IconData icon,
    required VoidCallback onPressed,
    Color backgroundColor = Colors.white,
    Color foregroundColor = Colors.black,
    bool isLoading = false,
  }) {
    return Semantics(
      label: text,
      button: true,
      enabled: true,
      child: ElevatedButton.icon(
        icon: isLoading ? const SizedBox.shrink() : Icon(icon, size: 20),
        label: isLoading
            ? SizedBox(
                width: 24,
                height: 24,
                child: CircularProgressIndicator(
                  color: foregroundColor,
                  strokeWidth: 3,
                ),
              )
            : Text(
                text,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
        onPressed: isLoading ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: backgroundColor,
          foregroundColor: foregroundColor,
          padding: const EdgeInsets.symmetric(vertical: 14),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(30.0),
          ),
          elevation: 2,
        ),
      ),
    );
  }
}
