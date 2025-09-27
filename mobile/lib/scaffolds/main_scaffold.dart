import 'package:flutter/material.dart';
import '../pages/login.dart';

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

class _MainPageState extends State<MainPage> with TickerProviderStateMixin {
  late PageController _pageViewController;
  late TabController _tabController;

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
    _pageViewController = PageController();
    _tabController = TabController(length: pages.length, vsync: this);
  }

  @override
  void dispose() {
    _pageViewController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(
            horizontal: screenWidth * 0.10,
            vertical: screenWidth * 0.15,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Align(
                alignment: Alignment.center,
                child: Text(
                  'AREA',
                  style: TextStyle(
                    fontSize: 36,
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
                  _showConnectionOptions(context);
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

void _showConnectionOptions(BuildContext context) {
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
            _buildOptionButton(
              context,
              'Continue with Google',
              'assets/icons/logo_google.png',
            ),
            const SizedBox(height: 10),
            _buildOptionButton(
              context,
              'Continue with Facebook',
              'assets/icons/logo_facebook.png',
            ),
            const SizedBox(height: 10),
            _buildOptionButton(
              context,
              'Continue with Email',
              'assets/icons/logo_email.png',
            ),
          ],
        ),
      );
    },
  );
}

Widget _buildOptionButton(BuildContext context, String text, String iconPath) {
  return ElevatedButton.icon(
    onPressed: () {
      Navigator.of(context).pop();
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => const Login()),
      );
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
