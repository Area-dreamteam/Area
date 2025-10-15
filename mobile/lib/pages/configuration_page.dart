import 'package:flutter/material.dart';

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

    // Initialisation selon le type de champ
    for (var field in widget.configSchema) {
      final name = field['name'] as String;
      final type = field['type'] as String;
      final values = field['values'];

      if (type == 'check_list' && values is List) {
        // Convertir la liste [{key: bool}, ...] en Map<String, bool>
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
                itemCount: widget.configSchema.length,
                itemBuilder: (context, index) {
                  final field = widget.configSchema[index] as Map<String, dynamic>;
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

                    // On reconstruit le payload final
                    final List<Map<String, dynamic>> finalPayload = [];

                    for (var field in widget.configSchema) {
                      final name = field['name'];
                      final type = field['type'];
                      final value = _configData[name];

                      finalPayload.add({
                        'name': name,
                        'type': type,
                        'values': value,
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
    final String type = field['type'];
    final String name = field['name'];
    final dynamic values = field['values'];

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
          validator: (value) => (value?.isEmpty ?? true)
              ? 'This field is required'
              : null,
          onSaved: (value) => _configData[name] = value ?? '',
        ),
        'select' => DropdownButtonFormField<String>(
          value: _configData[name] as String?,
          decoration: InputDecoration(
            labelText: name,
            labelStyle: const TextStyle(color: Colors.white70),
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
          validator: (value) =>
              (value == null || value.isEmpty) ? 'Please select a value' : null,
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
              final initialValue = (_configData[name] as Map<String, bool>)[key] ?? false;

              return CheckboxListTile(
                title: Text(key, style: const TextStyle(color: Colors.white)),
                value: initialValue,
                onChanged: (bool? newValue) {
                  setState(() {
                    (_configData[name] as Map<String, bool>)[key] = newValue ?? false;
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
