import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class RedirectPage extends StatefulWidget {
  final String url;

  const RedirectPage({super.key, required this.url});

  @override
  State<RedirectPage> createState() => _RedirectPageState();
}

class _RedirectPageState extends State<RedirectPage> {

  @override
  void initState() {
    super.initState();
    _launchURLAndPop();
  }

  Future<void> _launchURLAndPop() async {
    final Uri parsedUrl = Uri.parse(widget.url);

    if (await canLaunchUrl(parsedUrl)) {
      await launchUrl(
        parsedUrl,
        mode: LaunchMode.inAppWebView,
      );
    } else {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Can\'t lauch URL : ${widget.url}')),
        );
      }
    }
    
    if (context.mounted) {
       Navigator.of(context).pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}