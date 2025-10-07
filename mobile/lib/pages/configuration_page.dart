import 'package:flutter/material.dart';

extension TakeIf<T> on T {
  T? takeIf(bool Function(T) predicate) => predicate(this) ? this : null;
}

class ConfigurationPage extends StatefulWidget {
  final List<dynamic> configSchema;
  final String serviceName;
  final String itemName;

  const ConfigurationPage({
    super.key,
    required this.configSchema,
    required this.serviceName,
    required this.itemName,
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
    final List<dynamic> fields = widget.configSchema;
    for (var field in fields) {
      final fieldName = field['name'];
      final fieldType = field['type'];
      final fieldValues = field['values'] as List<dynamic>? ?? [];

      if (fieldType == 'check_list') {
        _configData[fieldName] = Map<String, bool>.fromEntries(
          fieldValues
              .map((e) => (e as Map<String, dynamic>).entries.first)
              .map((e) => MapEntry(e.key, e.value as bool)),
        );
      } else {
        _configData[fieldName] = fieldValues.isNotEmpty
            ? fieldValues.first.toString()
            : '';
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final List<dynamic> fields = widget.configSchema;

    return Scaffold(
      backgroundColor: const Color(0xFF212121),
      appBar: AppBar(
        title: Text(widget.itemName),
        backgroundColor: Colors.white,
      ),
      body: Form(
        key: _formKey,
        child: Column(
          children: [
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(16.0),
                itemCount: fields.length,
                itemBuilder: (context, index) {
                  final field = fields[index] as Map<String, dynamic>;
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
                ),
                onPressed: () {
                  if (_formKey.currentState!.validate()) {
                    _formKey.currentState!.save();

                    List<Map<String, dynamic>> finalPayload = [];

                    for (var field in widget.configSchema) {
                      final fieldName = field['name'];
                      final fieldType = field['type'];
                      dynamic userValue =
                          _configData[fieldName];

                      if (fieldType == 'check_list' &&
                          userValue is Map<String, bool>) {
                        userValue = userValue.entries
                            .map((entry) => {entry.key: entry.value})
                            .toList();
                      }
                      finalPayload.add({
                        'name': fieldName,
                        'type': fieldType,
                        'values': userValue,
                      });
                    }
                    Navigator.pop(context, finalPayload);
                  }
                },
                child: const Text(
                  'Confirm Configuration',
                  style: TextStyle(color: Colors.white),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFormField(Map<String, dynamic> field) {
    String type = field['type'];
    String name = field['name'];
    dynamic values = field['values'];

    return Padding(
      padding: const EdgeInsets.only(bottom: 20.0),
      child: switch (type) {
        'input' => TextFormField(
          initialValue: _configData[name] as String?,
          decoration: InputDecoration(
            labelText: name,
            labelStyle: const TextStyle(color: Colors.white70),
            border: const OutlineInputBorder(),
          ),
          style: const TextStyle(color: Colors.white),
          validator: (value) =>
              (value?.isEmpty ?? true) ? 'This field is required' : null,
          onSaved: (value) => _configData[name] = value,
        ),
        'select' => DropdownButtonFormField<String>(
          initialValue: (_configData[name] as String?).takeIf(
            (v) =>
                v != null &&
                (values as List).map((e) => e.toString()).contains(v),
          ),
          decoration: InputDecoration(
            labelText: name,
            labelStyle: const TextStyle(color: Colors.white70),
            border: const OutlineInputBorder(),
          ),
          style: const TextStyle(color: Colors.white),
          items: (values as List<dynamic>).map((option) {
            return DropdownMenuItem(
              value: option.toString(),
              child: Text(option.toString()),
            );
          }).toList(),
          onChanged: (value) {
            setState(() {
              _configData[name] = value;
            });
          },
          onSaved: (value) => _configData[name] = value,
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
              final initialValue = map.values.first as bool;

              return CheckboxListTile(
                title: Text(key, style: const TextStyle(color: Colors.white)),
                value:
                    (_configData[name] as Map<String, bool>)[key] ??
                    initialValue,
                onChanged: (bool? newValue) {
                  setState(() {
                    (_configData[name] as Map<String, bool>)[key] =
                        newValue ?? false;
                  });
                },
                controlAffinity: ListTileControlAffinity.leading,
              );
            }),
          ],
        ),
        _ => Text(
          'Unsupported field type: $type',
          style: const TextStyle(color: Colors.red),
        ),
      },
    );
  }
}
