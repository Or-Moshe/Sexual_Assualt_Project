import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/foundation.dart' show kIsWeb;

class UploadContext extends StatefulWidget {
  @override
  _UploadContextState createState() => _UploadContextState();
}

class _UploadContextState extends State<UploadContext> {
  final TextEditingController _controller = TextEditingController();
  bool _isHebrew = false;
  bool _isLoading = false;

  Future<Map<String, dynamic>> sendDataToServer(
      String text, String lang) async {
    try {
      final uri = Uri.http('127.0.0.1:8000', '/analyze_by_vectors',
          {'text': text, 'lang': lang});
      final response =
          await http.get(uri, headers: {'Content-Type': 'application/json'});

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

  Future<Map<String, dynamic>> sendFileToServer(
      {Uint8List? bytes, String? filename}) async {
    try {
      final uri = Uri.http('127.0.0.1:8000', '/analyze_file_no_vectors');
      final bodyTemp =
          jsonEncode({'file': base64Encode(bytes!), 'filename': filename});
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: bodyTemp,
      );

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

  Future<void> _pickFile() async {
    setState(() {
      _isLoading = true;
    });

    FilePickerResult? result = await FilePicker.platform
        .pickFiles(type: FileType.custom, allowedExtensions: ['xlsx']);
    if (result != null) {
      final bytes = result.files.single.bytes;
      final filename = result.files.single.name;
      if (bytes != null) {
        Map<String, dynamic> response =
            await sendFileToServer(bytes: bytes, filename: filename);
        _showResponseDialog(response);
      }
    }

    setState(() {
      _isLoading = false;
    });
  }

  void _showResponseDialog(Map<String, dynamic> response) {
    String formatValue(String key, dynamic value) {
      if (key == 'level of suicide/ level of risk' || key == 'prediction') {
        return value.toString();
      } else if (value == 1) {
        return '✓';
      } else if (value == 0) {
        return '✗';
      } else {
        return value.toString();
      }
    }

    Widget formatResponse(Map<String, dynamic> response) {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: response.entries.map((entry) {
          if (entry.value is Map) {
            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('${entry.key}:',
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Container(
                    padding: EdgeInsets.symmetric(horizontal: 8.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: (entry.value as Map).entries.map((e) {
                        return Text('${e.key}: ${formatValue(e.key, e.value)}');
                      }).toList(),
                    ),
                  ),
                ],
              ),
            );
          } else {
            return Text('${entry.key}: ${formatValue(entry.key, entry.value)}');
          }
        }).toList(),
      );
    }

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Response from Server'),
        content: SingleChildScrollView(
          child: formatResponse(response),
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
        backgroundColor: Colors.teal,
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Card(
            elevation: 5,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(15),
            ),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    TextField(
                      controller: _controller,
                      decoration: InputDecoration(
                        labelText: 'Enter your text here',
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
                    Center(
                      child: Column(
                        children: [
                          ElevatedButton(
                            onPressed: () async {
                              setState(() {
                                _isLoading = true;
                              });

                              String lang = _isHebrew ? 'he' : 'en';
                              Map<String, dynamic> response =
                                  await sendDataToServer(
                                      _controller.text, lang);
                              _showResponseDialog(response);

                              setState(() {
                                _isLoading = false;
                              });
                            },
                            child: Text('Send'),
                            style: ElevatedButton.styleFrom(
                              foregroundColor: Colors.white,
                              backgroundColor: Colors.teal,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                              padding: EdgeInsets.symmetric(
                                  horizontal: 20, vertical: 12),
                            ),
                          ),
                          SizedBox(height: 20),
                          ElevatedButton(
                            onPressed: _pickFile,
                            child: Text('Upload XLSX File'),
                            style: ElevatedButton.styleFrom(
                              foregroundColor: Colors.white,
                              backgroundColor: Colors.teal,
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                              padding: EdgeInsets.symmetric(
                                  horizontal: 20, vertical: 12),
                            ),
                          ),
                        ],
                      ),
                    ),
                    if (_isLoading) SizedBox(height: 20),
                    if (_isLoading) Center(child: CircularProgressIndicator()),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
