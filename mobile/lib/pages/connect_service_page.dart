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
    final theme = Theme.of(context);
    final serviceColor = hexToColor(widget.service.color);
    final bool isDark = serviceColor.computeLuminance() < 0.5;
    final Color textColor = isDark ? Colors.white : Colors.black;
    final Color buttonBackgroundColor = isDark ? Colors.white : Colors.black;
    final Color buttonForegroundColor = isDark ? Colors.black : Colors.white;

    return Scaffold(
      backgroundColor: serviceColor,
      appBar: AppBar(
        title: Text(
          'Connect to ${widget.service.name}',
          style: TextStyle(color: textColor),
        ),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: IconThemeData(color: textColor),
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: textColor),
          tooltip: 'Retour',
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: MergeSemantics(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                getServiceIcon(
                  widget.service.name,
                  size: 100.0,
                  imageUrl: widget.service.imageUrl,
                ),
                const SizedBox(height: 24),
                Semantics(
                  header: true,
                  child: Text(
                    widget.service.name,
                    textAlign: TextAlign.center,
                    style: theme.textTheme.headlineLarge?.copyWith(
                      color: textColor,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  'You need to connect your ${widget.service.name} account to use this service.',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.bodyLarge?.copyWith(
                    color: textColor.withOpacity(0.7),
                  ),
                ),
                const SizedBox(height: 48),
                ElevatedButton(
                  onPressed: _isLoading ? null : _linkService,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: buttonBackgroundColor,
                    foregroundColor: buttonForegroundColor,
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
                      : Text(
                          'Connect',
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: buttonForegroundColor,
                          ),
                        ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
