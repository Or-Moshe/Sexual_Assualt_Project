import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart' show kIsWeb;

class UploadContext extends StatefulWidget {
  @override
  _UploadContextState createState() => _UploadContextState();
}

class _UploadContextState extends State<UploadContext> {
  final TextEditingController _controller = TextEditingController();
  bool _isHebrew = false;

  Future<Map<String, dynamic>> sendDataToServer(
      String text, String lang) async {
    try {
      final uri = Uri.http('127.0.0.1:8000', '/analyze_by_vectors',
          {'text': text, 'lang': lang});
      final response = await http.get(uri, headers: {
        'Content-Type': 'application/json',
      });

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {
          'error': 'Failed to load data: Status code ${response.statusCode}'
        };
      }
    } catch (e) {
      return {'error': 'Failed to send data: $e'};
    }
  }

  Future<Map<String, dynamic>> sendFileToServer(File file) async {
    try {
      final uri = Uri.http('127.0.0.1:8000', '/analyze_file_no_vectors');
      var request = http.MultipartRequest('POST', uri);
      request.files.add(await http.MultipartFile.fromPath('file', file.path));
      var response = await request.send();

      if (response.statusCode == 200) {
        var responseData = await response.stream.bytesToString();
        return jsonDecode(responseData);
      } else {
        return {
          'error': 'Failed to load data: Status code ${response.statusCode}'
        };
      }
    } catch (e) {
      return {'error': 'Failed to send data: $e'};
    }
  }

  Future<void> _pickFile() async {
    FilePickerResult? result = await FilePicker.platform
        .pickFiles(type: FileType.custom, allowedExtensions: ['xlsx']);
    if (result != null) {
      if (kIsWeb) {
        // Handle web-specific logic here if needed
      } else {
        File file = File(result.files.single.path!);
        Map<String, dynamic> response = await sendFileToServer(file);
        print(response);
        _showResponseDialog(response);
      }
    }
  }

  void _showResponseDialog(Map<String, dynamic> response) {
    String formatValue(dynamic value) {
      if (value == 1) {
        return '✓';
      } else if (value == 0) {
        return '✗';
      } else {
        return value.toString();
      }
    }

    String formattedResponse = response.entries.map((entry) {
      if (entry.value is Map) {
        return '${entry.key}: {\n' +
            (entry.value as Map)
                .entries
                .map((e) => '  ${e.key}: ${formatValue(e.value)}')
                .join(',\n') +
            '\n}';
      } else {
        return '${entry.key}: ${formatValue(entry.value)}';
      }
    }).join('\n');

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Response from Server'),
        content: SingleChildScrollView(
          child: Text(formattedResponse),
        ),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Upload Context'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextField(
                controller: _controller,
                decoration: InputDecoration(
                  hintText: 'Enter your text here Please',
                  border: OutlineInputBorder(),
                ),
                maxLines: 10,
              ),
              SizedBox(height: 20),
              Row(
                children: [
                  Checkbox(
                    value: _isHebrew,
                    onChanged: (bool? value) {
                      setState(() {
                        _isHebrew = value ?? false;
                      });
                    },
                  ),
                  Text('Hebrew (check for Hebrew, uncheck for English)'),
                ],
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () async {
                  String lang = _isHebrew ? 'he' : 'en';
                  Map<String, dynamic> response =
                      await sendDataToServer(_controller.text, lang);
                  _showResponseDialog(response);
                },
                child: Text('Send'),
              ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: _pickFile,
                child: Text('Upload XLSX File'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
