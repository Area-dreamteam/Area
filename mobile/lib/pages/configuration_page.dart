import 'package:flutter/material.dart';
import 'package:mobile/utils/icon_helper.dart';
import 'package:mobile/core/config.dart';

class ConfigurationPage extends StatefulWidget {
  final List<dynamic> configSchema;
  final String serviceName;
  final String itemName;

  final String itemDescription;
  final String itemType;

  const ConfigurationPage({
    super.key,
    required this.configSchema,
    required this.serviceName,
    required this.itemName,

    required this.itemDescription,
    required this.itemType,
  });

  @override
  State<ConfigurationPage> createState() => _ConfigurationPageState();
}

class _ConfigurationPageState extends State<ConfigurationPage> {
  final _formKey = GlobalKey<FormState>();
  final Map<String, dynamic> _configData = {};

  @override
  void initState() {
    super.initState();

    for (var field in widget.configSchema) {
      final name = field['name'] as String;
      final type = field['type'] as String;
      final values = field['values'];

      if (type == 'check_list' && values is List) {
        _configData[name] = Map<String, bool>.fromEntries(
          values
              .map((e) => (e as Map<String, dynamic>).entries.first)
              .map((e) => MapEntry(e.key, e.value as bool)),
        );
      } else if (type == 'select' && values is List && values.isNotEmpty) {
        _configData[name] = values.first.toString();
      } else {
        _configData[name] = '';
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        title: Text(
          widget.itemName,
          style: const TextStyle(color: Colors.white),
        ),
        backgroundColor: const Color(0xFF212121),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Form(
        key: _formKey,
        child: Column(
          children: [
            const SizedBox(height: 60),
            _buildHeader(widget.serviceName),

            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(16.0),
                itemCount: widget.configSchema.length,
                itemBuilder: (context, index) {
                  final field =
                      widget.configSchema[index] as Map<String, dynamic>;
                  return _buildFormField(field);
                },
              ),
            ),

            Padding(
              padding: const EdgeInsets.all(16.0),
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(double.infinity, 50),
                  backgroundColor: Colors.blue,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(30.0),
                  ),
                ),
                onPressed: _handleConfirmation,
                child: Text(
                  'Create ${widget.itemType}',
                  style: const TextStyle(color: Colors.white, fontSize: 18),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(String serviceName) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          getServiceIcon(serviceName, size: 100.0, imageUrl: null),
          const SizedBox(height: 16),
          Text(
            widget.itemName,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Text(
            widget.itemDescription,
            style: const TextStyle(color: Colors.white70, fontSize: 16),
            textAlign: TextAlign.start,
          ),
        ],
      ),
    );
  }

  void _handleConfirmation() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      final List<Map<String, dynamic>> finalPayload = [];

      for (var field in widget.configSchema) {
        final name = field['name'];
        final type = field['type'];
        final value = _configData[name];

        finalPayload.add({'name': name, 'type': type, 'values': value});
      }

      Navigator.pop(context, finalPayload);
    }
  }

  Widget _buildFormField(Map<String, dynamic> field) {
    final String type = field['type'];
    final String name = field['name'];
    final dynamic values = field['values'];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (type != 'check_list')
          Padding(
            padding: const EdgeInsets.only(bottom: 8.0),
            child: Text(
              name,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),

        Padding(
          padding: const EdgeInsets.only(bottom: 20.0),
          child: switch (type) {
            'input' => TextFormField(
              initialValue: _configData[name] as String?,
              decoration: InputDecoration(
                labelStyle: const TextStyle(color: Colors.white70),
                enabledBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.white54),
                ),
                focusedBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blue),
                ),
                border: const OutlineInputBorder(),
              ),
              style: const TextStyle(color: Colors.white),
              validator: (value) =>
                  (value?.isEmpty ?? true) ? 'This field is required' : null,
              onSaved: (value) => _configData[name] = value ?? '',
            ),

            'select' => DropdownButtonFormField<String>(
              initialValue: _configData[name] as String?,
              decoration: InputDecoration(
                labelStyle: const TextStyle(color: Colors.white70),
                enabledBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.white54),
                ),
                focusedBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blue),
                ),
                border: const OutlineInputBorder(),
              ),
              dropdownColor: Colors.black87,
              style: const TextStyle(color: Colors.white),
              items: (values as List<dynamic>).map((option) {
                return DropdownMenuItem(
                  value: option.toString(),
                  child: Text(option.toString()),
                );
              }).toList(),
              onChanged: (value) => setState(() {
                _configData[name] = value ?? '';
              }),
              validator: (value) => (value == null || value.isEmpty)
                  ? 'Please select a value'
                  : null,
            ),

            'check_list' => Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(color: Colors.white, fontSize: 16),
                ),
                const SizedBox(height: 8),
                ...(values as List<dynamic>).map((item) {
                  final map = item as Map<String, dynamic>;
                  final key = map.keys.first;
                  final initialValue =
                      (_configData[name] as Map<String, bool>)[key] ?? false;

                  return CheckboxListTile(
                    title: Text(
                      key,
                      style: const TextStyle(color: Colors.white),
                    ),
                    value: initialValue,
                    onChanged: (bool? newValue) {
                      setState(() {
                        (_configData[name] as Map<String, bool>)[key] =
                            newValue ?? false;
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    checkColor: Colors.white,
                    activeColor: Colors.blue,
                  );
                }),
              ],
            ),
            _ => Text(
              'Unsupported field type: $type',
              style: const TextStyle(color: Colors.red),
            ),
          },
        ),
      ],
    );
  }
}
