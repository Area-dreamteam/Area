// ignore_for_file: avoid_print

import 'package:flutter/material.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:provider/provider.dart';
import '../pages/login.dart';
import '../pages/my_area.dart';
import '../services/oauth_service.dart';

class MainPageApp extends StatelessWidget {
  const MainPageApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(home: MainPage());
  }
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> with TickerProviderStateMixin, WidgetsBindingObserver {
  late PageController _pageViewController;
  late TabController _tabController;
  List<OAuthProvider> _oauthProviders = [];

  final List<Widget> pages = const <Widget>[
    Center(
      child: Image(image: AssetImage('assets/images/homepage_page_2.jpg')),
    ),
    Center(
      child: Image(image: AssetImage('assets/images/homepage_page_2.jpg')),
    ),
    Center(
      child: Image(image: AssetImage('assets/images/homepage_page_3.jpg')),
    ),
    Center(
      child: Image(image: AssetImage('assets/images/homepage_page_4.jpg')),
    ),
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _pageViewController = PageController();
    _tabController = TabController(length: pages.length, vsync: this);
    _loadOAuthProviders();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    super.didChangeAppLifecycleState(state);
    if (state == AppLifecycleState.resumed) {
      print('App resumed - checking for OAuth results');
      Future.delayed(const Duration(milliseconds: 500), () {
        _checkAuthenticationStatus();
      });
    }
  }

  Future<void> _checkAuthenticationStatus() async {
    final oauthService = context.read<OAuthService>();
    final isAuth = await oauthService.isAuthenticated();
    if (isAuth && mounted) {
      print('User is authenticated after resume, navigating to MyArea');
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const MyAreaPage()),
      );
    }
  }

  Future<void> _loadOAuthProviders() async {
    print('Loading OAuth providers in main scaffold...');
    final oauthService = context.read<OAuthService>();
    try {
      final providers = await oauthService.getAvailableProviders();
      print(
        'Loaded ${providers.length} OAuth providers for main page: ${providers.map((p) => p.name).toList()}',
      );
      setState(() {
        _oauthProviders = providers;
      });
    } catch (e) {
      print('Failed to load OAuth providers in main scaffold: $e');
    }
  }

  Future<void> _handleOAuthLogin(OAuthProvider provider) async {
    print('Starting OAuth login for: ${provider.name}');

    final oauthService = context.read<OAuthService>();
    try {
      final result = await oauthService.loginWithOAuth(provider.name);

      if (result.isSuccess) {
        print('OAuth login successful!');
        if (mounted) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => const MyAreaPage()),
          );
        }
      } else {
        print('OAuth login failed: ${result.error}');
        if (mounted) {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => const LoginPage()),
          );
        }
      }
    } catch (e) {
      print('OAuth error: $e');
      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const LoginPage()),
        );
      }
    }
  }

  void _showConnectionOptions() {
    print('Showing connection options with ${_oauthProviders.length} OAuth providers');

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: const Color(0xFF212121),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(15.0),
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ..._oauthProviders.map((provider) {
                final displayName = provider.name.toUpperCase();

                return Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: _buildOAuthOptionButton(
                    context,
                    'Continue with $displayName',
                    provider,
                    _handleOAuthLogin,
                  ),
                );
              }),

              if (_oauthProviders.isNotEmpty) const SizedBox(height: 10),
              _buildOptionButton(
                context,
                'Continue with Email',
                'assets/icons/logo_email.png',
                'email',
              ),
            ],
          ),
        );
      },
    );
  }
  
  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _pageViewController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(25),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Align(
                alignment: Alignment.center,
                child: Text(
                  'AREA',
                  style: TextStyle(
                    fontSize: 50,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 4,
                    color: Colors.white,
                  ),
                ),
              ),
              Expanded(
                child: PageView(
                  controller: _pageViewController,
                  onPageChanged: (index) {
                    setState(() {
                      _tabController.index = index;
                    });
                  },
                  children: pages,
                ),
              ),
              Center(
                child: TabPageSelector(
                  controller: _tabController,
                  color: Colors.black,
                  selectedColor: Colors.white,
                ),
              ),
              const SizedBox(height: 70),
              ElevatedButton(
                onPressed: () {
                  _showConnectionOptions();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 18),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30),
                  ),
                ),
                child: const Text(
                  'Get started',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }
}


Widget _buildOAuthOptionButton(
  BuildContext context,
  String text,
  OAuthProvider provider,
  Function(OAuthProvider) onOAuthLogin,
) {
  return ElevatedButton.icon(
    onPressed: () {
      Navigator.of(context).pop();
      onOAuthLogin(provider);
    },
    icon: getServiceIcon(provider.name, size: 24.0, imageUrl: provider.imageUrl),
    label: Text(
      text,
      style: const TextStyle(color: Colors.black, fontSize: 16.0),
    ),
    style: ElevatedButton.styleFrom(
      backgroundColor: Colors.white,
      foregroundColor: Colors.black,
      minimumSize: const Size(double.infinity, 50),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
    ),
  );
}

Widget _buildOptionButton(
  BuildContext context,
  String text,
  String iconPath,
  String name,
) {
  return ElevatedButton.icon(
    onPressed: () {
      Navigator.of(context).pop();
      if (name == 'email') {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const LoginPage()),
        );
      }
    },
    icon: Image.asset(iconPath, height: 24.0, width: 24.0),
    label: Text(
      text,
      style: const TextStyle(color: Colors.black, fontSize: 16.0),
    ),
    style: ElevatedButton.styleFrom(
      backgroundColor: Colors.white,
      foregroundColor: Colors.black,
      minimumSize: const Size(double.infinity, 50),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
    ),
  );
}