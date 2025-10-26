// pages/connect_service_page.dart

import 'package:flutter/material.dart';
import 'package:mobile/models/service_model.dart';
import 'package:mobile/services/oauth_service.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/widgets/hex_convert.dart';
import 'package:provider/provider.dart';

class ConnectServicePage extends StatefulWidget {
  final Service service;
  const ConnectServicePage({super.key, required this.service});

  @override
  State<ConnectServicePage> createState() => _ConnectServicePageState();
}

class _ConnectServicePageState extends State<ConnectServicePage> {
  bool _isLoading = false;

  Future<void> _linkService() async {
    setState(() => _isLoading = true);
    final oauthService = context.read<OAuthService>();

    try {
      final result = await oauthService.linkWithOAuth(widget.service.name);

      if (result.isSuccess && mounted) {
        Navigator.pop(context, true);
      } else {
        throw Exception(result.error ?? 'Failed to link service');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to connect: $e'),
            backgroundColor: Colors.red,
          ),
        );
        Navigator.pop(context, false);
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final serviceColor = hexToColor(widget.service.color);

    return Scaffold(
      backgroundColor: serviceColor,
      appBar: AppBar(
        title: Text('Connect to ${widget.service.name}',
            style: const TextStyle(color: Colors.white)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              getServiceIcon(widget.service.name, size: 100.0),
              const SizedBox(height: 24),
              Text(
                widget.service.name,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'You need to connect your ${widget.service.name} account to use this service.',
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Colors.white70,
                  fontSize: 16,
                ),
              ),
              const SizedBox(height: 48),
              ElevatedButton(
                onPressed: _isLoading ? null : _linkService,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  foregroundColor: Colors.black,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30.0),
                  ),
                ),
                child: _isLoading
                    ? const SizedBox(
                        width: 24,
                        height: 24,
                        child: CircularProgressIndicator(color: Colors.black),
                      )
                    : const Text(
                        'Connect',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}